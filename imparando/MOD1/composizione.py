import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class Motore:  # chiamo la classe motore

    def __init__(self, cavalli):  # che ha un attributo cavalli

        self.cavalli = cavalli

    def accensione(self):  # che ha un metodo accensione
        return print("Motore acceso")


class Ruota:  # definisco la classe ruota

    def __init__(self, diametro):
        self.diametro = diametro

    def gonfia(self, pressione):

        return f"Ruota gonfiata a {pressione} bar"


class Car:

    def __init__(self):  # definisco il costruttore della classe car
        # tramite la composizione, la classe car possiede come attributo
        # un oggetto della classe motore con 150 cavalli

        self.motore = Motore(150)
        self.ruote = Ruota(40)

    def avvia(self):  # metodo avvia della classe car che richiama il metodo accensione
        # della classe motore
        self.motore.accensione()  # self.motore.accensione() è come dire motore.accensione()
        return print("Macchina avviata")

    def gonfia_ruote(self):  # metodo gonfia_ruote della classe car
        # che usa il metodo della classse ruota (gonfia) attraverso la composizione

        self.ruote.gonfia(2.2)
        return print("Ruote gonfiate")


mia_macchina = Car()  # creo un oggetto di tipo car che tramite composizione avrà un
# attributo motore che è un oggetto della classe motore

mia_macchina.avvia()
mia_macchina.gonfia_ruote()
