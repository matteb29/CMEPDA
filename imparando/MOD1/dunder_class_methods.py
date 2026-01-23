import numpy as np

# ricorda che per chiamare un membro qualsiasi la sintassi è istanza.membro


# i dunder method rendono le classe più potenti
# ci posso fare un sacco di cose come printare l' oggetto della classe
# oppure iterare oggetti in un ciclo for etc


class Persona:

    archivio = (
        []
    )  # definisco l' attributo globale della classe persona, che è una lista vuota

    "posso vedere init come un metodo che assegna valori agli attributi"

    def __init__(self, nome="Luca", età=25):  # attributi che anche se inizializzati
        # possono essere cambiati

        self.età = età
        self.nome = nome
        self.append()  # con questo ogni volta che chiami un oggetto usa anche self.append
        # poichè ogni volta che crei una istanza si chiama il metodo dunder __init__ che
        # quindi chiama append

    def __str__(
        self,
    ):  # questo è un secondo esempio di dunder method e si usa per permettere di
        # utilizzare il print sull' istanza della classe persona che ho creato ora
        return f"Nome: {self.nome}, età: {self.età}"

    def __len__(self):  # dunder method che ti resituisce la lunghezza del nome
        # così ora posso definire il built-in len anche su amico, mentre prima non avrebbe saputo
        # come comportarsi

        return len(self.nome)

    def __add__(
        self, altra_persona
    ):  # dunder method che permette di fare somme tra attributi di oggetti diversi
        # ma appartenenti alla stessa classe

        return self.età + altra_persona.età  # qui c' è scritto cosa deve fare add

    def __iter__(self):

        return iter([self.nome, self.età])

    def __eq__(
        self, other
    ):  # questo metodo speciale serve per poter poi scrivere il confronto
        # con == tra due oggetti della stessa classe

        return (
            self.nome == other.nome and self.età == other.età
        )  # nel return ci solo le indicazioni di cosa
        # deve gestire l' operatore == , in questo caso lui deve gestire il confronto
        # con il nome delle due persone e con la loro età
        # in logica con il chiedersi se due persone sono la stessa persona

    def append(
        self, *args
    ):  # *args mi fa aggiungere tutti gli argomenti che voglio in metodo append:
        # è praticamente il jolly degli argomenti

        Persona.archivio.append(
            self
        )  # Persona.archivio richiama l' attributo della classe:archivio
        # ci vail self perchè stiamo appendendo l' oggetto che stiamo chiamando

    @classmethod  # decoratore che trasforma un metodo in metodo di classe
    # cioè posso applicarlo alla classe piuttosto che all' oggetto
    # nel codice invece di scrivere il solito my_car.guida()
    # sono autorizzato a scrivere car.guida() con my_car istanza della classe car

    def tutte(cls):  # cls è diventata una parola
        # speciale grazie al @classmethod
        return cls.archivio


amico = Persona("Giovanni", 30)
nemico = Persona("Anti-Giovanni", 12)
print(amico)  # chiamando print lui va a usare il metodo __str__ della classe persona
# e quindi stampa quello che c'è dentro il return del metodo __str__

collega = Persona("Antonino", 19)

print("Archivio:", Persona.tutte())


gente = [amico, nemico, collega]  # posso fare una lista di oggetti della classe persona

lunghezza_nome_amico = len(amico)  # chiamando len(amico) lui normalmente non
# saprebbe cosa fare, però noi glielo facciamo gestire agiunger eil dunder method __len__
# così ora lui può usare len su amico e restituire quello che c'è nel return del metodo __len__


amico_nemico = amico + nemico  # chiamando amico + nemico lui non saprebbe cosa fare
# però noi glielo diciamo nel metodo __add__,
# infatti nel return scriviamo cosa deve fare add cioè sommare le età delle due persone


print(amico_nemico)  # a 3 non funziona perchè la somma non è chiusa
# perché amico + nemico restituisce un int e non una Persona

print(amico == collega)  # senza il dunder method __eq__ lui non sa come
# gestire il confronto tra due istanze della stessa classe, tuttavia il metodo speciale __eq__
# gli dà le istruzione di come fare, leggendo dal return di __eq__


print(lunghezza_nome_amico)


for (
    tizio
) in gente:  # posso fare un ciclo for su una lista di oggetti della classe persona
    # e questo grazie al dunder method __iter__ che permette
    # di iterare in cicli for sugli oggetti della classe persona

    print(tizio)  # qui lui usa il solito metodo __str__ della classe perosona

print("\n Ora con metodo dell' archivio....\n ")

for tizio in Persona.archivio:

    print(tizio)
