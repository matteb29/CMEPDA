# usiamo un mutex in python per creare un algoritmo thread-safe che
# incrementi una variabile globale


import threading

lock = threading.Lock()


counter = 0


def incrementa_counter():
    global counter  # global serve per far utilizzare la solita variabile a
    # tutti i thread

    for i in range(5000):  # ogni thread incrementa di 5000
        with (
            lock
        ):  # nota che python implementa il GIL quindi funziona anche senza usare il lock
            # cioè senza creare un mutex, posso far passare il GIL ad un altro thread
            # tramite la chiamata time.sleep()
            counter += 1


# adesso devo creare 2 thread:

thread1 = threading.Thread(target=incrementa_counter, name="Thread 1")
thread2 = threading.Thread(target=incrementa_counter, name="Thread 2")


# poi li devo avviare con.start

thread1.start()
thread2.start()

# poi devo dire al programma principale di aspettare che finisca il thread1 e il thread2
# cioè non posso eseguire il thread principale print(counter) prima che i due abbiano finito

thread1.join()
thread2.join()


print(counter)
