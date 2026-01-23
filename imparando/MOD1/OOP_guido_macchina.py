import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class Car:  # definisco inizializzazione della Classe Car

    modello = "Tesla"  # modello è un attributo di classe uguale per tutti gli oggetti della classe car

    def __init__(
        self, velocità=0, accensione=0
    ):  # che possiede un attributo velocità, usando i metodi questo attributo
        # caratterizzerà la classe car
        # nota che gli attributi chiamati in __init__ sono attributi d istanza/oggetto

        self.__velocità = (
            velocità  # attributo privato, non accessibile dall' esterno della classe
        )
        # così evito che qualcuno modifichi direttamente la velocità della macchina

    @property  # decoratore che trasforma il metodo velocità in un attributo di sola lettura
    def velocità(
        self,
    ):  # metodo velocità che restituisce il valore dell' attributo privato __velocità
        return self.__velocità

    def accelera(self, deltaV):  # metodo accelera che prende come parametro deltaV

        self.deltaV = deltaV
        self.__velocità = (
            self.__velocità + self.deltaV
        )  # aggiorno la velocità della macchina

        if self.deltaV > 0:
            print(f"La macchina accelera di {self.deltaV} km/h")

        elif self.deltaV < 0:
            print(f"La macchina frena di {self.deltaV} km/h")

        return self.__velocità

    def accensione(self, stato=0):

        self.__stato = stato  # avendo messo self.stato, lo stato diventa un attributo della classe car
        # piuttosto che un parametro del metodo accensione

        if self.__stato == 0:

            scelta = input(("La macchina è spenta, vuoi accendere il quadro? "))
            if scelta == "si":
                self.stato = 1
                scelta_2 = input("Vuoi avviare il motore? ")
                if scelta_2 == "si":
                    self.stato = 2
                    print("Macchina accesa, buon viaggio")

        if self.__stato == 1:
            scelta = input(("Il quadro è acceso, vuoi avviare il motore? "))
            if scelta == "si":
                self.stato = 2
                print("Macchina accesa, buon viaggio")

            elif scelta == "no":
                scelta_2 = input(("Vuoi spegnere l' auto? "))
                if scelta_2 == "si":
                    self.stato = 0
                    print("Macchina spenta, saluti")


mia_macchina = Car()

mia_macchina.accensione(0)
mia_macchina.accelera(20)
mia_macchina.accelera(30)
mia_macchina.velocità = 100000  # qui mi dà AttributeError perchè velocità è un
# attributo di sola lettura
mia_macchina.accelera(-10)


print(f"La velocità della macchina è {mia_macchina.velocità} km/h")
