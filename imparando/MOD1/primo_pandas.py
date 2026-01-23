import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

data = {  # crea un dizionario con due chiavi "x" e "y"
    # la struttura di un dizionario è "chiave": valore
    "x": np.random.rand(100),
    "y": np.random.rand(100),
    "z": np.random.rand(100),
}

df = pd.DataFrame(data)  # crea un DataFrame da un dizionario

print(df)  # stampa il DataFrame
print(df.describe())  # fornisce statistiche descrittive come media, std, min, max, ecc.

plt.figure(figsize=(10, 5))  # crea una figura di dimensioni 10x5 per primo scatter plot
plt.scatter(df["x"], df["y"])  # crea un grafico a dispersione (scatter plot)
plt.xlabel("x")
plt.ylabel("y")
plt.title("Scatter plot di x vs y")

plt.figure(figsize=(10, 5))  # crea una figura di dimensioni 10x5 per l'istogramma
plt.hist(df["z"], bins=10, color="blue", alpha=0.8)

plt.show()
