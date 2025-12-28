
"""
    Here we want to write a naive demo 
    to test our simulator with dummy data

"""

import collections
import torch
import numpy as np
from learned_simulator_repo import Normalizer, Simulator
"from noise_utils_repo import"


#lenght of input data: current velocity + 5 past ones
INPUT_LENGHT = 6

#lenght of sequence: 6 inputs + 1 target
SEQUENCE_LENGHT = INPUT_LENGHT + 1

#dimension of the dummy data 
NUM_DIMENSIONS = 2

#number of type of different dummy particles
NUM_PARTICLE_TYPES = 6
EMBEDDING_SIZE = 16

BATCH_SIZE = 2

#account for global features such as gravity, 
#Temperature, possibile Magnetic fields, size of the box etc
GLOBAL_LENGHT = 6


#define a named tuple for stats of dummy data
stats = collections.namedtuple("stats", ["mean", "std_dev"])

#define torch tensor for dummy stats of the particles
dummy_particles_stats = stats(
    mean = torch.zeros(NUM_DIMENSIONS),
    std_dev = torch.ones(NUM_DIMENSIONS)
)

#define torch tensor for dummy global stats
dummy_global_stats = stats(
    mean = torch.zeros(GLOBAL_LENGHT),
    std_dev = torch.ones(GLOBAL_LENGHT)
)

#define dummy boundaries for the box
dummy_boundaries = [(-1, 1)] * NUM_DIMENSIONS


#define a function to simulate dummy data
def get_random_positions_sequence():

    num_particles = torch.randint(low = 50, high = 100, size = (1,)).item()

    #define a dummy sequence of random positions as torch tensor
    position_sequence = torch.randn(num_particles, SEQUENCE_LENGHT, NUM_DIMENSIONS)

    return position_sequence



def main():

    print("Initializating the model...")

    #define the model as Simulator from learned_simulator
    dummy_model = Simulator(

        particle_dimensions = NUM_DIMENSIONS,
        connectivity_radius = 0.05,
        latent_size = 128,
        num_layers = 2,
        connectivity_radius = 0.05,
        message_passing_steps = 10,
        boundaries = dummy_boundaries,
        num_particle_types = NUM_PARTICLE_TYPES,
        dim_particle_embedding = EMBEDDING_SIZE

    )

    #define the normalized stats
    dummy_model.output_normalizer = Normalizer(
        size = NUM_DIMENSIONS, 
        name = "accelerations"
        )
    #normalize the stats with 0 mean and 1 std dev
    dummy_model.output_normalizer.mean = dummy_global_stats.mean
    dummy_model.output_normalizer.std_dev = dummy_global_stats.std_dev

    #let's train the model
    dummy_model.train()


    #now generate the dummy data
    dummy_sequence = [
        get_random_positions_sequence() 
        for i in range(BATCH_SIZE)
    ]

    dummy_positions = torch.cat(dummy_sequence, dim = -1)

    #count the number of particles in each simulation
    number_particles = [seq.shape[0] for seq in dummy_positions]

    #label the simulated data according their simulation
    simulations_label = []

    for i in range(len(number_particles)):
        number = number_particles[i]
        l = torch.ones(number, dtype = torch.long) * i
        simulations_label.append(l)

    batch_labels = torch.cat(simulations_label, dim = -1)

    #get a random number of types particles
    particle_types = torch.randint(
        low = 0, high = NUM_PARTICLE_TYPES,
        dim = dummy_positions.shape[0]
    )

    #dummy global features for each simulations
    global_features = torch.randint(BATCH_SIZE, GLOBAL_LENGHT)

    past_and_current_pos = dummy_positions[:, :-1]
    next_positions = dummy_positions[:, -1]


    #now let's do the inference
    print("Starting inference on dummy data...")

    #predict positions(we don't give next_position to the model for inference!)
    next_positions_predicted = dummy_model(
        past_and_current_pos,
        particle_types,
        global_features,
        batch = batch_labels
    )

    print(f"output shape: {next_positions_predicted.shape} ")


    #now let's compute the loss on predictions

    print("Computing the Loss")

    "------------------------------------------------------------"
    position_sequence_noise = noise_utils_repo.get_random_walk(
        position_sequence = dummy_positions,

    )

    "---------------------------------------------"

    predicted_acc, target_acc = dummy_model.helper_training(
        next_positions = next_positions,
        positions_sequence_noise = position_sequence_noise,
        position_sequence = past_and_current_pos,
        particle_types = particle_types,
        global_context = global_features,
        batch = batch_labels
    )

    loss = torch.nn.functional.mse_loss(predicted_acc, target_acc)

    print(f"Loss:  {loss.item():.6f}")

    if __name__ == "__main__":
        main()