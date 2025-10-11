import multiprocessing 
from multiprocessing import Process #cosi posso scrivere p1 = Process(target= ....)

# empty list with global scope 
result = [] 

def square_list(mylist): 
        global result  
        for num in mylist: 
                result.append(num * num) 
        print("Result(in process p1): "+str(result)) 
 
#MAIN
if __name__ == "__main__":
    # input list 
    mylist = [1,2,3,4] 
    # creating new process: PROCESSO FIGLIO
    p1 = multiprocessing.Process(target=square_list, args=(mylist,)) 
    #avrei potuto anche scrivere p1 = Process(target = funzione, args = (argomento della funzione))


    # starting process 
    p1.start() 
    # wait until process is finished 
    p1.join() 
        
    # print global result list 
    print("Result(in main program): "+str(result)) 

    #questa ultima riga serve per farci vedere che quando io 
    #creo un processo tramite p1 = multiprocessing.Process il sistema operativo
    #crea una memoria indipendente da fornire a p1 processo figlio, in essa è contenuta una copia 
    #della variabile globale result da assegnare al processo principale.
    #L' output dell' ultima riga ci mostra come le modifiche compiute su result da parte del processo 
    # p1 non toccano la variabile globale ma modificano solo la copia che sta in p1 


        
