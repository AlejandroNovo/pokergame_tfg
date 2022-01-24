from JUGADOR import Jugador


class IA(Jugador):

    def __init__(self):

        Jugador.__init__(self)
        self.nombre = "IA"
        self.esIA = True
        self.atributogenericoIA = None
