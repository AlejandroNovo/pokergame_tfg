class Utilidades:

    @staticmethod
    def preguntar_opcion(texto, opciones):
        valor = ""
        flag = False
        while not valor in opciones:
            if flag:
                print("Valor incorrecto, intente de nuevo.")
            valor = input(texto).upper()
            flag = True
        return valor

    @staticmethod
    def preguntar_numero(texto, minimo, maximo):
        valor = minimo-1
        flag = False
        while (valor < minimo) or (valor > maximo):
            if flag:
                print("Valor incorrecto, intente de nuevo.")
            valor = int(input(texto))
            flag = True
        return valor


