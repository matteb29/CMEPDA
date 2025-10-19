

import seaborn as sns #importiamo la libreria per il scaricare il dataset degli iris

iris = sns.load_dataset("iris")
print(iris)


import numpy as np

iris_np = np.array(iris)
print(iris_np)

print(iris_np.shape)  
#L'attributo .shape è una "etichetta" attaccata all'array che ne descrive la forma.
#Restituisce una tupla (una lista immutabile) di numeri, dove: Il primo numero è il numero di righe.
# Il secondo numero è il numero di colonne.