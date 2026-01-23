import random

numeri = random.sample(range(1, 100), 10)

massimo = numeri[0]
minimo = numeri[0]

i = 0
while i < 10:
    if numeri[i] < minimo:
        minimo = numeri[i]

    elif numeri[i] > massimo:
        massimo = numeri[i]
    i += 1


print(
    f"Il numero massimo è {massimo}, mentre il minimo è {minimo}, la lista di 10 numeri era {numeri}"
)

vocali = "aeiouAEIOU"
with open("numeri.txt", "w") as file:
    file.write(
        f"Il numero massimo è {massimo}, mentre il minimo è {minimo}, la lista di 10 numeri era {numeri}"
    )

cont = 0
with open("numeri.txt", "r") as file:
    for riga in file:
        for lettere in riga:
            if lettere in vocali:
                cont += 1

print(f"Il numero di vocali nel file è: {cont}")
