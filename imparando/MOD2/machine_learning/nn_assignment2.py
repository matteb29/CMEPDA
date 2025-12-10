#RETE NEURALE PER PROBLEMA DI REGRESSIONE

import numpy as np
from keras.layers import Input, Dense
from keras.layers import Flatten, Dropout #nuovi import
from keras.metrics import Accuracy
from keras.models import Model
from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt

#generiamo dei dati per un problema di regressione

np.random.seed(123) #imposto il seme

funzione = lambda x1, x2, x3, x4, x5 : (np.sin(x1*10) + x2 ** x3) * x4 + x5


N = 800
x1 = np.random.rand(N)
x2 = np.random.rand(N)
x3 = np.random.rand(N)
x4 = np.random.rand(N)
x5 = np.random.rand(N)


dati = np.stack((x1,x2,x3,x4,x5), axis = 1)
y = funzione(x1,x2,x3,x4,x5)


#print(f"stampo le prime diegi righe del set di dati {dati[:10, :]}")
#print(f"stampo l' ultimo valore della funzione {y[-1]}")  
# #se avessi messo un semplice dati[10] avrebbe stampato solo il numero 10



print("stampiamo le correlazioni tra le 5 features del set di dati ... ")

for i in range(5):

    for j in range(i+1, 5):

        plt.figure()
        plt.scatter(dati[:,i], dati[:, j], c = y,  cmap = plt.cm.RdBu, edgecolors = "k")
        plt.xlabel(f"features-{i}")
        plt.ylabel(f"features-{j}")





#creiamo i layer della rete

input_layer = Input(shape=(5,))
hidden_layer = Dense(5, activation = "relu")(input_layer)
output_layer = Dense(1, activation = "linear")(hidden_layer) 

"""

Ricordiamo che per un problema di regressione la miglior funzione di attivazione per l' output layer
è la funzione lineare visto che non è limitata all' immagine [0,1] e quindi può assumere tutti i valori della funzione

"""
#uniamo i layer in una rete

rete = Model(inputs = input_layer, outputs = output_layer)


#impostiamo la rete con le sue caratteristiche

rete.compile(loss = "mse", optimizer = "adam", metrics = ["mse"])


rete.summary()

"""
Ricordiamo che per un problema di regressione la miglior loss da utilizzare è la mean squared error

"""

#splittiamo i dati in training e validation

dimensioni_split = int(N/2)

dati_training = dati[:dimensioni_split, :]
y_training = y[:dimensioni_split]

dati_validation = dati[(dimensioni_split): , :]
y_validation = y[(dimensioni_split):]


#alleniamo la rete sui dati di test e sui dati di training
risultati_training = rete.fit(dati_training, y_training, validation_data = (dati_validation, y_validation), epochs = 200, verbose = 0)


#facciamo fare una predizione alla rete sui dati del modello
y_predetto = rete.predict(dati_validation)

print(f"Shape del validation {y_validation.shape}, shape dei valori predetti {y_predetto.shape}")


#calcoliamo i residui dei dati prodotti dalla rete shallow
residui =  y_predetto[:, 0] - y_validation

print(f"shape dei residui {residui.shape}")


"""
for i in range(10):

    print(f"Valore reale, valore predetto, residuo: {y_validation[i]}, {y_predetto[i]}, {residui[i]}")

"""


#creiamo una seconda rete, densa, con più hidden layer

layer_input_dense = Input(shape = (5,))
hidden_layer_dense1 = Dense(5, activation = "relu")(layer_input_dense)
hidden_layer_dense2 = Dense(5, activation = "relu")(hidden_layer_dense1)
hidden_layer_dense3 = Dense(5, activation = "relu")(hidden_layer_dense2)
output_layer_dense = Dense(1, activation = "linear")(hidden_layer_dense3)


rete_densa = Model(inputs = layer_input_dense, outputs = output_layer_dense)

rete_densa.compile(loss = "mse", optimizer = "adam", metrics = ["mse"])

rete_densa.summary()


risultati_rete_densa = rete_densa.fit(dati_training, y_training, validation_data = (dati_validation, y_validation), epochs = 30, verbose = 0)


plt.figure()

plt.plot(risultati_training.history["loss"], label = "Loss Training set")
plt.plot(risultati_training.history["val_loss"], label = "Loss Validation set")
plt.plot(risultati_rete_densa.history["loss"], label = "Training loss rete densa")
plt.plot(risultati_rete_densa.history["val_loss"], label = "Validation loss rete densa")
plt.xlabel("Epoche [u.a]")
plt.ylabel("Loss function [u.a.]")
plt.legend()


#facciamo fare una predizione alla rete densa, sempre sui dati di validation
y_predetto_rete_densa = rete_densa.predict(dati_validation)

#calcoliamo i residui della predizione della rete densa
residui_rete_densa = y_predetto_rete_densa[:, 0] - y_validation


#grafico dei residui delle due reti, quella shallow e quella densa

plt.figure()

plt.hist(residui, 20, label="Residui shallow network", alpha=0.7)
plt.hist(residui_rete_densa, 20, label="Residui deep network", alpha=0.7)

plt.xlabel("Residui [u.a.]")
plt.ylabel("Numero di occorrenze / bin [u.a.]")
plt.title("Istogramma dei residui della rete neurale")


plt.legend() 

plt.show()











plt.show() 












