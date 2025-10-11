import multiprocessing as mp
import os 
import time



#questa è la funzione che voglio eseguire con il parallelismo
def cube(x):
    #metto uno sleep per far usare diversi porcessi altrimenti vedevo
    #un unico PID
    time.sleep(1)
    #con questo vedo effettivamente 4 PID diversi corrispondenti ai 4 processi della pool
    print (str(os.getpid())+" "+str(os.getppid()))
    return x**3


#MAIN

if __name__ == "__main__":

    #la pool serve per un parallelismo controllato, 
    #se per esempio volessi lavorare con 4 soli processi anche se ho 1000 task
    #con la pool posso gestir equesti 1000 task sui 4 processi

    #evito di creare ogni volta un nuovo processo
    #sembra un array di 4 processi 

    pool = mp.Pool(processes=4)

    #questa funzione serve per mappare una funzione in una lista di valori
    #cioè eseguo la funzione cube sulla lista di valori scritta come range(1,7)
    #siccome ho 7 numeri e soltanto 4 processi, il os gestisce prima i primi 4 numeri e poi quando
    #si liberano i processi assegna gli altri 3 
    results = pool.map_async(cube,range(1,7))

    #stai eseguendo il compito di fare il cubo dei numeri da 1 a 7, ma 
    #mentre prima avremmo chiamato un processo per ogni numero, qui
    #ci limitiamo ad usare solo 4 processi


    #inoltre con async posso fare dell' altre operazioni nel mentre che sto
    #aspettando il risultato della funzione cube.
    #infatti lui usando async non ti restituisce subita una lista di risultati ottenuti 
    #dalla funzione cube
    #piuttosto ti fornisce un risultato speciale che si chiama AsyncResult che vedrò solo
    #quando stampo result.get()


    print(results)
    
    #questa riga sopra serve per farti stampare questa:
    #<multiprocessing.pool.MapResult object at 0x109e3e2a0>
    #che significa ho un oggetto speciale di Python che si chiama MapResult
    #ottenuta grazia la funzione map.async 
    #0x109... è l' indirizzo di memoria dell' oggetto MapResult

    #Se i processi hanno finito, ti restituisce la lista dei cubi [1, 8, 27, 64, 125, 216].
    #timeout=1 significa: “Aspetta al massimo 1 secondo; se non sono finiti, lancia un errore.”
    #infatti se metto timeout = 0.00000000000000001 mi dice multiprocessing.context.TimeoutError


    print(results.get(timeout=7))
    

    

    




#output = [p.get() for p in results]
#print(output)
