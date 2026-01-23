voti_studenti = {"Marco": [28, 30, 29], "Luca": [30, 30, 30], "Giulio": [29, 28, 30]}


def calcola_media(nome_studente):
    for i in voti_studenti[nome_studente]:
        return sum(voti_studenti[nome_studente]) / len(voti_studenti[nome_studente])


media_marco = calcola_media("Marco")
print(f"La media di Marco è: {media_marco}")

media_luca = calcola_media("Luca")
print(f"La media di Luca è {media_luca}")

media_giulio = calcola_media("Giulio")
print(f"La media di Giulio è {media_giulio}")


voti_studenti["Anna"] = [30, 30, 30]

media_anna = calcola_media("Anna")
print(f"La media di Anna è {media_anna}")


def esame(nome_studente, esame):
    voto = voti_studenti["Marco"][esame]
    return voto


voto_esame_marco = esame("Marco", 2)
print(f"il secondo voto di marco è stato: {voto_esame_marco}")
