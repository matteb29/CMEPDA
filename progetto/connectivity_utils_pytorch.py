import torch
from torch_geometric.nn import radius_graph

def compute_connectivity(positions, radius, add_self_edges=True, batch=None):
    """
    Calcola la connettività usando PyTorch Geometric.
    
    Args:
      positions: Tensor [num_nodes, num_dims].
      radius: float, raggio di connettività.
      add_self_edges: bool, se includere self-loops.
      batch: (Opzionale ma raccomandato) Tensor [num_nodes] che indica 
             a quale grafo appartiene ogni nodo. Serve per non collegare 
             nodi di simulazioni diverse.
    
    Returns:
      senders: Tensor Long [num_edges]
      receivers: Tensor Long [num_edges]
    """
    
    # PyTorch Geometric ha una funzione ottimizzata per questo: radius_graph.
    # Restituisce edge_index di forma [2, num_edges].
    # La prima riga sono i 'source' (senders), la seconda i 'target' (receivers).
    edge_index = radius_graph(
        positions, 
        r=radius, 
        batch=batch, 
        loop=add_self_edges, 
        max_num_neighbors=100  # Opzionale: limita i vicini per risparmiare memoria se serve
    )

    # Separiamo senders e receivers per mantenere la compatibilità 
    # con la logica originale di DeepMind che si aspetta due vettori separati.
    senders = edge_index[0]
    receivers = edge_index[1]

    return senders, receivers