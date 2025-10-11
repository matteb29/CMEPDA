import threading 
import time

# global variable x 
x = 0


#ricorda che con thread il GIL blocca le race condition
#a meno che non usi delle scorciatoie per farlo rilasciare
#tipo facendo uso di time.sleep()
#occhio però che il GIL non sempre protegge come nel caso di cicli più complessi 
#infatti ogni 100bytecode lo rilascia



def increment(): 

    #questo serve per dire che la variabile x che usa 
    #non è una locale della funzione ma quella globale definita sopra
   

    global x 

    x += 1




def thread_task(): 

   
    #se qui mettessi global x, x = 0 
    #allora ogni volta che parte un thread avrei la inizializzazione a 0,
    #cancellando il lavoro del thread precedente, quindi avrei una corruzione del dato
    #dovuta all' accesso alla solita variabile globale global x 



    for _ in range(100000): 
        increment() 


def main_task(): 

    global x 

    # setting global variable x as 0 
    # resetto a 0 perchè poi ci farò un ciclo for sopra e quindi voglio ripetere il programma 
    # 10 volte

    x = 0

    #se togliessi x = 0 avrei che sommo ad ogni 


    # creating threads secondari che agiscono entrmabi sulla solita funzione thread_task
    t1 = threading.Thread(target=thread_task) 
    t2 = threading.Thread(target=thread_task) 
    
    # start threads 
    t1.start() 
    t2.start() 
    # wait until threads finish their job 
    t1.join() 
    t2.join() 



#MAIN che verrà eseguito dal main thread

for i in range(10): 

    main_task() 

    print("Iteration {0}: x = {1}".format(i,x)) 

