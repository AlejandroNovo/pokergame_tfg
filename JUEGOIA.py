from JUEGO import *
from JUGADORIA import JugadorIA
from random import choice


class JuegoIA(Juego):
    def __init__(self):
        Juego.__init__(self)
        self.ultima_apuesta_rival = 0

    def iniciar_jugadores(self):
        jugador = Jugador()
        IA = JugadorIA()
        nombre = input("Elija el nombre del jugador: ")
        jugador.nombre = nombre
        self.jugadores_partida.append(jugador)
        self.jugadores_partida.append(IA)
        print("")

    def preguntar_accion(self, jugador):

        if not jugador.esIA:
            self.ultima_apuesta_rival = super().preguntar_accion(jugador)

        if jugador.esIA:
            jugador.info_jugador()
            respuesta = jugador.tomar_decision(self.mesa, self.ultima_apuesta_rival)

            if respuesta == "P":
                jugador.pasar()
                print(str(jugador.nombre) + " ha pasado.")
                print("")

            elif respuesta == "I":
                apuesta_realizada = jugador.igualar(self.comprueba_apuesta_maxima())
                self.mesa.sumar_al_bote_fase(apuesta_realizada)
                print(str(jugador.nombre) + f" ha igualado {apuesta_realizada} fichas.")
                print("")

            elif respuesta == "S1" or "S2" or "S3" or "S4":
                apuesta_realizada = 0
                if respuesta == "S1":
                    apuesta_realizada = jugador.subir_ia("subida_estandar", self.mesa.bote_fase,
                                                         self.comprueba_apuesta_maxima())  # Subida estandar
                elif respuesta == "S2":
                    apuesta_realizada = jugador.subir_ia("subida_media", self.mesa.bote_fase,
                                                         self.comprueba_apuesta_maxima())  # Subida media
                elif respuesta == "S3":
                    apuesta_realizada = jugador.subir_ia("subida_fuerte", self.mesa.bote_fase,
                                                         self.comprueba_apuesta_maxima())  # Subida fuerte
                elif respuesta == "S4":
                    apuesta_realizada = jugador.subir_ia("subida_muy_fuerte", self.mesa.bote_fase,
                                                         self.comprueba_apuesta_maxima())  # Subida muy fuerte)
                self.mesa.sumar_al_bote_fase(apuesta_realizada)
                print(str(jugador.nombre) + f" ha subido {apuesta_realizada} fichas.")
                print("")

            elif respuesta == "N":
                jugador.no_ir()
                print(str(jugador.nombre) + " no ha ido.")
                print("")

            self.comprobar_victoria_por_abandono()




