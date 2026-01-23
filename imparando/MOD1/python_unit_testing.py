# modo pythonico di fare il unit testing a differenza del modo fai da te
# del programma dumpo_unit_testing.py


import unittest  # importo questo modulo


def square(x):
    return x * x


class TestSquare(unittest.TestCase):  # definsco una classe ereditaria
    # di test sulla funzione quadrato

    def test1(self):  # definisco il modulo test che verifica il funzionamento
        # della funzione quadrato verificando che il quadrato di 2 sia 4

        self.assertAlmostEqual(square(2.0), 4)  # metodo del modulo unittest
        # per tenere conto anche delle disguaglianze dovute all' arrotondamento per esempio distingue 4.00 con 4.01
        # per esempio se scrivessi 0.1 + 0.2 == 0.3 mi direbbe false

    def test2(
        self,
    ):  # ora provo a metterci un secondo test che scrive una cosa falsa per vedere
        # se si accorge

        self.assertAlmostEqual(square(3.0), 7)


if __name__ == "__main__":

    unittest.main()  # questa funzione serve per lanciare tutti i test che sono stati definiti
    # come moduli di una classe di test figlia di unittest.TestCase
    # usi la funzione main che sta dentro la libreria unittest


print(
    0.1 + 0.2 == 0.3
)  # questo mi da falso, per problemi in virgola mobile, per questo si usa
# assertAlmostEqual
