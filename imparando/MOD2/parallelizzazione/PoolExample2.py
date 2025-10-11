import multiprocessing as mp
import time
import os

def doingstuff(x):
    print ("Process: "+str(x)+" "+str(os.getpid()))
    #scrivere os.getpid() e farselo stampare è un buon controllo per
    #verificare quanti processi sono stati creati

    #se io non metto il time.sleep allora il processo si riduce ad un semplice
    #print stringa

    time.sleep(1)

    #noto che se non metto time.sleep(1) allora vedo un solo PID (massimo 2 PID), cioè
    #creo un solo processo (massimo 2 ), perchè il codice da eseguire è troppo veloce e gli altri processi
    #non ricevono lavoro
    




if __name__ == "__main__":
    #misuro il tempo segnandomi lo start
    start=time.time()

    pool = mp.Pool(processes=4)

    #questo non è asincrono perciò prima devono finire tutti i processi
    #e poi dopo si proseguo con il resto del codice, restituisce direttamente i risultati e
    #non serve scrivere print(results.get())

    results = pool.map(doingstuff ,range(1,10))

    #e qui mi segno lo stop
    end=time.time()


    print("elapsed time: "+str(end-start))
    #print(results.get())

