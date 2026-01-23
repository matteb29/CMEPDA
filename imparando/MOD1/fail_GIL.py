import threading
import time

lock = threading.Lock()
counter = 0


def increment_counter():
    global counter
    for i in range(100000):
        with (
            lock
        ):  # Fa in modo che il thread 1 finisca prima che il thread 2 possa cominciare
            # Simula una race condition forzando il cambio di contesto
            temp = counter
            time.sleep(0.0000001)  # Forza il cambio di thread
            counter = temp + 1


t1 = threading.Thread(target=increment_counter)
t2 = threading.Thread(target=increment_counter)

t1.start()
t2.start()
t1.join()
t2.join()

print(f"Risultato: {counter} (atteso: 2000000)")
# ❌ Probabilmente NON sarà 2000000!
