import torch
import torch.nn as nn
from torch_cluster import radius_graph
from model_pytorch import EncodeProcessDecode

class Normalizer(nn.Module):
    """
    Classe helper per normalizzare input e output.
    Le GNN non funzionano se i dati non sono centrati in 0 con deviazione standard 1.
    """
    def __init__(self, size, max_accumulations=10**6, std_epsilon=1e-8):
        super(Normalizer, self).__init__()
        self.register_buffer('acc_sum', torch.zeros(size))
        self.register_buffer('acc_sum_squared', torch.zeros(size))
        self.register_buffer('acc_count', torch.zeros(1))
        self.register_buffer('mean', torch.zeros(size))
        self.register_buffer('std', torch.ones(size))
        self.std_epsilon = std_epsilon
        self.accumulating = True

    def update(self, batch):
        if not self.accumulating: return
        count = batch.shape[0]
        self.acc_count += count
        self.acc_sum += batch.sum(dim=0)
        self.acc_sum_squared += (batch**2).sum(dim=0)
        
        self.mean = self.acc_sum / self.acc_count
        self.std = torch.sqrt((self.acc_sum_squared / self.acc_count) - self.mean**2 + self.std_epsilon)

    def normalize(self, batch):
        return (batch - self.mean) / self.std

    def inverse(self, batch):
        return batch * self.std + self.mean

class Simulator(nn.Module):
    def __init__(self, 
                 particle_dimension=2, 
                 node_in=30, 
                 edge_in=3, 
                 latent_dim=128, 
                 num_layers=2, 
                 mp_steps=10, 
                 connectivity_radius=0.015):
        super(Simulator, self).__init__()
        
        self.connectivity_radius = connectivity_radius
        self.particle_dimension = particle_dimension
        
        # Le normalizzazioni (Statistiche)
        self.node_normalizer = Normalizer(node_in)
        self.edge_normalizer = Normalizer(edge_in)
        self.output_normalizer = Normalizer(particle_dimension) # Prediciamo l'accelerazione (2D)

        # Il modello GNN (quello che abbiamo scritto prima)
        self.gnn = EncodeProcessDecode(
            input_node_dim=node_in,
            input_edge_dim=edge_in,
            latent_size=latent_dim,
            num_layers_mlp=num_layers,
            num_message_passing_steps=mp_steps,
            output_size=particle_dimension
        )

    def _get_edge_features(self, pos, edge_index):
        """
        Costruisce le feature degli spigoli: (dx, dy, distanza, ...)
        """
        sender = pos[edge_index[0]]
        receiver = pos[edge_index[1]]
        
        # Distanza relativa (vettore)
        relative_pos = sender - receiver 
        # Distanza assoluta (scalare)
        norm = torch.norm(relative_pos, dim=-1, keepdim=True)
        
        # Le features sono: [dx, dy, distanza]
        edge_attr = torch.cat([relative_pos, norm], dim=-1)
        return edge_attr

    def predict_accelerations(self, position_sequence, particle_types):
        """
        Questo è il cuore della simulazione.
        INPUT:
          - position_sequence: [N_particelle, 6, 2] (Posizioni attuali e 5 passate)
          - particle_types: [N_particelle] (Tipo materiale)
        OUTPUT:
          - accelerazione predetta
        """
        
        # 1. Prepara i nodi (Input Node Features)
        # Calcoliamo le velocità passate: v(t) = x(t) - x(t-1)
        # La rete usa le ultime 5 velocità come input
        current_pos = position_sequence[:, -1] # Posizione attuale
        
        velocities = []
        for t in range(1, 6):
            v = position_sequence[:, t] - position_sequence[:, t-1]
            velocities.append(v)
            
        # Concateniamo tutto per fare il vettore di input del nodo
        # Input = [velocità_passate, distanza_bordi(opzionale), one_hot_types]
        # Nota: Qui semplifico un po' rispetto al paper originale per chiarezza
        # particle_types andrebbe convertito in One-Hot encoding e appeso qui.
        node_features = torch.cat(velocities, dim=-1) # Shape: [N, 10]
        
        # 2. Costruisci il Grafo Dinamico
        # Usa torch_cluster.radius_graph: è velocissimo su GPU
        edge_index = radius_graph(current_pos, r=self.connectivity_radius, loop=False)
        
        # 3. Calcola features spigoli
        edge_features = self._get_edge_features(current_pos, edge_index)
        
        # 4. Normalizza
        norm_nodes = self.node_normalizer.normalize(node_features)
        norm_edges = self.edge_normalizer.normalize(edge_features)
        
        # 5. Passa nella GNN
        pred_normalized = self.gnn(norm_nodes, edge_index, norm_edges)
        
        # 6. Denormalizza l'output
        return self.output_normalizer.inverse(pred_normalized)

    def step(self, position_sequence, particle_types):
        """
        Esegue un passo di simulazione (Integrazione di Eulero)
        """
        # Prediciamo l'accelerazione (o il cambio di velocità)
        acc = self.predict_accelerations(position_sequence, particle_types)
        
        # Integrazione di Eulero: x(t+1) = x(t) + v(t) + a(t)
        # v_last = x(t) - x(t-1)
        current_pos = position_sequence[:, -1]
        last_pos = position_sequence[:, -2]
        current_vel = current_pos - last_pos
        
        # Nuova posizione
        next_pos = current_pos + current_vel + acc
        
        return next_pos