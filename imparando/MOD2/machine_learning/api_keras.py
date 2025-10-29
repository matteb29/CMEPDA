
#con questo programma usiamo uno standard più moderno per le reti neurali
#stampiamo un diagramma schematico della rete 

from keras.models import Model
from keras.layers import Input, Dense
from keras.utils import plot_model


#definiamo il layer di input, il numero di nodi è il numero di features con cui descrivo
#un singolo dato

x = Input(shape = (32,))


#definiamo l' hidden layer dove con questo standard di programmazione
#metto x alla fine per dire cosa dargli in input. Ci saranno 32 x 32 pesi da ottimizzare durante il training

hid = Dense(32, activation = "relu")(x)


#definiamo il layer di output

out = Dense(1, activation = "sigmoid")(hid)



model = Model(inputs = x, outputs = out )

model.summary()

plot_model(model, to_file = "model.png", show_shapes = True)




