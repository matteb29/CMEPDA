
"""
    Here we write the model assembled in a simulator, including:
    a Normalizer to better handle the data passed to the Networks,
    an instance of our Encoder-Processor-Decoder framework,
    an Euler Integrator to predict particles next positions

"""


import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_cluster import radius_graph
from graph_net_repo import EncoderProcessorDecoder



"""
defining a normalizer for all the input and output of the Network as a
herereditary class of nn.Module to better handle the passage of data to GPU
resulting in a faster training 
"""
class Normalizer(nn.Module):

    def __init__(self, size, max_accumulation = 10**6, std_epsilon = 1e-8 ):

        super().__init__()

        self.max_accumulation = max_accumulation

        #Initializing some variables as buffers inside nn.Module:

        #sum of accumulated to compute the mean
        self.register_buffer("accumulated_sum", torch.zeros(size))

        #sum of squared accumulated to compute the standard deviation 
        self.register_buffer("accumulated_sum_squared", torch.zeros(size))

        #number of accumulated considered
        self.register_buffer("accumulated_count", torch.zeros(1))

        #inizialize mean of the features as zero
        self.register_buffer("mean", torch.zeros(size))

        #inizialize standard devations of the features as 1 
        self.register_buffer("std_dev", torch.ones(size))

        #to prevent the division by zero in normalize method
        self.std_epsilon = std_epsilon

        #if accumulating = True continue to do inference on data
        self.accumulating = True

    #define a method to update the variables inside the buffers
    def update_stats(self, batch):

        if not self.accumulating:
            return
        
        count = batch.shape[0]
        self.accumulated_count += count

        self.accumulated_sum += batch.sum(dim = 0)
        self.accumulated_sum_squared += (batch**2).sum(dim = 0)

        self.mean[:] = self.accumulated_sum / self.accumulated_count
        self.std_dev[:] = torch.sqrt(
            (self.accumulated_sum_squared / self.accumulated_count) 
            - self.mean**2 + self.std_epsilon 
            )
        
        #stop inference if number of particles accumulated is bigger than max_accumulation
        if self.accumulated_count > self.max_accumulation:
            self.accumulating = False

    
    #define a method to normalize the data before passing them to the Networks
    def normalize(self, batch):
        return (batch - self.mean) / self.std_dev
    
    #to process the normalized output of the Networks
    def inverse(self, batch):
        return batch * self.std_dev + self.mean
    

"""
defining the simulator which implement
 EncoderProcessorDecoder, Normalizer and Euler Integrator
"""
class Simulator(nn.Module):

    def __init__(self, 
                 particle_dimensions = 2,
                 node_in = 30,
                 edge_in = 3,
                 latent_size = 128,
                 num_layers = 2,
                 message_passing_steps = 10,
                 connectivity_radius = 0.015,
                 boundaries = [[-1.,1.],[-1.,1.]],
                 normalization_stats = None,
                 num_particle_types = 9,
                 dim_particle_embedding = 16
                 ):
        
        super().__init__()

        self.connectivity_radius = connectivity_radius
        self.particle_dimension = particle_dimensions
        self.num_particle_types = num_particle_types

        self.register_buffer("boundaries", torch.tensor(boundaries, dtype = torch.float))

        #account for different type of particles
        if self.num_particle_types > 1:
            self.particle_embedding = nn.Embedding(num_particle_types, dim_particle_embedding)

        #define the normalization for node features
        self.node_normalizer = Normalizer(node_in)

        #define the normalization for edge features
        self.edge_normalizer = Normalizer(edge_in)

        #define the normalizer for the output of the simulator 
        self.output_normalizer = Normalizer(particle_dimensions)

        #deal with possible normalized stats already computed and given as input to the simulator
        normalizers_map = {
            "accelerations": self.output_normalizer,
            "nodes": self.node_normalizer,
            "edges": self.edge_normalizer
        }

        if normalization_stats is not None:
            for key, normalizer in normalizers_map.items():

                if key in normalization_stats:
                    stats = normalization_stats[key]

                if normalizer.mean.shape != stats["mean"].shape:
                    raise ValueError(f"Errore dimensioni per {key}")
                
                #handle shift data between CPU and GPU
                device = normalizer.mean.device
                normalizer.mean.data = stats["mean"].to(device)
                normalizer.std.data = stats["std"].to(device)

                normalizer.accumulating = False

                print(f"Normalized stats loaded")

                

        #define the framework of our simulator as an instance of EncoderProcessorDecoder
        self.framework = EncoderProcessorDecoder(
            input_node_dim = node_in,
            input_edge_dim = edge_in,
            latent_size = latent_size,
            num_layers_mlp = num_layers,
            num_message_passing_steps = message_passing_steps,
            output_size = particle_dimensions
        )

    #defining edge features to impose inductive biases for spatial invariance"
    def get_edge_features(self, positions, edge_index):

        #define sender and receiver positions
        sender_pos = positions[edge_index[0]]
        receiver_pos = positions[edge_index[1]]

        #define their distance
        relative_pos = sender_pos - receiver_pos

        #making it adimensional dividing by connectivity radius
        relative_pos = relative_pos / self.connectivity_radius

        #define its absolute value
        norm = torch.norm(relative_pos, dim = -1, keepdim = True)

        #definining edge features as relative position between sender and receiver and its norm
        edge_features = torch.cat([relative_pos, norm], dim = -1)

        return edge_features
    
    #define a function to comupute particle distances from boundaries 
    def get_boundary_distances(self, current_positions):

        #defining the left bound and the lower bound of the bow
        lower_bounds = self.boundaries[:, 0].unsqueeze(0)

        #defining the right bound and the upper bound of the box
        upper_bounds = self.boundaries[:, 1].unsqueeze(0)

        #define particle distances from the bounds of the box
        distances_to_lower = current_positions - lower_bounds
        distances_to_upper = upper_bounds - current_positions

        distances_to_boundaries = torch.concatenate(
            [distances_to_lower, distances_to_upper], 
            dim = -1
            )
        
        #now normalize and clip the distances from boundaries
        norm_clipped_distances = torch.clamp(
            distances_to_boundaries / self.connectivity_radius,
            min = -1.0, max = 1.0
        )
        
        return norm_clipped_distances

    

    def predict_accelerations(self, position_sequence, particle_types, batch = None):

        #define current position as last column of the temporal sequence of positions 
        current_positions = position_sequence[:, -1]

        #compute the past velocities as spatial differences 
        velocities = [
            position_sequence[:, t] - position_sequence[:, t-1] 
            for t in range(1, position_sequence.shape[1])
        ]
        velocities_tensor = torch.cat(velocities, dim = -1)

        #get the particle distances from boundaries
        boundary_distances = self.get_boundary_distances(current_positions)

        #define particles features
        node_input_features_list = [velocities_tensor, boundary_distances]

        node_input_features = torch.cat(node_input_features_list, dim = -1)

        #building edges with radius_graph according to nodes current positions 
        edge_index = radius_graph(
            current_positions,
            r = self.connectivity_radius,
            batch = batch,
            loop = False
            )
        edge_input_features = self.get_edge_features(current_positions, edge_index) 

        #compute mean and std dev to normalize features
        if self.training:
            self.node_normalizer.update_stats(node_input_features)
            self.edge_normalizer.update_stats(edge_input_features)

        #normalizing edges and nodes features before giving them to net
        norm_node_input_features = self.node_normalizer.normalize(node_input_features)
        norm_edge_input_features = self.edge_normalizer.normalize(edge_input_features)

        #handling with more particle types, embedding features must not be normalized
        if self.num_particle_types > 1:
            final_node_features = [norm_node_input_features]
            final_node_features.append(
            self.particle_embedding(particle_types)
            )
            norm_node_input_features = torch.cat(final_node_features, dim=-1)
        else:
            norm_node_input_features = norm_node_input_features
            



        #now we can give them to the net to predict normalized accelerations
        prediction_norm = self.framework(
                          norm_node_input_features, 
                          edge_index, 
                          norm_edge_input_features) 
        
        #de-normalize the output for the simulation 
        return self.output_normalizer.inverse(prediction_norm)
    
    
    #define Euler Integrator to calculate particles next positions from predicted accelerations
    def Euler(self, positions_sequence, particle_types, batch = None):

        accelerations = self.predict_accelerations(positions_sequence, particle_types, batch)

        current_positions = positions_sequence[:,-1]
        last_positions = positions_sequence[:, -2]
        
        current_velocities = current_positions - last_positions

        #updating positions of the particles
        next_positions = current_positions + current_velocities + accelerations

        return next_positions
    

    #define a method to handle noise in training sessions
    def helper_training(self, 
                        next_positions, 
                        positions_sequence_noise,
                        positions_sequence,
                        particle_types,
                        global_context = None,
                        batch = None
                        ):
        
        #add noise to positions
        noisy_pos_sequence = positions_sequence + positions_sequence_noise

        #now predict accelerations replicating the logic in predict_accelerations
        current_noisy_positions = noisy_pos_sequence[:, -1]
        
        velocities = [
             noisy_pos_sequence[:, t] - noisy_pos_sequence[:, t-1] 
             for t in range(1, noisy_pos_sequence.shape[1])
             ]
    
        noisy_velocities = torch.cat(velocities, dim = -1)
        boundary_positions = self.get_boundary_distances(current_noisy_positions)
        
        noisy_node_input_list = [noisy_velocities, boundary_positions]

        noisy_physical_features = torch.cat(noisy_node_input_list, dim=-1)

        if self.training:
            self.node_normalizer.update_stats(noisy_physical_features)

        norm_physical_features = self.node_normalizer.normalize(noisy_physical_features)

        if self.num_particle_types > 1:
            final_node_features = [norm_physical_features]
            final_node_features.append(
            self.particle_embedding(particle_types)
            )
            norm_nodes_input_features = torch.cat(final_node_features, dim=-1)
        else:
            norm_nodes_input_features = norm_physical_features


        noisy_edge_index = radius_graph(
            current_noisy_positions, 
            r = self.connectivity_radius,
            batch = batch,
            loop = False
        )        

        noisy_edge_input = self.get_edge_features(current_noisy_positions, noisy_edge_index)

        if self.training:
            self.edge_normalizer.update_stats(noisy_edge_input)

        norm_edges_input_features = self.edge_normalizer.normalize(noisy_edge_input)

        #make a prediction with the net
        pred_norm_accelerations = self.framework(
            norm_nodes_input_features,
            noisy_edge_index,
            norm_edges_input_features
        )

        #now compute the target positions adding noise to the labels of the simulation
        next_norm_pos_adjusted = next_positions + positions_sequence_noise[:,-1]

        #to compute the loss we need to compute the corrispondent accelerations
        target_velocities = next_norm_pos_adjusted - noisy_pos_sequence[:, -1]
        previous_target_velocities = noisy_pos_sequence[:, -1] - noisy_pos_sequence[:, -2]

        target_accelerations_unnormalized = target_velocities - previous_target_velocities

        #normalize the results
        if self.training:
            self.output_normalizer.update_stats(target_accelerations_unnormalized)

        target_norm_accelerations = self.output_normalizer.normalize(
            target_accelerations_unnormalized
        )

        #return the two elements to compute the loss
        return  pred_norm_accelerations, target_norm_accelerations
    

    def forward(self, 
                positions_sequence, 
                particle_types, 
                global_context = None, 
                batch = None
                ):
        
        return self.Euler(positions_sequence, particle_types, batch)




        
        
        









    


    
 

