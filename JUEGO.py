from itertools import cycle
import numpy as np
import random
from MESA import Mesa
from JUGADOR import Jugador
from EVALUADOR import Evaluador
from Utilidades import Utilidades
from CARTA import Carta


class Juego(object):
    MINIMO_JUGADORES = 2
    MAXIMO_JUGADORES = 10
    CARTAS_INICIALES = 2
    CARTAS_FLOP = 3
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
            if not self.fin_juego:
                self.fin_juego = self.comprobar_fin_juego()

    def inicio_partida(self):
        self.iniciar_jugadores()
        self.iniciar_roles()

    def iniciar_jugadores(self):
        num_jugadores = Utilidades.preguntar_numero("Introduzca el numero de jugadores.\n"
        "Minimo 2, maximo 10: ", self.MINIMO_JUGADORES, self.MAXIMO_JUGADORES)
        for i in range(num_jugadores):
            nombre = input("Nombre del jugador " + str(i + 1) + ": ")
            jugador = Jugador()
            jugador.nombre = nombre
            self.jugadores_partida.append(jugador)
        print("")

    def iniciar_roles(self):
        print("          Roles iniciales: ")
        print("          ~~~~~~~~~~~~~~~~ ")
        jugador_boton = self.asignar_boton_aleatorio()
        self.asignar_ciegas(jugador_boton)
        self.imprimir_roles()
        self.jugadores_partida[0].aniadir_fichas(10)
        # self.jugadores_partida[1].aniadir_fichas(10)

    def asignar_boton_aleatorio(self):
        jugador = random.choice(self.jugadores_partida)
        jugador.asignar_rol(self.ROLES["boton"])
        return jugador

    def asignar_ciegas(self, jugador_boton):
        indice_boton = self.jugadores_partida.index(jugador_boton)
        if len(self.jugadores_partida) == 2:
            jugador_boton.asignar_rol(self.ROLES["ciega_peque"])
            self.jugadores_partida[(indice_boton + 1) %
                                   len(self.jugadores_partida)].asignar_rol(self.ROLES["ciega_grande"])
        else:
            self.jugadores_partida[(indice_boton + 1) %
                                   len(self.jugadores_partida)].asignar_rol(self.ROLES["ciega_peque"])
            self.jugadores_partida[(indice_boton + 2) %
                                   len(self.jugadores_partida)].asignar_rol(self.ROLES["ciega_grande"])

    def orquestar_fases(self):
        try:
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
            self.showdown()
        except:
            if not self.fin_juego:
                self.fin_juego = self.comprobar_fin_juego()
            while not self.fin_juego:
                self.orquestar_fases()
                self.fin_juego = self.comprobar_fin_juego()

    def inicial(self):

        self.contador_ronda += 1
        print("*******************************************")
        print(f"             Ronda numero: {self.contador_ronda}")
        print("*******************************************")
        print("")
        self.mesa.mazo_mesa.barajar_fisher_yates()
        if self.contador_ronda != 1:
            self.actualizar_valores()
            self.actualizar_roles()

        self.pagan_ciegas()
        self.repartir_cartas_iniciales()

    def actualizar_valores(self):
        for jugador in self.jugadores_partida:
            jugador.activo = True
            jugador.allin = False
            jugador.mano.clear()
            jugador.valor_mano = np.zeros(6, dtype=int)
            jugador.valor_final = 0
        self.mesa.bote = 0
        self.mesa.bote_dinamico = 0
        self.FLOP = False
        self.TURN = False
        self.RIVER = False
        self.mesa.cartas_mesa.clear()


    def actualizar_roles(self):
        print("          Roles actualizados:")
        print("          ~~~~~~~~~~~~~~~~~~~")
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

        # carta1 = Carta(8, "\u2663")
        # carta2 = Carta(3, "\u2660")
        # carta3 = Carta(9, "\u2665")
        # carta4 = Carta(9, "\u2663")
        # carta5 = Carta("Q", "\u2663")
        # carta6 = Carta(7, "\u2663")
        # carta7 = Carta("Q", "\u2660")
        # #
        #carta8 = Carta(14, "\u2663")
        # carta9 = Carta(13, "\u2663")
        # carta10 = Carta(9, "\u2665")
        # carta11 = Carta(9, "\u2663")
        # carta12 = Carta("Q", "\u2663")
        # carta13 = Carta(6, "\u2665")
        # carta14 = Carta(7, "\u2665")
        # # #
        # self.jugadores_partida[0].aniadir_carta(carta1)
        #self.jugadores_partida[0].aniadir_carta(carta2)
        # self.jugadores_partida[0].aniadir_carta(carta3)
        # self.jugadores_partida[0].aniadir_carta(carta4)
        # self.jugadores_partida[0].aniadir_carta(carta5)
        # self.jugadores_partida[0].aniadir_carta(carta6)
        # self.jugadores_partida[0].aniadir_carta(carta7)
        # # #
        # self.jugadores_partida[1].aniadir_carta(carta8)
        # self.jugadores_partida[1].aniadir_carta(carta9)
        # self.jugadores_partida[1].aniadir_carta(carta10)
        # self.jugadores_partida[1].aniadir_carta(carta11)
        # self.jugadores_partida[1].aniadir_carta(carta12)
        # self.jugadores_partida[1].aniadir_carta(carta13)
        # self.jugadores_partida[1].aniadir_carta(carta14)

    def decision_primera(self):
        table = cycle(self.jugadores_partida)
        ciega_encontrada = False
        for jugador in table:
            if jugador.activo and ciega_encontrada and not jugador.allin:
                self.preguntar_accion(jugador)
                if self.fase_resuelta():
                    self.comprobar_all_in(self.mesa.bote_fase)
                    break
            if jugador.es_ciega_grande():
                ciega_encontrada = True

    def decision_estandar(self):
        table = cycle(self.jugadores_partida)
        boton_encontrado = False
        for jugador in table:
            if jugador.activo and boton_encontrado and not jugador.allin:
                self.preguntar_accion(jugador)
                if self.fase_resuelta():
                    self.comprobar_all_in(self.mesa.bote_fase)
                    break
            if jugador.es_boton():
                boton_encontrado = True

    '''def decision_estandar(self):
        table = cycle(self.jugadores_partida)
        ciega_encontrada = False
        for jugador in table:
            if jugador.es_ciega_peque():
                ciega_encontrada = True  
            if jugador.activo and ciega_encontrada and not jugador.allin:
                self.preguntar_accion(jugador)
                if self.fase_resuelta():
                    self.comprobar_all_in(self.mesa.bote_fase)
                    break '''

    def fase_resuelta(self):
        for jugador in self.jugadores_partida:
            if jugador.allin:
                continue
            if jugador.activo:
                if not jugador.ha_actuado or not jugador.fichas_igualadas(self.comprueba_apuesta_maxima()):
                    return False
        return True

    def preguntar_accion(self, jugador):
        apuesta_realizada = 0
        jugador.info_jugador()
        self.mostrar_info()
        if jugador.fichas_comprometidas_fase == self.comprueba_apuesta_maxima():
            respuesta = Utilidades.preguntar_opcion("Que desea hacer: P=Pasar, S=Subir.\n"
                                                    "Indique una accion: ", ["P", "S"])
        else:
            jugador.info_igualar(self.comprueba_apuesta_maxima())
            respuesta = Utilidades.preguntar_opcion("Que desea hacer: I=Igualar, S=Subir, N=No ir.\n"
                                                    "Indique una accion: ", ["I", "S", "N"])

        if respuesta == "P":
            jugador.pasar()

        elif respuesta == "I":
            apuesta_realizada = jugador.igualar(self.comprueba_apuesta_maxima())
            self.mesa.sumar_al_bote_fase(apuesta_realizada)

        elif respuesta == "S":
            apuesta_realizada = jugador.subir_estandar(self.comprueba_apuesta_maxima())
            self.mesa.sumar_al_bote_fase(apuesta_realizada)

        elif respuesta == "N":
            jugador.no_ir()

        self.comprobar_victoria_por_abandono()
        return apuesta_realizada

    def mostrar_info(self):
        print(f"El bote total es: {self.mesa.bote}")
        print(f"El bote de la fase es: {self.mesa.bote_fase}")

    def imprimir_roles(self):
        for jugador in self.jugadores_partida:
            print(jugador.nombre, jugador.roles)
        print("")

    def comprueba_apuesta_maxima(self):
        lista_apuestas_jugadores = []
        for jugador in self.jugadores_partida:
            lista_apuestas_jugadores.append(jugador.fichas_comprometidas_fase)
        return max(lista_apuestas_jugadores)

    def flop(self):
        for _ in range(self.CARTAS_FLOP):
            cartas_flop = (self.mesa.mazo_mesa.mazo_stdr.pop())
            self.mesa.sacar_carta_mesa(cartas_flop)
        print("ººººººººººººººººººººººººººººººººººººººººººº")
        print("                FLOP:")
        self.mesa.mostar_mesa()
        self.FLOP = True

    def turn(self):
        carta = (self.mesa.mazo_mesa.mazo_stdr.pop())
        self.mesa.sacar_carta_mesa(carta)
        print("ººººººººººººººººººººººººººººººººººººººººººº")
        print("                TURN:")
        self.mesa.mostar_mesa()
        self.TURN = True

    def river(self):
        carta = (self.mesa.mazo_mesa.mazo_stdr.pop())
        self.mesa.sacar_carta_mesa(carta)
        print("ººººººººººººººººººººººººººººººººººººººººººº")
        print("                RIVER:")
        self.mesa.mostar_mesa()
        self.RIVER = True

    def gestionar_atributos(self):
        self.mesa.sumar_al_bote(self.mesa.bote_fase)
        self.mesa.bote_fase = 0
        for jugador in self.jugadores_partida:
            jugador.fichas_comprometidas_fase = 0
            jugador.ha_actuado = False

    def showdown(self):
        evaluador = Evaluador(self.jugadores_partida, self.mesa.cartas_mesa)
        ganadores = evaluador.orquestar_evaluador()
        particion_bote = int(self.mesa.bote/len(ganadores))
        print("···········································")
        for jugador in ganadores:
            jugador.aniadir_fichas(particion_bote)
            print(f"El jugador {jugador.nombre} ha ganado la ronda {self.contador_ronda}, con"
                  f": {particion_bote} fichas.")
        print("")
        print("")

    def comprobar_victoria_por_abandono(self):
        cont = 0
        jugador_ganador = None
        for jugador in self.jugadores_partida:
            if jugador.activo:
                jugador_ganador = jugador
                cont += 1
        if cont < 2:
            print("          Victoria por abandono ")
            self.mesa.sumar_al_bote(self.mesa.bote_fase)
            self.mesa.bote_fase = 0
            jugador_ganador.aniadir_fichas(self.mesa.bote)
            for jugador in self.jugadores_partida: # Para resetear los valores sin pasar por gestion de atributos
                jugador.fichas_comprometidas_fase = 0
                jugador.ha_actuado = False
            print("···········································")
            for jugador in self.jugadores_partida:
                if jugador.activo:
                    print(f"El jugador {jugador.nombre} ha ganado un bote de: {self.mesa.bote} fichas.")
                    print("")
                    print("")
            raise RuntimeError

    def comprobar_all_in(self, bote_parcial):
        for jugador in self.jugadores_partida:
            if jugador.allin:
                self.modo_all_in(bote_parcial)

    def modo_all_in(self, bote_parcial):
        cont = 0
        for jugador in self.jugadores_partida:
            if jugador.activo:
                cont += 1
        if cont == 2:
            self.all_in_simple()
        else:
            self.all_in_multiple(bote_parcial)

    def all_in_simple(self):
        print("All-in 2 con jugadores.")
        cantidad_abonar = 0
        ap_max = self.comprueba_apuesta_maxima()
        for jugador in self.jugadores_partida:
            if jugador.allin:
                if jugador.fichas_comprometidas_fase < ap_max:
                    cantidad_abonar = (ap_max - jugador.fichas_comprometidas_fase)

        for jugador in self.jugadores_partida:
            if jugador.fichas_comprometidas_fase == ap_max:
                self.mesa.sumar_al_bote_fase(-cantidad_abonar)
                jugador.aniadir_fichas(cantidad_abonar)

        if not self.FLOP:
            self.flop()
            self.turn()
            self.river()
            self.gestionar_atributos()
            self.showdown()
            raise RuntimeError
        elif not self.TURN:
            self.turn()
            self.river()
            self.gestionar_atributos()
            self.showdown()
            raise RuntimeError
        elif not self.RIVER:
            self.river()
            self.gestionar_atributos()
            self.showdown()
            raise RuntimeError
        else:
            self.gestionar_atributos()
            self.showdown()
            raise RuntimeError

    def all_in_multiple(self, bote_parcial):
        print("All in con multiples jugadores")
        # Chiquita movida
        bote_parcial = bote_parcial
        # El jugador que esta en all-in se queda en standby. Los demás jugadores continuan la partida con normalidad
        # Al final el jugador de all-in solo puede optar al bote_parcial.
        pass

    def comprobar_fin_juego(self):
        if not self.fin_juego:    # si no había fin de juego compruebas si ahora lo hay
            cont = 0
            jugador_ganador = None
            for jugador in self.jugadores_partida:
                if jugador.fichas > 0:
                    jugador_ganador = jugador
                    cont += 1
            if cont <= 1:
                print(f"El ganador de la partida es el jugador {jugador_ganador.nombre}"
                      f" con {jugador_ganador.fichas} fichas.")
                return True   # si hay sólo un jugador vivo fin de juego = true
            return False   # si hay más de un jugador vivo no es fin de juego
        else:  # si ya había un fin de juego devuelves un true
            return True
