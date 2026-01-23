# scrivere 100000 numeri casuali con distribuzione gaussiana
# stamparne statistiche e modificare minimo e massimo della distribuzione

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

x = np.random.normal(0, 100, 100000)  # li genera gaussiani con media 0 e dev std 100
x = pd.Series(x)  # pandas converte questa lista di numeri in una serie pandas

g = np.random.default_rng()  # genera numeri casuali
y = g.normal(0, 100, 100000)  # genera numeri casuali con distribuzione gaussiana

y = pd.Series(y)  # converte y in una serie pandas
# le serie pandas sono simili agli array numpy ma hanno più funzionalità
# ad esempio posso fare y.describe() che mi dà tutte le statistiche del campione


print(y.describe())  # qui y.describe() mi dice tutte le statistiche del campione

print(y.median())  # mediana del campione y

print(x.describe())
print(x.median())  # mediana del campione x


x_min = x.min()
x_max = x.max()

statistiche = x.describe()  # vedo le statistiche come una serie pandas


statistiche.loc["min"] = (
    x_max * 5
)  # loc seleziona l'elemento con nome min e lo modifica
# è meglio usare il metodo loc per selezionare gli elementi di una serie pandas
# perchè se usassi x[3] potrei avere problemi se l'indice della serie non è numerico


print(f"statistiche truccate con minimo sbagliato: {statistiche}")

x[x == x_min] = (
    x_max * 5
)  # seleziona solo gli elementi di x che corrispondono al minimo
print(f"Statistiche aggiornate con nuovo massimo {x.describe()}")
