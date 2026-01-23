import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class elettrone:
    carica = -1.6e-19
    massa = 0.511  # MeV/c^2
    spin = 1 / 2
    numero_leptonica = 1
    numero_barionico = 0


class muone:
    carica = -1.6e-19
    massa = 105.7  # MeV/c^2
    spin = 1 / 2
    numero_leptonico = 1
    numero_barionico = 0


class positrone:
    carica = +1.6e-19
    massa = 0.511  # MeV/c^2
    spin = 1 / 2
    numero_leptonico = -1
    numero_barionico = 0


scelta1 = int(input("La particella rivelata ha numero leptonico: "))
if scelta1 == +1:
    scelta_2 = int(input("La particella rivelata ha carica positiva o negativa? "))
    if scelta_2 == +1:
        print("La particella rivelata è un positrone")
