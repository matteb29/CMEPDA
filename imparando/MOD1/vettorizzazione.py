import numpy as np

lista1 = [1, 2, 3, 4]
lista2 = [10, 20, 30, 40]
lista_unita = lista1 + lista2


lista_somma = []

for i in range(len(lista1)):
    a = lista1[i] + lista2[i]
    lista_somma.append(a)

print(f"Lista somma: {lista_somma}")


# la vettorizzazione in numpy invece mi permette di fare operazioni su array,
# prendo delle liste e le converto in array usando numpy

x = np.array(lista1)
y = np.array(lista2)

z = x + y
print(f"z è della forma: {np.shape(z)}")

# Le dimensioni degli array devono essere uguali, oppure
##una delle dimensioni deve essere 1.
# Espansione delle dimensioni:
# Se una dimensione è 1, NumPy "espande" l'array lungo quella dimensione per renderlo compatibile con l'altro array.


A = np.array([[1, 2, 3, 4]])  # matrice 1x4
B = np.array([[10, 20, 30, 40]]).reshape(4, 1)  # reshape cambia la forma dell'array
C = A + B

Matrice1 = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]])

Matrice2 = np.array([[1, 2, 3, 4]])  # questa è un array di shape (1,4) che
# è possibile sommare con una mtrice 4x4 grazie alla regola di broadcasting
# in cui se una dimensione è 1, numpy la espande per renderla compatibile


print(f"Array somma: {z}")


print(f"con reshape: {C}")
print(f"Matrice 4x4 : {Matrice1}")

print(f"Matrice 3 : {Matrice1 + Matrice2}")
