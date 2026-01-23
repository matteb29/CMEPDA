import os
import threading

# qui la concorrenza avviene tramite utilizzo di threading
# il modulo da importare non è più multiprocessing ma threading
# ricordiamo che i thread hanno limitazioni dovute al GIL che fa si che soltanto
# un thread alla volta può accedere al bytecode cioè al codice
# se non ci sono tempi morti(chiamate di numpy, time.sleep(), scritture su file, accedere a file etc)
# allora i thread nonn portano alcun vantaggio rispetto alla programmazione sequenziale


def task1():

    print("Task 1 assigned to thread: " + threading.current_thread().name)

    # siccome i thread vivono all' interno del solito processo quando scrivo
    # os.getpid() ottengo sempre i soliti ID, getpid = get process id
    print("ID of process running task 1: " + str(os.getpid()))


def task2():

    print("Task 2 assigned to thread: " + threading.current_thread().name)

    # threading.current_thread() è una funzione del modulo threading
    # return un oggetto della classe thread in particolare quello che sta rannando al momento
    # e per questo posso fare l' "attributo della funzione"

    print("ID of process running task 2: " + str(os.getpid()))


# MAIN


# questa parte di codice è eseguita dal main thread
if __name__ == "__main__":

    # print ID of current process
    print("ID of process running main program: " + str(os.getpid()))

    # print name of main thread

    print("Main thread name: " + threading.main_thread().name)

    # la funzione threading.main_thread() della libreria threading restituisce
    # il main thread cioè quel thread che ha iniziato l' esecuzione del programma,
    # t1 e t2 qui sono thread secondari detti "workers"

    # creating threads

    # qui definisco i thread aggiungendo il parametro (attributo) facoltativo
    # "name" così che riesco a specificare il thread con un nome. Avendolo definito
    # potrò poi usarlo come in threading.current_thread().name

    t1 = threading.Thread(target=task1, name="t1")
    t2 = threading.Thread(target=task2, name="t2")

    # starting threads
    t1.start()
    t2.start()
    # wait until all threads finish
    t1.join()
    t2.join()
