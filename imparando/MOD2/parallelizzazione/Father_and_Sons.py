from multiprocessing import Process

#il modulo os serve per interagire con il sistema operativo
#posso anche cambiare il nome di  un file usando os.rename()

import os


def f0(name):
    print()
    print("-----> function "+name)
    print ("I am still the main process with ID "
           +str(os.getpid())+" my father is ID:"+str(os.getppid()))


#os.getpid() è una funzione del modulo os, serve per farsi dare dal sistema operativo l' ID 
#del processo in esecuzione. L' ID del processo è un numero che il sistema operativo fornisce 
# ad un processo in esecuzione

#L’ID del processo è un’etichetta numerica unica che identifica un programma in esecuzione.



#os.getppid() ti restituisce l' ID del processo padre
#qui il processo padre è l' istanza di tutto il programma

def f1(name):
    print()
    print("-----> function "+name)
    print ("I am the first sub-process with ID "
           +str(os.getpid())+" my father is ID:"+str(os.getppid()))
    
    #siccome f2 e f1 sono una dentro l' altra allora
    #siccome le lancio con il solito processo p avranno soliti ID per processo figlio e
    #per processo padre

    f2('two')


def f2(name):
    print()
    print("-----> function "+name)
    print ("I am still the first sub-process with ID "
           +str(os.getpid())+" my father is ID:"+str(os.getppid()))
    print("This is the end!")

#MAIN
if __name__ == "__main__":
    print ("I am the main process with ID: "+str(os.getpid()))

    #nota che il programma principale ha anche esso un programma padre
    #che sarebbe il processo che ha fatto lanciare l' interprete python,
    #infatti ripetendo l' esecuzione del programma più volte
    #ottengo sempre il solito numero di ID: 62742
    #bash -> father -> son

    print(f"\n my father is: {os.getppid()}")

    #siccome la f0 non è eseguita usando un processo, come per esempio la f1 dove
    #scrivo la riga di codice p = Process(target = f1, args=("one",))
    f0('zero')

    #questo è il processo figlio cioè l' esecuzione della
    #funzione f1 con argomento "one"
    p = Process(target=f1, args=('one',))

    

    p.start()
    p.join()
