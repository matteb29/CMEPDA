import math
import multiprocessing
import random
import threading
import time
import matplotlib.pyplot as plt
import numpy 







#questa funzione timer sarà quella che ci terrà conto dei tempi
#di esecuzione di un programma che fattorizza una lista di numeri (nums)
#rannato in diverse tecniche di programmazione (seriale, con thread, con processi)


class Timer(object):


    def __init__(self, name=None):
        self.name = name
        self.timee=0



    #__enter__ è un metodo speciale che viene chiamato
    #quando entri nel blocco with

    def __enter__(self):
        self.tstart = time.time()



    #__exit__ è un metodo speciale che viene chiamato
    #quando esci dal blocco with

    def __exit__(self, type, value, traceback):

        if self.name:

        #nota che nell' attributo name  è inizializzato come None, che viene visto
        #come un false nella logica Booleana
            print('[%s]' % self.name, end=' ')


    #siccome time è un nome speciale questa variabile della classe
    #la chiamo con 2 e cioè timee

        self.timee = (time.time() - self.tstart)


        print('Elapsed: %s' % (time.time() - self.tstart))

        #chiamo il metodo output della classe timer
        self.output()



    def output(self):
        return self.timee


#questa è una funzione per scomporre in fattori un numero n
#e la applicherò con varie tecniche di programmazione: seriale, processi, thread 

def factorize_naive(n):



    """ A naive factorization method. Take integer 'n', return list of
        factors.
    """
    if n < 2:
        return []
    
    #una lista vuota in cui metterò i fattori del numero n
    factors = []


    p = 2



    #simile a while 1 è per fare un ciclo infinito
    while True:


        if n == 1:
            return factors
        

        r = n % p #qui definisce il resto della divisione tra n e p
        #dove p = 2



        #se resto = 0 allora il numero p =  2 è un fattore del numero n
        if r == 0:
            #quindi lo appendo alla lista dei fattori
            factors.append(p)


            n = n // p #questo fa la divisione intera togliendo la parte decimale e arrotondando
            #sempre per difetto, aggiornando il valore di n



        elif p * p >= n:


            #la lista dei fattori contiene anche il numero stesso
            factors.append(n)

        #sono finiti i fattori e quindi ti restuisce la lista dei fattori
            return factors
        

        #qui serve per trovare i fattori dispari
        elif p > 2:

            # Advance in steps of 2 over odd numbers
            p += 2

        else:
            # If p == 2, get to 3
            p += 1
            

    #se per qualche motivo arrivo qui stampa l' errore  
    #non era necessario      
    assert False, "unreachable"









# Each "factorizer" function returns a dict mapping num -> factors




#qui ti mostra l' esecuzione seriale della fattorizzazione 
#di più numeri contenuti in una lista nums

def serial_factorizer(nums):

    #parentesi graffe sono un dizionario, che ricordiamo essere
    #un insieme di coppie del tipo (chiave, valore)
    #in questo dizionario n è una chiave
    #e il "valore" del dizionario è "factorize_naive" 

    return { n: factorize_naive(n) for n in nums}



#questa è una dictionary comprehension che ha la seguente sintassi
# {chiave: valore for elemento in iterabile} 
#la dictionary comprehension è un modo veloce per creare un dizionario in python
#piuttosto che fare un ciclo for


#qui ti vuole far vedere la fattorizzazione di più numeri contenuti nella lista nums
#usando la programmazione concorrenziale con threads
#in particolare la funzione threaded_factorizer ha come input la lista di numeri da fattorizzare: 
# nums ed il numero di thread da usare: nthreads

def threaded_factorizer(nums, nthreads):

    #in seguito faremo prove con nthread = 2, 4, 8

    #ogni funzione worker sarà il target di un thread
    #la funzione worker ha il compito di fattorizzare tutti i numeri nella lista nums
    #e di scrivere questi fattori in outdict(variabile parametro della funzione worker)
    def worker(nums, outdict):

        """ The worker function, invoked in a thread. 'nums' is a
            list of numbers to factor. The results are placed in
            outdict.
        """
        for n in nums: #ricorda che nums è una lista di numeir che vogliamo fattorizzare

            
            outdict[n] = factorize_naive(n)

    

    # Each thread will get 'chunksize' nums and its own output dict
    #math.ceil arrotonda per eccesso all' intero più vicino, ad esempio 1.4 diventa 2

    chunksize = int(math.ceil(len(nums) / float(nthreads)))

    #per dire che ogni thread deve elaborare al massimo una certa quantità di numeri da fattorizzare
    #(contenuti all' interno di nums), per dividere il carico di lavoro tra i thread

    #così che ogni thread avrà come target la funzione worker con argomento una lista di 
    # dimensioni chunksize




    #faccio una lista di thread
    threads = []


    #qui crea un dizionario vuoto per ogni thread
    outs = [{} for i in range(nthreads)]




    for i in range(nthreads):

        # Create each thread, passing it its chunk of numbers to factor
        # and output dict.



        t = threading.Thread(

                target=worker,

                #se per esempio chunksize fosse 3 allora il trhread 0 associato
                #alla i = 0 lavorebbe con soli 3 elementi della lista nums, in particolare
                #lavorerebbe con 3 * 0 = 0 e con elemento 1 e 2 

                args=(nums[chunksize * i:chunksize * (i + 1)],
                      
                      #chunksize * i =  start
                      #chunksize * (i+1) = stop (non è compreso)



                      #l' argomento di worker per outdic è il dizionario "vuoto" outs[i]
                      #che fa riferiemento al thread i-esimo

                      outs[i]))
        

        threads.append(t)
        t.start()

    # Wait for all threads to finish
    for t in threads:
        t.join()

    # Merge all partial output dicts into a single dict and return it
    return {k: v for out_d in outs for k, v in out_d.items()}

#creo un nuovo dizionario che ha come chiave k e come valore v 
#ci sono poi due cicli for annidati per creare questo dizionario unito:

#i due for annidati significano
#per ogni dizionario out_d (variabile contatore) scorri l' iterabile outs(lista di dizionario
#che voglio unire) 
# e per ogni dizionario nella lista scorri le coppie chiave valore del dizionario
#che diventeranno coppie chiave valore del dizionario unito


# (PER OGNI DIZIONARIO CONTENUTO NELLA LISTA OUTS DEI DIZIONARI)
#(E PER OGNI COPPIA K, V CHIAVE VALORE CONTENUTA ALL' INTERNO DEL DIZIONARIO OUT_D)

#out_d.items() restituisce la coppia chiave valore del dizionario



#serve per unire tutti i dizionari creati per ogni thread in un unico grande dizionario




#ora ti vuole far vedere come si può fattorizzare una lista di numeri
#usando più processi e quindi applicando il parallelismo 



def mp_worker(nums, out_q):

    """ The worker function, invoked in a process. 'nums' is a
        list of numbers to factor. The results are placed in
        a dictionary that's pushed to a queue.
    """
    outdict = {}

    for n in nums:
        outdict[n] = factorize_naive(n)

    #out_q è chiaramente una coda
    #cioè un oggetto condiviso tra più processi di tipo FIFO 
    #che ha il metodo put per inserire e get per farsi restituire   

    #nella coda inserisco la lista di dizionario contenenti ciascuno la lista di fattori del numero
    #n con n contenuto nella lista di numeri nums




    out_q.put(outdict)










def mp_factorizer(nums, nprocs):
    # Each process will get 'chunksize' nums and a queue to put his out
    # dict into


    #proprio qui definisce out_q come un oggetto di tipo coda
    out_q = multiprocessing.Queue()


    #come per i thread
    chunksize = int(math.ceil(len(nums) / float(nprocs)))

    #qui creo una lista vuota di processi
    procs = []

    for i in range(nprocs):


        #qui definice il processo i-esimo
        p = multiprocessing.Process(

                target=mp_worker,
                args=(nums[chunksize * i:chunksize * (i + 1)],
                      
                      out_q))
        
        #sfruttando il fatto che out.q è un oggetto condiviso tra i processi 
        #faccio lavorare ciascun processo con out.q piuttosto che come facevo prima 
        #dove lavoravo con outdict[i] e poi dovevo unire tutto

        #ogni processo aggiungerà alla coda un numero limitato di elementi 
        #in particolare ogni processo aggiungerà alla coda il suo dizionario
        #relativo ai numeri con cui ha lavorato

        procs.append(p)
        p.start()

    # Collect all results into a single result dict. We know how many dicts
    # with results to expect.

    resultdict = {}
    for i in range(nprocs):

        #tutti i dizionari sono già uniti nella coda avendo fatto lavorare ogni processso
        #con argomento la coda stessa

        resultdict.update(out_q.get())

        #.update serve per aggiornare il dizionario vuoto facendosi dare tutta la coda
        #tuttavia per farsi restituire qualcosa dalla coda bisogna usare il metodo .get()




    # Wait for all worker processes to finish
    for p in procs:
        p.join()



    return resultdict




#funzione per plottare i risultati

def plot_results(elapsed):

    plt.rcdefaults()
    fig, ax = plt.subplots()
    laby = ('Serial','Thread 2','Process 2','Thread 4','Process 4','Thread 8','Process 8')
    y_pos = numpy.arange(len(laby))
    ax.barh(y_pos, elapsed, align='center')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(laby)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel('Elapsed time')
    ax.set_title('Serial, threads, processes comparison')
    plt.show()

    wait()







#stampa tutti i risultati ottenuti con le varie tecniche di programmazione

def benchmark(nums):


    print('Running benchmark...')

    #creo una lista di tempi trascorsi
    elapsed_times=[] 

    #tserial è un oggetto di tipo timer con il nome "serial" (attributo)
    tserial= Timer('serial')

    
    with tserial as qq:  #utilizza timer e che ciò che restituisce timer viene assegnato a qq
        #ma siccome tserial non restituisce nulla questa riga è inutile


        s_d = serial_factorizer(nums) #s_d è il dizionario
        #restituito dalla funzione serial_factorizer costuito dai fattori di tutti i numeri
        #presenti nella lista nums


    #ricordo che la classe timer possiede il metodo speciale __exit__ che mi dice cosa
    #fare dopo che esco dal with, per questo utilizzo il blocco with tserial




    #dove ricordo che il metodo output dell' oggetto timer restituisce il tempo 
    #trascorso durante l' esecuzione dell' algoritmo con cui fattorizzo 


    elapsed_times.append(tserial.output())





    #da ora parliamo di programmazione concorrente

    for numparallel in [2, 4, 8]:

        #qui chiamo un oggetto di tipo timer chiamato con il nome threaded2
        #al primo ciclo, threaded4 al secondo ciclo etc

        tthread= Timer('threaded %s' % numparallel)


        #solita tecnica della seriale
        with tthread as qq:

            t_d = threaded_factorizer(nums, numparallel)
            #fattorizzazione usando un numero specifico di thread che al primo ciclo è 2
            #al secondo è 4 etc


        elapsed_times.append(tthread.output())




        #questo invece, sempre nel solito ciclo for
        #è per la programmazione concorrente usando i multiprocessi

        tmpar= Timer('mp %s' % numparallel)
        #dove ho definito un oggetto di classe timer 

        #solita tecnica
        with tmpar as qq:
            m_d = mp_factorizer(nums, numparallel)




        elapsed_times.append(tmpar.output())



    
    print (elapsed_times)
    plot_results(elapsed_times)
    







#MAIN


if __name__ == "__main__":


    N = 299


    #inizializzo nums come una lista di 1 solo valore di 12 cifre
    nums = [999999999999]
    #creo il resto della lista con il ciclo for sottostante


    #questo ciclo serve per creare la lista nums a partire da quella inizializzata sopra

    for i in range(N):

        nums.append(nums[-1] + 2)

        #nums[-1] il fatto che ci sia -1 è dovuto al fatto che la lista utilizza sia spostamento
        #in avanti che indietro
        #tuttavia se sono in posizione 0 cioè ho un solo elemento allora -1 mi ritorna in me stesso
        #quando ho due elementi tornando indietro con effetto packman mi ritrovo al secondo elemento

        #quindi nums[-1] è un metodo astuto per spostare il focus all' ultimo elemento aggiunto


    #alla fine nums contiene 300 elementi che dovrò fattorizzare
    #con i diversi algoritmi: seriale, threading, multiprocessi
    print(nums) 



    benchmark(nums)
