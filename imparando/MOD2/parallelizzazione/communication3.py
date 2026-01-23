import multiprocessing


def add_element(record, records):
    records.append(record)
    print("New element added to records list")


def sum_elements(records):
    summ = sum(records)
    print("New sum is: " + str(summ))


# MAIN

# with serve per creare qualcosa che si chiuderà automaticamente terminato questo blocco di
# codice perchè questo "Manager" ha bisogno di essere aperto e chiuso


if __name__ == "__main__":

    with multiprocessing.Manager() as manager:

        list_elements = [
            1,
            2,
            3,
            4,
        ]  # c' è una variabile globale che si chiama list_elements

        records = manager.list(
            list_elements
        )  # serve per creare una variabile di tipo lista
        # che sia condivisa tra i processi dove qui serve manager perchè è l' unico
        # che puo creare una lista, può anche creare dizionari
        # il modulo manager di multiprocessing fornisce un porcesso detto Server Process che
        # permette ai processi figli di accedere alle liste condivise

        # manager.list() è un oggetto proxy (simile ai puntatori in python)

        # list_elements  quindi è diventata una lista condivisa che si chiama records
        # VARIABILE CONDIVISA: Tutti i processi leggono e scrivono sullo stesso oggetto,
        # non su copie separate.

        new_element = 5

        print("Old sum is: " + str(sum(list_elements)))

        # creating new processes

        p1 = multiprocessing.Process(target=add_element, args=(new_element, records))
        p2 = multiprocessing.Process(target=sum_elements, args=(records,))

        # running process p1 to insert new element
        p1.start()
        p1.join()

        # running process p2 to sum list elements
        p2.start()
        p2.join()
