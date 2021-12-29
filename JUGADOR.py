from Utilidades import Utilidades


class Jugador(object):

    def __init__(self, nombre):
        self.nombre = nombre
        self.mano = []
        self.roles = []  # [Dealer, Ciega_Peque, Ciega_Grande]
        self.fichas = 20
        self.activo = True
        self.fichas_comprometidas_fase = 0

    def dibujar_mano(self):
        for carta in self.mano:
            carta.dibujar_carta()
        
    def asignar_rol(self, rol):
        self.roles.append(rol)

    def aniadir_carta(self, carta):
        self.mano.append(carta)

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
        self.fichas -= fichas_descontar
        self.fichas_comprometidas_fase += fichas_descontar

    def igualar(self, apuesta_maxima_actual):
        cantidad_a_igualar = apuesta_maxima_actual - self.fichas_comprometidas_fase
        if cantidad_a_igualar <= self.fichas:
            self.apuesta(cantidad_a_igualar)
            return cantidad_a_igualar

        else:
            # cosas de all-in (para mas tarde)
            pass

    def subir(self, apuesta_maxima_actual):

        cantidad_a_subir = Utilidades.preguntar_numero("Introduzca la cantidad que desea Subir: ",
                                                       apuesta_maxima_actual, self.fichas)
        self.apuesta(cantidad_a_subir)
        return cantidad_a_subir

    def no_ir(self):
        self.activo = False




