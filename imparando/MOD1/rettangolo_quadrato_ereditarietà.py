"""
il paradosso si risolve con la composizione

"""


# 1. La classe "Motore" (chi fa i calcoli)
class Rettangolo:
    def __init__(self, w, h):
        self.width = w
        self.height = h

    def cambia_altezza(self, deltah):
        self.deltah = deltah
        return self.height + self.deltah

    def cambia_larghezza(self, deltaw):
        self.deltaw = deltaw
        return self.width + self.deltaw

    def get_area(self):
        return self.width * self.height


# 2. La classe "Wrapper" (chi comanda)
# Nota: NON c'è ereditarietà (non c'è parentesi con Rettangolo)
class Quadrato:
    def __init__(self, lato):
        # COMPOSIZIONE: Creiamo un rettangolo nascosto dentro
        # Lo costringiamo subito ad avere lati uguali
        self.__rettangolo_interno = Rettangolo(lato, lato)

    def get_area(self):
        # DELEGA: Passiamo la palla al componente interno
        return self.__rettangolo_interno.get_area()

    def set_lato(self, nuovo_lato):
        # LOGICA DI CONTROLLO:
        # Aggiorno manualmente ENTRAMBI i lati del rettangolo interno.
        # Così l'invariante del quadrato è salvo.
        self.__rettangolo_interno.cambia_altezza(5)
        self.__rettangolo_interno.cambia_larghezza(5)


q = Quadrato(5)
print(f"Area iniziale: {q.get_area()}")  # 25

# Modifico il lato
q.set_lato(10)
print(f"Nuova area: {q.get_area()}")  # 100

# PROVA DEL PARADOSSO (Non è più possibile!)
# q.set_width(5)
