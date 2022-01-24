import JUEGO


class Evaluador:

    def __init__(self, lista_jugadores, cartas_mesa):
        self.lista_jugadores = lista_jugadores
        self.cartas_mesa = cartas_mesa

    def orquestar_evaluador(self):
        jugadores_activos = []
        for jugador in self.lista_jugadores:
            if jugador.activo:
                jugadores_activos.append(jugador)
        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        for jugador in jugadores_activos:
            self.comparador_combinacion(jugador)
            jugador.valor_final = self.conversor_letras(jugador.valor_mano)
            jugador.valor_final = ("".join(jugador.valor_final))
            jugador.valor_final = int(jugador.valor_final, 16)

        valor_maximo = 0
        for jugador in jugadores_activos:
            if jugador.valor_final >= valor_maximo:
                valor_maximo = jugador.valor_final
            else:
                continue

        jugadores_ganadores = []
        for jugador in jugadores_activos:
            if jugador.valor_final == valor_maximo:
                jugadores_ganadores.append(jugador)

        return jugadores_ganadores

    def comparador_combinacion(self, jugador):
        cartas_totales = jugador.mano + self.cartas_mesa
        valores = self.vector_valores(cartas_totales)
        palos = self.vector_palos(cartas_totales)

        escalera_real = self.es_escalera_real(cartas_totales, palos)
        if escalera_real:
            jugador.valor_mano[0] = 10
            print(f"El jugador {jugador.nombre} tiene escalera real")
            return

        escalera_color = self.es_escalera_color(cartas_totales, palos)
        if escalera_color[0]:
            jugador.valor_mano[0] = 9
            jugador.valor_mano[1] = escalera_color[1]
            print(f"El jugador {jugador.nombre} tiene escalera de color con la carta mas alta de: {escalera_color[1]}")
            return

        poker = self.es_poker(valores)
        if poker[0]:
            jugador.valor_mano[0] = 8
            jugador.valor_mano[1] = poker[1]
            jugador.valor_mano[2] = poker[2]
            print(f"El jugador {jugador.nombre} tiene poker de: {poker[1]}, con kicker: {poker[2]}")
            return

        full = self.es_full(valores)
        if full[0]:
            jugador.valor_mano[0] = 7
            jugador.valor_mano[1] = full[1]
            jugador.valor_mano[2] = full[2]
            print(f"El jugador {jugador.nombre} tiene full house con un trio de: {full[1]} y una pareja de: {full[2]}")
            return

        color = self.es_color(cartas_totales, palos)
        if color[0]:
            jugador.valor_mano[0] = 6
            valores_color = self.vector_valores(color[1])
            valores_color.sort(reverse=True)
            for i in range(len(valores_color)):
                jugador.valor_mano[i+1] = valores_color[i]
            print(f"El jugador {jugador.nombre} tiene color con las cartas:")
            for carta in color[1]:
                carta.dibujar_carta()
            return

        escalera = self.es_escalera(valores)
        if escalera[0]:
            jugador.valor_mano[0] = 5
            jugador.valor_mano[1] = escalera[1]
            print(f"El jugador {jugador.nombre} tiene escalera con la carta mas alta de: {escalera[1]}")
            return

        trio = self.es_trio(valores)
        if trio[0]:
            jugador.valor_mano[0] = 4
            cartas_resto = trio[2]
            cartas_resto.sort(reverse=True)
            for i in range(2):
                jugador.valor_mano[i + 1] = cartas_resto[i]
            print(f"El jugador {jugador.nombre} tiene trio de: {trio[1]}, con kickers:"
                  f" {cartas_resto[0]}, {cartas_resto[1]}")
            return

        doble_pareja = self.es_doble_pareja(valores)
        if doble_pareja[0]:
            if doble_pareja[1] > doble_pareja[2]:
                pareja_mayor = doble_pareja[1]
                pareja_menor = doble_pareja[2]
            else:
                pareja_mayor = doble_pareja[2]
                pareja_menor = doble_pareja[1]
            jugador.valor_mano[0] = 3
            jugador.valor_mano[1] = pareja_mayor
            jugador.valor_mano[2] = pareja_menor
            jugador.valor_mano[3] = doble_pareja[3]
            print(f"El jugador {jugador.nombre} tiene doble pareja de: {pareja_mayor} y {pareja_menor},"
                  f" con kicker: {doble_pareja[3]}")
            return

        pareja = self.es_pareja(valores)
        if pareja[0]:
            jugador.valor_mano[0] = 2
            jugador.valor_mano[1] = pareja[1]
            cartas_resto = pareja[2]
            cartas_resto.sort(reverse=True)
            for i in range(3):
                jugador.valor_mano[i + 2] = cartas_resto[i]
            print(f"El jugador {jugador.nombre} tiene pareja de: {pareja[1]}, con kickers:"
                  f" {cartas_resto[0]}, {cartas_resto[1]}, {cartas_resto[2]}")
            return

        carta_alta = self.es_carta_alta(valores)
        if carta_alta[0]:
            cartas_resto = carta_alta[1]
            cartas_resto.sort(reverse=True)
            jugador.valor_mano[0] = 1
            for i in range(5):
                jugador.valor_mano[i + 1] = cartas_resto[i]
            print(f"El jugador {jugador.nombre} tiene carta alta: {cartas_resto[0]}, con kickers:"
                  f" {cartas_resto[1]}, {cartas_resto[2]}, {cartas_resto[3]}, {cartas_resto[4]}")
            return

#################################################################################################################

    def es_escalera_real(self, mano, palos):
        escalera_color = self.es_escalera_color(mano, palos)
        if escalera_color[0] and escalera_color[1] == 14:
            return True
        return False

    def es_escalera_color(self, mano, palos):
        color = self.es_color(mano, palos)
        if color[0]:
            comprobar_escalera = color[1]
            valores = self.vector_valores(comprobar_escalera)
            escalera = self.es_escalera(valores)
            if escalera[0]:
                return True, escalera[1]
        return False, 0

    def es_poker(self, valores):
        valores_copia = []
        for valor in valores:
            valores_copia.append(valor)
        for valores_mano in valores_copia:
            if valores_copia.count(valores_mano) == 4:
                numero_poker = valores_mano
                for i in range(4):
                    valores_copia.remove(valores_mano)
                return True, numero_poker, max(valores_copia)
        return False, 0, 0

    def es_full(self, valores):
        trio = self.es_trio(valores)
        pareja = self.es_pareja(valores)
        if trio[0] and pareja[0]:
            return True, trio[1], pareja[1]
        return False, 0, 0

    def es_color(self, mano, palos):
        flag = False
        cartas_color = []
        for carta in mano:
            if palos.count(carta.palo) >= 5:
                flag = True
                cartas_color.append(carta)
        if flag:
            return True, cartas_color
        return False, cartas_color

    def es_escalera(self, valores):
        valores_numericos = []
        for valor in valores:
            valores_numericos.append(valor)
        valores_numericos.sort()
        n_valores = len(valores_numericos)
        contador = 0
        if (14 in valores_numericos) and (valores_numericos[0] == 2):
            contador += 1
        for i in range(n_valores - 1):
            if valores_numericos[i] == valores_numericos[i + 1] - 1:
                contador += 1
            elif valores_numericos[i] == valores_numericos[i + 1]:
                pass
            else:
                contador = 0
            if contador >= 4:
                carta_mas_alta = valores_numericos[i + 1]
                if i < n_valores - 2:
                    if valores_numericos[i + 1] == valores_numericos[i + 2] - 1:
                        continue
                    if valores_numericos[i + 1] == valores_numericos[i + 2]:
                        continue
                return True, carta_mas_alta
        return False, 0

    def es_trio(self, valores):
        valores_copia = []
        for valor in valores:
            valores_copia.append(valor)
        for valores_mano in valores_copia:
            if valores_copia.count(valores_mano) == 3:
                numero_trio = valores_mano
                for i in range(3):
                    valores_copia.remove(valores_mano)
                return True, numero_trio, valores_copia
        return False, 0, 0

    def es_doble_pareja(self, valores):
        valores_copia = []
        for valor in valores:
            valores_copia.append(valor)

        pareja_primera = self.es_pareja(valores_copia)
        if pareja_primera[0]:
            for i in range(2):
                valores_copia.remove(pareja_primera[1])

        pareja_segunda = self.es_pareja(valores_copia)
        if pareja_segunda[0]:
            for i in range(2):
                valores_copia.remove(pareja_segunda[1])
            return True, pareja_primera[1], pareja_segunda[1], max(valores_copia)

        return False, 0, 0, 0

    def es_pareja(self, valores):
        valores_copia = []
        for valor in valores:
            valores_copia.append(valor)

        for valores_mano in valores_copia:
            if valores_copia.count(valores_mano) == 2:
                numero_pareja = valores_mano
                for i in range(2):
                    valores_copia.remove(valores_mano)
                return True, numero_pareja, valores_copia
        return False, 0, 0

    def es_carta_alta(self, valores):
        return True, valores

#################################################################################################################

    def vector_valores(self, lista):
        valores = []
        for carta in lista:
            if carta.valor == "T":
                valores.append(10)
            elif carta.valor == "J":
                valores.append(11)
            elif carta.valor == "Q":
                valores.append(12)
            elif carta.valor == "K":
                valores.append(13)
            elif carta.valor == "A":
                valores.append(14)
            else:
                valores.append(int(carta.valor))
        return valores

    def vector_palos(self, lista):
        palos = []
        for carta in lista:
            palos.append(carta.palo)
        return palos

    def conversor_letras(self, vector):
        valores = []
        for numero in vector:
            if numero == 10:
                valores.append("A")
            elif numero == 11:
                valores.append("B")
            elif numero == 12:
                valores.append("C")
            elif numero == 13:
                valores.append("D")
            elif numero == 14:
                valores.append("E")
            else:
                valores.append(str(numero))
        return valores





