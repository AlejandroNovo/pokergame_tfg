from CARTA import Carta
import random


pica = "\u2660"
corazon = "\u2665"
diamante = "\u2666"
trebol = "\u2663"


class Baraja(object):
    VALORES = ["2", "3", "4", "5", "6", "7", "8",
               "9", "T", "J", "Q", "K", "A"]
    #VALORES = {"2": "2", "3": "3", "4": "4", "5": "5", "6": "6", "7": "7",
               #"8": "8", "9": "9", "T": "10", "J": "11", "Q": "12", "K": "13", "A": "14"}
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

    """def repartir_carta(self):
        return self.mazo_stdr.pop(0) """

    def barajar_fisher_yates(self):
        ultimo_indice = len(self.mazo_stdr) - 1
        while ultimo_indice > 0:
            indice_rand = random.randint(0, ultimo_indice)
            temp = self.mazo_stdr[ultimo_indice]
            self.mazo_stdr[ultimo_indice] = self.mazo_stdr[indice_rand]
            self.mazo_stdr[indice_rand] = temp
            ultimo_indice -= 1


    ''' def shuffle(self):
        tmplist = deepcopy(self)
        m = len(tmplist)
        while (m):
            m -= 1
            i = randint(0, m)
            tmplist[m], tmplist[i] = tmplist[i], tmplist[m]
        return tmplist'''





