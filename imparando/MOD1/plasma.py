# simulazione di un plasma contenente particelle
# cariche elettroni e ioni, usando programmazione ad oggetti, ereditarietà e composizione
# ereditarietà mi dice che la classe elettrone e ione SONO un tipo specifico di classe particella
# composizione mi dice che la classe Plasma HA dentro di sè la classe elettrone e la classe ione

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class Particella:  # classe base, madre, da cui devono ereditare attributi e metodi
    # le classi figlie Elettrone e Ione

    def __init__(
        self, carica, massa, posizione, velocità
    ):  # attributi della classe madre
        self.carica = carica
        self.massa = massa
        self.posizione = np.array(posizione, dtype=float)
        self.velocità = np.array(velocità, dtype=float)

    def muovi(
        self, dt, campo_elettrico, campo_magnetico
    ):  # metodo per aggiornare la posizione
        # della particella in base alla forza di Lorentz
        # gli attributi del metodo non sono attributi della classe perchè campo elettrico e
        # campo magnetico sono quelli esterni
        self.campo_elettrico = np.array(campo_elettrico, dtype=float)
        self.campo_magnetico = np.array(campo_magnetico, dtype=float)
        self.dt = dt

        forza = np.array(
            self.carica * self.campo_elettrico
            + self.carica * np.cross(self.velocità, campo_magnetico)
        )  # forza di Lorentz in cui
        # prodotto vettoriale è calcolato con np.cross

        accelerazione = (
            forza / self.massa
        )  # quando chiamo un attributo della classe scrivo sempre il self con lui

        self.velocità = self.velocità + accelerazione * dt  # aggiorno la velocità
        self.posizione = self.posizione + self.velocità * dt  # aggiorno la posizione

        return f"La posizione della particella ora è {self.posizione}, la velocità è {self.velocità}"


class Elettrone(
    Particella
):  # classe figlia elettrone che eredita dalla classe madre attributi e metodi

    def __init__(
        self, posizione, velocità
    ):  # elettrone singolo avrà come attributo la posizione e la velocità
        # che lo distinguono dagli altri elettroni, come dire che una macchina ha l' attributo colore per distinguerla dalle altre

        self.velocità = velocità
        self.posizione = posizione

        super().__init__(
            carica=-1.6e-19, massa=0.511, posizione=posizione, velocità=velocità
        )
        # se specifico un attributo li devo specificare tutti,
        # per quelli non inizializzati con valori fissi scrivo posizione = posizione,
        # dove gli passo gli attributi della classe figlia, cioè sto dicendo che un elettrone è un oggetto
        # di carica tot, massa tot, posizione e velocità non fisse ma che variano da elettrone a elettrone


class Ione(
    Particella
):  # classe figlia dello ione che eredita dalla classe madre attributi e metodi

    def __init__(self, posizione, velocità):

        self.velocità = velocità
        self.posizione = posizione

        super().__init__(
            carica=1.6e-19, massa=938, posizione=posizione, velocità=velocità
        )


class Plasma(
    Particella
):  # classe che contiene un insieme di particelle, sia elettroni che ioni
    # avrà tramite composizione un metodo costruito con la classe elettrone o ione

    def __init__(
        self, num_particelle
    ):  # il plasma ha uno specifico numero di particelle: elettroni e ioni

        self.num_particelle = np.array((0, 0))

    def aggiungi_particella(
        self, tipo, num_elettroni, num_ioni
    ):  # metodo per aggiungere particelle al plasma
        # con attributo dato dal tipo di particella da aggiungere

        self.tipo = tipo
        self.num_elettroni = num_elettroni
        self.num_ioni = num_ioni

        if tipo == "elettrone":

            self.num_particelle[0] = self.num_particelle[0] + num_elettroni

            for i in range(num_elettroni):

                Particella.posizione = (
                    np.random.rand(2) * 100
                )  # posizione casuale in un quadrato 100x100

        elif tipo == "ione":

            self.num_particelle[1] = self.num_particelle[1] + num_ioni

            for i in range(num_ioni):

                Particella.posizione = (
                    np.random.rand(2) * 100
                )  # posizione casuale in un quadrato 100x100

    def evoluzione_temporale(self, dt, campo_elettrico, campo_magnetico):

        self.dt = dt
        self.campo_elettrico = campo_elettrico
        self.campo_magnetico = campo_megnetico

        for particella in self.num_particelle:

            particella.muovi(dt, campo_elettrico, campo_magnetico)

    def centro_di_massa(self):  # metodo per calcolare il centro di massa del plasma

        array_posizioni = (
            []
        )  # array che contiene la posizione di tutte le particelle nel plasma

        numeratore = 0
        denominatore = 0

        for particella in self.num_particelle:

            particella.posizione = (
                np.random.rand(2) * 100
            )  # posizione casuale in un quadrato 100x100
            array_posizioni.append(
                particella.posizione
            )  # costruisco l' array delle posizioni

            if particella.tipo == "elettrone":
                particella.massa = elettrone.massa

            elif particella.tipo == "ione":
                particella.massa = ione.massa

            numeratore = numeratore + particella.massa * particella.posizione
            denominatore = denominatore + particella.massa

        centro_massa = numeratore / denominatore

        return print(f"Il centro di massa della particella è {centro_massa}")


mio_plasma = Plasma(0)
mio_plasma.aggiungi_particella("elettrone", 10, 5)
mio_plasma.centro_di_massa()
