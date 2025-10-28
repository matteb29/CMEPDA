import torch
import torch.nn.functional as F
from torch_geometric.data import HeteroData
from torch_geometric.nn import HeteroConv, SAGEConv, GATConv, Linear
from torch.optim import Adam

# --- 1. Definizione del Grafo Eterogeneo (i Dati) ---
# Questo simula i dati che la HGNN riceve in input.
# Immaginiamo di avere 2 alberi di decadimento e 3 particelle neutre.

data = HeteroData()

# Definiamo i tipi di nodi e le loro "features" (proprietà)
# Es. le features di un albero potrebbero essere [massa, energia, vertice_x, vertice_y]
data['decay_tree'].x = torch.randn(2, 4)  # 2 alberi, 4 features ciascuno

# Es. le features di una neutra potrebbero essere [energia_calorimetro, pos_x, pos_y]
data['neutral_particle'].x = torch.randn(3, 3)  # 3 neutre, 3 features ciascuna

# Definiamo gli archi (i "link") che vogliamo classificare.
# Questi sono TUTTI i link possibili tra neutre e alberi.
# Es: [neutra 0, neutra 0, neutra 1, neutra 2, ...]
#     [albero 0, albero 1, albero 0, albero 1, ...]
edge_index = torch.tensor([
    [0, 0, 1, 1, 2, 2],  # Indice della particella neutra
    [0, 1, 0, 1, 0, 1]   # Indice dell'albero di decadimento
], dtype=torch.long)
data['neutral_particle', 'links_to', 'decay_tree'].edge_index = edge_index

# Definiamo le "etichette" (ground truth) per la classificazione binaria
# 1 = link vero (segnale), 0 = link falso (fondo)
# Supponiamo che solo (neutra 0 -> albero 0) e (neutra 2 -> albero 1) siano veri.
edge_labels = torch.tensor([1, 0, 0, 0, 0, 1], dtype=torch.float)
data['neutral_particle', 'links_to', 'decay_tree'].edge_label = edge_labels


# --- 2. Definizione del Modello HGNN (l'Architettura) ---
# Questa è la rete neurale vera e propria.

class HGNNLinkPredictor(torch.nn.Module):

    def __init__(self, hidden_channels):
        super().__init__()
        
        # Un primo strato HGNN. Applica SAGEConv a tutti i tipi di nodi.
        # Impara a "propagare" le informazioni all'interno del grafo.
        self.conv1 = HeteroConv({
            # Definiamo le convoluzioni per ogni tipo di arco
            ('neutral_particle', 'links_to', 'decay_tree'): SAGEConv((-1, -1), hidden_channels),
            ('decay_tree', 'rev_links_to', 'neutral_particle'): SAGEConv((-1, -1), hidden_channels),
        }, aggr='sum') # 'sum' = aggrega i messaggi sommandoli

        # Un secondo strato HGNN per imparare relazioni più complesse
        self.conv2 = HeteroConv({
            ('neutral_particle', 'links_to', 'decay_tree'): SAGEConv((-1, -1), hidden_channels),
            ('decay_tree', 'rev_links_to', 'neutral_particle'): SAGEConv((-1, -1), hidden_channels),
        }, aggr='sum')

        # Un classificatore (MLP) che prende le "features" finali
        # di una neutra e di un albero e predice se sono collegate.
        # Input: (features_neutra + features_albero) -> Output: 1 (logit)
        self.link_predictor = Linear(2 * hidden_channels, 1)

    def forward(self, x_dict, edge_index_dict, edge_label_index):
        # x_dict contiene {'decay_tree': features, 'neutral_particle': features}
        # edge_index_dict contiene {('neutral', 'links_to', 'tree'): ...}
        
        # Invertiamo gli archi per permettere la propagazione in entrambe le direzioni
        edge_index_dict[('decay_tree', 'rev_links_to', 'neutral_particle')] = \
            edge_index_dict[('neutral_particle', 'links_to', 'decay_tree')].flip([0])
        
        # Esegui i due strati di convoluzione
        x_dict = self.conv1(x_dict, edge_index_dict)
        x_dict = {key: x.relu() for key, x in x_dict.items()}
        x_dict = self.conv2(x_dict, edge_index_dict)

        # Ora abbiamo le features "arricchite" (embedding) per tutti i nodi.
        
        # Prepariamo l'input per il classificatore
        src, dst = edge_label_index
        src_emb = x_dict['neutral_particle'][src]
        dst_emb = x_dict['decay_tree'][dst]
        
        # Concateniamo le features della neutra e dell'albero
        link_input = torch.cat([src_emb, dst_emb], dim=-1)
        
        # Facciamo la predizione binaria
        prediction_logits = self.link_predictor(link_input)
        
        return prediction_logits.squeeze()


# --- 3. Addestramento del Modello ---

model = HGNNLinkPredictor(hidden_channels=64)
optimizer = Adam(model.parameters(), lr=0.01)

# Usiamo la "BCE with Logits Loss" (come menzionato nella slide)
# È più stabile numericamente che usare una Sigmoid + BCE Loss separata.
criterion = torch.nn.BCEWithLogitsLoss()

def train():
    
    model.train()
    optimizer.zero_grad()
    
    # Prendi gli archi (link) che vogliamo classificare
    edge_label_index = data['neutral_particle', 'links_to', 'decay_tree'].edge_index
    
    # Esegui il modello
    out = model(data.x_dict, data.edge_index_dict, edge_label_index)
    
    # Prendi le etichette (ground truth)
    target = data['neutral_particle', 'links_to', 'decay_tree'].edge_label
    
    # Calcola la loss (BCE)
    loss = criterion(out, target)
    
    loss.backward()
    optimizer.step()
    return loss

# Ciclo di addestramento (molto semplificato)
for epoch in range(1, 101):
    loss = train()
    if epoch % 10 == 0:
        print(f'Epoch: {epoch:03d}, Loss: {loss:.4f}')

# --- 4. Ottenere le Predizioni Finali ---
model.eval()
with torch.no_grad():
    edge_label_index = data['neutral_particle', 'links_to', 'decay_tree'].edge_index
    logits = model(data.x_dict, data.edge_index_dict, edge_label_index)
    
    # Applichiamo la funzione sigmoide per ottenere probabilità (0.0 a 1.0)
    probabilities = logits.sigmoid()
    
    print("\n--- Predizioni Finali ---")
    print(f"Link (Neutra, Albero): Probabilità")
    for i in range(edge_label_index.shape[1]):
        neutra_idx = edge_label_index[0, i].item()
        albero_idx = edge_label_index[1, i].item()
        prob = probabilities[i].item()
        vero = edge_labels[i].item()
        print(f"Link ({neutra_idx}, {albero_idx}): {prob:.4f} (Vero: {vero})")