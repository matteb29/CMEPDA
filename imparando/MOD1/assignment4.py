import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.interpolate import InterpolatedUnivariateSpline


class PDF(InterpolatedUnivariateSpline):  # Faccio ereditare alla classe PDF tutti
    # i metodi della classe madre InterpolatedUnivariateSpline così
    # che posso fare su pdf operazioni come interpolazioni, integral, derivative etc
    # Interpolate usa solo array crescenti

    def __init__(self, x, y):  # parto con dei dati x, y

        super().__init__(x, y)
        # equivalente a quello che scrive baldini con InterpolatedUnivariateSpline.__init__(self, x,y)

        # definisco la cumulante

        ycdf = np.array(
            [self.integral(x[0], x_star) for x_star in x]
        )  # ycdf[i] è la cumulante
        # da x[0] a x[i], mi calcolo tutte le cumulanti per ogni x
        print(ycdf)

        self.cdf = InterpolatedUnivariateSpline(
            x, ycdf
        )  # ora creo una istanza della classe Interpolated
        # UnivariateSpline dei punti x, ycdf cosi ottengo una funzione che interpoli i dati con le cumulanti

        print(
            self.cdf(1.2)
        )  # così che ora la spline facendo l' interpolazione sa tutti i valori delle cdf
        # e mi sa dire il valore della cdf in x = 1.2

        # ora cerco un metodo per fornire numeri distribuiti con la
        # pdf scelta....

        # xppf sono i valori della CDF che sono valori da 0 a 1
        # yppf sono i valori delle x associate alla CDF contenuta nell' array xppf

        xppf, ippf = np.unique(ycdf, return_index=True)  # np.unique ordina i dati
        # ed elimina i duplicati, la funzionalità return_index = True ti restituisce gli indici ordinati
        # np.unique restituisce una tupla quindi xppf si prende i valori ordinati e senza doppioni di ycdf
        # mentre ippf si prende i valori degli indici

        yppf = x[
            ippf
        ]  # le y della percentual point function sono le x della cdf con x[i]
        # associato alla y_cdf[i]

        # ora interpolo la mia percentual point function che è la funzione inversa della cumulante
        self.ppf = InterpolatedUnivariateSpline(xppf, yppf)

    def random(self, size=100000):

        return self.ppf(np.random.uniform(0, 1, size))

    def prob(self, x1, x2):

        # quando scrivo cdf(x2) sto chiamando il metodo speciale della classe madre InterpolatedUnivariateSpline
        # __call__ per poter valutare la cdf nel punto x2
        return self.cdf(x2) - self.cdf(x1)


def test_triangolare():  # Unit test del programma con una retta
    # vista come una triangolare nel primo tratto 0 a 1

    x = np.linspace(0, 10, 1000)  # creo un array di 100 valori, che sono il dominio
    # della mia pdf
    y = 2 * x  # la funzione pdf sarà una semplice retta solo per verifica

    pdf_triangolare = PDF(x, y)  # ora definisco una istanza della classe PDF
    # che sarà una pdf a forma di retta con pendenza 2

    a = np.array([0.2, 0.5])  # prendo due punti su cui valutare la pdf di prova

    # quando definisco pdf_triangolare(a) io sto chiamando un metodo speciale (sono quelli
    # con due underscore) della classe madre InterpolatedUnivariateSpline
    # chiamato __call__, che permette di valutare la spline nei punti scelti
    # da cui ora scrivere pdf_triangolare(a) è come dire valuta la funzione pdf_triangolare nei punti
    # dell' array a

    print(pdf_triangolare(a))  # controllo che la classe pdf funzioni
    # controllando che mi restituisca i valori giusti cioè 2 * a

    numeri_triangolari = (
        pdf_triangolare.random()
    )  # ora genero i numeri secondo la pdf scelta
    # cioè secondo la pdf =  2*x

    plt.figure("Campionamento")
    plt.hist(numeri_triangolari, bins=200, alpha=0.4)


if (
    __name__ == "__main__"
):  # ogni file python che si scrive ha una variabile speciale chiamata
    # name questa variabile assume il <<valore>> __main__ se  il programma è eseguito direttamente,
    # altrimenti prende "nome_file" se viene eseguito importato come nome_file con la sintassi import nome_file
    # in un altro programma...

    # in poche parole io gli sto dicendo di eseguire questa parte di codice, cioè
    # l' unit testing soltanto se eseguo il programma da questo file, ma non farglielo eseguire se un giorno
    # importerò questo programma in un altro

    test_triangolare()
    plt.show()


x = np.linspace(
    0, 100, 50
)  # così numpy crea un array di numeri da 0 a 10 soaziati di 100
# in ordine crescente
y = np.exp(-x / 20) / 20  # la mia pdf

mia_pdf = PDF(x, y)  # ora interpolo la mia pdf
plt.figure(figsize=(10, 5))
plt.xlabel("tempi [s]")
plt.ylabel("esponenziale decrescente [u.a.]")
plt.plot(x, y)
# plt.show()


print(f"La cumulante di 1.2 è data da: {mia_pdf.cdf(1.2)}")

print(mia_pdf.prob(0.5, 2.5))

print(f"I dieci numeri generati secondo la mia pdf sono: \n {mia_pdf.random()}")
