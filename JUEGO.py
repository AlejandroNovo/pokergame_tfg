from MESA import Mesa
from JUGADOR import Jugador
from Utilidades import Utilidades
import itertools

class Juego:
    CARTAS_INICIALES = 2
    NUMERO_ROLES = 3
    FASES = {0: "inicial", 1: "apuestas", 2: "flop"}
    #  ROLES = ["Botón", "Ciega Pequeña", "Ciega Grande"]

    def __init__(self):
        self.mesa = Mesa()
        self.jugadores = []
        self.apuesta_maxima = 0
        self.contador_ronda = 0
        # self.fase = self.FASES[0]

    def orquestar(self):
        self.inicio_partida()
        self.orquestar_ronda()
        self.orquestar_ronda()

    def inicio_partida(self):
        self.mesa = Mesa()
        self.iniciar_jugadores()
        self.iniciar_roles()

    def orquestar_ronda(self):
        # contador_fase = 0
        self.fase_inicial()
        self.fase_apuesta()
        # self.jugadores[2].fichas = 0
        # self.jugadores[0].fichas = 0
        # self.comprobar_actividad()
        # for i in range(len(self.jugadores)):
        # print(str(self.jugadores[i].nombre))

    def fase_inicial(self):
        self.contador_ronda += 1
        self.mesa.mazo_mesa.barajar()
        self.repartir_cartas_iniciales()
        self.actualizar_roles()

    def actualizar_roles(self):
        if self.contador_ronda != 1:

            print("Roles actualizados:")
            self.set_dealer()
            for jugador in self.jugadores:
                jugador.asignar_rol(1, False)
                jugador.asignar_rol(2, False)
            # self.jugadores[2].fichas = 0
            self.comprobar_actividad()
            self.set_ciega_peque()
            self.set_ciega_grande()
            self.imprimir_roles()
        else:
            pass

    def set_dealer(self):
        i = 0
        for jugador in self.jugadores:
            if jugador.rol[0]:  # Chequeo quien es el dealer, lo asigno al jugador +1 y pongo a false el anterior
                self.jugadores[(i + 1) % len(self.jugadores)].asignar_rol(0, True)
                self.jugadores[i].asignar_rol(0, False)
                break
            i += 1

    def set_ciega_peque(self):
        i = 0
        for jugador in self.jugadores:
            if jugador.rol[0]:  # Chequeo quien es el dealer, lo asigno al jugador +1 y pongo a false el anterior
                self.jugadores[(i + 1) % len(self.jugadores)].asignar_rol(1, True)
                break
            i += 1

    def set_ciega_grande(self):
        i = 0
        for jugador in self.jugadores:
            if jugador.rol[0]:  # Chequeo quien es el dealer, lo asigno al jugador +1 y pongo a false el anterior
                self.jugadores[(i + 2) % len(self.jugadores)].asignar_rol(2, True)
            i += 1

    def iniciar_jugadores(self):
        num_jugadores = int(input("Introducir numero de jugadores: "))
        for i in range(num_jugadores):
            nombre = input("Nombre del jugador " + str(i + 1) + ": ")
            jugador = Jugador(nombre)
            self.jugadores.append(jugador)

    def comprobar_actividad(self):
        for jugador in self.jugadores:
            if jugador.comprueba_fichas():
                self.jugadores.remove(jugador)

    def iniciar_roles(self):
        print("Roles iniciales: ")
        if len(self.jugadores) == 2:
            self.jugadores[0].asignar_rol(0, True)
            self.jugadores[0].asignar_rol(1, True)
            self.jugadores[1].asignar_rol(2, True)
        else:
            for i in range(self.NUMERO_ROLES):
                self.jugadores[i].asignar_rol(i, True)

        self.imprimir_roles()

    def repartir_cartas_iniciales(self):
        for _ in range(self.CARTAS_INICIALES):
            for jugador in self.jugadores:
                carta_propia = (self.mesa.mazo_mesa.mazo_stdr.pop())
                jugador.mano.append(carta_propia)


    def fase_apuesta(self):
        for jugador in self.jugadores:
            # self.tomar_decision(jugador)
            pass

    def tomar_decision(self, jugador):
        ##print(f"Estas son sus dos cartas:{jugador.dibujar_mano()}")
        print("Estas son sus dos cartas:")
        jugador.dibujar_mano()

    def imprimir_roles(self):
        for i in range(len(self.jugadores)):
            print(str(self.jugadores[i].nombre) + " " + str(self.jugadores[i].rol))





    ''' def ronda(self):
        print("cartas en la mesa")
        self.mesa.mostar_mesa()  # Muestra las cartas añadidas a la mesa
        for jugador in self.jugadores:
            self.jugar(jugador)

    def jugar(self, jugador):
        print("Tus dos cartas:")
        jugador.dibujar_mano()
        opciones = Utilidades.preguntar_opcion("Acciones a realizar[I:Igualar,P:Pasar, S:Subir,N: No ir]", ["T","C"])
    '''

    def fin_de_juego(self):
        return False

#Prueba git hub



