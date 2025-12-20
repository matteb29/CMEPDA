import torch

def get_random_walk_noise_for_position_sequence(position_sequence, noise_std_last_step):
    """
    Returns random-walk noise in the velocity applied to the position.
    
    Args:
        position_sequence: Tensor [n_particles, seq_len, dim]
        noise_std_last_step: float, deviazione standard del rumore all'ultimo step.
    """

    # 1. Calcoliamo la velocità come differenza tra posizioni adiacenti
    # TensorFlow usava learned_simulator.time_diff, qui lo facciamo inline per semplicità.
    # position_sequence[:, 1:] prende dal secondo elemento in poi
    # position_sequence[:, :-1] prende fino al penultimo
    velocity_sequence = position_sequence[:, 1:] - position_sequence[:, :-1]

    # 2. Calcoliamo la scala del rumore
    # Vogliamo che la varianza del rumore si accumuli in modo controllato.
    num_velocities = velocity_sequence.shape[1]
    
    # torch.randn_like crea numeri casuali (media 0, std 1) con la stessa shape dell'input
    noise_scaling = noise_std_last_step / (num_velocities ** 0.5)
    velocity_sequence_noise = torch.randn_like(velocity_sequence) * noise_scaling

    # 3. Applica il random walk alla velocità (somma cumulativa lungo l'asse temporale)
    # dim=1 è l'asse della sequenza temporale
    velocity_sequence_noise = torch.cumsum(velocity_sequence_noise, dim=1)

    # 4. Integra il rumore della velocità per ottenere il rumore sulla posizione.
    # Assumiamo integrazione di Eulero e dt=1.
    # Non aggiungiamo rumore alla primissima posizione (indice 0).
    
    # Creiamo un tensore di zeri per il primo step temporale.
    # IMPORTANTE: device=... assicura che se stai usando la GPU, gli zeri siano sulla GPU.
    zeros = torch.zeros(
        (velocity_sequence_noise.shape[0], 1, velocity_sequence_noise.shape[2]),
        dtype=position_sequence.dtype,
        device=position_sequence.device
    )

    # Integriamo il rumore della velocità
    position_noise_integrated = torch.cumsum(velocity_sequence_noise, dim=1)

    # Concateniamo lo zero iniziale con il rumore integrato
    position_sequence_noise = torch.cat([zeros, position_noise_integrated], dim=1)

    return position_sequence_noise