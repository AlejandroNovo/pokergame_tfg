jugadores = []  # Lista de jugadores


class Jugador(object):

    def __init__(self, nombre):
        self.nombre = nombre
        self.mano = []

    @staticmethod  # Método de clase, no hace falta una instancia del obj
    def iniciar_jugadores():
        num_jugadores = int(input("Introducir numero de jugadores:"))
        for i in range(num_jugadores):
            nombre = input("Nombre del jugador " + str(i+1) + ": ")
            jugadores.append(Jugador(nombre))

    def get_mano(self, mano):
        self.mano = mano

    def asignar_mano(self, carta):
        self.mano.append(carta)

    def dibujar_mano(self):
        for carta in self.mano:
            carta.dibujar_carta()   # Duda como que podemos hacer ese dibujar_carta





