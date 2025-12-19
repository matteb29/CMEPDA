
"""

Vogliamo creare una Graph Neural Network che sia in grado di distinguere i 
cerchi dai rettangoli, rapppresentando le immagini come nuvole di punti

"""


import torch
import torch_geometric #utile per gestire le GNN
from torch_cluster import knn_graph #per trovare i primi k vicini di un nodo nel grafo
import networkx as nx #per disegnare un grafo
from torch.nn import Sequential, Linear, ReLU
from torch_geometric.nn import MessagePassing, global_max_pool, global_mean_pool
import torch.nn.functional as F
from torch_geometric.loader import DataLoader



import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split

import random




N = 2000 #numero di figure

filled = False

if filled:

    S = 200 #numero di nodi nel grafo (numero di punti per ogni figura)

else:
    S = 20 #numero di nodi nel grafo se l' immagine non è riempita



#generiamo rettangoli come nuvole di punti

if not filled: #facciamo i punti del perimetro


    xy = np.random.randint(0, 2, size = N*S) #genero un array di lunghezza N*S contenente 0 or 1
    #in base al quale decide se il punto sta su asse x o su asse y

    #print(xy[:10])

    side = np.random.randint(0, 2, size = N*S) #genera un array di lunghezza N*S contenente 0 or 1
    #in base al quale decide su quale lato sta il punto

   # print(side[:10])


    # a, b sono le coordinate del punto all' interno
    # di un sistema di coordinate [0,1] x [0,1], quindi il cerchio e il rettangolo cadono in un rettangolo [0,1]x[0,1]


    a = np.random.uniform(0, 1, size = S*N) * xy + side*(1-xy) #coordinata orizzontale
    b = np.random.uniform(0,1, size = S*N) * (1-xy) + side*xy #coordinata verticale

    #le prime S entries del vettore A sono le coordinate orizzontali degli S punti che formano un rettangolo
    #le prime S entries del vettore B sono le coordinate verticali degli S punti che formano un rettangolo

else:

    #se la figura la faccio piena mi basta generare 2 numeri compresi tra 0 e 1
    #per creare le coordinate del punto

    a = np.random.uniform(0, 1, size = N*S)
    b = np.random.uniform(0,1, size = N*S)




#creiamo ora  un array per cambiare altezza e larghezza del rettangolo modificando della solita quantità le coordinate orizzontali e verticali 
#degli S punti che compongono il rettangolo

width = np.repeat(np.random.uniform(3,10, size = N), S ) #np.repeat ripete per S volte un array di dimensione N 
#costituito da numeri uniformi tra 3 e 10
#cosi riesco a moltiplicare tutte le S coordinate orizzontali degli S punti del rettangolo della stessa quantità (trasformazione rigida)



height = np.repeat(np.random.uniform(3,10, size = N), S) 



#array per cambiare la posizione dei punti su x e su y
px = np.repeat(np.random.uniform(1,90, size = N), S)
py = np.repeat(np.random.uniform(1,90, size = N), S)


#usiamo gli array creati prima per cambiare il rettangolo

rx = (a * width + px).reshape(N, -1) #cambio la coordinata x degli N rettangoli
ry = (b * height + py).reshape(N, -1) #cambio la coordinata y degli N rettangoli


#creiamo la matrici di dati del rettangolo

X_rect = np.stack([rx,ry], axis = 2) #con axis = 2 creo un oggetto
#a 3 indici in cui i primi 2 sono (riga, colonna) mentre il terzo serve per specificare di 
#quale matrice si parla




"Ora generiamo i cerchi come nuvole di punti"


theta = np.random.uniform(0, 2*np.pi, S*N )

if filled:
    radius = np.random.uniform(0,1, S*N) ** 0.5 # per rendere uniforme il raggio al quadrato
    #cosi riempio l' area in modo uniforme

else:
    radius = np.ones(S*N) #array di 1 di dimensione S*N 


#creiamo un vettore per riscalare il cerchio e per cambaire la posizione del suo centro

scale = np.repeat(np.random.uniform(3,10, size = N), S)
ox = np.repeat(np.random.uniform(10,90, size = N), S)
oy = np.repeat(np.random.uniform(10,90, size = N), S)


cx = (radius * np.cos(theta) * scale + ox).reshape(N,-1)
cy = (radius * np.sin(theta) * scale + oy).reshape(N, -1)


#creiamo i dati per il cerchio
X_circ = np.stack([cx,cy], axis = 2)


#creiamo il dataset completo, fatto da cerchi e rettangoli

X = np.concatenate([X_rect, X_circ]) #come usare np.stack con axis = 0, cioè impila con righe

y = np.concatenate([np.zeros(N), np.ones(N)]).reshape((-1,+1))
#se y = 0 ho un rettangolo, se 1 ho un cerchio: problema di CLASSIFICAZIONE

#reshape(-1,+1) impone che il numero di righe sia automatico per generare i dati con una sola colonna 
#quindi concateno e poi faccio il reshape



#splittiamo il dataset e le etichette in training e test

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.5, random_state = 1 )
#ricordiamo che con random state divide i dati di test e training sempre nello stesso modo
#cioè imponi un seme con il quale dividere i dati


"Mostriamo ora qualche figura"


for j in range(2):

    plt.xlim(0,100)
    plt.ylim(0,100)


    #X_train[j, :, 0] prendiamo la figura j, tutte le sue colonne e selezioniamo la prima
    #matrice che è quella delle coordinate x 

    plt.scatter(X_train[j, :, 0], X_train[j, :, 1])
    #s(=1 if filled else 5)
    plt.show()


"""
Ora creiamo una struttura dati per il grafo 

"""


#prepariamo i dati per essere utilizzati con pytorch geometric

#training
dataset_train = [torch_geometric.data.Data(x=torch.Tensor(x[:random.randint(S/2, S)]), y = torch.Tensor(y.reshape(1,1))) for x,y in zip(X_train, y_train)]

#ogni dato di training (ogni figura) non avrà il solito numero di punti cosi che la graph net 
#impari a distinguere la figura indipendentemente dal numero di punti che compongonon la figura
#ad esempio dataset_train[0].x	(72, 2) è il primo esempio di training

"""

for x,y in zip(x_train,y_train) scorre su tutti i dati e etichette del training
definisco  x il tensore torch prendendo  un numero casuale tra S/2 e S e considerando tutti gli elementi di x
fino a quel numero casuale

per y invece genero il tensore torch scrivendo un etichetta y (0 or 1) nel formato di matrice 1x1
per calcolare la loss della GNN devo lavorare con tensore pytorch quindi anche un semplice scalare va
scritto come tensore pytorch (1,1)

"""


#test
dataset_test = [torch_geometric.data.Data(x=torch.Tensor(x[:random.randint(S/2, S)]), y = torch.Tensor(y.reshape(1,1))) for x,y in zip(X_test, y_test)]




"""
creiamo un grafo con i k vicini di ogni nodo
CREARE UN GRAFO = FARE I COLLEGAMENTI DEI PUNTI

"""



if filled:

    nNeighbours = 15

else:

    nNeighbours = 5

for data in dataset_train:

    #la funzione knn_graph crea un grafo per ogni data in dataset_train
    #prendendo ciascun punto (che diventerà un nodo del grafo) e collegandolo ai k vicini
    #e salva i collegamenti nel tensore data.edge_index che è un tensore specifico di pytorch
    #che contiene tutti i collegamenti dei nodi per ogni grafo

    #i vicini vengono calcoli di default assumendo che i dati contengano le coordinate dei punti
    #e utilizzando la distanza euclidea

    data.edge_index = knn_graph(data.x, k = nNeighbours) 

    #l' attributo .x sono le features dei nodi (nel nostro codice le coordinate spaziali dei punti)
    #l' attributo .edge_index sono i collegamenti dei nodi

for data in dataset_test:

    data.edge_index = knn_graph(data.x, k = nNeighbours)



#vediamo tutti i collegamenti dei neuroni del grafo 0 usando l' attributo .edge_index
#dell' elemento 0 del dataset_train
print(dataset_train[0].edge_index)

"visualizzando il grafo come immagine"

for j in range(3):

    data = dataset_train[j]

    #per fare il disegno del grafo
    grafo = torch_geometric.utils.to_networkx(data)

    x = data.x

    #utilizziamo la libreria Networkx per forzare i nodi del grafo
    #nello stare nella posizione specificata dalle loro coordinate
    #p[0] coordinata x del punto da disegnare, p[1] coordinata y del punto
    #i mi dice l' indice del punto 
    
    nx.draw(grafo,{i:[p[0],p[1]] for i,p in enumerate(x)},node_size=(25 if filled else 100))

    plt.show()



"""
    creiamo gli strati della GNN

"""


class DNNMPLayer(MessagePassing): #MessagePassing è una classe che gestisce il passaggio di info tra i neuroni del grafo


    def __init__(self, in_channels, out_channels): #in_channels sarà 2 poichè ogni dato è specificato da 2 coordinate (x,y)
        #out_channels è il numero di "output features" che produce la rete 

        #ereditiamo gli attributi dalla classe ereditaria

        super().__init__(aggr = "max") #imponiamo la funzione di aggregazione come il massimo
        #cioè  aggiorniamo i neuroni sulla base del massimo delle features che riceve

        """
        creiamo un multilayer perceptron 
        come una sequenza di layer lineari
        
        
        
        """
        
        #DEFINIAMO UN MULTI-LAYER-PERCEPTRON, ci aiuterà a definire le features degli edges
        # con cui aggiornare i nodi  

        self.mlp = Sequential(

            Linear(2*in_channels, out_channels), #hidden layer della MLP
                              
            ReLU(),                             #funzione di attivazione dei neuroni della hidden layer

            Linear(out_channels, out_channels)  #output layer della MLP

            ) 

        #Sequential impone che le azioni riportate tra parentesi (gialle) siano svolte nell' ordine con cui le scrivo
        
        #Linear è per definire un layer che prende 2*in_channels dati e li porta (li collega) ad un layer successivo di out_channels neuroni
        # per fare questo ha bisogno di definire dei pesi con cui fare i collegamenti e di out_channels bias -> PARAMETRI DA IMPARARE

        #ReLU() mi fa applicare la specifica funzione di attivazione all' hidden layer di out_channels neuroni

        #Linear 2 mi manda l' uscita dell' hidden layer all' output layer anche esso composto da out_channels neuroni


        "Ad ora abbiamo creato una MLP che da in uscita 32 output per costruire un messaggio da passare ai nodi"

        

    def forward(self, h, edge_index): #h matrice delle features di tutti i nodi

        #prendiamo la lista di collegamenti tra nodi: edge_index 
        #se nodo A è collegato a nodo B lui prende le features del nodo A e le features del nodo B e le mette insieme



        accumulated_message = self.propagate(edge_index, h = h )

        #h = h vuol dire che i dati che voglio trasportare sono contenuti nella variabile h

        #le C_out features di ogni nodo vengono comunicate tra i nodi del grafo basandoci su i collegamenti
        #visti in edge_index, per comunicare si intende che il nodo A collegato al nodo B ha ora accesso alle features di B

        #la funzione propagate restituisce UN TENSORE PYTORCH di dimensione (N, C_out)
        #con N numero di nodi del grafo e C_out è il numero di features di ogni nodo 
        
        """
        immaginiamo che il nodo A sia collegato a nodo B, nodo C e nodo D

        ogni nodo ha C_out features, dopo il passaggio di informazioni il nodo A si vede con C_out features per 3 
        poichè collegato a 3 nodi

        di queste 3x32 features lui decide di selezionare il massimo per ogni features (cioè guarda la features 1 del nodo B, 
        del nodo C e del nodo D e salva il valore più alto)
        
        per questo alla fine ho solo 32 features per ogni nodo, che rappresentano il massimo delle features dei nodi a cui è
        collegato ciascun nodo

        """

        return accumulated_message
        

    
    def message(self, h_j, h_i): #funzione chiamata da propagate numerose volte

        input = torch.cat([h_i, h_j-h_i], dim = -1) #cat sta per concatenate e li incolla in orizzontale (h_i, h_j - h_i)
        #poichè è impostato con dim = -1

        return(self.mlp(input)) #il messaggio che dovrò passare e quello prodotto dalla mlp con i dati di input qui definiti
        #ovvero 32 features per ogni nodo 


"""
    Creiamo la nostra GNN utilizzando le DNNMP create precedentemente


"""

class MessagePassingNetwork(torch.nn.Module):


    def __init__(self):

        super().__init__()
        N_features = 20

        torch.manual_seed(12345)

        """
            ogni DNNMPLayer fa comunicare tutti i nodi del grafo in base ai loro collegamenti

            pass1 è il primo step di comunicazione tra nodi: prendo in input 2 features del nodo e le elebaoro in 20
            facendo comunicare ogni nodo con i suoi collegamenti
        
        
        """


        self.pass1 = DNNMPLayer(2, N_features) #creo una istanza dell' oggetto DNNMP layer che ha dentro un MLP
        #che lavora prendendo in input 2 dati e producendone 20

        self.pass2 = DNNMPLayer(N_features, N_features) #faccio comunicare un altra volta i nodi con i suoi collegamenti
        #questa ogni volta ogni nodo ha 20 features perchè risultanti dalla precedente azione di pass1

        self.pass3 = DNNMPLayer(N_features, N_features) #facciamo una ultima comunicazione tra nodi


        self.classifier = Linear(N_features, 1) #produco un unico output perchè devo saper distinguere i cerchi dai rettangoli
        #a questo layer ricordo che dovrò applicare una funzione di attivazione sigmoide o softmax


    def forward(self, data, batch): #data sarà il dataset che devi dare al grafo
        #batch è un vettore di lotti di grafi

        edge_index = data.edge_index  #collegamenti

        x = data.x      #dati

        h = self.pass1(h = x, edge_index = edge_index) #facciamo fare il forward a pass1 
        h = h.relu()

        h = self.pass2(h = h, edge_index = edge_index)
        h = h.relu()

        h = self.pass3(h = h, edge_index = edge_index)
        h = torch.sigmoid(self.classifier(h)) 

        h_global = global_mean_pool(h, batch) #prende tutte le features di tutti i nodi del grafo di tutti i grafi "h" e per ogni grafo
        #ne fa la media, restituendo un vettore di valor medi dei nodi del singolo grafo, dandoci così una valutazione globale
        #di ogni grafo (globale nel senso che si considera una risposta media dei nodi che compongono il grafo)
    

        #h_global è una matrice in cui la riga i descrive tutte le features del nodo 
        #mentre la colonne j è la features j-esima di tutti i nodi dei grafi nel batch

        #global_mean_pool(h,batch) vuol dire prendi tutti i dati h e considera la suddivisione in batch dettata dalla variabile "batch"
        #e "fai media"
       

        return h_global, h
    


"""
    ora creiamo una istanza della nostra GNN, sarà il nostro modello

"""

model = MessagePassingNetwork()
print(model)


"""
    ora facciamo il training ed il test

"""

#prendiamo il dataset di training e dividiamolo in batch di 10 grafi ciascuno

train_loader = DataLoader(dataset_train, batch_size = 10, shuffle = True ) #con dataset_train definito come tensore torch sopra
#shuffle mescola il dataset prima di fare il training
# analizza 10 grafi alla volta, ogni batch ha 10 grafi



test_loader = DataLoader(dataset_test, batch_size = 10)  #organizza il dataset di training in batch di 10 grafi
#da qui test_loader sarà un array di batch, quindi il primo elemento di test_loader contiene il primo batch costituito dai primi 10 grafi


optimizer = torch.optim.Adam(model.parameters(), lr = 0.001) 
lossFunc = torch.nn.BCELoss() #classificazione quindi Binary Cross Entropy


"""
    creiamo la funzione di training con parametri:
    modello, ottimizzatore, vettore dei batch (di training)

"""


def train(model,optimizer, loader):

    model.train() #setto il modello in modalità training

    total_loss = 0 


    #ciclo for sui batch

    for data in loader: #loader è il batch di grafi da analizzare nel training verrà 
        #poi posto uguale a training_loader

        optimizer.zero_grad() #mettiamo il gradiente a zero per calcolare le ottimizzazioni

        out, out_nodes = model(data, data.batch) #chiama il forward del modello MessagePassingNetwork

        #ricordiamo che il forward ritorna (h_global, h)  con h_global l' output globale del grafo mentre out_nodes sono tutti gli output 
        #di tutti i nodi dei grafi contenuti nel batch, senza aver fatto il mean pooling, ricordiamo che h_global = global_mean_pool(h, batch)

        #out: risposta del grafo restituita dal modello
        #out_nodes è la risposta dei nodi del grafo restituita dal modello

        loss = lossFunc(out, data.y) #calcolo loss, data.y sono le etichette 0,1 in base a che siano cerchi o rettangoli

        loss.backward() #facciamo la backpropagation
        optimizer.step() #ottimizziamo i parametri


        total_loss += loss.item() * data.num_graphs #l' errore nel batch è data dallo loss di ogni grafo per il numero di grafi


    return total_loss/ len(loader.dataset) #per ottenere la loss media sul singolo grafo 
    #loader.dataset è la lista di tutti i grafi nel loader




@torch.no_grad()
#non calcoliamo più i gradienti visto che abbiamo finito il training e quindi non aggiorniamo più i parametri




def test(model, loader): #CREIAMO LA FUNZIONE DI TEST

    model.eval() #poniamo il modello in modalità test, una delle cose che fa è disattivare il
    #dropout ad esempio, cosa che invece utilizza quando fa il training 

    total_correct = 0
    total_loss = 0

    for data in loader:

        pred, pred_nodes = model(data, data.batch) #pred è la predizione totale sui 10 grafi del batch
        #ottenuta facendo il mean pooling, mentre il pred_nodes è la predizione su tutti i nodi dei grafi del batch

        loss = lossFunc(pred, data.y)
        total_loss += loss.item() * data.num_graphs

        total_correct += int(((pred > 0.5) ==  data.y ).sum())  #data.y è 0 or 1 e lui lo setta in automatico a True or False
        #per confrontarlo con la vericità della disequazione pred > 0.5 (se la predizione è maggiore di 0.5 lo considera un rettangolo
        #oppure un cerchio)

    return total_correct/len(loader.dataset), total_loss / len(loader.dataset)


test_losses = []
train_losses = []

for epoch in range(1,10):

    loss = train(model, optimizer, train_loader) #ricordiamo che la funzione training restituisce la loss "media" del grafo

    test_acc, test_loss = test(model, test_loader) #ricordiamo che la fuzione test restituisce la loss "media" del grafo e il numero
    #"medio" di previsioni corrette

    test_losses.append(test_loss)
    train_losses.append(loss)


    print(f'Epoch: {epoch:02d}, Train Loss: {loss:.4f}, Test Loss: {test_loss:.4f}, Test Accuracy: {test_acc:.4f}')



plt.figure(figsize=(10,5))
plt.title("Training and Validation Loss")
plt.plot(test_losses,label="val")
plt.plot(train_losses,label="train")
plt.xlabel("iterations")
plt.ylabel("Loss")
plt.legend()
plt.show()







