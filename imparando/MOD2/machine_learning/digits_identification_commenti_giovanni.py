from sklearn.manifold import Isomap
import matplotlib.pyplot as plt 
#la funzione load_digits che stiamo importando dalla libreria di sklearn contiene 
#immagini di cifre scritte a mano 
from sklearn.datasets import load_digits

#load_digits è una funzione che ha come ritorno l'oggetto di una classe di sklearn detta bunch
#questa ha come attributi .images che contiene 1797 immagini nel formato 8X8
#pixel che posso indicare come (1797,8,8), poi abbiamo .data che contiene le 
#stesse immagini ma sottoforma di 1797 vettori da 64 pixel, poi abbiamo.target
#che contiene un array da 1797 elementi (cifre da 0 a 9) le quali sono 
#sostanzialmente le etichette. Infine abbiamo .DESCR che descrive il dataset 
digits = load_digits()

# La forma (shape) dei dati è (1797, 8, 8), cioè 1797 immagini di 8x8 pixel
# print(digits.images.shape) 

#plt.subplot restituisce 2 oggetti che sono fig e axes fig è la tela intera
#l'altro oggetto axes è l'organizzazione della griglia, sarebbero i primi due
#comandi 10, 10 che sarebbero 10 righeX 10 colonne 
#figsize è la dimensione dell'intera figura 8 pollici X 8 pollici 
#l'ultimo invece decide lo spazio tra i sub plot 
fig, axes = plt.subplots(10, 10, figsize=(8, 8),
                         subplot_kw={'xticks':[], 'yticks':[]},
                         # Imposta la spaziatura tra i subplot
                         gridspec_kw=dict(hspace=0.1, wspace=0.1))

#axes.flat mi restituisce un vettore con tutti i subplot
for i, ax in enumerate(axes.flat):
    # imshow è il comando per disegnare le immagini cioè per ogni ax(subplot)
    #in axes(la griglia) disegna un immagine (digits.images[i]) colorata in un
    #certo modo (cmap='binary') e zumma i pixel (interpolation='nearest')
    ax.imshow(digits.images[i], cmap='binary', interpolation='nearest')
    # Questo è il comando per disegnare nel testo. Il primo (0.5,0.5) dice dove
    #posizionare la scritta, ma senza sistema di riferimento che sarà dato da 
    #invece d trasform, quest'ultimo in questo caso dice con ax.transAxes
    #di mettere il sistema di riferimento volta per volta su un subplot 
    #infine str... è òa scritta vera e propria
    ax.text(0.05, 0.05, str(digits.target[i]),
            transform=ax.transAxes, color='green')

# Mostra il grafico
plt.show()
#Isomap è un algoritmo di riduzione dimensionale. Il suo scopo è prendere dati
#che si trovano in uno spazio con molte dimensioni (come le tue immagini, che
#hanno 64 dimensioni/pixel) e "schiacciarli" in uno spazio con meno dimensioni
#(nel tuo caso, 2 dimensioni), cercando di preservare la struttura e le
#relazioni intrinseche tra i punti.
#È una tecnica di Manifold Learning (apprendimento di varietà). L'idea è che
#i tuoi dati a 64 dimensioni, pur vivendo in uno spazio enorme, in realtà si
#dispongono lungo una superficie o una struttura "curva" (la "varietà") a
#dimensioni inferiori.
#n_compnents=2 è il numero di dimensioni a cui voglio ridurlo 
iso=Isomap(n_components=2)
#Il metodo di apprendimento .fit fa diverse cose tra queste abbiamo:
#1. Costruzione del Grafo dei Vicini (Neighborhood Graph):
#Questa prima parte non fa altro che costruire un grafo tra i punti vicini
#cioè da ogni punto partono 5 (generalmente è il numero di default) branch 
#che si collegano a quelli più vicini. Ho creato un grafo
#2. Calcolo delle Distanze Geodetiche (Geodesic Distances)
#In questa parte suppongo che sulla scala delle distanze tra i punti la 
#superficie sia abbastanza piatta da far finta che la distanza tra i primi
#vicini siano tangenti alla curva (questa ipotesi dipende fortemente da quanto
#sono densi i punti). A questo punto se so calcolare la distanza tra tutte
# le possibili coppie di punti ho sostanzialmente le distanze geodetiche
#Viene creata una grande matrice di distanze (1797x1797) che contiene la
#distanza geodetica tra ogni immagine e ogni altra immagine.
#A questo punto abbiamo una matrice 1979X1979 che contiene tutte le distanze 
#geodetiche. Quello che fa l'algoritimo a questo punto e definire 1797 punti
#casuali nel piano e cerca di aggiustarli spostando ogni punto in modo che
#abbassi lo stress S =\sqrt(sum_i,j((D64_ij-D2ij)^2)) cioè la radice della 
#somma dei quadrati delle differenze tra le distanze.
#IMPORTANTE: Dopo .fit il modello non ha imparato una matrice di proiezione
#o qualche formula analitica semplice, la sua conoscienza si limita a come
#mappare quei punti in 64 dimensioni in una mappa 2 dimensionale 
iso.fit(digits.data)
#Quando chiami iso.transform() su un nuovo punto (un punto che non era nel training set), Isomap esegue un
#processo chiamato "out-of-sample extension" (estensione fuori campione).
#La prima cosa che accade è il calcolo di tutte le distanze dai punti nello spazio 64D
#a questo punto ho tutte le distanze geodetiche da questo punto. Adesso l'idea sarebbe quella di dire:
#siccome io sto assumendo che le mie distanze geodetiche si conservano allora vado nello spazio 2D 
#disegno i cerchi con raggio pari alle geodetiche calcolate prima e centrati nei 1797 punti e
#l'intersezione tra questi punti dovrebbe darmi le coordinate del punto, ma  questo non è vero.
# Essendo i conti delle geodetiche delle approssimazioni ci sono un groviglio di punti di intersezione 
#disordinati. Quindi l'algoritmo ignora completamente le intersezioni e si dedica invece ad usare le 
#geodeyiche come verità assolute tramite lo stress. Prende dunque un punto a caso sulla mappa 2D e calcola
#lo stess in quel punto facendo la differenza tra le geodeditiche calcolate nello spazio 64 D e quelle 
#nello spazio 2D del punto scelto a caso, dopodichè si sposta di poco in tande direzioni diverse e ricalcola
#divolta in volta lo stress nei nuovi punti trovando alla fine il punto che lo minimizza o esaurendo le
#interazioni
data_projected=iso.transform(digits.data)
data_projected.shape
#Qui c=digits.target crea una funziona biunivca tra i colori e le targhette reali,è un test per capire se
#l'algoritmo ha fatto davvero bene, se tutti i punti dello stesso colore si trovano nello stessa ragione 
#allora il programma è stato allenato bene 
plt.scatter(data_projected[:, 0], data_projected[:, 1], c=digits.target, 
            edgecolor='none', alpha=0.5,
            cmap=plt.cm.get_cmap('cubehelix',10))
plt.colorbar(label='digit label', ticks=range(10))
plt.clim(-0.5,9.5)
plt.show()




