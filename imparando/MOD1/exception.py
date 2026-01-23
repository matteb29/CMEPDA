import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# domanda 10: uso di except in confronto a codici di errore
# come primo svantaggio ci può essere il fatto che il codice diventa più lento e quindi
# non bisogna abusarne


try:  # si usa per azioni che possiedono casi speciali che mi possono restituire un errore

    y = int(input("Inserisci un numero: "))
    x = 1 / y

    print(x)

except (
    ZeroDivisionError
):  # questo except mi dice che se provo a dividere per 0 ho un errore
    # tiene conto dei casi di errori all' interno delle possibilità del mio try
    # anche se non lo mettessi e provassi a fare la divisione per 0 otterrei il solito messaggio di errore,
    # tuttavia in un codice più complesso e lungo questo può essere una possibile spia visto che conosco il posto in cui succede
    # l' errore

    print(
        "Non puoi dividere per 0"
    )  # questo è il messaggio di errore da asssociare all' except


try:  # adesso uso il try perchè voglio aprire file ma esiste il caso patologico
    # in cui il file che sto cercando di aprire non è nella cartella in cui sto cercando,
    # il try tiene conto del fatto che la mia azione può avere un caso patologico

    mio_file = input("Inserisci un file che vuoi aprire: ")
    f = open(mio_file)  # salvo la mia apertura del file in una variabile

except (
    FileNotFoundError
):  # questo è il tipo di errore (FileNotFoundError è una parola speciale)
    # che si usa quando non si trova il file che è anche il solito error che restituirebbe il programma
    # se non usassi except: il famoso codice di errore

    print(
        "Il file che vuoi aprire non è stato trovato"
    )  # messaggio di errore da inviare all' interfaccia


finally:  # serve a dire di eseguire sempre questo pezzo di codice a prescindere che ci sia
    # stato un errore oppure no

    print("Saluti!")

try:

    f.close()

except NameError:  # anche questo è un except per gestire il caso in cui
    # non esiste un file con il nome f e quindi non può fare f.close perchè il
    # mio file non è stato aperto

    pass

try:

    z = int(input("Inserisci: "))
    w = 1 / z
    print(w)

except Exception as errore:  # questo uso di except con Exception mi
    # restituisce in automatico l' errore che ho fatto però tieni conto che ogni funzione che io applico
    # ha una parola speciale associata ai casi patologici quindi se voglio fare a meno di questo
    # Exception devo conoscere tutti i casi di errore che la funzione può dare, SVANTAGGIO

    # inoltre usare except Exception catturi tutti i tipi di errore, anche quelli che non ti aspetti

    print(f"L' errore  è stato: {errore}")


def divisione(a):
    if a == 0:
        return (
            -1
        )  # qui -1 è un error code che ci metto io per segnalare un caso speciale
    # ma può essere solo un numero a differenza delle exception che sono dei casi speciali

    elif a != 0:
        return 1 / x


print(divisione(0))
