import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB

sns.set()

iris = sns.load_dataset("iris")
iris_np = np.array(iris)


X_iris = iris_np[:, 0:-1]
y_iris = iris_np[:, -1]

print(X_iris.shape)
print(X_iris[0:10])


# ricordiamo che X_iris è un dataset costituito da 4 features da cui
# ogni dato è rappresentato in uno spazio 4 dimensionale,
# qui noi vorremmo ridurre la dimensionalità con cui rappresentiamo ogni riga di X_iris a questo scopo...


# utilizzo un modello non supervisionato che riduce i dati a sole 2 componenti: modello è un oggetto
# con attributo il numero di dimensioni alla quale voglio ridurre il dataset
model = PCA(n_components=2)


model.fit(X_iris)

# qui abbiamo utilizzato il metodo .fit(X_iris) questo metodo nello specifico:
# 1) prende i dati e calcola la media di ogni caratteristica
# 2) sottrae per ogni dato, ad ogni caratteristica, la sua media calcolata in 1)
# 3) calcola la matrice di covarianza
# 4) diagonalizza la matrice di covarianza trovandone autovettori ed autovalori
# 5) l' autovettore associato all' autovalore più grande sarà il 1° principal ass
# poichè abbiamo deciso che lavoreremo con due componenti allora ci prendiamo anche l' autovettore
# associato al secondo autovalore più grande

# alla fine di model.fit noi abbiamo una matrice di proiezione composta da due colonne che sono gli autovettori
# trovati prima, cioè abbiamo una matrice 4 X 2


X_2d = model.transform(X_iris)

# model.transform trasforma il dataset in uno di dimensione ridotta, proiettando il dataset iniziale
# sulla matrice di proiezione <--> faccio prodotto tra matrice dataset (150 X 4) x (4 X 2) = (150 X 2)


print(X_2d.shape)
print(X_2d[0:10])


iris["PCA1"] = X_2d[
    :, 0
]  # mettere tra le quadre "PCA1" è un modo per chiamare la prima colonna
iris["PCA2"] = X_2d[:, 1]

sns.lmplot(x="PCA1", y="PCA2", hue="species", data=iris, fit_reg="False")
# il comando fit_reg = "False" disattiva il calcolo e la visualizzazione
# della linea di regressione (la linea di tendenza).

plt.show()


# qui segue una prova di algoritmo supervisionato a partire dal dataset trasformato 2d
# la precisione diminuisce

X_2d, X_test, y_iris, y_test = train_test_split(X_2d, y_iris, random_state=1)
model2 = GaussianNB()

model2.fit(X_2d, y_iris)

y_model = model2.predict(X_test)

accuracy = sum(y_model == y_test) / len(y_model)
print(accuracy)
