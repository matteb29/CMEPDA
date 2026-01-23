# Definisco il decoratore (L'armatura)
def raddoppia_risultato(funzione_originale):

    def wrapper(a, b):
        # Chiama la funzione originale
        risultato_originale = funzione_originale(a, b)
        # Modifica il risultato DINAMICAMENTE
        return risultato_originale * 2

    return wrapper


# Funzione Originale (Tony Stark)
# Nota: qui dentro NON c'è scritto "per 2". La logica è pura.


@raddoppia_risultato
def somma(a, b):
    return a + b


# Esecuzione
# Quando chiami somma, Python esegue il wrapper, non la funzione originale nuda.
print(somma(2, 3))


"""
real life application

"""


# Definizione del decoratore per gestire gli accessi ad una funzione pericolosa
def require_admin(func):

    # il decoratore ha dentro di se la funzione wrapper
    def wrapper(user):

        if not user.is_admin:

            raise PermissionError("Accesso Negato!")

        return func(user)  # Chiama la funzione originale solo se il check passa

    return wrapper


# Applicazione
@require_admin
def delete_database(user):
    print("Database cancellato.")
