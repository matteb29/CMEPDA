import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from keras.layers import Dense, Input
from keras.models import Model
from math import *



np.random.seed(1234)

"""uso lambda per dichiarare una funzione matematica dove la sintassi è strutturata 
#come segue lambda parametri funzione: funzione"""

theFunction = lambda x1, x2 : np.sin(x1*20) > x2 * x2 - x1

N = 3000

#creo due array di 3000 valori 

x1 = np.random.rand(N)
x2 = np.random.rand(N)

"""y è una funzione di due array, cioè restituisce un array dove l' elemento 1 è la funzione
#applicata all' elemento 1 di x1 e all' elemento 1 di x2"""

y = theFunction(x1, x2)

print(x1[:10])
print(x2[:10])

#metodo di numpy per unire due set di dati in due colonne 
matrix = np.column_stack((x1,x2))

print(matrix[:10])
print(y[:10])
print(matrix.shape)
print(y.shape)


"""FF0000: È il codice esadecimale per il Rosso
#ho solo due colori visto che la y ha solo 2 possibili valori: True, False"""

cm_bright = ListedColormap(["#FF0000", "#0000FF"])

"""creo due matrici xx1, xx2, generando due vettori di numeri da 0 a 1 a passi di 0.01 e quindi 100 numeri in totale
facendo il prodotto esterno tra due vettori crea la prima matrice, la seconda matrice è la trasposta della prima"""

xx1, xx2 = np.meshgrid(np.arange(0, 1, 0.01 ), np.arange(0, 1, 0.01))






"""faccio il plot di tutta la colonna 1 matrix[:,0] e tutta la colonna 2 
c = y è per colorare in base al valore corrispondente nell' array y
"k" è il bordo nero dei punti"""

plt.figure()
plt.scatter(matrix[:, 0], matrix[:, 1], c = y , cmap = cm_bright, edgecolors = "k")

plt.contourf(xx1, xx2, (theFunction(xx1, xx2)).reshape(xx1.shape), cmap = plt.cm.RdBu, alpha = .8)

"""con plt.contourf coloro i pixel del grafico, in particolare applico la funzione a tutti i punti di xxx1
e a tutti i punti di xx2 così da colorare tutto il piano cartesiano in base alla funzione, FORSE è un check per vedere 
se l' assegnazione fatta sui punti casuali è corretta o meno"""





layer_input = Input(shape = (2,)) #numero di neuroni iniziali è uguale al numero di feature: quindi il numero di colonne
hidden_layer = Dense(10, activation = "relu")(layer_input)
layer_output = Dense(1, activation = "sigmoid")(hidden_layer)

rete = Model(inputs = layer_input, outputs = layer_output )

#per farmi stampare le caratteristiche della rete
rete.summary()

rete.compile(loss = "binary_crossentropy", optimizer = "adam", metrics = ["accuracy"])

accuracy = rete.evaluate(matrix, y, verbose=0)
#accuracy è un array di due elementi, il valore della loss raggiunto, il secondo è la precisione raggiunta

print(f"Precisione:{accuracy}")

history = rete.fit(matrix, y, validation_split = 0.5, epochs = 200, verbose = 0)

"""verbose = 0 per non stampare una righa ad ogni epoca
matrix sono i dati di input mentre y sono le etichette che la rete dovrà indovinare
i dati di input e le etichette venogno splitatti in 2 set per fare la fase di training e quella di validation

"""



print(history.history.keys())
print(history.history["loss"])


print("Plotting training vs validation...")
plt.figure()
plt.plot(history.history["loss"], label = "Training loss" )
plt.plot(history.history["val_loss"], label = "Validation loss")

plt.xlabel("Epoche")
plt.ylabel("Loss")

plt.legend()

plt.show()













