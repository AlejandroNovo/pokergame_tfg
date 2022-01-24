class Carta(object):

    def __init__(self, valor, palo):
        self.valor = valor
        self.palo = palo

    def dibujar_carta(self):
        print(f"                      [{self.valor}-{self.palo}]")











