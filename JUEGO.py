import random
from MESA import Mesa
from JUGADOR import Jugador
from Utilidades import Utilidades

class Juego:
    CARTAS_INICIALES = 2
    FASES = {0: "inicial", 1: "apuestas", 2: "flop"}
    ROLES = {"boton": "Botón", "ciega_peque": "Ciega Pequeña", "ciega_grande": "Ciega Grande"}

    def __init__(self):
        self.mesa = Mesa()
        self.jugadores = []
        self.apuesta_maxima = 0
        self.contador_ronda = 0
        # self.fase = self.FASES[0]

    def orquestar(self):
        self.inicio_partida()
        self.orquestar_ronda()
        # self.orquestar_ronda()

    def inicio_partida(self):
        self.mesa = Mesa()
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
            self.jugadores[(indice_boton + 1) % len(self.jugadores)].asignar_rol(self.ROLES["ciega_grande"])
        else:
            self.jugadores[(indice_boton + 1) % len(self.jugadores)].asignar_rol(self.ROLES["ciega_peque"])
            self.jugadores[(indice_boton + 2) % len(self.jugadores)].asignar_rol(self.ROLES["ciega_grande"])

    def orquestar_ronda(self):
        # contador_fase = 0
        self.fase_inicial()
        # self.fase_apuesta()
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
            indice_boton = 0

            for jugador in self.jugadores:
                if self.ROLES["boton"] in jugador.roles:
                    indice_boton = self.jugadores.index(jugador)
                    
                jugador.roles.clear()

            nuevo_boton = self.jugadores[(indice_boton + 1) % len(self.jugadores)]
            nuevo_boton.asignar_rol(self.ROLES["boton"])
            self.comprobar_actividad()
            self.asignar_ciegas(nuevo_boton)
            self.imprimir_roles()


    def comprobar_actividad(self):
        self.jugadores[0].fichas = 0
        for jugador in self.jugadores:
            if jugador.comprueba_fichas():
                if self.ROLES["boton"] in jugador.roles:
                    indice_boton = self.jugadores.index(jugador)
                    self.jugadores[(indice_boton + 1) % len(self.jugadores)]
                self.jugadores.remove(jugador)

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
        for jugador in self.jugadores:
            print(jugador.nombre, jugador.roles)


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
#Prueba actualisima



