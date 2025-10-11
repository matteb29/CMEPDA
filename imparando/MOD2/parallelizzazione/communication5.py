import multiprocessing 
import time


#qui si utilizza una PIPE: cioè un meccanismo 
#di comunicazione tra 2 processi, quello che un processo manda con il send() 
# l' altro lo riceve con il recv() questo meccanismo fa parte di IPC (inter-process-comunication)

def sender(conn, msgs): 
    for msg in msgs:

        time.sleep(1) 

        conn.send(msg) 
        print("Sent the message: "+str(msg)) 

    conn.close() 
    #Una Connection usa risorse del sistema operativo
    #quindi è buona pratica chiuderla per poter renderle disponibili ad altro

def receiver(conn): 

    time.sleep(2)
    #serve pe rcoordinare i tempi di invio e ricezione 



    while 1:  #serve per creare un ciclo infinito
        #che si interromperà quando riceverò un END 
        #questo è perchè non avendo ancora ricevuto il messaggio non posso
        #scrivere condizioni su di esso del tipo while msg != "END"
        #sono costretto a farlo partire con un ciclo infinito
        msg = conn.recv() 

        if msg == "END": 
            break
        
        print("Received the message: " +str(msg)) 

#MAIN
if __name__== "__main__":

    # messages to be sent in forma di lista
    msgs = ["hello,", "how", "are you?", "END"] 


    # creating a pipe usando la libreria multiprocessing,
    #uso la connessione padre che invia il messaggio
    #uso la connessione figlia che riceve il messaggio

    parent_conn, child_conn = multiprocessing.Pipe() 

    #esse sono entrambe istanze della classe Connection che è una classe 
    #di multiprocessing
    #Pipe è una funzione del modulo multiprocessing, che ritorna due oggetti Connection
    #che possono comunicare tra di loro


    
    # creating new processes 
    p1 = multiprocessing.Process(target=sender, args=(parent_conn,msgs)) 
    p2 = multiprocessing.Process(target=receiver, args=(child_conn,)) 
    
    # running processes 
    p1.start() 
    p2.start() 

    # wait until processes finish 
    p1.join() 
    p2.join() 



#la creazione delle connection avviene come :
#def Pipe(duplex=True):
    #'''
    #Returns pair of connection objects at either end of a pipe
    #'''
    #from multiprocessing.connection import Pipe
    #return Pipe(duplex)


#multiprocessing.connection contiene pipe

#def Pipe(duplex=True):
    #if duplex:
        # crea una pipe bidirezionale (entrambi gli estremi possono send/recv)
        #s1, s2 = socket.socketpair()
    #else:
        # crea una pipe unidirezionale (uno scrive, l’altro legge)
       # s1, s2 = socket.socketpair()
        #s1 = _read_only(s1)
        #s2 = _write_only(s2)

    #c1 = Connection(s1)
    #c2 = Connection(s2)
    #return c1, c2
