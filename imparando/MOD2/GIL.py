#il GIL è un meccanismo thread-safe implementato in automatico da python, 
#è come una chiave che il cpython interprete fornisce ad un thread alla volta
#per accedere alle variabili condivise

import threading
import time 


def worker(thread_id):
    for i in range(5):
        print(f"Thread {thread_id} - Iterazione {i} - Ha il GIL")
        time.sleep(0.1) #quando chiamo lo sleep il GIL viene rilasciato
        #nota che nell' output vedo la sequenza di thread non crescente cioè ci sono
        #anche output del tipo 0-2-3-4
        #vuol dire il GIL è assegnato "casualmente" 


        #nota che al primo ciclo quando ho thread 0 che va in sleep, 
        #il GIL viene passato a thread 1 che quindi può fare il suo ciclo di iterazioni
        

#Python non garantisce un ordine fisso tra i thread.
#Di fatto, il thread successivo che prende il GIL 
#è scelto dal sistema operativo e dall’implementazione di Python, quindi 
# sembra “casuale” a livello pratico.


#se per esempio chiamassi time.sleep(0.0001), la durata è così breve 
# che il thread potrebbe non essere effettivamente sospeso abbastanza a 
# lungo da consentire al sistema operativo di schedulare un altro thread. e quindi il thread0
#finisce il suo ciclo di iterazioni



threads = []

for i in range(5):
    t = threading.Thread(target = worker, args = (i, ))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

















