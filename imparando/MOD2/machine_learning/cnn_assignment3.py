"Vogliamo realizzare una CNN in grado di riconoscere cerchi e rettangoli"

import cv2
import numpy as np
from keras.layers import (
    Conv2D,  # importo i layers necessari per la CNN
    Dense,
    Flatten,
    Input,
    MaxPooling2D,
    ZeroPadding2D,
)
from keras.models import Model
from matplotlib import pyplot as plt

"Gneriamo delle immagini con figure utilizzando la libreria OpenCV"


nsamples = 500
simple = True
mixed = False
withBB = False
conv = True


def background():
    return np.zeros(
        (64, 64, 3), np.uint8
    )  # creo una immagine nera 64X64 poichè riempita di zeri


def randomColor():
    return (
        int(np.random.rand() * 128 + 128),
        int(np.random.rand() * 128 + 128),
        int(np.random.rand() * 128 + 128),
    )


"Generiamo cerchi"


def drawCircle(c, x, y, r):

    img = background()  # prendiamo la matrice di 0 di dim 64x64 e la chiamiamo img

    cv2.circle(
        img, (x, y), r, c, -1
    )  # al centro di tale matrice di coordinate x, y disegno un cerchio di raggio r
    # di colore c e riempito (-1), nella pratica i valori degli elementi di matrice che definiscono il cerchio
    # cambiano da 0 a c

    return (
        img,
        x - r,
        y - r,
        x + r,
        y + r,
    )  # oltre all' immagine ci facciamo restituire le 4 coordinate della bounding box
    # nota che l' immagine è la matrice 64x64 con entries modificate


# funzione per generare i cerchi
def genCircle():

    return drawCircle(
        randomColor(),
        int(np.random.rand() * 50) + 10,
        int(np.random.rand() * 50) + 10,
        int(np.random.rand() * 6) + 3,
    )


"Generiamo i rettangoli"


def drawRectangle(c, x, y, w, h):
    img = background()
    cv2.rectangle(img, (x, y), (x + w, y + h), c, -1)
    return (
        img,
        x,
        y,
        x + w,
        y + h,
    )  # mi faccio sempre restituire le coordinate di due estremi opposti di un rettangolo: bounding box


def genRectangle():
    return drawRectangle(
        randomColor(),
        int(np.random.rand() * 40) + 10,
        int(np.random.rand() * 40) + 10,
        int(np.random.rand() * 6) + 3,
        int(np.random.rand() * 6) + 3,
    )


"Creiamo una funzione per gestire più figure"


# f sarà la funzione che genera la figura, i è il numero di figure all' interno dell' immagine
def genN(f, i):

    img_bkg = np.zeros(
        (64, 64, 3), np.uint8
    )  # uint 8 significa numero a 8 bit che equivale ad un numero da 0 a 255

    for x in range(i):

        img_bkg += f()[0]  # riconduco la creiazione di nuove figure in una immagine
        # alla somma di specifici numeri nella matrice di bkg in base alla componente 0 di f
        # notiamo che f è una funzione drawRectangle che restituisce 4 oggetti di cui la componente 0 è l'
        # immagine con il rettangolo

    return img_bkg


"Se simple è true facciamo immagini con un solo tipo di figura"
if simple:

    targets = (
        np.random.rand(nsamples) > 0.5
    )  # ho un arrey di 100 numeri casuali tra 0 e 1 che viene confrontato con 0. 5
    # ottengo alla fine un array di lunghezza 100 contenente True or False

    # ciclo for rapido in cui genero 100 immagini in base alla entry target[x] sia True or False
    images = np.array(
        [genCircle()[0] if targets[x] else genRectangle()[0] for x in range(nsamples)]
    )

"Se mixed è true facciamo immagini sia con rettangoli che con cerchi nella solita figura"
if mixed:

    # creo una matrice 100 x 2 fatta di numeri casuali tra 0 e 4
    # ogni riga sarà il numero di cerchi e il numero di rettangoli da disegnare
    targets = np.stack(
        (np.random.rand(nsamples) * 4, np.random.rand(nsamples) * 4), axis=1
    )

    # trasforma l' array targets in un array di interi mentre prima il numero di cerchi e rettangoli era un decimale
    targets = np.array(targets, dtype=int)

    # immagine con cerchi e rettangoli intesa come somma tra le matrici che contengono i pixel colorati
    images = np.array(
        [
            genN(genRectangle, targets[x, 0]) + genN(genCircle, targets[x, 1])
            for x in range(nsamples)
        ]
    )


"Se withBB è true facciamo figure con un rettangolo o un cerchio ma disegnamo anche la bounded box"
if withBB:

    targets = np.random.rand(nsamples) > 0.5

    # ricordiamo che le funzioni genCircle e genRectangle restituiscono tuple 5 dimensionali di cui componente 0 è l' immagine
    # componente 1 e 2 sono coordinate x1 e y1 del bounding box, componente 3 e 4 sono coordinate x2 e y2 della bounding box

    imagesWithBB = [
        genCircle() if targets[x] else genRectangle() for x in range(nsamples)
    ]

    # creo il vettore delle immagini di lunghezza nsamples
    images = np.array([imagesWithBB[x][0] for x in range(nsamples)])

    # creo il vettore che contiene le coordinate della bounding box di ciascuna delle n samples immagini
    # che sono le coordinate da 1 a 4 della tupla restituita da genCircle e genRectangle
    boundingBoxes = np.array([imagesWithBB[x][1:] for x in range(nsamples)])

    "disegniamo le boundig boxes"
    for i in range(5):

        images_labelled = images[i].copy()
        x1 = boundingBoxes[i][0]
        y1 = boundingBoxes[i][1]
        x2 = boundingBoxes[i][2]
        y2 = boundingBoxes[i][3]

        cv2.rectangle(images_labelled[i], (x1, y1), (x2, y2), (0, 255, 0), 1)


"Ora mostriamo qualche immagine generata"

"""
for i in range(4):
   plt.imshow(images[i])
   plt.show()

"""


print(targets.shape)
print(images.shape)

lista = []
for j in range(4):
    lista.append(targets[j])

print(lista)


"Ora creiamo la nostra CNN"


inputs = Input(shape=(64, 64, 3))

if conv:

    "primo blocco convolutional, pooling"

    kernel = Conv2D(16, (5, 5), padding="same")(inputs)
    # primo argomento è il numero di filtri da utilizzare, secondo argomento è la dimensione della matrice di convoluzione
    # same è invece il padding in cui la mappa resta della solita dimensione dell' immagine

    # primo argomento è la riduzione, devo poi passare il layer su cui fare pooling, ottengo poi una mappa 32x32
    pooling = MaxPooling2D((2, 2))(kernel)

    "secondo blocco convolution, pooling"

    kernel = Conv2D(32, (5, 5), padding="same")(kernel)
    pooling = MaxPooling2D((2, 2))(kernel)
    # le mappe ora sono 16x16

    "terzo blocco convolutional, pooling"

    kernel = Conv2D(64, (5, 5), padding="same")(kernel)
    pooling = MaxPooling2D((2, 2))(kernel)

    # alla fine ho una mappa 8x8 che posso dare ad un MLP
    # la mappa finale sarà un suo hidden layer

    hidden_layerMLP = Flatten()(pooling)

    hidden_layerMLP = Dense(64, activation="relu")(hidden_layerMLP)
    hidden_layerMLP = Dense(16, activation="relu")(hidden_layerMLP)
    hidden_layerMLP = Dense(8, activation="relu")(hidden_layerMLP)

    # definiamo l' output layer
    if simple:

        # questo è un problema di classificazione 0,1 quindi ho un solo output interpretato come la probabilità di essere
        # un triangolo o un rettangolo

        output_layer = Dense(1, activation="sigmoid")(hidden_layerMLP)
        loss = "binary_crossentropy"  # la binary cross entropy è utile nei problemi di classificazione perchè
        # penalizza di più le classificazione sbagliate

    if mixed:

        # questo è un problema di regressione in cui mi viene restituito il numero di rettangoli o il numero di cerchi

        output_layer = Dense(2, activation="relu")(hidden_layerMLP)
        loss = "mean_squared_error"

# imposto il modello
model = Model(inputs=inputs, outputs=output_layer)

# e lo compilo

model.compile(loss=loss, optimizer="adam", metrics=["accuracy"])

model.summary()


" Per visualizzare la rete "

"""
from tensorflow.keras.utils import plot_model
plot_model(model, show_shapes = True, show_layer_names = True, to_file = "model.png")
from IPython.display import Image
Image(retina = True, filename = "model.png")

"""


risultati_modello = model.fit(x=images, y=targets, epochs=10, validation_split=0.5)
# ricordiamo che il batch size è il numero di dati dopo il quale fare un aggiornamento dei pesi


"Grafico di confronto tra loss nel validation e loss nel training"

print(risultati_modello.history.keys())
plt.plot(risultati_modello.history["val_loss"])
plt.plot(risultati_modello.history["loss"])
plt.show()


print(f"precisione modello: {risultati_modello.history["accuracy"]}")


"Creiamo nuove immagini e vediamo se la rete la sa distinguere"

if simple:

    testing = genCircle[0]
    print(testing.shape)
    plt.imshow(testing)

    # facciamo fare una predizione al modello su un singolo dato 64x64x3
    prediction = model.predict(testing.reshape(1, 64, 64, 3))

    # prediction[0] è un numero tra 0 e 1 inerente alla immagine nuova

    print("è un ", "cerchio" if prediction[0] > 0.5 else "rectangle")
