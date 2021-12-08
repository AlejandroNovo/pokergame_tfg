class Carta(object):

    def __init__(self, valor, palo):
        self.valor = valor
        self.palo = palo

    ''' def __str__(self):
        return "[{}-{}]".format(self.valor, self.palo)'''

    def dibujar_carta(self):
        print("[{}-{}]".format(self.valor, self.palo))









