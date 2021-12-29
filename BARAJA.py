
from CARTA import Carta
from copy import deepcopy
import random


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
            carta.dibujar_carta()

    def barajar(self):
        random.shuffle(self.mazo_stdr)

    def repartir_carta(self):
        return self.mazo_stdr.pop(0)

    def barajar_fisher_yates(self):
        last_index = len(self.mazo_stdr) - 1
        while last_index > 0:
            rand_index = random.randint(0, last_index)
            temp = self.mazo_stdr[last_index]
            self.mazo_stdr[last_index] = self.mazo_stdr[rand_index]
            self.mazo_stdr[rand_index] = temp
            last_index -= 1


    ''' def shuffle(self):
        tmplist = deepcopy(self)
        m = len(tmplist)
        while (m):
            m -= 1
            i = randint(0, m)
            tmplist[m], tmplist[i] = tmplist[i], tmplist[m]
        return tmplist'''





