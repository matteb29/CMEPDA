import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class Car:

    def __init__(self, colore, marca, modello, anno):
        # attributi sono: colore, marca, modello, anno
        # ingredienti

        self.colore = colore
        self.marca = marca
        self.modello = modello
        self.anno = anno

    # metodi andranno a caratterizzare gli attributi della classe
    # regole, ricetta che dice come fare una classe specfica con gli attributi dati

    def colore(self):  # metodo colore aplicato alla classe car
        return print(f"Il colore dell' auto è {self.colore}")

    def marca(self):
        return print(f"La marca dell' auto è {self.marco}")

    def modello(self):
        return print(f"Il modello dell' auto è {self.modello}")

    def anno(self):
        return print(f"L' anno dell' auto è {self.anno}")

    def descrizione(self):
        return print(
            f"La mia macchina è di colore {self.colore}, è del gruppo {self.marca}, il modello è {self.modello} ed è dell' anno {self.anno}"
        )

    def verniciatura(self, nuovo_colore):
        self.colore = nuovo_colore
        print(f"La macchina è stata verniciata di {self.colore}")


# creo due oggetti della classe Car

mia_macchina = Car("rosso", "kia", "soul", "2014")
macchina_giovanni = Car("blu scuro", "Volkswagen", "Passat", "1997")
print(
    f"La mia macchina è di colore {mia_macchina.colore}, è del gruppo {mia_macchina.marca}, il modello è {mia_macchina.modello} ed è dell' anno {mia_macchina.anno}"
)
print(
    f"La macchina di Giovanni è di colore {macchina_giovanni.colore}, è del gruppo {macchina_giovanni.marca}, è una {macchina_giovanni.modello}, ed è del {macchina_giovanni.anno}"
)


# mia_macchina.colore() applico il metodo colore alla mia macchina
