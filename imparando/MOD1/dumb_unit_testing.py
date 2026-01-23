import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def quadrato(x):
    return x * x


def test():  # definisco una funzione test per verificare che la funzione
    # quadrato funzioni effettivamente

    assert quadrato(2.0) == 4
    print("OK! la funzione quadrato funziona")


if __name__ == "__main__":  # questa riga di codice serve per non far eseguire
    # il test quando un giorno dovessi importare il suddetto programma: unit_testing.py
    # in un altro programma

    test()

    # addizionalmente posso scriverci:

    print(quadrato(3))
