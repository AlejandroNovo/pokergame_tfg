class Jugador(object):

    def __init__(self, nombre):
        self.nombre = nombre
        self.mano = []

    def dibujar_mano(self):
        for carta in self.mano:
            carta.dibujar_carta()   # Duda como que podemos hacer ese dibujar_carta

#prueba2



