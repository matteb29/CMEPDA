import requests #questa libreria serve per scaricare file da internet HTTP
import threading as thr
from time import perf_counter #perf_counter è un timer ad alta prestazione


#un modulo (come requests) è un altro programma (file.py) che posso utilizzare
#in un altro codice, d' altra parte numpy è un package (pacchetto) che contiene tanti moduli
#di cui la maggior parte scritti in C



#inizializzo la lunghezza in byte su cui opero ogni volta
buffer_size=1024 # uguale a 1kB



#define a function to manage the download



def download(url):
 


 response = requests.get(url, stream=True) #la libreria requests
 #contiene la funzione get 
 #requests.get restituisce un oggetto della classe response il quale avrà come metodo iter_content()
 #e contiene tutti i dati scaricati dall' url data in parametro


#url.split significa che crea una lista i cui elementi sono creati
#in modo che scorrendo in url, ogni volta che trova uno ("/") allora crea un nuovo elemento

#il nome del file sarà l' ultimo elemento della lista
#cioè l' ultima parte dell' url
 
 
 
 filename = url.split("/")[-1]

 #[-1] serve per prendere l' ultimo elemento della lista




 with open(filename, "wb" ) as f:

    #as f vuol dire che ciò che restituisce open(filename, "wb") 
    #lo rinomino come f


    #se open non trova un file di nome filename lo crea lui stesso
    #se invece lo trova lo apre e cancella il contenuto precedente

    # "wb" significa w = write, b = binary cioè apri il file
    # in modalità scrittura binaria




    #realizzazione di un ciclo for per leggere dati da un file (caricato da internet)
    #1kB alla volta



    for data in response.iter_content(buffer_size):

        #iter_content è un metodo della classe Response che serve per leggere il contenuto
        #a blocchi di dimensione buffer_size

        #scriviamo il kB letto dall' oggetto response nel file filename
        # ricordandomi che il file f è in modalità scrittura binaria

        f.write(data)




#MAIN

if __name__ == "__main__":

    urls= [
       
    "http://cds.cern.ch/record/2690508/files/201909-262_01.jpg",
    "http://cds.cern.ch/record/2274473/files/05-07-2017_Calorimeters.jpg",
    "http://cds.cern.ch/record/2274473/files/08-07-2017_Spectrometer_magnet.jpg",
    "http://cds.cern.ch/record/2127067/files/_MG_3944.jpg",
    "http://cds.cern.ch/record/2274473/files/08-07-2017_Electronics.jpg",

    ]

    t = perf_counter()



#sequential download
for url in urls:

    download(url)

    print("Time: "+str(perf_counter()-t)) 
    #l' output del programma è in secondi