from Utilidades import Utilidades
import numpy as np


class Jugador(object):

    def __init__(self):
        self.nombre = ""
        self.mano = []
        self.roles = []  # [Dealer, Ciega_Peque, Ciega_Grande]
        self.fichas = 20
        self.activo = True
        self.ha_actuado = False
        self.allin = False
        self.fichas_comprometidas_fase = 0
        self.valor_mano = np.zeros(6, dtype=int)
        self.valor_final = 0
        self.esIA = False


    def dibujar_mano(self):
        for carta in self.mano:
            carta.dibujar_carta()
        
    def asignar_rol(self, rol):
        self.roles.append(rol)

    def aniadir_carta(self, carta):
        self.mano.append(carta)

    def aniadir_fichas(self, cantidad):
        self.fichas += cantidad

    def no_tiene_fichas(self):
        if self.fichas == 0:
            return True
        return False

    def es_boton(self):
        if "Botón" in self.roles:
            return True
        return False

    def es_ciega_peque(self):
        if "Ciega Pequeña" in self.roles:
            return True
        return False

    def es_ciega_grande(self):
        if "Ciega Grande" in self.roles:
            return True
        return False

    def apuesta(self, fichas_descontar):
        if self.fichas - fichas_descontar == 0:
            self.fichas -= fichas_descontar
            self.fichas_comprometidas_fase += fichas_descontar
            self.allin = True
        else:
            self.fichas -= fichas_descontar
            self.fichas_comprometidas_fase += fichas_descontar

    def pasar(self):
        self.ha_actuado = True
        print(str(self.nombre) + " ha pasado.")
        print("")

    def igualar(self, apuesta_maxima_actual):

        cantidad_a_igualar = apuesta_maxima_actual - self.fichas_comprometidas_fase

        if cantidad_a_igualar < self.fichas:
            self.apuesta(cantidad_a_igualar)
            self.ha_actuado = True
            print(str(self.nombre) + f" ha igualado {cantidad_a_igualar} fichas.")
            print("")
            return cantidad_a_igualar

        elif cantidad_a_igualar >= self.fichas:
            fichas = self.fichas
            self.apuesta(self.fichas)
            self.ha_actuado = True
            print(str(self.nombre) + f" ha igualado {fichas} fichas.")
            print("")
            return fichas

    def subir_estandar(self, apuesta_maxima_actual):
        cantidad_minima_subir = apuesta_maxima_actual - self.fichas_comprometidas_fase
        cantidad_a_subir = Utilidades.preguntar_numero("Introduzca la cantidad que desea Subir: ",
                                                       cantidad_minima_subir, self.fichas)
        if cantidad_a_subir == cantidad_minima_subir:
            return self.igualar(apuesta_maxima_actual)

        self.apuesta(cantidad_a_subir)
        self.ha_actuado = True
        print(str(self.nombre) + f" ha subido {cantidad_a_subir} fichas.")
        print("")
        return cantidad_a_subir

    def no_ir(self):
        self.activo = False
        self.ha_actuado = True
        print(str(self.nombre) + " no ha ido.")
        print("")

    def info_igualar(self, apuesta_maxima_actual):
        cantidad_a_igualar = apuesta_maxima_actual - self.fichas_comprometidas_fase
        print(f"La cantidad a igualar sería de: {cantidad_a_igualar}")

    def fichas_igualadas(self, apuesta_maxima_actual):
        if self.fichas_comprometidas_fase == apuesta_maxima_actual:
            return True

    def info_jugador(self):
        print("===========================================")
        print(f"        Turno del jugador: {self.nombre}")
        print("Estas son sus cartas: ")
        self.dibujar_mano()
        print(f"Fichas disponible: {self.fichas}")
        print(f"Cantidad aportada: {self.fichas_comprometidas_fase}")

    def modo_allin(self):
        print("EL jugador esta en modo all-in")

