import numpy as np
import pandas as pd
from keras.layers import Dense
from keras.models import Sequential

# URL AGGIORNATO: Questo link è stabile e funzionante
url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.csv"

"""
pima indians diabetes è un dataset famoso che contiene informazioni su donne sopra i 21 anni
#di origine pima (nativi americani) allo scopo di prevedere insorgenza di diabete (classe A) o
#meno (classe B) tramite un problema di classificazione

"""


# Definiamo i nomi delle colonne perché anche questo file non ha un'intestazione
# l' ultima colonna "class" sarà la mia etichetta su cui alleno il modello

column_names = ["preg", "plas", "pres", "skin", "test", "mass", "pedi", "age", "class"]

"""
il dataset contiene info circa:
preg = n volte rimasta in cinta
plas = concentrazione di glucosio nel sangue 
pres = pressione sanguigna
skin = spessore della plica cutanea del tricipite
test = insulina sierica
mass = indice di massa corporea
pedi =  funzione che stima probabilità insorgenza diabete sulla storia famigliare
age = età

"""


# Carichiamo il dataset direttamente dall'URL usando pandas
dataset_pd = pd.read_csv(url, names=column_names)

# Convertiamo il DataFrame di pandas in un array NumPy
dataset = dataset_pd.values

print(dataset.shape)

# Separa input (X) e output (y)
X = dataset[:, 0:8]
y = dataset[:, 8]


# Definisci il modello model che è un' istanza della classe sequential che è una rete neurale
model = Sequential()


"""
utilizziamo il metodo .add della classe sequential per aggiungere layer di input
 12 = numero di neuroni del primo strato
 8 = numero di features del dato di input
 "relu" è la funzione di attivazione per tutti i neuroni di questo layer
 "dense" indica che i neuroni del layer i  sono tutti attaccati ai neuroni del layer i-1 
 direzione in avanti

"""
model.add(Dense(12, input_dim=8, activation="relu"))


"""
secondo strato: hidden layer, che prende come input i 12 valori di output dell' input layer
e, tramite una funzione di attivazione di tipo relu, restituisce 8 valori di output: uno per ogni neurone 
infatti 8 indica che in questo hidden layer ci sono 8 neuroni

"""

model.add(Dense(8, activation="relu"))


"""
terzo strato: output layer che prende in input gli 8 output degli 8 neuroni dell' hidden layer e lo trasforma in un 
unico valore di output, infatti 1 indica che l' output layer è composto da un unico neurone

"""
model.add(Dense(1, activation="sigmoid"))


# Compila il modello
model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])


"""

utiliziamo come objective funcion la binary cross entropy
durante l' apprendimento i pesi della rete vengono aggiustati dall' algoritmo di ottimizzazione adam:
Adaptive moment estimation

All' inizio ho 12 x 8 = 96 pesi iniziali random, uno per ogni connessione.
dopo la prima previsione vi è un confronto con l' output atteso, a questo punto entra in gioco adam 
che applica la backpropagation 

Un semplice SGD farebbe lo studio
di come l' output varia in funzione di uno dei 96 pesi iniziali, lo farebbe
per ogni peso calcolando un gradiente = vettore di 108 componenti contenente le derivata della loss rispetto ai pars e 
12 aggiuntive fatte rispetto ai bias, ho un bias per ogni neurone dello strato secondario 


Derivata della loss function rispetto a un peso:
se positiva vuol dire che se aumento il peso allora L aumenta ---> il peso va diminuito per minimizzare L
se negativa vuol dire che se aumento il peso allora L diminuisce ---> il peso va aumentato per minimizzare L



ADAM ha bisogno di qualcosa in più: La backpropagation calcola il gradiente per tutti i parametri (pesi e bias) in tutta la rete.
In totale: 
Primo Strato = 96 pesi e 12  bias (uno per ogni neurone) Totale: 108 gradienti calcolati
Secondo Strato = 96 pesi e 8 bias Totale: 104 gradienti calcolati
Terzo Strato = 8 pesi e 1 bias  Totale: 9 gradienti calcolati
Adam riceve questa lista di 221 derivate e le usa per aggiornare ognuno dei 221 parametri.


Per ognuno dei tuoi 221 parametri, Adam tiene traccia di due numeri:
m (Il Momento)
v (La Varianza)
all' inizio questi 2 x 221 numeri sono tutti impostati a 0 
verranno poi aggiornati ad ogni produzione di output

vale che questi m, v vengono aggiornati secondo la formula di media mobile esponenziale del gradiente
(sta forse facendo il metodo dei momenti per stimare il gradiente medio)

m_{nuovo} = beta_1 x m_{vecchio}) + ( (1 - beta) x {gradiente}_{attuale} )

con beta_1 = 0.9 fattore di attrito, m_{nuovo} rappresenta la direzione più probabile e
stabile in cui andare, basata sulla storia recente
per gradiente_attuale intende la derivata della loss rispetto al parametro che voglio aggiornare
inoltre il momento aiuta a non stagnarmi in minimi locali poichè
 anche se gradiente è piccolo (perchè sono in una valle) ho aggiornamento che tiene conto del vecchio gradiente


tenere la storia del momento e della varianza è utile per ovviare ai casi in cui ho un set di dati che se
sfortunato mi dà valori eccessivamente grandi o piccoli (set anomalo)

la formula è la media mobile esponenziale dei gradienti al quadrato:
(sta forse facendo il metodo dei momenti per stimare la varianza del gradiente usando il secondo momento)

v_{nuovo} = (beta_2 x v_{vecchio}) + ( (1 - beta_2) x {gradiente}_{attuale}^2 )

con beta_2 = 0.999 da cui poichè vi è il quadrato favorismo le grandi deviazioni del gradiente
v_{nuovo} è una stima di quanto possiamo fidarci di quel gradiente, se v è alto il gradiente calcolato non è affidabile
quindi è stato calcolato su un set di dati anomalo, ovvero gli aggiornamenti per quel peso sono cambiati molto
nel corso del training e quindi ne limito l' effetto.


Senza ( (1 - beta_2) x {gradiente}_{attuale}^2 )  ma con un semplice {gradiente}_{attuale}^2 se io trovassi un 
set anomalo che produce un grosso gradiente allora v_nuovo sarebbe aggiornato ad un valore grande e tutti i v successivi 
sarebbero anche essi grandi, ma abbiamo visto che un v grande diminuisce l' aggiornamento...quindi per tutta
la storia del training sarei bloccato nell' aggiornamento dei pesi



Per ognuno di questi 221 parametri adam calcola un aggiornamento:


{Aggiornamento} = ( {alpha} / { sqrt{v_{nuovo}} + epsilon} )  x  m_{nuovo}

che individua di quanto spostarsi nella direzione data dal gradiente, cioè di quanto lungo
deve essere il passo dell' aggiornamento, con alpha learning rate, epsilon numero piccolo per evitare divisioni per 0 


parametro_nuovo = parametro_vecchio - aggiornamento 

dove utilizziamo il segno meno perchè mi sposto nella direzione opposta a quella in cui il
la derivata della loss aumenta, visto che io la voglio minimizzare coerentemente con il fatto che se la derivata è:

se positiva vuol dire che se aumento il peso allora L aumenta ---> il peso va diminuito per minimizzare L
se negativa vuol dire che se aumento il peso allora L diminuisce ---> il peso va aumentato per minimizzare L



"""


# Addestra il modello
print("Inizio addestramento...")


model.fit(X, y, epochs=150, batch_size=10, verbose=0)

"""
batch_size = 10 significa che la backpropagation viene fatta ogni 10 dati usando adam
poichè ho 10 epoche ripeterò l' addestramento sui 768 dati del database per 150 volte

"""


print("Addestramento completato.")

# Valuta il modello
accuracy = model.evaluate(X, y, verbose=0)  # Aggiunto verbose=0 per pulizia

# Stampa l'accuracy
print("Accuracy: %.2f%%" % (accuracy * 100))
