import multiprocessing 

def square_list(mylist, q): 
    # append squares of mylist to queue 
    for num in mylist: 

        q.put(num * num)  #put è un metodo della coda per 
        #inserire un elemento nella coda

def print_queue(q): 
    print("Queue elements:") 

    while not q.empty():  #q.empty() usa il modulo empty della coda 
        #variabile booleana per dire se la coda è vuota o meno
        #sono tutti metodi dell' oggetto coda

        print(q.get()) 
        #qua tu estrai un valore una volta con l' ordine con cui
        #sono stati inseriti

    print("Queue is now empty!") 

#MAIN
if __name__ == "__main__":
    # input list 
    mylist = [1,2,3,4] 

    # creating multiprocessing Queue 
    q = multiprocessing.Queue() 
    #q è una variabile condivisa di tipo coda
    #il tipo coda è una variabile FIFO cioè first IN first OUT
    #è preferibile alla lista perchè mi permette di gestire i dati in ordine di arrivo 
    #migliorando la comunicazione tra processi poichè se due processi vogliono scrivere sulla lista
    #nello stesso momento allora queue assicura che solo una alla volta scriva dando il permesso di 
    #scrittura un processo alla volta



   
    
    # creating new processes 
    p1 = multiprocessing.Process(target=square_list, args=(mylist, q)) 
    p2 = multiprocessing.Process(target=print_queue, args=(q,)) 

    #q è una variabile condivisa e non privata del processo 
    #perchè la variabile q che p2 usa è quella restituita dal processo 1 e modificata 
    #con l' inserimento di quadrati di mylist
    
    # running process p1 to square list 
    p1.start() 
    p1.join() 

    # running process p2 to get queue elements 
    p2.start() 
    p2.join() 
