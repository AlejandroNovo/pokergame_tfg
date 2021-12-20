from itertools import cycle
import random
from MESA import Mesa
from JUGADOR import Jugador
from Utilidades import Utilidades


class Juego:
    CARTAS_INICIALES = 2
    FASES = {0: "inicial", 1: "apuestas", 2: "flop"}
    ROLES = {"boton": "Botón", "ciega_peque": "Ciega Pequeña",
             "ciega_grande": "Ciega Grande"}
    CIEGA_PEQUE = 1
    CIEGA_GRANDE = 2

    def __init__(self):
        self.mesa = Mesa()    # ¡¡1 mesa aquí!!
        self.jugadores = []
        self.apuesta_maxima = 0
        self.contador_ronda = 0
        # self.fase = self.FASES[0]

    def orquestar(self):
        self.inicio_partida()
        self.orquestar_fase()
        self.orquestar_fase()

    def inicio_partida(self):
        self.iniciar_jugadores()
        self.iniciar_roles()

    def iniciar_jugadores(self):
        num_jugadores = int(input("Introducir numero de jugadores: "))
        for i in range(num_jugadores):
            nombre = input("Nombre del jugador " + str(i + 1) + ": ")
            jugador = Jugador(nombre)
            self.jugadores.append(jugador)

    def iniciar_roles(self):
        print("Roles iniciales: ")
        jugador_boton = self.asignarBotonAleatorio()
        self.asignar_ciegas(jugador_boton)
        self.imprimir_roles()

    def asignarBotonAleatorio(self):
        jugador = random.choice(self.jugadores)
        jugador.asignar_rol(self.ROLES["boton"])
        return jugador

    def asignar_ciegas(self, jugador_boton):
        indice_boton = self.jugadores.index(jugador_boton)
        if len(self.jugadores) == 2:
            jugador_boton.asignar_rol(self.ROLES["ciega_peque"])
            self.jugadores[(indice_boton + 1) % len(self.jugadores)
                           ].asignar_rol(self.ROLES["ciega_grande"])
        else:
            self.jugadores[(indice_boton + 1) % len(self.jugadores)
                           ].asignar_rol(self.ROLES["ciega_peque"])
            self.jugadores[(indice_boton + 2) % len(self.jugadores)
                           ].asignar_rol(self.ROLES["ciega_grande"])

    def orquestar_fase(self):
        # contador_fase = 0
        self.fase_inicial()
        self.primera_toma_decision()

    def fase_inicial(self):
        self.contador_ronda += 1
        self.mesa.mazo_mesa.barajar()
        self.repartir_cartas_iniciales()
        self.actualizar_roles()
        self.pagan_ciegas()

    def repartir_cartas_iniciales(self):
        for _ in range(self.CARTAS_INICIALES):
            for jugador in self.jugadores:
                carta_propia = (self.mesa.mazo_mesa.mazo_stdr.pop())
                jugador.mano.append(carta_propia)

    def actualizar_roles(self):
        if self.contador_ronda != 1:
            print("Roles actualizados:")
            indice_boton = 0

            for jugador in self.jugadores:
                if self.ROLES["boton"] in jugador.roles:
                    indice_boton = self.jugadores.index(jugador)

                jugador.roles.clear()

            nuevo_boton = self.jugadores[(
                indice_boton + 1) % len(self.jugadores)]
            nuevo_boton.asignar_rol(self.ROLES["boton"])
            self.comprobar_actividad()
            self.asignar_ciegas(nuevo_boton)
            self.imprimir_roles()

    def comprobar_actividad(self):
        self.jugadores[0].fichas = 0
        self.jugadores[1].fichas = 0
        for jugador in self.jugadores:
            if jugador.comprueba_fichas():
                if self.ROLES["boton"] in jugador.roles:
                    indice_boton = self.jugadores.index(jugador)
                    self.jugadores[(indice_boton + 1) % len(self.jugadores)
                                   ].asignar_rol(self.ROLES["boton"])
                self.jugadores.remove(jugador)

    def pagan_ciegas(self):
        for jugador in self.jugadores:
            if self.ROLES["ciega_peque"] in jugador.roles:
                jugador.apuesta(self.CIEGA_PEQUE)
                self.mesa.sumar_al_bote(self.CIEGA_PEQUE)
            elif self.ROLES["ciega_grande"] in jugador.roles:
                jugador.apuesta(self.CIEGA_GRANDE)
                self.mesa.sumar_al_bote(self.CIEGA_GRANDE)

    def primera_toma_decision(self):
        table = cycle(self.jugadores)
        primera_fase = True
        apuesta_maxima_actual = self.CIEGA_GRANDE

        self.mostrar_informacion()
        for jugador in table:
            if (self.ROLES["ciega_grande"] in jugador.roles) and primera_fase:
                primera_fase = False
                continue
            if not primera_fase:
                self.preguntar_accion(apuesta_maxima_actual, jugador)
                

    def preguntar_accion(self, apuesta_maxima_actual, jugador):
        if jugador.apuesta_actual == apuesta_maxima_actual:
            opciones = Utilidades.preguntar_opcion("Acciones a realizar: P=Pasar I=Igualar S=Subir N=No ir\n"
                                                   "Indique una accion: ", ["P", "I", "S", "N"])
        else:
            opciones = Utilidades.preguntar_opcion("Acciones a realizar: I=Igualar S=Subir N=No ir\n"
                                                   "Indique una accion: ", ["I", "S", "N"])
        if opciones == "P":
            print(str(jugador.nombre) + " ha pasado.")
        elif opciones == "I":
            print(str(jugador.nombre) + " ha igualado.")
        elif opciones == "S":
            print(str(jugador.nombre) + " ha subido.")
        elif opciones == "N":
            print(str(jugador.nombre) + " no ha ido.")

        return apuesta_maxima_actual


    def mostrar_informacion(self):
        print("=============== BOTE ACTUAL ==============")
        print(f"El bote actual es {self.mesa.bote}")
        print("==========================================")

    def imprimir_roles(self):
        for jugador in self.jugadores:
            print(jugador.nombre, jugador.roles)

    def comprueba_apuesta(self):
        # Comprueba si la apuesta realizada es la mayor de la toma de desción
        # y actualiza un valor cuando si lo sea
        pass

    ''' def ronda(self):
        print("cartas en la mesa")
        self.mesa.mostar_mesa()  # Muestra las cartas añadidas a la mesa
        for jugador in self.jugadores:
            self.jugar(jugador)
    '''

    def fin_de_juego(self):
        return False
