class Cassaforte:
    def __init__(self):
        # Attributo PUBBLICO (accessibile a tutti)
        self.colore = "Grigio"

        # Attributo PRIVATO (inizia con __)
        self.__codice_segreto = 1234


class Cassaforte2:

    def __init__(self):

        self.__colore = "Nero"


# creiamo un'istanza
c = Cassaforte()

# Posso leggere e modificare il pubblico
print(c.colore)

# questa è una modifica
c.colore = "Nero"

# Se provo a toccare il privato ti restituisce attribute error
# print(c.__codice_segreto)


# l' user non sa nemmeno l' esistenza dell' attributo privato
# quando scrivo
c.__codice_segreto = 123456

# python crea un nuovo attributo
# print(c.__codice_segreto)

"se ci facciamo stampare il dizionario riusciamo a vedere il codice segreto"
"le due lineette fanno salvare la variabile come _Cassaforte__codice_segreto"
print(c.__dict__)
