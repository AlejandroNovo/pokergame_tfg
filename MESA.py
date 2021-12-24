from BARAJA import Baraja


class Mesa(object):
    def __init__(self):
        self.mazo_mesa = Baraja()
        self.cartas_mesa = []
        self.bote = 0
        self.bote_fase = 0

    def sacar_carta_mesa(self, carta):
        self.cartas_mesa.append(carta)

    def mostar_mesa(self):
        for carta in self.cartas_mesa:
            carta.dibujar_carta()

    def sumar_al_bote(self, cantidad):
        self.bote += cantidad

    def sumar_al_bote_fase(self, cantidad):
        self.bote_fase += cantidad










