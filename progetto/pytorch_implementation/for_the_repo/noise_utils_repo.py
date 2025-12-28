
"""
    Here we write a function to add noise to the input of the Network,
    this results in a more robustness for long simulations,
    with the Simulator learning to adjust its own error

"""




import torch

#define a function to create random noise for the input data
def get_random_walk(positions_sequence, noise_last_step):

    velocities_list= [
        positions_sequence[:, time_i] - positions_sequence[:, time_i -1]
        for time_i in range(positions_sequence.shape[1])
    ]
    velocities_sequence = torch.stack(velocities_list, dim = 1)
    number_velocities = velocities_sequence.shape[1]

    #define the single step noise for random walk 
    single_step_noise = noise_last_step / (number_velocities) ** 0.5

    #and now define the noise for the velocities with std dev = single_step_noise
    noise_velocities = torch.randn_like(velocities_sequence) * single_step_noise

    #summing noise over time
    noise_velocities = torch.cumsum(noise_velocities, dim = 1)
    



