
"""
Here we write the network framework structured as:

    ENCODER: 2 MLPs to build nodes and edges
    PROCESSOR: M Graph Networks 
    DECODER: 1 MLP to predict the accelerations of the particles at the next time step

"""


import torch
import torch.nn as nn
from torch_scatter import scatter_add 




"Defining MLP for learnable functions used in ENCODER, PROCESSOR and DECODER"

class MLP(nn.Module):


    def __init__(self, 
                 input_size, 
                 hidden_size, 
                 output_size, 
                 num_layers, 
                 layer_norm = True
                ):

        super().__init__()

        layers = [] 

        in_dim = input_size


        #creating a set of hidden layers with activation function ReLU
        for i in range (num_layers - 1):

            layers.append(nn.Linear(in_dim, hidden_size))
            layers.append(nn.ReLU())

            in_dim = hidden_size

    
        #adding the output layer without activation function 
        layers.append(nn.Linear(hidden_size, output_size)) 


        #including a possible LayerNorm layer as suggested by DeepMind to enhance performances
        if layer_norm:

            layers.append(nn.LayerNorm(output_size))

        
        #definining the network
        self.network = nn.Sequential(*layers)


    def forward(self, input_data):

        return self.network(input_data)


"Defining a Network to implement message passing among the nodes, main core of PROCESSOR  "


class InteractionNetwork(nn.Module):


    def __init__(self, hidden_size, num_layers_mlp):

        super().__init__()

        #MLP to update the edges using: past edge features, sender features, receiver features
        self.edges_mlp = MLP(hidden_size * 3, hidden_size, hidden_size, num_layers_mlp)

        #MLP to update the nodes using: past node features, aggregated features from edges
        self.node_mlp = MLP(hidden_size * 2, hidden_size, hidden_size, num_layers_mlp)



    def forward(self, input, edge_index, edge_attr):

        #define senders and receivers
        senders, receivers = edge_index

        #and their features
        senders_features = input[senders]
        receivers_features = input[receivers]

        #defining the inputs to update edges
        edge_inputs = torch.cat(
            [edge_attr, senders_features, receivers_features], 
             dim = 1
             )

        #updating edges using a MLP as phi^e function
        update_edge_features = self.edges_mlp(edge_inputs)

        #aggregating information from edges to update nodes attributes
        aggr_message = scatter_add(
            update_edge_features, 
            receivers, 
            dim = 0 , 
            dim_size = input.size(0))

        #defining the inputs to update the nodes
        node_inputs = torch.cat([input, aggr_message], dim = 1)

        #updating nodes using another MLP as phi^v
        update_node_features = self.node_mlp(node_inputs)


        return update_node_features, update_edge_features


"Defining the chain ENCODER, PROCESSOR, DECODER"

class EncoderProcessorDecoder(nn.Module):

    def __init__(self, 
                 input_node_dim,
                 input_edge_dim,
                 latent_size,
                 num_layers_mlp,
                 num_message_passing_steps,
                 output_size
                 ):
        
        super().__init__()

        self.num_steps = num_message_passing_steps

        #defining the node ecoder using an MLP
        self.node_encoder = MLP(
            input_node_dim, 
            latent_size, 
            latent_size,
            num_layers_mlp 
            )
        
        #defining the edges ENCODER using an MLP
        self.edge_encoder = MLP(
            input_edge_dim,
            latent_size,
            latent_size,
            num_layers_mlp
            )
        
        #define PROCESSOR as a list of InterctionNetworks
        self.processor_layers = nn.ModuleList([
            InteractionNetwork(latent_size, num_layers_mlp)
            for i in range(self.num_steps)
        ])

        #define DECODER
        self.decoder = MLP(
            latent_size,
            latent_size,
            output_size,
            num_layers_mlp,
            layer_norm = False
        )

    def forward(self, node_input_data, edge_index, edge_input_data):

        #ENCODE the data
        node_features = self.node_encoder(node_input_data)
        edge_features = self.edge_encoder(edge_input_data)

        #PROCESS the data using the Interaction Networks
        for layer in self.processor_layers:
            delta_node, delta_edge = layer(
            node_features, 
            edge_index,
            edge_features
            )

            #update the node/edge features using residuals
            node_features += delta_node
            edge_features += delta_edge

        #DECODE the data to return the output
        output = self.decoder(node_features)
        
        return output


"""
TEST
model = EncoderProcessorDecoder(10, 10, 5, 2, 3, 1)
print(model)

"""







        




