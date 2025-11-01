#RETE NEURALE PER UN PROBLEMA DI CLASSIFICAZIONE


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

#questo se voglio disegnare i dati
"""
plt.figure()
plt.scatter(matrix[:, 0], matrix[:, 1], c = y , cmap = cm_bright, edgecolors = "k")

plt.contourf(xx1, xx2, (theFunction(xx1, xx2)).reshape(xx1.shape), cmap = plt.cm.RdBu, alpha = .8)

"""

"""con plt.contourf coloro i pixel del grafico, in particolare applico la funzione a tutti i punti di xxx1
e a tutti i punti di xx2 così da colorare tutto il piano cartesiano in base alla funzione, FORSE è un check per vedere 
se l' assegnazione fatta sui punti casuali è corretta o meno"""

#INPUT
layer_input = Input(shape = (2,)) #numero di neuroni iniziali è uguale al numero di feature: quindi il numero di colonne

# 4 HIDDEN
hidden_layer1 = Dense(50, activation = "relu")(layer_input)
hidden_layer2 = Dense(50, activation = "relu")(hidden_layer1)
hidden_layer3 = Dense(50, activation = "relu")(hidden_layer2)
hidden_layer4 = Dense(50, activation = "relu")(hidden_layer3)

layer_output = Dense(1, activation = "sigmoid")(hidden_layer4)


#il comando model mette insieme i vari strati e restituisce una rete neurale da allenare
rete = Model(inputs = layer_input, outputs = layer_output )

#per farmi stampare le caratteristiche della rete
rete.summary()

#per dire come voglio impostare le caratteristiche della rete, adam per backpropagation
rete.compile(loss = "binary_crossentropy", optimizer = "adam", metrics = ["accuracy"])


risultati_prima_training = rete.evaluate(matrix, y, verbose = 0)

print(f"Risultati prima del traininng di Loss e accuracy: {risultati_prima_training}")




risultati_training = rete.fit(matrix, y, validation_split = 0.5, epochs = 500, verbose = 0)


#vediamo come cambia la rete dopo il training
rete.summary()

"""verbose = 0 per non stampare una righa ad ogni epoca
matrix sono i dati di input mentre y sono le etichette che la rete dovrà indovinare
i dati di input e le etichette venogno splitatti in 2 set per fare la fase di training e quella di validation
in particolare validation_split mi dice la percentuale di dati da usare per il validation.
L' intero processo di fit chiamato con rete.fit restituisce l' oggetto che io chiamo history
che posso pensare come un record dell' addestramento, contenente info sui valori di loss function e su altre metriche

"""



print(f" Chiavi del dizionario restituito da rete.fit: {risultati_training.history.keys()}")

"""
l' oggetto history che ci facciamo restituire da rete.fit contiene un dizionario chiamato anch' esso history, 
usando il metodo -keys()- mi faccio stampare le chiavi del dizionario che saranno le metriche di cui tengo traccia durante il training
del tipo: loss, val_loss che sono rispettivamente la loss sul set di trainign e la loss sul set di validation

"""


#print(risultati.history["loss"])

#con questa riga mi faccio stampare i valori della loss sul set di validation
#print(risultati.history["val_loss"])


print("Plotting training vs validation...")


#creo una nuova figura
plt.figure()

#faccio il plot dei valori della loss sul training set, plt.plt riceve questa lista di valori 
#e sull' asse x ci mette gli indici della lista
plt.plot(risultati_training.history["loss"], label = "Training loss" )

#faccio il plot dei valori della loss sul validation set
plt.plot(risultati_training.history["val_loss"], label = "Validation loss")


plt.xlabel("Epoche")
plt.ylabel("Loss")

plt.legend()




risultati_validation = rete.evaluate(matrix, y, verbose=0)
#risultati validation è un array di due elementi: il primo è il valore della loss raggiunto, il secondo è la precisione raggiunta

print(f" Valore della loss sul set di validation: {risultati_validation[0]}")
print(f"Valore della accuracy sul set di validation: {risultati_validation[1]}")


#proviamo il modello sui punti xx1 e xxx2 usando come set di test,
#ricordiamo che si possono dividere i set in: training, validation, test

testSet = np.stack((xx1.flatten(), xx2.flatten()), axis = 1 ) #axis = 1 li impila come colonne, axis = 0 li avrebbe impilati come colonne
#metodo flatten serve per far diventare la matrice un array

label_test = theFunction(testSet[:,0], testSet[:,1])


predizioni = rete.predict(testSet)

"""
    Ricordiamo che il metodo evaluate serve per farsi restituire le prestazioni del modello su un set
    di dati a seguito della fase di training, ma su cui conosco le etichette.
    Il metodo .predict() invece mi serve per quando non conosco le etichette


"""

print(f"Risultato della predizione della rete sul primo dato del test set: {predizioni[0]}" ) #questo contiene delle probabilità perciò facciamo np.round, 

"""

il motivo è che l' ultimo layer ha come activation function una sigmoide e quindi il numero che
restituisce è compreso tra 0 e 1: interpretato come la fiducia del modello che il dato appartenga alla classe 1: TRUE
con cui 0.001 è quasi sicuro che il dato appartenza alla classe 0: FALSE

"""


accuracy_test = np.mean(np.round(predizioni) == label_test)
print(f"Accuracy sul set di test {accuracy_test}")


plt.figure()

plt.scatter(matrix[:, 0], matrix[:, 1], c = y , cmap = cm_bright, edgecolors = "k")
plt.contourf(xx1, xx2, predizioni.reshape(xx1.shape), cmap = plt.cm.RdBu, alpha = .8)

plt.show()








