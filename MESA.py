from BARAJA import Baraja


class Mesa(object):
    def __init__(self):
        self.mazo_mesa = Baraja()
        self.cartas_mesa = []
        self.bote = ""

    def sacar_carta_mesa(self, carta):
        self.cartas_mesa.append(carta)

    def mostar_mesa(self):
        for carta in self.cartas_mesa:
            carta.dibujar_carta()










