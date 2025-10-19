
#ci si riferisce alle righe della matrice di dati come "samples" mentre 
# al numero di righe come n_samples, ogni colonna della matrice descrive una feature del singolo dato
#la matrice contenente tutte queste informazioni la chiameremo feature matrix

#le feature(quindi le colonne) si riferiscono a osservabili distinti che descrivono ogni campione
#(cioè ogni riga) in maniera quantitativa


import seaborn as sns #importiamo la libreria per il scaricare il dataset degli iris
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split #per splittare il dataset in training e valutazione
from sklearn.naive_bayes import GaussianNB #per importare lo stimatore
from sklearn.metrics import accuracy_score #per quantizzare precisione del modello


iris = sns.load_dataset("iris")
#print(iris)

iris_np = np.array(iris)
#dopo averlo printato come dataset preso da seaborn, lo prindiamo
#come array numpy
#print(iris_np)

print(iris_np.shape)  
#L'attributo .shape è una "etichetta" attaccata all'array che ne descrive la forma.
#Restituisce una tupla (una lista immutabile) di numeri, dove: Il primo numero è il numero di righe.
# Il secondo numero è il numero di colonne.


sns.set()
#applica lo stile e il tema di default di Seaborn a tutti i grafici futuri che creo.


sns.pairplot(iris, hue='species', height=1.5)
#Crea un'intera griglia di grafici che mostra la relazione tra ogni coppia di colonne numeriche nel tuo dataset. 

# Gli argomenti sono:
#iris -> È il DataFrame Pandas da usare. È fondamentale che sia un DataFrame e non l'array NumPy (iris_np)
#perché Seaborn ha bisogno dei nomi delle colonne (es. sepal_length, petal_width) per creare le etichette degli assi.
#hue -> Disegna tutti i punti, ma colorali in modo diverso in base alla loro colonna species

plt.show()


#X_iris = iris.drop('species', axis=1)

#print(iris_np[:10]) #first 10 lines

X_iris=iris_np[:,0:-1] #-1 indica l' ultimo elemento escluso,
# : -> prendi tutte le righe
# , -> introduce le colonne
# 0 -> start
# -1 -> stop (escluso)

print(X_iris.shape)

#print(X_iris[:10]) #first 10 lines


#questo sarà il vettore target: cioè l' ultima colonna del dataframe iris,
#ovvero la specie dei fiori
y_iris = iris_np[:, -1]

#print(y_iris.shape)
#print(y_iris)

#print(y_iris[:10]) se volessi stampare le prime 10 



#Adesso cerchiamo di prevedere la specie dei fiori usando Estimator di Scikit learn
#si indica con Scikit learn API le regole e i comandi che Estimator segue:
#most commonly, the steps in using the Scikit-Learn estimator API are as follows (we will step through 
# a handful of detailed examples in the sections that follow).
#1)Choose a class of model by importing the appropriate estimator class from Scikit-Learn.
#2)Choose model hyperparameters by instantiating this class with desired values.
#3)Arrange data into a features matrix and target vector following the discussion above.
#4)Fit the model to your data by calling the fit() method of the model instance.
#5)Apply the Model to new data:
#   For supervised learning, often we predict labels for unknown data using the predict() method
#   For unsupervised learning, we often transform or infer properties of the data using the transform() or predict() method.



#utilizziamo la funzione train_spleet importatata da sklearn.model_selection
#per dividere i dati in parte di training e parte di test

X_train, X_test, y_train, y_test = train_test_split(X_iris, y_iris, random_state = 1)


#train_test_split nello specifico cosa fa?
#prende i dati (X_iris, cioè le misurazioni dei fiori) e le  etichette (y_iris, cioè le specie di fiori).
#li mescola in modo casuale (shuffle).
#li divide in due gruppi. Di default, il 75% dei dati va nel set di addestramento e il 25% nel set di test.

#random_state = 1: Questo è un parametro cruciale per la riproducibilità. In realtà la suddivisione del set di dati
#è pseudocasuale e  = 1 indica il seme da cui partire pertanto questa inizializzazione del parametro
#assicura che ogni volta che lancio il codice i dati siano suddivisi nel solito modo
#  tra parte di training e parte di test: possiamo vedere random_state = 1 come generatore pseudocasuale



model = GaussianNB() #creo una istanza dell' oggetto GaussianNB: uno stimatore

model.fit(X_train, y_train) #chiamo il metodo .fit() dell' oggetto model
#per allenare il mio modello, .fit(features, etichette)
#model.fit fa un fit per ogni feature di ogni specie utilizzando una funzione gaussiana per ogni fit. Restituisce per
#ogni specie la media e la deviazione standard di ogni feature della specie: sa disegnare la pdf gaussiana di ogni caratteristica 
#per ogni specie: può lavorare con 12 gaussiane diverse
#alla fine di questo processo ha info su tutte e 3 le specie, può iniziare a fare classificazione


y_model = model.predict(X_test)  #definisco le y predette dal modello chiamando
#il metodo .predict dell' oggetto model, le y che dovrà predire saranno quelle associate
#ai dati X_test    .predict(features delle etichette da predire)
#per ogni feature del dato di test lui confronta il valore della feature con la gaussiana corrispondente, assegnando
#un punteggio sulla base di quanto sia probabile che il dato appartenga a quella gaussiana: il valore della pdf in quel punto



print(np.stack((y_model, y_test), axis = 1))  #qui creo una tabella di confronto tra le etichette di test
#e le etichette predette dal mio modello, axis = 1 dice prendi i due array y_model e y_test e mettili uno affianco all' altro
#se avessi messo axis = 0 li avrebe messi uno sotto l' altro (axis = 0 oppure 1)


print(y_model != y_test) #questo stampa un array di False, True. False se il modello ha azzeccato e quindi
#non è vero che y_model è diverso da y_test; True se il modello ha sbagliato cioè se è vero che y_test è diverso da y_model

print(sum(y_model == y_test)/len(y_model)) #così stampo quantre volte il modello ha azzeccato 
#sum(y_model == ytest) conta il numero totale di True, che corrisponde al numero totale di previsioni corrette.


#accuracy_score serve per capire quanto è stato accurato il modello
print(accuracy_score(y_test, y_model))