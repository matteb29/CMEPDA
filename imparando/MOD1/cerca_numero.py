import random

numeri = random.sample(range(1, 100), 20)
cont = 0

numero_da_cercare = int(input("Inserisci un numero da cercare: "))

while numero_da_cercare not in range(1, 100):
    print("Il numero deve essere compreso tra 1 e 100")
    numero_da_cercare = int(input("Inserisci un numero da cercare: "))

if numero_da_cercare in numeri:
    for i in numeri:
        if numeo_da_cercare == numeri[i]:
            cont += 1
    print(
        f"Il numero è stato trovato, la lista era {numeri} , il numero è apparso {cont} volte"
    )


else:
    print(
        f"Il numero non è stato trovato, la lista era {numeri} , il numero è apparso 0 volte"
    )
