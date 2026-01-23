""""

Ho avuto problemi di segmentation fault con il programma 
utilizzando pytorch e matplotlib quindi imposto questa serie di comandi addizionali
per fargli fare un thread alla volta

"""

import os

os.environ["OMP_NUM_THREADS"] = "1"

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"


"""
Creiamo una dnn per un problema di classificazione 
utilizzando pytorch piuttosto che keras 

"""


import time

import matplotlib.pyplot as plt
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from matplotlib.colors import ListedColormap

np.random.seed(123)


"""
lambda è un modo semplice per creare funzioni senza usare il def
altrimenti sarebbe stato il classico:

def funzione_classica(x1, x2):
    return np.sin(x1 * 20) > x2 * x2 - x1

"""


funzione = lambda x1, x2: np.sin(x1 * 20) > x2 * x2 - x1

N = 300

# creo 3000 numeri casuali tra 0 e 1
x1 = np.random.rand(N)
x2 = np.random.rand(N)


y = funzione(x1, x2)


matrice_x = np.stack((x1, x2), axis=1)


immagine = ListedColormap(["#FF0000", "#0000FF"])


plt.scatter(matrice_x[:, 0], matrice_x[:, 1], c=y, cmap=immagine, edgecolors="k")


xx1, xx2 = np.meshgrid(np.arange(0, 1, 0.01), np.arange(0, 1, 0.01))


print(x1[:10])


plt.contourf(
    xx1, xx2, (funzione(xx1, xx2)).reshape(xx1.shape), cmap=plt.cm.RdBu, alpha=0.8
)

plt.show()


"""
i dati array numpy in pytorch vanno caricati come tensori 
e rispettare le dimensioni, ad esempio le previsioni saranno tensori (N,1)
pertanto le label dei dati dovranno anch' esse essere tensori (N,1)

"""

X = torch.tensor(matrice_x, dtype=torch.float32).to("cpu")

# reshape(-1,+1) serve per far diventare le y un vettore colonna
# +1 forza che ci sia una sola colonna, -1 fa si che calcoli in automatico quante righe servono per far
# stare tutti i dati su una colonna

Y = torch.tensor(y, dtype=torch.float32).reshape(-1, +1).to("cpu")


print(X.shape)  # 300 righe, 2 colonne
print(Y.shape)  # 300 righe, 1 colonna


print(X[:, :3])
print(Y[:, :3])


"""

Ora definiamo la rete neurale,
ricordiamo che in pytorch le reti sono scritte come istanze della
classe torch.Module.nn da cui ereditano

"""


class rete_neurale_prova(nn.Module):

    def __init__(self):

        super().__init__()  # facciamogli ereditare dalla classe Module.nn

        self.layer1 = nn.Linear(
            2, 50
        )  # 2 perchè ho 2 dati in ingresso, 50 è il numero di output corrispondente al numero di neuroni
        # nel layer 1 ogni neurone ha 2 pesi, uno per x1 e uno per x2

        # la MATRICE DEI PESI sarà una matrice 50x2 quindi ho 100 parametri, ai quali devo aggiungere anche un parametro
        # per ogni neurone per il suo bias

        self.layer2 = nn.Linear(50, 50)
        self.layer3 = nn.Linear(50, 50)

        self.layer_output = nn.Linear(50, 1)

    def forward(self, x):

        hidden = self.layer1(x)
        hidden = hidden.relu()

        hidden = self.layer2(hidden)
        hidden = hidden.relu()  # metodo 1 sintatticamente equivalente a metodo 2

        hidden = self.layer3(hidden)
        hidden = torch.relu(hidden)  # metodo 2

        hidden = self.layer_output(hidden)
        hidden = torch.sigmoid(hidden)

        return hidden


# faccio una istanza della mia classe ereditaria chiamata rete_neurale_prova
model = rete_neurale_prova().to("cpu")
print(model)

# stampiamo i parametri del modello
# il primo layer ha 50x2 tensor di pesi
# il secondo ha un tensore 50x50 etc
# print([x for x in model.parameters()])


print("I parametri della rete: ")
for name, param in model.named_parameters():
    print(f"Nome: {name} | Forma: {param.shape} | numero parametri: {param.numel()}")


loss_function = nn.BCELoss()
ottimizzatore = optim.Adam(model.parameters(), lr=0.002)

numero_epoche = 100
batch_size = 30

loss_history = []


# il training si fa con dei cicli for concatenati


for epoch in range(numero_epoche):  # ciclo for per le epoche

    start_time = time.time()

    for i in range(
        0, len(X), batch_size
    ):  # ciclo for per ogni epoca per ottimizzare i parametri

        # dividiamo manualmente i dati X (in formato torch) in batch di grandezza batch_size
        lotto_dati = X[i : i + batch_size]

        # facciamo predizione sul batch di dati
        y_prediction_lotto_dati = model(lotto_dati)

        # dividiamo manualmente le etichette Y (in formato torch) in batch di grandezza batch_size
        y_batch = Y[i : i + batch_size]

        # calcoliamo la loss function sul nostra batch
        loss_batch = loss_function(y_prediction_lotto_dati, y_batch)

        # impostiamo a zero i gradienti, da calcolare con la backpropagation
        ottimizzatore.zero_grad()

        loss_batch.backward()

        ottimizzatore.step()

    print(
        f"finita epoca numero: {epoch}, ultimo valore loss {loss_batch}, tempo di esecuzione: {time.time() - start_time} sec"
    )

    loss_history.append(loss_batch.detach().numpy())
    # loss_batch è un tensore pytorch che voglio trasformare in un tensore numpy necessario per poi plottare la loss_history con pyplot
    # in alternativa uso loss_history.append(loss_batch.item())

    # SE USASSI LA GPU loss_history.append(loss_batch.cpu().detach().numpy())


plt.figure()


# plottiamo la loss
plt.plot(loss_history)
plt.show()


"""

Facciamo ora il test sul nostro modello
una volta completato il training


"""


set_test = np.stack((xx1.flatten(), xx2.flatten()), axis=-1)


# essenziale per la fase di test non utilizzare i gradienti visto che non voglio più aggiornare i pesi
torch.no_grad()

predizioni_test = model(torch.tensor(set_test, dtype=torch.float32).to("cpu"))
predizioni_test = predizioni_test.detach().numpy()

plt.scatter(matrice_x[:, 0], matrice_x[:, 1], c=y, cmap=immagine, edgecolors="k")

# disegno i punti xx1 e xx2 con colore dipendente dalle predizioni fatte dal modello
plt.contourf(xx1, xx2, predizioni_test.reshape(xx1.shape), cmap=plt.cm.RdBu, alpha=0.8)

plt.show()
