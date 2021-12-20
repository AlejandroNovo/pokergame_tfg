class Utilidades:

    @staticmethod
    def preguntar_opcion(texto, opciones):
        valor = ""
        while not valor in opciones:
            valor = input(texto).upper()
        return valor

    @staticmethod
    def preguntar_numero(texto, minimo, maximo):
        valor = minimo-1
        while valor < minimo or valor > maximo:
            valor = int(input(texto))
        return valor
