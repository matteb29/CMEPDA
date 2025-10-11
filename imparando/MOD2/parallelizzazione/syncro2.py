import multiprocessing



#qui ovviamo il problema delle race condition su 
#regioni critiche del codice andando a lavorare con il lock
#il programma ha la solita funzionalità di "syncro1.py"
#attenzione che il lock non ti garantisce l' ordine con cui i 2 processi accedono
#piuttosto fa si che non si perdano delle azioni a causa dei due processi che 
#accedono contemporaneamente (esiste un tempo finito tra la modifica e il salvataggio
#se dopo che faccio un' azione, prima di salvarla un' altra azione entra dentro la variabile
#allora salvo la variabile modificata dalla seconda azione, scordandomi dell' azione prima)



# function to withdraw from account
def withdraw(balance, lock):
    
   
 
    for x in range(10000):
        lock.acquire()
        balance.value = balance.value - 1
        lock.release()





# function to deposit to account
def deposit(balance, lock):


    for x in range(10000):

        lock.acquire()
        balance.value = balance.value + 1
        lock.release()

def perform_transactions():


 # initial balance (in shared memory) cioè creo una variabile condivisa di tipo intero 
 #inizializzata a 100

    balance = multiprocessing.Value('i', 100)



 # creating a lock object che avrà come metodi
 #acquire() e release()

    lock = multiprocessing.Lock()
 
 
 # creating new processes

    p1 = multiprocessing.Process(target=withdraw, args=(balance,lock))
    p2 = multiprocessing.Process(target=deposit, args=(balance,lock))


 # starting processes
    p1.start()
    p2.start()


 # wait until processes are finished
    p1.join()
    p2.join()


 # print final balance
    print("Final balance = "+str(balance.value))


#MAIN

if __name__ == "__main__":


    for x in range(10):
    # perform same transaction process 10 times
        perform_transactions()