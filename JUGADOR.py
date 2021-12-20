from Utilidades import Utilidades


class Jugador(object):

    def __init__(self, nombre):
        self.nombre = nombre
        self.mano = []
        self.roles = [] # [Dealer, Ciega_Peque, Ciega_Grande]
        self.fichas = 20
        self.activo = True
        self.apuesta_actual = 0

    def dibujar_mano(self):
        for carta in self.mano:
            carta.dibujar_carta()   # Duda como que podemos hacer ese dibujar_carta
        
    def asignar_rol(self, rol):
        self.roles.append(rol)

    def comprueba_fichas(self):
        if self.fichas == 0:
            return True
        return False

    def es_boton(self):
        if "Botón" in self.roles:
            return True
        return False

    def apuesta(self, fichas_descontar):
        self.fichas -= fichas_descontar

    def acciones(self, apuesta_maxima_actual):
        print("Estas son sus dos cartas " + str(self.nombre) + ":")
        self.dibujar_mano()

        if self.apuesta_actual == apuesta_maxima_actual:
            opciones = Utilidades.preguntar_opcion("Acciones a realizar: P=Pasar I=Igualar S=Subir N=No ir\n"
                                                   "Indique una accion: ", ["P", "I", "S", "N"])
            if opciones == "P":
                print(str(self.nombre) + " ha pasado.")
            elif opciones == "I":
                print(str(self.nombre) + " ha igualado.")
            elif opciones == "S":
                print(str(self.nombre) + " ha subido.")
            elif opciones == "N":
                print(str(self.nombre) + " no ha ido.")
            else:
                pass
        else:
            opciones = Utilidades.preguntar_opcion("Acciones a realizar: I=Igualar S=Subir N=No ir\n"
                                                   "Indique una accion: ", ["I", "S", "N"])
            if opciones == "I":
                print(str(self.nombre) + " ha igualado.")
            elif opciones == "S":
                print(str(self.nombre) + " ha subido.")
            elif opciones == "N":
                print(str(self.nombre) + " no ha ido.")
            else:
                pass






