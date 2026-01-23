import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class Persona:

    specie = "Homo sapiens"  # specie è un attributo della classe persona

    def __init__(self, etnia, velocità):  # definisco  attributi dell' istanza
        self.etnia = etnia
        self.__velocità = velocità

    def saluta(self, saluto):  # definisco il metodo dell' istanza
        print(f"{saluto}")

    @classmethod
    def appartenenza(
        cls,
    ):  # usando il decoratore @classmethod posso definire un decoratore di
        # classe cioè un metodoo che può usare gli attributi di classe
        return print(f"\nchi ti ha salutato appartiene alla razza: {Persona.specie}")

    # le righe di codice sottostante sono utilizzate anche per il setter
    # quindi sia che io voglia rendere l' attributo privato definendo un metodo attributo
    # non cambiabile, sia che io lo voglia cambiare solo entro limiti da me scelti, defo utilizzare
    # prima il property

    @property
    def velocità(
        self,
    ):  # usando il decoratore @property ora posso utilizzare il metodo velocità come
        # se fosse un attributo (e infatti devo aggiungere un attributo all' istanza) e quindi non c' è modo di cambiargli la velocità
        # infatti non posso mettere corri(self, velocità)
        # quindi ora ho ho reso la velocità privata e nessuno gliela può far cambiare

        return (
            self.__velocità
        )  # avendo usato questo return chiamare il metodo ti fornisce l' attributo

    # self.__velocità

    # posso anche fare delle modifiche controllate agli attributi che rendo privati
    # utilizzando il decoratore @attributo.setter se ad esempio volessi controllare le velocità possibili
    # poi sotto metto un metodo, da chiamare con il solito nome dell' attributo controllato,
    # che controlla le velocità possibili

    @velocità.setter
    def velocità(
        self, nuova_velocità
    ):  # il metodo sotto il setter deve avere il solito nome del
        # attributo che non posso cambiare come voglio

        if nuova_velocità > 30 or nuova_velocità < 20:
            raise ValueError("Non puoi impostare questo valore di velocità")
        # se la velocità è fuori dai limiti che voglio allora ho un messaggio di errore
        # il built-in raise serve per CREARE un messaggio di errore

        else:
            self.__velocità = nuova_velocità


carlo = Persona("indiano", 30)
carlo.saluta("aug!")
carlo.appartenenza()  # ricorda che negli attributi ci vanno le parentesi, mentre nei metodi no!!!
print(f"\ned è di etnia: {carlo.etnia} \n")
carlo.velocità

try:

    carlo.velocità = 25  # normalmente per cambiare un attributo si inizializza la
    # variabile in questo modo, ma ricordiamoci che abbiamo reso l' attributo privato


except AttributeError:  # per verificare che sia veramente privato
    # io gli metto un except Attribute Error
    # e se vedo il messaggio "questo attributo è privato" vuol dire che il voler settare la velocità
    # ai 40 all' ora ha prodotto un errore come volevo..la velocità è ora privata

    # ATTENZIONE quando ho il setter questo perde di valicidità tuttavia anche con il
    # setter ci vuole il property def velocità

    print("questo attributo è privato!")


print(carlo.velocità)
