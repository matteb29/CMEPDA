import multiprocessing as mp
import time


# define a example function
def Hello(pos,name, output):
    msg = "Hello "+name

    #inserisco nella coda la tupla di variabili (pos, msg) 
    output.put((pos, msg))

if __name__== "__main__":
    # Define an output queue

    #crea una coda condivisa tra i porcessi (condivisa =  tutti i processi possono
    # accedervi), tramite la quale posso
    #scambiare informazioni tra i processi
    output = mp.Queue()

    # Setup a list of processes that we want to run
    processes = [mp.Process(target=Hello, args=(x, "Gianluca", output)) for x in range(4)]

    # Run processes
    for p in processes:
        #qui ho aggiunto una time.sleep per farmeli stampare in ordine
        #altrimenti li stampa istantanemente 
        time.sleep(0.1)
        p.start()


    # Exit the completed processes
    for p in processes:
        p.join()
            
    # Get process results from the output queue
    #mi faccio restituisce in ordine di inserimento le variabili che ho inserito
    #nella cosa usando output.put(variabile1, variabile2)
    results = [output.get() for p in processes]
            
    print(results)