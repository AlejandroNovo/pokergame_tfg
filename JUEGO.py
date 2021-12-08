from MESA import *
from JUGADOR import Jugador, jugadores
from Utilidades import Utilidades


class Juego:
    def __init__(self):

        self.mesa = Mesa()
        Jugador.iniciar_jugadores()
        self.mesa.mazo_mesa.barajar()

        for i in range(2):  # Añadir dos cartas a cada jugador
            for jugador in jugadores:
                jugador.asignar_mano(self.mesa.mazo_mesa.mazo_stdr.pop())

        self.mesa.sacar_carta_mesa(self.mesa.mazo_mesa.mazo_stdr.pop())  # Añadir cartas a la mesa

        jugadores[0].dibujar_mano()             # Muestra las dos cartas añadidas al jugador 0
        print(len(self.mesa.mazo_mesa.mazo_stdr))    # Muestra las cartas que quedan en la baraja en este momento
        print(jugadores)                   # Muestra una lista de los jugadores actuales

    def ronda(self):
        print("cartas en la mesa")
        self.mesa.mostar_mesa()  # Muestra las cartas añadidas a la mesa
        for jugador in jugadores:
            self.jugar(jugador)

    def jugar(self,jugador):
        print("Tus dos cartas:")
        jugador.dibujar_mano()
        opciones = Utilidades.preguntar_opcion("Acciones a realizar[I:Igualar,P:Pasar, S:Subir,N: No ir]", ["T","C"])


    def fin_de_juego(self):
        return False




