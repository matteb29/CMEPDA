import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import InterpolatedUnivariateSpline


class pdf_triangolare:

    def __init__(self):

        self.x = None  # none indica ancora nessun valore
        # serve per gli array in cui non so ancora cosa mettere
        self.y = None
        self.z = None

    def campionare(self, n):

        self.x = np.random.rand(n)
        self.y = np.random.rand(n)
        self.z = self.x + self.y  # così ho generato n numeri con una distribuzione
        # triangolare tra 0 e 2

        plt.figure(figsize=(10, 5))
        plt.hist(self.z, bins=10, color="blue", alpha=0.3)
        plt.xlabel("z")
        plt.ylabel("pdf(z)")
        plt.show()

    def calcolo(self):

        scelta = int(input("Di quanti numeri vuoi conoscere il valore della pdf? "))

        z = 2 * np.random.rand(
            scelta
        )  # valuto la pdf di numeri generati casuali tra 0 e 2
        print(z)

        for i in range(scelta):

            point = z[i]

            if point > 0 and point < 1:
                u = point
                print(u)

            elif point < 2 and point > 1:
                u = 2 - point
                print(u)

            elif point > 2 or point < 0:
                u = 0
                print(0)

    def intervallo(
        self, z_inf, z_sup, prove
    ):  # definisco la probabilità di finire dentro
        # ad un intervallo

        self.z_inf = z_inf
        self.z_sup = z_sup
        self.prove = prove

        self.campionare(prove)  # posso chiamare un metodo dentro un altro
        # metodo scrivendo sempicemente self.campionare(prove)
        cont = 0
        cont = np.sum((self.z >= z_inf) & (self.z <= z_sup))  # al posto
        # del classico ciclo for dove ci metto for i in prove: z[i] > z_inf i++

        print(cont / prove)


triangolare = pdf_triangolare()
triangolare.campionare(10000)
triangolare.calcolo()
triangolare.intervallo(0.1, 0.2, 10000)
