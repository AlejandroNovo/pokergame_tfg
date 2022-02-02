from JUEGO import *
from JUGADORIA import JugadorIA
from random import choice


class JuegoIA(Juego):
    def __init__(self):
        Juego.__init__(self)
        self.ultima_apuesta_rival = 0

    def iniciar_jugadores(self):
        jugador = Jugador()
        nombre = input("Elija el nombre del jugador: ")
        jugador.nombre = nombre
        self.jugadores_partida.append(jugador)
        self.jugadores_partida.append(JugadorIA())
        print("")

    def actualizar_valores(self):
        for jugador in self.jugadores_partida:
            jugador.activo = True
            jugador.allin = False
            jugador.mano.clear()
            jugador.valor_mano = np.zeros(6, dtype=int)
            jugador.valor_final = 0
            jugador.posicion = False
            jugador.esta_en_preflop = False
            jugador.esta_en_postflop = False
        self.mesa.bote = 0
        self.mesa.bote_dinamico = 0
        self.FLOP = False
        self.TURN = False
        self.RIVER = False
        self.mesa.cartas_mesa.clear()

    def preguntar_accion(self, jugador):

        if not jugador.esIA:
            self.ultima_apuesta_rival = super().preguntar_accion(jugador)

        if jugador.esIA:
            jugador.info_jugador()
            respuesta = jugador.tomar_decision(self.mesa, self.ultima_apuesta_rival)
            print(f"Respuesta {respuesta}")

            if respuesta == "P":
                jugador.pasar()

            elif respuesta == "I":
                apuesta_realizada = jugador.igualar(self.comprueba_apuesta_maxima())
                self.mesa.sumar_al_bote_fase(apuesta_realizada)

            elif respuesta == "S1" or respuesta == "S2" or respuesta == "S3" or respuesta == "S4":
                apuesta_realizada = 0
                if respuesta == "S1":
                    apuesta_realizada = jugador.subir_ia("subida_estandar", self.mesa.bote_dinamico,
                                                         self.comprueba_apuesta_maxima())  # Subida estandar
                elif respuesta == "S2":
                    apuesta_realizada = jugador.subir_ia("subida_media", self.mesa.bote_dinamico,
                                                         self.comprueba_apuesta_maxima())  # Subida media
                elif respuesta == "S3":
                    apuesta_realizada = jugador.subir_ia("subida_fuerte", self.mesa.bote_dinamico,
                                                         self.comprueba_apuesta_maxima())  # Subida fuerte
                elif respuesta == "S4":
                    apuesta_realizada = jugador.subir_ia("subida_muy_fuerte", self.mesa.bote_dinamico,
                                                         self.comprueba_apuesta_maxima())  # Subida muy fuerte)

                self.mesa.sumar_al_bote_fase(apuesta_realizada)

            elif respuesta == "N":
                jugador.no_ir()

            self.comprobar_victoria_por_abandono()




