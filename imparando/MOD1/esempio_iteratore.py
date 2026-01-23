class mio_iteratore:

    #deve avere due attributi, contatore e dati su cui iterare
    def __init__(self, dati):
        self.dati = dati
        self.contatore = 0

    #possiede il metodo dunder iter
    def __iter__(self):
        return self
    
    #possiede il metodo dunder next
    def __next__(self):
        if self.contatore < len(self.dati):
            self.contatore += 1
            return self.dati[self.contatore]
        else:
            raise StopIteration


    

def generatore(dati):


    for i in range (dati):
        yield dati[i]

    print("stop generatore")





lista = [1,2,3]
paolo = mio_iteratore(lista)

paolo.__next__()

generatore([1,2,3])
