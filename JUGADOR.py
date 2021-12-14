class Jugador(object):

    def __init__(self, nombre):
        self.nombre = nombre
        self.mano = []
        self.rol = [False, False, False] # [Dealer, Ciega_Peque, Ciega_Grande]
        self.fichas = 20
        self.activo = True

    def dibujar_mano(self):
        for carta in self.mano:
            carta.dibujar_carta()   # Duda como que podemos hacer ese dibujar_carta

    def asignar_rol(self, rol, valor):
        self.rol[rol] = valor

    def comprueba_fichas(self):
        if self.fichas == 0:
            return True
        else:
            return False


