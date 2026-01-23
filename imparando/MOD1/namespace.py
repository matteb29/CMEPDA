x = 0


def function():
    x = 7  # io qui ho definito una nuova variabile locale
    # che ha lo stesso nome di quella globale, tuttavia
    # il conflitto di nomi non si verifica grazie al namespace
    # quindi la funzione lavora con la variabile locale
    return x + 1


print(x)
print(function())
