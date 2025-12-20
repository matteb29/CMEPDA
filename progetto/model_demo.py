import collections
import torch
import numpy as np

# Assumiamo che tu abbia già convertito questi moduli come discusso
from learning_to_simulate import learned_simulator
# from learning_to_simulate import noise_utils 
# (Se non hai ancora convertito noise_utils, useremo una funzione dummy qui sotto)

INPUT_SEQUENCE_LENGTH = 6
SEQUENCE_LENGTH = INPUT_SEQUENCE_LENGTH + 1  # aggiunge una posizione target
NUM_DIMENSIONS = 3
NUM_PARTICLE_TYPES = 6
BATCH_SIZE = 2  # Ridotto per il test
GLOBAL_CONTEXT_SIZE = 6

# Struttura dati semplice per le statistiche (non serve namedtuple complessa per ora)
Stats = collections.namedtuple("Stats", ["mean", "std"])

# Creiamo tensori PyTorch per le statistiche dummy
DUMMY_STATS = Stats(
    mean=torch.zeros(NUM_DIMENSIONS),
    std=torch.ones(NUM_DIMENSIONS))

DUMMY_CONTEXT_STATS = Stats(
    mean=torch.zeros(GLOBAL_CONTEXT_SIZE),
    std=torch.ones(GLOBAL_CONTEXT_SIZE))

DUMMY_BOUNDARIES = [(-1., 1.)] * NUM_DIMENSIONS

def get_random_walk_noise(position_sequence, noise_std_last_step):
    """Versione semplificata di noise_utils per la demo."""
    # Simula il rumore random walk
    velocity_sequence = position_sequence[:, 1:] - position_sequence[:, :-1]
    n_part, n_steps, dims = velocity_sequence.shape
    noise = torch.randn_like(velocity_sequence) * (noise_std_last_step / (n_steps**0.5))
    noise = torch.cumsum(noise, dim=1)
    
    # Aggiungiamo uno zero iniziale per matching delle dimensioni se necessario
    # Ma per semplicità, ritorniamo una noise mask della stessa shape dell'input
    position_noise = torch.cat([torch.zeros(n_part, 1, dims), noise], dim=1)
    return position_noise[:, :position_sequence.shape[1]]

def sample_random_position_sequence():
    """Genera dati finti per una simulazione."""
    num_particles = torch.randint(low=50, high=100, size=(1,)).item()
    
    # Shape: [num_particles, SEQUENCE_LENGTH, NUM_DIMENSIONS]
    position_sequence = torch.randn(num_particles, SEQUENCE_LENGTH, NUM_DIMENSIONS)
    return position_sequence

def main():
    print("Inizializzazione del modello PyTorch...")
    
    # 1. Costruiamo il modello
    model = learned_simulator.LearnedSimulator(
        num_dimensions=NUM_DIMENSIONS,
        connectivity_radius=0.05,
        graph_network_kwargs=dict(
            latent_size=128,
            mlp_hidden_size=128,
            mlp_num_hidden_layers=2,
            num_message_passing_steps=10,
        ),
        boundaries=DUMMY_BOUNDARIES,
        normalization_stats={
            "acceleration": DUMMY_STATS,
            "velocity": DUMMY_STATS,
            "context": DUMMY_CONTEXT_STATS
        },
        num_particle_types=NUM_PARTICLE_TYPES,
        particle_type_embedding_size=16,
    )

    # Mettiamo il modello in modalità valutazione (o training se vogliamo calcolare gradienti)
    model.train() 

    print("Generazione dati dummy...")
    
    # 2. Creiamo un Batch di dati
    # In PyTorch Geometric, concateniamo tutti i nodi e usiamo un vettore 'batch'
    sampled_sequences = [sample_random_position_sequence() for _ in range(BATCH_SIZE)]
    
    particle_counts = [seq.shape[0] for seq in sampled_sequences]
    
    # Concateniamo tutto in un unico tensore [TOTAL_PARTICLES, SEQ_LEN, DIMS]
    position_sequence_batch = torch.cat(sampled_sequences, dim=0)
    
    # Creiamo il vettore batch: [0,0,0, ..., 1,1,1, ...]
    batch_vector_list = []
    for i, count in enumerate(particle_counts):
        batch_vector_list.append(torch.full((count,), i, dtype=torch.long))
    batch_vector = torch.cat(batch_vector_list, dim=0)

    # Tipi di particelle casuali
    particle_types = torch.randint(0, NUM_PARTICLE_TYPES, (position_sequence_batch.shape[0],))
    
    # Contesto globale
    global_context = torch.rand(BATCH_SIZE, GLOBAL_CONTEXT_SIZE) * 2 - 1

    # Input e Target
    # Input: prime 6 posizioni
    input_position_sequence = position_sequence_batch[:, :-1] 
    # Target: l'ultima posizione (quella che vogliamo prevedere)
    target_next_position = position_sequence_batch[:, -1]

    print(f"Input shape: {input_position_sequence.shape}")
    print(f"Batch vector shape: {batch_vector.shape}")

    # 3. Inferenza (Forward Pass)
    # Nota: n_particles_per_example non serve più, usiamo batch_vector
    predicted_next_position = model(
        input_position_sequence, 
        global_context, 
        particle_types,
        batch=batch_vector
    )
    
    print("\n--- Risultato Inferenza ---")
    print(f"Predicted position shape: {predicted_next_position.shape}")
    print(f"Output tensor (primi 2): \n{predicted_next_position[:2]}")

    # 4. Calcolo Loss (Training Step simulato)
    # Generiamo rumore per il training
    position_sequence_noise = get_random_walk_noise(
        input_position_sequence, noise_std_last_step=6.7e-4)

    # Calcoliamo accelerazioni predette e target (per la loss function)
    pred_acc, target_acc = model.get_predicted_and_target_normalized_accelerations(
        next_position=target_next_position,
        position_sequence_noise=position_sequence_noise,
        position_sequence=input_position_sequence,
        global_context=global_context,
        particle_types=particle_types,
        batch=batch_vector
    )

    print("\n--- Risultato Training Step ---")
    print(f"Predicted Acceleration shape: {pred_acc.shape}")
    print(f"Target Acceleration shape: {target_acc.shape}")

    # Calcolo loss MSE semplice per dimostrazione
    loss = torch.nn.functional.mse_loss(pred_acc, target_acc)
    print(f"Loss calcolata: {loss.item()}")

if __name__ == "__main__":
    main()