import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_scatter import scatter_add

class MLP(nn.Module):
    """
    Un Multi-Layer Perceptron standard con LayerNorm.
    Corrisponde a snt.nets.MLP del codice originale.
    """
    def __init__(self, input_size, hidden_size, output_size, num_layers, layer_norm=True):
        super(MLP, self).__init__()
        layers = []
        in_dim = input_size
        
        for _ in range(num_layers - 1):
            layers.append(nn.Linear(in_dim, hidden_size))
            layers.append(nn.ReLU())
            in_dim = hidden_size
            
        layers.append(nn.Linear(in_dim, output_size))
        
        if layer_norm:
            # DeepMind mette la LayerNorm alla fine di ogni blocco MLP
            layers.append(nn.LayerNorm(output_size))
            
        self.net = nn.Sequential(*layers)

    def forward(self, x):
        return self.net(x)

class InteractionNetwork(nn.Module):
    """
    Il blocco fondamentale del "Processor".
    Corrisponde al blocco InteractionNetwork di Graph Nets.
    Aggiorna gli spigoli (edges) e poi i nodi (nodes).
    """
    def __init__(self, hidden_size, num_layers):
        super(InteractionNetwork, self).__init__()
        
        # MLP per aggiornare gli spigoli: Input = [edge_attr, node_sender, node_receiver]
        # Dimensione input = hidden (edge) + hidden (sender) + hidden (receiver) = 3 * hidden
        self.edge_mlp = MLP(3 * hidden_size, hidden_size, hidden_size, num_layers)
        
        # MLP per aggiornare i nodi: Input = [node_attr, aggregated_edges]
        # Dimensione input = hidden (node) + hidden (msg) = 2 * hidden
        self.node_mlp = MLP(2 * hidden_size, hidden_size, hidden_size, num_layers)

    def forward(self, x, edge_index, edge_attr):
        # x: [num_nodes, hidden_size]
        # edge_index: [2, num_edges] (row=senders, col=receivers)
        # edge_attr: [num_edges, hidden_size]
        
        row, col = edge_index
        senders = x[row]
        receivers = x[col]
        
        # 1. Edge Update Step
        # Concateniamo: feature spigolo + feature nodo mittente + feature nodo ricevente
        edge_inputs = torch.cat([edge_attr, senders, receivers], dim=1)
        updated_edge_attr = self.edge_mlp(edge_inputs) # phi^e
        
        # 2. Aggregation Step (Message Passing)
        # Sommiamo tutti gli spigoli che arrivano allo stesso ricevente (col)
        # unsorted_segment_sum di TF diventa scatter_add in PyTorch
        aggr_messages = scatter_add(updated_edge_attr, col, dim=0, dim_size=x.size(0))
        
        # 3. Node Update Step
        # Concateniamo: feature nodo originale + somma messaggi ricevuti
        node_inputs = torch.cat([x, aggr_messages], dim=1)
        updated_node_attr = self.node_mlp(node_inputs) # phi^v
        
        # Ritorniamo sia nodi che spigoli aggiornati (per le connessioni residue)
        return updated_node_attr, updated_edge_attr

class EncodeProcessDecode(nn.Module):
    """
    L'architettura completa GNS (Graph Network Simulator).
    """
    def __init__(self, 
                 input_node_dim, 
                 input_edge_dim, 
                 latent_size, 
                 num_layers_mlp, 
                 num_message_passing_steps, 
                 output_size):
        super(EncodeProcessDecode, self).__init__()
        
        self.num_steps = num_message_passing_steps
        
        # --- ENCODER ---
        # Trasforma gli input grezzi nello spazio latente
        self.node_encoder = MLP(input_node_dim, latent_size, latent_size, num_layers_mlp)
        self.edge_encoder = MLP(input_edge_dim, latent_size, latent_size, num_layers_mlp)
        
        # --- PROCESSOR ---
        # Una lista di InteractionNetworks che si passano i dati
        self.processor_layers = nn.ModuleList([
            InteractionNetwork(latent_size, num_layers_mlp) 
            for _ in range(num_message_passing_steps)
        ])
        
        # --- DECODER ---
        # Dal latente all'output fisico (accelerazione/velocità)
        self.decoder = MLP(latent_size, latent_size, output_size, num_layers_mlp, layer_norm=False)

    def forward(self, x, edge_index, edge_attr):
        """
        x: [N, input_node_dim] (Posizione, Velocità, Tipi particella)
        edge_index: [2, E] (Connettività)
        edge_attr: [E, input_edge_dim] (Distanza relativa, spostamento)
        """
        
        # 1. ENCODE
        x = self.node_encoder(x)
        edge_attr = self.edge_encoder(edge_attr)
        
        # 2. PROCESS (Message Passing Loop)
        # Manteniamo le connessioni residue (skip connections)
        # x_new = x_old + GNN(x_old)
        for layer in self.processor_layers:
            delta_x, delta_edge = layer(x, edge_index, edge_attr)
            
            # Residual connection: fondamentale per simulazioni stabili!
            x = x + delta_x
            edge_attr = edge_attr + delta_edge
            
        # 3. DECODE
        # L'output è solitamente l'accelerazione o la variazione di velocità
        output = self.decoder(x)
        
        return output