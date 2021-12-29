from itertools import cycle
import random
from MESA import Mesa
from JUGADOR import Jugador
from Utilidades import Utilidades


class Juego:
    CARTAS_INICIALES = 2
    CARTAS_FLOP = 3
    FASES = {0: "inicial", 1: "apuestas", 2: "flop"}
    ROLES = {"boton": "Botón", "ciega_peque": "Ciega Pequeña", "ciega_grande": "Ciega Grande"}
    CIEGA_PEQUE = 1
    CIEGA_GRANDE = 2

    def __init__(self):
        self.mesa = Mesa()
        self.jugadores_partida = []
        self.jugadores_ronda = []
        self.apuesta_maxima = 0
        self.contador_ronda = 0

    def orquestar(self):
        self.inicio_partida()
        self.orquestar_fase()
        # self.orquestar_fase()

    def inicio_partida(self):
        self.iniciar_jugadores()
        self.iniciar_roles()


    def iniciar_jugadores(self):
        num_jugadores = int(input("Introducir numero de jugadores: "))
        for i in range(num_jugadores):
            nombre = input("Nombre del jugador " + str(i + 1) + ": ")
            jugador = Jugador(nombre)
            self.jugadores_partida.append(jugador)

    def iniciar_roles(self):
        print("Roles iniciales: ")
        jugador_boton = self.asignar_boton_aleatorio()
        self.asignar_ciegas(jugador_boton)
        self.imprimir_roles()

    def asignar_boton_aleatorio(self):
        jugador = random.choice(self.jugadores_partida)
        jugador.asignar_rol(self.ROLES["boton"])
        return jugador

    def asignar_ciegas(self, jugador_boton):
        indice_boton = self.jugadores_partida.index(jugador_boton)
        if len(self.jugadores_partida) == 2:
            jugador_boton.asignar_rol(self.ROLES["ciega_peque"])
            self.jugadores_partida[(indice_boton + 1) % len(self.jugadores_partida)].asignar_rol(self.ROLES["ciega_grande"])
        else:
            self.jugadores_partida[(indice_boton + 1) % len(self.jugadores_partida)].asignar_rol(self.ROLES["ciega_peque"])
            self.jugadores_partida[(indice_boton + 2) % len(self.jugadores_partida)].asignar_rol(self.ROLES["ciega_grande"])

    def orquestar_fase(self):
        # contador_fase = 0
        self.fase_inicial()
        self.primera_toma_decision2()
        self.flop()

    def fase_inicial(self):
        self.contador_ronda += 1
        self.mesa.mazo_mesa.barajar_fisher_yates()
        self.actualizar_roles()
        self.pagan_ciegas()
        self.repartir_cartas_iniciales()

    def actualizar_roles(self):

        # self.jugadores[0].fichas = 0
        # self.jugadores[1].fichas = 0

        if self.contador_ronda != 1:
            print("Roles actualizados:")
            indice_boton = 0
            for jugador in self.jugadores_partida:
                if jugador.es_boton():
                    indice_boton = self.jugadores_partida.index(jugador)
                jugador.roles.clear()

            while self.jugadores_partida[(indice_boton + 1) % len(self.jugadores_partida)].no_tiene_fichas():
                indice_boton += 1

            nuevo_boton = self.jugadores_partida[(indice_boton + 1) % len(self.jugadores_partida)]
            nuevo_boton.asignar_rol(self.ROLES["boton"])
            self.comprobar_actividad()
            self.asignar_ciegas(nuevo_boton)
            self.imprimir_roles()

    def comprobar_actividad(self):
        iterador = False
        for jugador in self.jugadores_partida:
            if jugador.no_tiene_fichas():
                self.jugadores_partida.remove(jugador)
                iterador = True
                break
        if iterador:
            self.comprobar_actividad()

    def pagan_ciegas(self):
        for jugador in self.jugadores_partida:
            if jugador.es_ciega_peque():
                jugador.apuesta(self.CIEGA_PEQUE)
                self.mesa.sumar_al_bote_fase(self.CIEGA_PEQUE)
            elif jugador.es_ciega_grande():
                jugador.apuesta(self.CIEGA_GRANDE)
                self.mesa.sumar_al_bote_fase(self.CIEGA_GRANDE)

    def repartir_cartas_iniciales(self):
        for _ in range(self.CARTAS_INICIALES):
            for jugador in self.jugadores_partida:
                carta_propia = (self.mesa.mazo_mesa.mazo_stdr.pop())
                jugador.aniadir_carta(carta_propia)

    def primera_toma_decision(self):
        # self.jugadores_ronda = self.jugadores_partida
        apuesta_maxima_actual = self.comprueba_apuesta_maxima()
        # self.mostrar_info()
        while not self.ronda_resuelta():
            for jugador in self.jugadores_partida:
                if jugador.es_ciega_grande():
                    turno_jugador = self.gestion_turno(jugador)
                    self.preguntar_accion(apuesta_maxima_actual, turno_jugador)

    def primera_toma_decision2(self):
        table = cycle(self.jugadores_partida)
        primera_fase = True
        apuesta_maxima_actual = self.comprueba_apuesta_maxima()
        # self.mostrar_informacion()
        self.gestion_turno2()

    def gestion_turno2(self):
        table = cycle(self.jugadores_partida)
        apuesta_maxima_actual = self.comprueba_apuesta_maxima()
        while self.ronda_resuelta():
            for jugador in table:
                if jugador.es_ciega_grande():
                    continue
                elif not jugador.activo:
                    continue
                else:
                    self.preguntar_accion(apuesta_maxima_actual, jugador)

        print("ronda resuelta")

    def gestion_turno(self, jugador):
        indice_c = self.jugadores_partida.index(jugador)
        while not self.jugadores_partida[(indice_c + 1) % len(self.jugadores_partida)].activo:
            indice_c += 1
        siguiente_jugador = self.jugadores_partida[(indice_c + 1) % len(self.jugadores_partida)]
        return siguiente_jugador

    ''' def gestion_turnos(self):
        contador_llamada = 0
        if contador_llamada == 0:
            for jugador in self.jugadores_ronda:
                if jugador.es_ciega_grande():
                    indice_c = self.jugadores_ronda.index(jugador)
                    siguiente_jugador = self.jugadores_ronda[(indice_c + 1) % len(self.jugadores_ronda)]
                    contador_llamada = 1
                    return siguiente_jugador
        else:
            for i in self.jugadores_ronda:
                siguiente_jugador = self.jugadores_ronda[(i + 1) % len(self.jugadores_ronda)]
                return siguiente_jugador '''


    def ronda_resuelta(self):
        cont = 0
        for jugador in self.jugadores_ronda:
            if jugador.fichas_comprometidas_fase == self.comprueba_apuesta_maxima():
                cont += 1
        if cont == len(self.jugadores_ronda):
            return True

    def preguntar_accion(self, apuesta_maxima_actual, jugador):
        print("====================================")
        print(f"Turno del jugador: {jugador.nombre}")
        print("Estas son sus cartas: ")
        jugador.dibujar_mano()
        if jugador.fichas_comprometidas_fase == apuesta_maxima_actual:
            respuesta = Utilidades.preguntar_opcion("Acciones a realizar: P=Pasar I=Igualar S=Subir N=No ir\n"
                                                    "Indique una accion: ", ["P", "I", "S", "N"])
        else:

            respuesta = Utilidades.preguntar_opcion("Acciones a realizar: I=Igualar S=Subir N=No ir\n"
                                                    "Indique una accion: ", ["I", "S", "N"])
        if respuesta == "P":
            print(str(jugador.nombre) + " ha pasado.")

        elif respuesta == "I":
            apuesta_realizada = jugador.igualar(apuesta_maxima_actual)
            self.mesa.sumar_al_bote_fase(apuesta_realizada)
            print(str(jugador.nombre) + " ha igualado.")

        elif respuesta == "S":
            jugador.subir(apuesta_maxima_actual)
            print(str(jugador.nombre) + " ha subido.")

        elif respuesta == "N":
            jugador.no_ir()
            print(str(jugador.nombre) + " no ha ido.")

    def mostrar_info(self):
        print("=============== BOTE ACTUAL ==============")
        print(f"El bote actual es {self.mesa.bote}")
        print("==========================================")

    def imprimir_roles(self):
        for jugador in self.jugadores_partida:
            print(jugador.nombre, jugador.roles)

    def comprueba_apuesta_maxima(self):
        lista_apuestas_jugadores = []
        for jugador in self.jugadores_partida:
            lista_apuestas_jugadores.append(jugador.fichas_comprometidas_fase)
        return max(lista_apuestas_jugadores)

    def flop(self):
        for _ in range(self.CARTAS_FLOP):
            cartas_flop = (self.mesa.mazo_mesa.mazo_stdr.pop())
            self.mesa.sacar_carta_mesa(cartas_flop)

    def turn_o_river(self):
        carta = (self.mesa.mazo_mesa.mazo_stdr.pop())
        self.mesa.sacar_carta_mesa(carta)

    def fin_de_juego(self):
        return False
