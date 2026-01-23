import multiprocessing

# qui studiamo le sincronizzazioni: strumenti necesssari per ovviare le race condition
# su zone critiche del codice

# qui osserviamo che sia la funzione withdraw che quella deposit hanno accesso
# alla solita variabile balance.value


def withdraw(balance):

    for x in range(10000):
        balance.value = balance.value - 1


def deposit(balance):

    for x in range(10000):

        balance.value = balance.value + 1


def perform_transactions():

    # initial balance (in shared memory con 100)
    balance = multiprocessing.Value("i", 100)

    # qui definisco balance: nel processo padre
    # e quindi sia p1 che p2 processi figli possono accedervi = race condition
    # infatti osservo nelle 10 volte della chiamata della funzione perform_transaction()
    # 10 valori diversi

    # creating new processes
    p1 = multiprocessing.Process(target=withdraw, args=(balance,))
    p2 = multiprocessing.Process(target=deposit, args=(balance,))

    # starting processes
    p1.start()
    p2.start()
    # wait until processes are finished
    p1.join()
    p2.join()
    # print final balance
    print("Final balance = {}".format(balance.value))


# MAIN
if __name__ == "__main__":

    for x in range(10):
        # perform same transaction process 10 times
        perform_transactions()
