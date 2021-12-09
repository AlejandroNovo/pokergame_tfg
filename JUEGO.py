from MESA import Mesa
from JUGADOR import Jugador
from Utilidades import Utilidades


class Juego:
    CARTAS_INICIALES = 2
    FASES = {0: "inicial", 1: "apuestas", 2: "flop"}

    def __init__(self):
        self.mesa = Mesa()
        self.jugadores = []
        self.fase = self.FASES[0]

    def orquestrar(self):
        pass

    def empezar(self):

        self.mesa = Mesa()
        self.iniciar_jugadores()
        self.mesa.mazo_mesa.barajar()
        self.repartir_cartas_iniciales()

        self.mesa.sacar_carta_mesa(self.mesa.mazo_mesa.mazo_stdr.pop())  # Añadir cartas a la mesa

        self.jugadores[0].dibujar_mano()  # Muestra las dos cartas añadidas al jugador 0
        print(len(self.mesa.mazo_mesa.mazo_stdr))  # Muestra las cartas que quedan en la baraja en este momento
        print(self.jugadores)  # Muestra una lista de los jugadores actuales

    def iniciar_jugadores(self):
        num_jugadores = int(input("Introducir numero de jugadores: "))
        for i in range(num_jugadores):
            nombre = input("Nombre del jugador " + str(i + 1) + ": ")
            jugador = Jugador(nombre)
            self.jugadores.append(jugador)

    def repartir_cartas_iniciales(self):
        for _ in range(self.CARTAS_INICIALES):
            for jugador in self.jugadores:
                carta_propia = (self.mesa.mazo_mesa.mazo_stdr.pop())
                jugador.mano.append(carta_propia)

    def ronda(self):
        print("cartas en la mesa")
        self.mesa.mostar_mesa()  # Muestra las cartas añadidas a la mesa
        for jugador in self.jugadores:
            self.jugar(jugador)

    def jugar(self, jugador):
        print("Tus dos cartas:")
        jugador.dibujar_mano()
        opciones = Utilidades.preguntar_opcion("Acciones a realizar[I:Igualar,P:Pasar, S:Subir,N: No ir]", ["T","C"])


    def fin_de_juego(self):
        return False

#Prueba git hub



