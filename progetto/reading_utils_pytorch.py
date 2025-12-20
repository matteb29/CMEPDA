import torch
from torch.utils.data import Dataset

def split_trajectory(context, features, window_length=7):
    """
    Divide una lunga traiettoria in finestre scorrevoli (sliding windows) per il training.
    Equivalente alla funzione split_trajectory di DeepMind, ma usando PyTorch.
    
    Args:
      context: Dict con caratteristiche costanti (es. 'particle_type').
      features: Dict con caratteristiche variabili nel tempo (es. 'position').
      window_length: Lunghezza della sequenza di input + 1 target.
      
    Returns:
      Un dizionario contenente le traiettorie tagliate pronte per il batching.
    """
    
    # features['position'] ha shape [Time_Steps, Num_Particles, Dims]
    pos_sequence = features['position']
    particle_type = context['particle_type'] # Shape [Num_Particles]
    
    num_steps = pos_sequence.shape[0]
    
    # Calcoliamo quante finestre possiamo estrarre
    # Esempio: Se ho 1000 step e window=7, ottengo 994 finestre
    num_windows = num_steps - window_length + 1
    
    if num_windows < 1:
        raise ValueError(f"La traiettoria è troppo corta ({num_steps}) per la finestra richiesta ({window_length}).")

    # --- 1. Creazione delle finestre (Sliding Window) ---
    # In PyTorch usiamo .unfold() che è molto efficiente e non copia memoria
    # unfold(dimension, size, step)
    # Input: [Time, N, D] -> Output: [Num_Windows, N, D, Window_Len]
    windows = pos_sequence.unfold(0, window_length, 1)
    
    # Permutiamo le dimensioni per ottenere: [Num_Windows, Window_Len, N, D]
    # Questo corrisponde a [Batch, Time, Nodes, Features]
    trajectory_windows = windows.permute(0, 3, 1, 2)
    
    # --- 2. Gestione del Particle Type ---
    # Il tipo di particella è statico, ma dobbiamo ripeterlo per ogni finestra
    # per creare un batch coerente.
    # Shape: [Num_Windows, Num_Particles]
    particle_types_batch = particle_type.unsqueeze(0).expand(num_windows, -1)
    
    # --- 3. Gestione del Global Context (se presente) ---
    # Esempio: gravità o forze esterne che cambiano nel tempo
    step_context_batch = None
    if 'step_context' in features:
        context_seq = features['step_context'] # [Time, Context_Dim]
        # Creiamo finestre anche per il contesto
        context_windows = context_seq.unfold(0, window_length, 1)
        # Permute -> [Num_Windows, Window_Len, Context_Dim]
        step_context_batch = context_windows.permute(0, 2, 1)

    # Prepariamo l'output
    output = {
        'position': trajectory_windows,         # [Batch, Time, N, D]
        'particle_type': particle_types_batch,  # [Batch, N]
    }
    
    if step_context_batch is not None:
        output['step_context'] = step_context_batch

    return output

class SimulationDataset(Dataset):
    """
    Un Dataset PyTorch semplice per caricare dati già convertiti.
    Assumiamo che i dati siano una lista di dizionari (es. caricati da .npz).
    """
    def __init__(self, data_list, window_length=7):
        self.data_list = data_list
        self.window_length = window_length
        self.samples = []
        
        # Pre-processiamo tutte le traiettorie tagliandole in finestre
        # (Nota: per dataset enormi, questo si farebbe 'lazy' nel __getitem__, 
        # ma per iniziare va bene farlo qui).
        print(f"Processando {len(data_list)} simulazioni...")
        for example in data_list:
            # example deve avere chiavi: 'position', 'particle_type'
            context = {'particle_type': example['particle_type']}
            features = {'position': example['position']}
            if 'step_context' in example:
                features['step_context'] = example['step_context']
            
            # Tagliamo la traiettoria
            splitted = split_trajectory(context, features, window_length)
            
            # Aggiungiamo ogni singola finestra alla lista dei campioni
            num_windows = splitted['position'].shape[0]
            for i in range(num_windows):
                sample = {
                    'position': splitted['position'][i],       # [Time, N, D]
                    'particle_type': splitted['particle_type'][i] # [N]
                }
                if 'step_context' in splitted:
                    sample['step_context'] = splitted['step_context'][i]
                
                self.samples.append(sample)
    
    def __len__(self):
        return len(self.samples)
    
    def __getitem__(self, idx):
        return self.samples[idx]