from sklearn.datasets import load_digits
import matplotlib.pyplot as plt

from sklearn.manifold import Isomap
#importiamo dalla libreria manifold l' algoritmo isomap



digits = load_digits() 
print(digits.images.shape) #1797 campioni ciascuno formato da una griglia 8x8
#ovvero ho 1797 immagini di 8 pixel x 8 pixel cioè ogni dato ha 64 feature

fig, axes = plt.subplots (10, 10, figsize = (8,8), subplot_kw = {"xticks":[], "yticks":[]}, 
                          gridspec_kw=dict(hspace = 0.1, wspace = 0.1))


#creo grafici dove 10, 10 indicano una griglia 10x10 di grafici
#usando xticks=[] e yticks=[], diciamo a Matplotlib di non mostrare i numeri 
#(le "tacchette") sugli assi x e y per nessuno dei grafici,
#controllo lo spazio tra i subplots con gridspec_kw=dict(hspace = 0.1, wspace = 0.1)


#axes ora è un array numpy 10x10




#inizia ora un ciclo per riempire la griglia

for i, ax in enumerate(axes.flat): #axes.flat appiattisce l' array axes 10x10 in uno 1dim di lunghezza 100

    #.imshow dice ad ax di disegnare l' immagine i-esima del dataset
    #cmpa = binary fa la mappa di colore in bianco e nero
    #interpolation="nearest": Determina come Matplotlib deve "ingrandire" l'immagine 8x8 per riempire lo spazio del subplot. 
    #"nearest" (vicino più prossimo) fa sì che ogni pixel 8x8 sia mostrato come un quadrato netto, 
    # senza sfumature, il che è ideale per vedere i dati "grezzi".

    ax.imshow(digits.images [i], cmap = "binary", interpolation = "nearest")

    #in ax.imshow(), l'asse X va da 0 a 7 e l'asse Y va da 0 a 7.
    #trasformeremo poi l' asse X in coordinate relative in subplot


    ax.text(0.05, 0.05, str(digits.target[i]), transform = ax.transAxes, color = "green")

    #creo l' etichetta che ha come scritta str(digits.target[i])
    #transform = ax.transAxes dice che le coordinate 0.05 e 0.05 in cui posizionare la scritta sono relative all' asse
    # x=0.05: Muoviti a destra del 5% della larghezza totale del box.
    #dove ad esempio (1,1) è l' angolo in alto a destra, le coordinate possono anche essere relative al pixel (e andrebbero da 0 a 7
    #visto che ho 8 pixel per ogni immagine)



X = digits.data
print(X.shape)


y = digits.target
print(y.shape)





iso = Isomap(n_components = 2)
#utilizzeremo l' algoritmo isomap per ridurre le 64 dimensioni:
#caratteristiche di ogni dato (8x8) in 2 sole caratteristiche attraverso un algoritmo non supervisionato
#iso è una istanza della classe Isomap


#Isomap è un algoritmo basato sul concetto di manifold(spazi con la propria metrica che localmente sono spazi euclidei 2dim)
#i nostri dati avendo 64 features vivono in uno spazio 64-dimensionale euclideo
#si ipotizza che i dati si dispongano su una unica manifold che inizia a mappare (su una manifold ho una metrica)
#cioè costruisce prendendo, per ogni punto i suoi punti vicini e creando un unico grafo che li colleghi


#Pensiamo a tutte le cifre come a paesi(raggruppamento di dati) diversi su un unico continente (la manifold)
#Il "paese" degli '1' è molto vicino al "paese" dei '7'.
#Il "paese" degli '8' è vicino a quello dei '6' e dei '9'.
#Il "paese" degli '0' è forse più isolato, ma è comunque collegato agli altri da una "strada" (una serie di trasformazioni intermedie).
#L'intero dataset digits è visto come un unico continente curvo (la manifold) immerso nello spazio 64D.


#Una volta mappata tutta la manifold posso calcolare la distanza tra 2 punti qualsiasi della manifold usando la sua metrica piuttosto che
#calcolando come distanza euclidea 64 dimensionale, in particolare calcola la geodedica tra 2 punti approssimata.
#alla fine di questi calcoli approssimati di geodediche otteniamo una matrice 1797x1797 contenente le distanze tra tutti i punti sulla
#manifold dove la cella (i, j) contiene la distanza tra il punto i e il punto j solo se j è
#uno dei 5 vicini più prossimi di $i$. Tutte le altre celle sono zero (vuote).


#Dopo aver ottenuto questa matrice Isomap usa un algoritmo chiamato Multidimensional Scaling (MDS)
#il quale cerca un nuovo set di coordinate (2 perchè abbiamo creato un modello isomap a 2 componenti)
#con cui descrivere i 1797 punti, nel quale le distanze tra di essi siano il più fedele possibile alle distanze sulla manifold  



iso.fit(digits.data) 

#chiamo il metodo .fit() per allenare il mio algoritmo iso sui dati digits, che sono un array (1797, 64)
#.fit() "impara" la struttura sottostante dei tuoi dati. Isomap costruisce 
# un grafo dei vicini più prossimi per capire come i punti sono connessi tra loro nello spazio a 64 dimensioni.

#In particolare leggendo le specifiche di isomap troviamo il metodo fit() e scopriamo che usa l' algoritmo NearestNeighbors
#(vedi da 219 a 226 quando definisce l' istanza nbrs del modello)
#in 228 chiamo il metodo fit di NearestNeighbors


data_projected = iso.transform(digits.data)
#.transform() applica la riduzione dimensionale imparata nel .fit().
#Converte l'array (1797, 64) in un nuovo array, dove ogni campione ha solo 2 coordinate.


print(data_projected.shape) #qui otteniamo un array (1797,2)

plt.figure(figsize=(10,10))

#plottiamo questi 1797 dati bidimensionali per vedere se possiamo imparare qualcosa/vedere pattern
plt.scatter(data_projected[:,0], data_projected[:,1], c = digits.target, 
            edgecolors="none", alpha = 0.5, cmap = plt.cm.get_cmap("cubehelix", 10))



plt.colorbar(label = "digit label", ticks = range(10))


plt.clim(-0.5, 9.5)


plt.show()
