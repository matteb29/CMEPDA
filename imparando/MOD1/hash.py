x = hash("uela")
print(x)

##stampa l' indirizzo di memoria dell' oggetto

d = {"Luca": [25, 30, 28], "Marco": [30, 29, 30], "Anna": [29, 28, 27]}

voti_luca = d["Luca"]
voti_marco = d["Marco"]
voti_anna = d["Anna"]


chiave_luca = hash("Luca")
chiave_marco = hash("Marco")
chiave_anna = hash("Anna")


print(voti_marco[1])
print(chiave_marco)


month = "Genn Febb Marz".split()
giorni = "31 28 31".split()

d = dict(zip(month, giorni))
print(d)

for i, j in zip(range(len(month)), range(len(giorni))):
    print(i, j)


my_dict = {}
print(id(my_dict))
