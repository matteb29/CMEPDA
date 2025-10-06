
#Calculate for each number in a list, the sum of
#all primes which are smaller than the given
#number. It should output the pairs [n,
#sum_primes(n)] sorted by n. 
#Your task is to calculate range(100000,
#2500000, 100000). Please use the
#multiprocessing module and compare the
#result (in term of execution time) with the serial
#version of your code.

import math 
import multiprocessing as mp
import threading
import random
import time
import numpy
import matplotlib.pyplot as plt 
import numpy as np



#classe timer per poter poi paragonare 
#i tempi di esecuzione dei vari algoritmi: seriale, concorrente con multiprocessing
#e con threads

class Timer(object):

    #definiamone attributi
    def __init__(self, name = None):

        self.name = name
        self.tempo = 0 #inizializziamo il tempo a zero

    #il metodo speciale per quando chiamo la classe con with

    def __enter__(self):

        self.tstart = time.time() #tempo di inizio dalla chiamata dell' oggetto timer

    #metodo speciale da eseguire per quando esco dal blocco with
    def __exit__(self, type, value, traceback):

        if self.name:

            print(f"{self.name} ")

        self.tempo_impiegato =  time.time() - self.tstart
        print(f"tempo impiegato: {(time.time() - self.tstart)}")


        #chiamo il metodo output della classe timer
        #la sintassi della chiamata di altri metodi all' interno di un metodo è oggetto.metodo()
        # == self.metodo()
        self.output()


    #il metodo output è un semplice metodo per farmi restituire il tempo impiegato
    #che con self diventa una variabile accessibile agli altri metodo
    #infatti nota che l' ho definita in metodo speciale __exit__()

    def output(self):
        
        return self.tempo_impiegato

    
def factorize_naive(n):


    if n < 2:
        return[]
    
    factors = []

    p = 2


    while True:

        if n == 1:
            return factors

        r = n % p

        if r == 0:

            factors.append(p)

            n = n // p


        elif p*p >= n:

            factors.append(n)


            return factors
        

        elif p > 2:

            p += 2

        else: 
            p += 1





#funzione per trovare tutti i numeri primi più piccoli di n
#che si basa sul fatto che un numero primo è fattorizzato da un solo elemento coincidente
#con se stesso


def numeri_primi(n):

    lista_numeri_primi = []

    for i in range(n):

        lista_check = factorize_naive(i)

        if len(lista_check) == 1 :

            lista_numeri_primi.append(i)

        else:
            pass

    array_primi = np.array(lista_numeri_primi)

    return {n : array_primi.sum()}



def genera_lista():

    nums = []

    #la consegna dice 2.500.000.000 ma ci mette una marea quindi mi limito a fare solo
    #una lista di 8 numeri
    for i in range(100000, 900000, 100000):

        nums.append(i)

    
    return nums


#funzione per farmi stampare tutti i numeri primi della lista
def dizionario_somma_numeri_primi(lista):

    
    for num in lista:

        print(numeri_primi(num))


#funzione per eseguire l' algoritmo in programmazione seriale

def algoritmo_seriale():
    
    dizionario_somma_numeri_primi(genera_lista())


#funzione per eseguire l' algoritmo in programmazione parallela
#usando i multiprocessi


def algoritmo_multiprocessi(num_processi):
    
    lista_processi = []
    lista_numeri = genera_lista()

    #creo unità di lavoro del processo basata su quanto è lunga la lista
    chunksize = int(math.ceil(len(genera_lista()) / float(num_processi)))
    

    for n in range(num_processi):

        sottolista = lista_numeri[chunksize * n : chunksize * (n + 1)]
        processo = mp.Process(target = dizionario_somma_numeri_primi, 
                              args = (sottolista, ))
        
        #nota che args è una tupla e ci vuole la virgola finale
        
        lista_processi.append(processo)
        processo.start()

    for processo_attivo in lista_processi:

        processo_attivo.join()


def algoritmo_threads(num_threads):

    lista_threads = []
    lista_numeri = genera_lista()
    

    chunksize = int(math.ceil(len(lista_numeri)/float(num_threads)))


    for n in range(num_threads):

        sottolista = lista_numeri[n*chunksize:chunksize*(n+1)]

        thread = threading.Thread(target = dizionario_somma_numeri_primi, args = (sottolista, ))

        lista_threads.append(thread)

        thread.start()

    for thread_attivo in lista_threads:

        thread_attivo.join()


# MAIN

if __name__ == "__main__":

    serial = Timer("\n usando la programmazione seriale: ")

    #per utlizzare il metodo __start__ e __end__ dell' oggetto
    #utilizzo la chiamata con with oggetto
    with serial as qq:
        algoritmo_seriale()

    parallelo_processi = Timer("\n usando la progrmmazione parallela con i processi: ")

    with parallelo_processi as qq:
        #faccio 1 numeor per ogni processo
        algoritmo_multiprocessi(8)


    parallelo_threads = Timer("\n usando la programmazione parallela con i threads: ")

    with parallelo_threads as qq:

        algoritmo_threads(8)


    






    
    
   
    



    








