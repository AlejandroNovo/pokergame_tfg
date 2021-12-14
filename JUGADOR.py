class Jugador(object):

    def __init__(self, nombre):
        self.nombre = nombre
        self.mano = []
        self.roles = [] # [Dealer, Ciega_Peque, Ciega_Grande]
        self.fichas = 20
        self.activo = True

    def dibujar_mano(self):
        for carta in self.mano:
            carta.dibujar_carta()   # Duda como que podemos hacer ese dibujar_carta
        
    def asignar_rol(self, rol):
        self.roles.append(rol)

    def comprueba_fichas(self):
        if self.fichas == 0:
            return True
        
        return False

    def esBoton(self):
        if "Botón" in self.roles:
            return True
        
        return False



