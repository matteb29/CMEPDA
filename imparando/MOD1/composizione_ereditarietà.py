import matplotlib.pyplot as plt
import numpy as np


class Particle:  # classe madre delle particelle che ha attributi da far ereditare alle altre classi
    def __init__(self, carica=0, massa=0, spin=0.5, impulso=[0, 0, 0]):
        self.carica = carica
        self.massa = massa
        self.spin = spin
        self.impulso = impulso

    def coniugazione_carica(
        self,
    ):  # questo è un metodo della classe delle particelle che posso applicare a tutte le classi figlie
        self.carica = -self.carica
        return self.carica


class Elettrone(
    Particle
):  # classe figlia che eredita dalla classe madre Particle gli attributi massa, carica e spin
    def __init__(self, impulso):
        super().__init__(
            carica=-1.6e-19, massa=0.511, spin=0.5, impulso=impulso
        )  # richiama il costruttore della classe madre per stabilire
        # gli attributi che non cambiano della classe elettrone

    def collisione(
        self, deltap
    ):  # metodo specifico della classe elettrone, perchè studio solo scattering di elettroni
        self.impulso = self.impulso + np.array(deltap)
        energia = np.sqrt(np.sum(self.impulso**2) + self.massa**2)
        print(f"L'elettrone ha subito una collisione. Nuovo impulso: {self.impulso}")
        print(f"L'energia dell'elettrone è {energia:.3f} MeV")


class Muone(Particle):
    def __init__(self, impulso):
        super().__init__(carica=-1.6e-19, massa=105.7, spin=0.5, impulso=impulso)

    def collisione(self, deltap):
        self.impulso = self.impulso + np.array(deltap)
        print(f"Il muone ha subito una collisione. Nuovo impulso: {self.impulso}")


# Creo un elettrone con impulso iniziale di 7000 MeV/c
elettrone_LHC = Elettrone([0, 0, 7000])  # impulso in MeV/c
elettrone_LHC.collisione([0, 0, -500])  # collisione che riduce l'impulso

print(
    f"L'elettrone ha carica {elettrone_LHC.carica}, massa {elettrone_LHC.massa} MeV/c^2"
)
