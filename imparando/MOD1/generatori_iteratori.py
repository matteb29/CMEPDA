import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

"L' iteratore è una classe"


class IteratoreCiao:
    def __init__(self, numero_volte):
        # Qui salvo lo "stato" iniziale
        self.massimo = numero_volte
        self.contatore = 0

    def __iter__(self):
        # 1. OBBLIGATORIO: Restituisco me stesso come iteratore
        # È come se l'oggetto dicesse: "Il segnalibro sono io!"
        return self

    def __next__(self):
        # 2. OBBLIGATORIO: La logica del "prossimo passo"
        if self.contatore < self.massimo:
            self.contatore += 1
            return "Ciao"  # Restituisco il valore
        else:
            # 3. FONDAMENTALE: Se ho finito, devo lanciare l'errore
            raise StopIteration


# --- PROVIAMOLO ---

# 1. Creo l'istanza (Ho comprato il libro)
mio_iter = IteratoreCiao(3)

# 2. Lo uso in un ciclo for (Python chiama __iter__ e poi __next__ da solo)
print("--- Uso col FOR ---")
for parola in mio_iter:
    print(parola)

# 3. Oppure lo uso a mano
print("\n--- Uso a mano ---")
manuale = IteratoreCiao(2)
print(next(manuale))  # Ciao
print(next(manuale))  # Ciao
# print(next(manuale)) # Qui esploderebbe con StopIteration


"----------------------------------------------------------------------"


# generatore è un tipo particolare di iteratore

# sia generatori che iteratori ti permettono di scorrere una sequenza.
# L' iteratore ha la proprietà di saperti dare il valore successivo nella sequenza usando
# la funzione next e sa anche quando fermarsi usando la funzione StopIteration
# dovendo tenere tutto in memoria se la lista fosse lunga sprecherei un sacco di memoria

# i generatori invece fanno la solita cosa ma sono in grado di salvare un elemento alla
# volta, cioè non legge da una lista già pronta ma li genera mano a mano


quadrati = [x**2 for x in range(10)]  # qui ho una lista già pronta


for (
    i
) in (
    quadrati
):  # in questo caso l' iteratore scorre la lista già pronta salvato in memoria e
    # stampa uno ad uno i valori, più veloce però ho rischio che se la lista
    # è troppo lunga il vantaggio non c'è più
    print(i)

print("\n\n\n")


def quadratis(n):  # qui possiamo vedere un uso di un generatore
    # usando lo yield il ciclo si blocca ogni volta che incontra la parola "yield" e passa
    # il valore al ciclo for sottostante per farlo stampare

    for c in range(n):  # questo ciclo for genera i quadrati da 0 a n,
        # ma lo fa in modo particolare, interrompendosi ogni volta che incontra yield per poter
        # passare il valore generato alla funzione

        yield c**2  # quando arriva qui il ciclo "for c in range(n)"":
        # si blocca per passare il valore di c**2 (che lui stesso ritorna) al ciclo "for q in
        # quadratis(10)"" così che quest' ultimo può stamparlo


for q in quadratis(10):  # il ciclo for q in quadratis(10) che vuole stampare 10 numeri
    # non legge da una lista già pronta ma comunica con il ciclo della funzione quadratis che contenendo
    # lo yield si blocca ogni volta che restituisce un c
    print(q)


print("\n\n\n")


# un un programma simile ma con ciclo che usa un iteratore sarebbe...


lista = []


def iteratore(n):
    for i in range(n):
        lista.append(i * i)

    return lista  # qui non sto usando lo yield quindi l' esecuzione cambia... sto facendo un


# iteratore  e non un generatore

for q in iteratore(
    10
):  # quando io chiamo la funzione iteratore(10) in questo ciclo for
    # quello che succede, non avendo messo lo yield è che lui ora
    # esegue per intero da 1 a n il ciclo for i in range(n) lista.append(i)
    # andando a creare una lista di 10 elementi
    # solo dopo aver creato qiesta lista allora il ciclo for q in iteratore(10)
    # potrà partire e stampare i valori della lista
    print(q)
