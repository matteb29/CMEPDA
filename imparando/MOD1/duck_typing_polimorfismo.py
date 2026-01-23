import numpy as np


class Cane:  # definisco classe cane
    # deve avere un metodo che sarà uguale anche per le altre classi
    # così da poter usare il polimorfismo

    def verso(self):
        return "bau bau"

    def caga(self):  # metodo specifico della classe cane
        # non succede nulla tuttavia se lo chiamo in fai_rumore
        # perchè fai rumore usa solo il metodo verso
        return print("il cane ha cagato")


class Gatto:

    # definisco classe gatto che anche lei ha un metodo verso
    # così da poter usare il polimorfismo

    def verso(self):
        return "miao miao"


class Mucca:

    # anche qui definisco la classe mucca con un metodo verso

    def verso(self):
        return "muu muu"


class Serpente:  # se uso la classe serpente senza metodo verso lui mi dà errore
    # perchè quando lo chiamo in fai rumore cerca il metodo verso che non esiste

    pass


class Robot:  # il potere del polimorfismo sta nel poter usare la funzione
    # fai_verso anche con una classe che per natura non c' entra un cazzo con gli animali
    # come ad esempio la classe robot purchè abbia il metodo giusto

    def verso(self):
        return "bi bu bo"


def fai_rumore(
    animale,
):  # come paramaetro alla funzione fai_rumore devo dargli un animale

    print(animale.verso())  # qui uso il polimorfismo, basato sul fatto che
    # tutte le classi hanno un metodo verso
    # animale.verso ritorna il verso dell' animale, quindi se metto print lo printa lui


fattoria = [Cane(), Gatto(), Mucca(), Serpente()]

for animals in fattoria:

    fai_rumore(animals)
