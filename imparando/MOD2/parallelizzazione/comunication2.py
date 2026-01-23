import multiprocessing


def square_list(mylist, result, square_sum):

    for idx, num in enumerate(
        mylist
    ):  # enumerate prende una lista e la trasforma in una
        # serie numerata cioè crea anche la lista degli indici associata alla lista che
        # passi a enumerate

        result[idx] = num * num

    # square_sum value dove questa variabile square_sum è una istanza della classe
    # multiprocessing.Value
    square_sum.value = sum(result)

    # print result Array
    print(
        "Result(in process p1): " + str(result[:])
    )  # lo slice : serve per farti restituire
    # gli elementi come una lista, in questo caso te li ranna tutti
    # result[:] ti fa creare una copia

    # print square_sum Value
    print(f"Sum of squares(in process p1): {square_sum.value}")


if __name__ == "__main__":
    # input list
    mylist = [1, 2, 3, 4]

    # creating Array of int data type with space for 4 integers
    result = multiprocessing.Array("i", 4)
    # in questa riga ho creato una variabile array di 4 elementi interi

    # la libraria multiprocessing possiede anche l' oggetto Array, Value oltre
    # al già incontrato Process

    # creating Value of int data type
    square_sum = multiprocessing.Value("i")  # qui sto creando una variabile
    # condivisa dai processi di tipo intero

    # esiste una classe chiamata multiprocessing.Value che ha come attributo value
    # per questo utilizzo square_sum.valore()

    # creating new process
    p1 = multiprocessing.Process(target=square_list, args=(mylist, result, square_sum))
    # ricordarsi di esplicitare gli argomenti della funzione mylist, result, square_sum come args

    # starting process
    p1.start()
    # wait until process is finished
    p1.join()

    # print result array
    print("Result(in main program): " + str(result[:]))
    # print square_sum Value
    print("Sum of squares(in main program): " + str(square_sum.value))

    # qui il main program restituisce il solito risultato del processo
    # poichè prima in comunication1.py avevo una variabile globale mentre qui result
    # e square_sum non vengono mai copiati
