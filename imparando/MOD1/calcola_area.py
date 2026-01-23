import math


def calcola_area_triangolo():
    base = float(input("Inserisci la base del tuo triangolo: "))
    altezza = float(input("Inserisci l' altezza del tuo triangolo: "))
    area = base * altezza / 2
    return area


def calcola_area_rettangolo():
    base = float(input("Inserisci la base del tuo rettangolo: "))

    cont = 2
    while cont < base:
        while base % cont != 0:
            cont += 1
        else:
            break

    if cont == base:

        print("La base è un numero primo")

    altezza = float(input("inserisci l' altezza del tuo rettangolo: "))
    area = base * altezza
    return area


def calcola_area_quadrato():
    lato = float(input("Inserici il lato del quadrato: "))
    area = lato * lato
    return area


def calcola_area_cerchio():
    raggio = float(input("Inserisci il raggio del cerchio: "))
    area = math.pi * raggio * raggio
    return area


scelta = input(
    "Scegli la figura geometrica di cui vuoi calcolare l' area: triangolo, rettangolo, quadrato, cerchio: "
)

while scelta not in ["triangolo", "cerchio", "quadrato", "rettangolo"]:
    scelta = input(
        "Scelta non valida...scegli la figura geometrica di cui vuoi calcolare l' area: triangolo, rettangolo, quadrato, cerchio: "
    )


if scelta == "triangolo":
    area = calcola_area_triangolo()
    print(f"L' area del tuo triangolo e': {area:.3f}")

elif scelta == "rettangolo":
    area = calcola_area_rettangolo()
    print(f"l' area del tuo rettangolo e': {area:.3f}")

elif scelta == "quadrato":
    area = calcola_area_quadrato()
    print(f"L' area del tuo quadrato è {area:.3f}")

elif scelta == "cerchio":
    area = calcola_area_cerchio()
    print(f"L' area del tuo cerchioo è {area:.3f}")
