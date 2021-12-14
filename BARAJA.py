import random
from CARTA import Carta

pica = "\u2660"
corazon = "\u2665"
diamante = "\u2666"
trebol = "\u2663"


class Baraja(object):
    VALORES = ["2", "3", "4", "5", "6", "7", "8",
               "9", "T", "J", "Q", "K", "A"]
    PALOS = [pica, corazon, diamante, trebol]

    def __init__(self):
        self.mazo_stdr = []
        for i in self.VALORES:
            for j in self.PALOS:
                carta = Carta(i, j)
                self.mazo_stdr.append(carta)

    def mostrar_baraja(self):
        for carta in self.mazo_stdr:
            print(carta)

    def barajar(self):
        random.shuffle(self.mazo_stdr)

    def repartir_carta(self):
        return self.mazo_stdr.pop(0)




