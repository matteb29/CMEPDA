import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Sequential


# 1. FUNZIONE OBIETTIVO E DATI
# ------------------------------
# Definiamo la funzione che vogliamo imitare (quella nel grafico della slide)
def target_function(x):
    return x**3 + x**2 - x - 1


# Creiamo i nostri dati di addestramento (training)
# Usiamo 100 punti "perfetti" tra -2 e 2
x_train = np.linspace(-2, 2, 100).reshape(-1, 1)  # reshape(-1, 1) serve per Keras
y_train = target_function(x_train)


# 2. COSTRUZIONE DEL MODELLO
# ------------------------------
# Questa è l'architettura 1-5-1 nel diagramma della slide
model = Sequential()

# Strato nascosto: 5 neuroni (i pallini verdi), attivazione ReLU
model.add(Dense(units=5, activation="relu", input_shape=(1,)))

# Strato di output: 1 neurone (il pallino giallo)
# L'attivazione 'linear' (default) va bene perché vogliamo un numero qualsiasi come output
model.add(Dense(units=1))

# 3. COMPILAZIONE E ADDESTRAMENTO
# ------------------------------
# Diciamo al modello come imparare
# 'adam' è un buon ottimizzatore
# 'mean_squared_error' è la nostra misura di "errore"
model.compile(optimizer="adam", loss="mean_squared_error")

# Addestriamo il modello
# epochs=1000 significa che il modello "guarda" i dati 1000 volte
# verbose=0 significa che non stampa nulla durante l'addestramento
print("Inizio Addestramento (può richiedere qualche secondo)...")
model.fit(x_train, y_train, epochs=1000, verbose=0)
print("Addestramento completato.")

# 4. VISUALIZZAZIONE DEI RISULTATI
# ------------------------------
# Usiamo il modello addestrato per "predire" i valori di y
y_pred = model.predict(x_train)

# Plot!
plt.figure(figsize=(10, 6))
# La curva "vera" che volevamo imparare
plt.plot(
    x_train,
    y_train,
    label="Funzione Reale ($x^3 + x^2 - x - 1$)",
    color="blue",
    linewidth=3,
)
# La curva che la nostra rete ha imparato
plt.plot(
    x_train,
    y_pred,
    label="Approssimazione Rete Neurale",
    color="red",
    linestyle="--",
    linewidth=2,
)
plt.title("Approssimazione di Funzione con Rete Neurale")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.grid(True)
plt.show()
