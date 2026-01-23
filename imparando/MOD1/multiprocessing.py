# qui divido un programma in due processi figli utilizzando il
# multiprocessing, questo mi permetterebbe di applicare il vero parallelismo
# ricordiamo che un processo è una istanza di un programma e quindi il sistema operativo
# per ogni programma assegna risorse (CPU, MEMORIA ETC) quindi ogni processo ha il suo GIL.
# Poichè in python il GIL blocca l' esecuzione di più thread non sarebbe possibile il parallelismo
# allora avere più processi riesce ad aggirare il problema del GIL


import os
from multiprocessing import Process


def task_a():
    count = 0
    for i in range(100):
        count += 1
    print(count)


def task_b():
    count = 0
    for i in range(60):
        count += 1
    print(count)


if __name__ == "__main__":
    p1 = Process(target=task_a)
    p2 = Process(target=task_b)
    p1.start()
    p2.start()
    p1.join()
    p2.join()
