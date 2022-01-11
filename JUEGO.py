from itertools import cycle
import random
from MESA import Mesa
from JUGADOR import Jugador
from Utilidades import Utilidades


class Juego(object):
    MINIMO_JUGADORES = 2
    MAXIMO_JUGADORES = 10
    CARTAS_INICIALES = 2
    CARTAS_FLOP = 3
    FASES = {0: "inicial", 1: "apuestas", 2: "flop"}
    ROLES = {"boton": "Botón", "ciega_peque": "Ciega Pequeña", "ciega_grande": "Ciega Grande"}
    CIEGA_PEQUE = 1
    CIEGA_GRANDE = CIEGA_PEQUE * 2
    FLOP = False
    TURN = False
    RIVER = False

    def __init__(self):
        self.mesa = Mesa()
        self.jugadores_partida = []
        self.contador_ronda = 0
        self.fin_ronda = False
        self.fin_juego = False

    def orquestar(self):
        self.inicio_partida()
        while not self.fin_juego:
            self.orquestar_fases()
            self.fin_juego = self.comprobar_fin_juego()

    def inicio_partida(self):
        self.iniciar_jugadores()
        self.iniciar_roles()

    def iniciar_jugadores(self):
        num_jugadores = Utilidades.preguntar_numero("Introducir el numero de jugadores.\n"
        "Minimo 2, maximo 10: ", self.MINIMO_JUGADORES, self.MAXIMO_JUGADORES)
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

    def orquestar_fases(self):
        try:
            # while True:
                self.inicial()
                self.decision_primera()
                self.gestionar_atributos()
                self.flop()
                self.decision_estandar()
                self.gestionar_atributos()
                self.turn()
                self.decision_estandar()
                self.gestionar_atributos()
                self.river()
                self.decision_estandar()
                self.gestionar_atributos()
                # self.showdown()
        except:
            print("Victoria por abandono ")
            #Continuar a la siguiente ronda

    def inicial(self):
        self.contador_ronda += 1
        self.mesa.mazo_mesa.barajar_fisher_yates()
        if self.contador_ronda != 1:
            self.actualizar_roles()

        self.pagan_ciegas()
        self.repartir_cartas_iniciales()

    def actualizar_roles(self):
        print("Roles actualizados:")
        indice_boton = 0
        # self.jugadores_partida[0].fichas = 0
        # self.jugadores_partida[1].fichas = 0
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
        i = 0
        while i < len(self.jugadores_partida):
            if self.jugadores_partida[i].no_tiene_fichas():
                self.jugadores_partida.remove(self.jugadores_partida[i])
            else:
                i += 1

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

    def decision_primera(self):
        table = cycle(self.jugadores_partida)
        ciega_encontrada = False
        for jugador in table:
            if jugador.activo and ciega_encontrada:
                self.preguntar_accion(jugador)
                if self.fase_resuelta():
                    self.comprobar_all_in()
                    break
            if jugador.es_ciega_grande():
                ciega_encontrada = True

        print("ronda resuelta")

    def decision_estandar(self):
        table = cycle(self.jugadores_partida)
        ciega_encontrada = False
        for jugador in table:
            if jugador.es_ciega_peque():
                ciega_encontrada = True  
            if jugador.activo and ciega_encontrada:
                self.preguntar_accion(jugador)
                if self.fase_resuelta():
                    self.comprobar_all_in()
                    break
        print("fase resuelta")

    def fase_resuelta(self):
        for jugador in self.jugadores_partida:
            if jugador.activo:
                if not jugador.ha_actuado or not jugador.fichas_igualadas(self.comprueba_apuesta_maxima()):
                    return False
        return True

    def preguntar_accion(self, jugador):
        print("====================================")
        self.mostrar_info()
        print(f"Turno del jugador: {jugador.nombre}")
        jugador.info_jugador()
        if jugador.fichas_comprometidas_fase == self.comprueba_apuesta_maxima():
            respuesta = Utilidades.preguntar_opcion("Que desea hacer: P=Pasar, S=Subir.\n"
                                                    "Indique una accion: ", ["P", "S"])
        else:
            jugador.info_igualar(self.comprueba_apuesta_maxima())
            respuesta = Utilidades.preguntar_opcion("Que desea hacer: I=Igualar, S=Subir, N=No ir.\n"
                                                    "Indique una accion: ", ["I", "S", "N"])

        if respuesta == "P":
            jugador.pasar()
            print(str(jugador.nombre) + " ha pasado.")

        elif respuesta == "I":
            apuesta_realizada = jugador.igualar(self.comprueba_apuesta_maxima())
            self.mesa.sumar_al_bote_fase(apuesta_realizada)
            print(str(jugador.nombre) + " ha igualado.")

        elif respuesta == "S":
            apuesta_realizada = jugador.subir(self.comprueba_apuesta_maxima())
            self.mesa.sumar_al_bote_fase(apuesta_realizada)
            print(str(jugador.nombre) + " ha subido.")

        elif respuesta == "N":
            jugador.no_ir()
            print(str(jugador.nombre) + " no ha ido.")

        self.comprobar_victoria_por_abandono()

    def mostrar_info(self):
        print(f"El bote total es: {self.mesa.bote}")
        print(f"El bote de la fase es: {self.mesa.bote_fase}")

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
        print("ººººººººººººººººººººººººº")
        print("Flop:")
        self.mesa.mostar_mesa()
        self.FLOP = True

    def turn(self):
        carta = (self.mesa.mazo_mesa.mazo_stdr.pop())
        self.mesa.sacar_carta_mesa(carta)
        print("ººººººººººººººººººººººººº")
        print("Turn:")
        self.mesa.mostar_mesa()
        self.TURN = True

    def river(self):
        carta = (self.mesa.mazo_mesa.mazo_stdr.pop())
        self.mesa.sacar_carta_mesa(carta)
        print("ººººººººººººººººººººººººº")
        print("River:")
        self.mesa.mostar_mesa()
        self.RIVER = True

    def gestionar_atributos(self):
        self.mesa.sumar_al_bote(self.mesa.bote_fase)
        self.mesa.bote_fase = 0
        for jugador in self.jugadores_partida:
            jugador.fichas_comprometidas_fase = 0
            jugador.ha_actuado = False

    def showdown(self):
        pass

    def comprobar_victoria_por_abandono(self):
        cont = 0
        for jugador in self.jugadores_partida:
            if jugador.activo:
                cont += 1
        if cont < 2:
            # pasar cantidad del bote_fase al bote total y de ahi al jugador que gana

            raise RuntimeError

    def comprobar_all_in(self):
        cont = 0
        for jugador in self.jugadores_partida:
            if jugador.allin:
                self.modo_all_in()

    def modo_all_in(self):
        cont = 0
        for jugador in self.jugadores_partida:
            if jugador.activo:
                cont += 1
        if cont == 2:
            self.all_in_simple()
        else:
            self.all_in_multiple()

    def all_in_simple(self):
        print("All-in 2 jugadores.")
        if not self.FLOP:
            self.flop()
            self.turn()
            self.river()
            self.showdown()
            raise RuntimeError
        elif not self.TURN:
            self.turn()
            self.river()
            self.showdown()
            raise RuntimeError
        elif not self.RIVER:
            self.river()
            self.showdown()
            raise RuntimeError
        else:
            self.showdown()
            raise RuntimeError

    def all_in_multiple(self):
        print("All in con multiples jugadores")
        # Chiquita movida
        pass

    def comprobar_fin_juego(self):
        return True
