import random
from EVALUADOR import Evaluador
from JUGADOR import Jugador
from random import choice

class JugadorIA(Jugador):

    def __init__(self):

        Jugador.__init__(self)
        self.nombre = "IA"
        self.esIA = True
        self.posicion = False
        self.han_subido = False
        self.pocket_pair = False
        self.suited = False

    def subir_ia(self, tipo_subida, bote, apuesta_maxima_actual):
        cantidad_a_subir = 0
        cantidad_minima_subir = apuesta_maxima_actual - self.fichas_comprometidas_fase

        # en funcion del tipo_subida se pasa un valor a subir u otro

        if tipo_subida == "subida_estandar":
            # cantidad_a_subir = int(bote/3)
            cantidad_a_subir = random.randint(cantidad_minima_subir, int(bote/3))
            if cantidad_a_subir >= self.fichas:                              # Pero no puede pasarse del cantidad total
                cantidad_a_subir = self.fichas
            print(f"SUBIDA ESTANDAR, LA CANTIDAD A SUBIR ES {cantidad_a_subir}")

        elif tipo_subida == "subida_media":
            cantidad_a_subir = round(bote/2)
            if cantidad_a_subir >= self.fichas:
                cantidad_a_subir = self.fichas
            elif cantidad_a_subir <= cantidad_minima_subir:
                cantidad_a_subir = cantidad_minima_subir
            print(f"SUBIDA MEDIA, LA CANTIDAD A SUBIR ES {cantidad_a_subir}")

        elif tipo_subida == "subida_fuerte":
            cantidad_a_subir = int(bote)
            if cantidad_a_subir >= self.fichas:
                cantidad_a_subir = self.fichas
            elif cantidad_a_subir <= cantidad_minima_subir:
                cantidad_a_subir = cantidad_minima_subir
            print(f"SUBIDA FUERTE, LA CANTIDAD A SUBIR ES {cantidad_a_subir}")

        elif tipo_subida == "subida_muy_fuerte":
            cantidad_a_subir = int(2*bote)
            if cantidad_a_subir >= self.fichas:
                cantidad_a_subir = self.fichas
            elif cantidad_a_subir <= cantidad_minima_subir:
                cantidad_a_subir = cantidad_minima_subir
            print(f"SUBIDA MUY FUERTE, LA CANTIDAD A SUBIR ES {cantidad_a_subir}")

        self.apuesta(cantidad_a_subir)
        self.ha_actuado = True
        return cantidad_a_subir

    def tomar_decision(self, mesa, ultima_apuesta_rival):
        bote_mesa = mesa.bote_fase
        cartas_evaluar = self.mano + mesa.cartas_mesa
        print(f"Ultima apuesta del rival : {ultima_apuesta_rival}")
        if len(cartas_evaluar) == 2:
            return self.decision_preflop(bote_mesa, ultima_apuesta_rival)

        elif len(cartas_evaluar) == 5:
            return self.decision_flop()

        elif len(cartas_evaluar) == 6:
            return self.decision_turn()

        elif len(cartas_evaluar) == 7:
            return self.decision_river()

    def decision_preflop(self, bote, ultima_apuesta_rival):
        print("Decision Pre-Flop")
        valor_fuerza_mano = self.fuerza_mano()
        print(valor_fuerza_mano)

        igual = self.comprueba_igualdad(bote, ultima_apuesta_rival)
        if igual[0]:
            print("Estamos iguales, no ha subido")
            # si no ha subido es por que ha limpeado, le apostamos a saco, vamos a subir
            if 4 <= valor_fuerza_mano <= 5:
                return "S4"
            elif 2 <= valor_fuerza_mano <= 3:
                return "S3"
            elif 0 <= valor_fuerza_mano <= 1:
                return "S2"

        elif not igual[0]:                     # Apostamos en funcion de lo que haya subido ellos y la fuerza de nuestra mano
            cantidad_subida = igual[1]

            if cantidad_subida != 0:                  # Si es diferente de cero es pq aun subido manualmente, entonces comprobamos la fuerza y actuamos
                fuerza_subida = igual[2]
                print(f"No estamos iguales, han subido {cantidad_subida}")
                print(f"La fuerza de su subida es {fuerza_subida}")
                if fuerza_subida == 4:
                    if valor_fuerza_mano == 5:
                        return "S4"
                    elif valor_fuerza_mano == 4:
                        return "S3"
                    elif 2 <= valor_fuerza_mano <= 3:
                        return "I"
                    elif 0 <= valor_fuerza_mano <= 1:
                        return "N"
                elif fuerza_subida == 3:
                    if 4 <= valor_fuerza_mano <= 5:
                        return "S4"
                    elif 2 <= valor_fuerza_mano <= 3:
                        return "S2"
                    elif 0 <= valor_fuerza_mano <= 1:
                        return "N"
                elif fuerza_subida == 2:
                    if 4 <= valor_fuerza_mano <= 5:
                        return "S3"
                    elif 2 <= valor_fuerza_mano <= 3:
                        return "S1"
                    elif 0 <= valor_fuerza_mano <= 1:
                        return "I"
                elif fuerza_subida == 1:
                    if 4 <= valor_fuerza_mano <= 5:
                        return "S4"
                    elif 2 <= valor_fuerza_mano <= 3:
                        return "S2"
                    elif 0 <= valor_fuerza_mano <= 1:
                        return "S1"

            elif cantidad_subida == 0:                        # si es igual a cero es pq no han subido, es que solo toca hablar primero e igualar bote
                print("Estamos primer turno, hablamos primero")
                if 4 <= valor_fuerza_mano <= 5:
                    return "S4"
                elif 2 <= valor_fuerza_mano <= 3:
                    return "S1"
                elif 0 <= valor_fuerza_mano <= 1:
                    return "I"

    def fuerza_mano(self):

        evaluador = Evaluador(self, 0)
        valores = evaluador.vector_valores(self.mano)
        palos = evaluador.vector_palos(self.mano)
        contador_fuerza = 0

        if self.comprueba_posicion():
            contador_fuerza += 1
        if self.comprueba_pocket_pair(valores):
            contador_fuerza += 2
        if self.comprueba_suited(palos):
            contador_fuerza += 1
        fuerza_rango = self.compueba_rango_valores(valores)
        contador_fuerza += fuerza_rango
        return contador_fuerza

    def comprueba_igualdad(self, bote, ultima_apuesta_rival):
        bote_antes = bote - ultima_apuesta_rival
        if self.fichas_comprometidas_fase == bote/2:     # estamos igualados, no han subido
            # self.han_subido = False
            return True, 0, 0
        elif bote == 3 and self.posicion:                # Somos ciega_peque, primeros en hablar
            ultima_apuesta_rival = 0
            return False, ultima_apuesta_rival, 0
        else:                                            # han subido
            # self.han_subido = True
            fuerza_subida = 0
            if ultima_apuesta_rival > bote_antes:
                fuerza_subida = 4
            elif (bote_antes/2) < ultima_apuesta_rival <= bote_antes:
                fuerza_subida = 3
            elif (bote_antes/3) < ultima_apuesta_rival <= (bote_antes/2):
                fuerza_subida = 2
            elif 0 <= ultima_apuesta_rival <= (bote_antes/3):
                fuerza_subida = 1
            return False, ultima_apuesta_rival, fuerza_subida


    def comprueba_posicion(self):
        if self.es_boton():
            self.posicion = True
            return True
        else:
            self.posicion = False
            return False

    def compueba_rango_valores(self, valores):
        sum = valores[0] + valores[1]
        if 4 <= sum <= 10:
            return 0
        elif 11 <= sum <= 20:
            return 1
        elif 21 <= sum <= 28:
            return 2

    def comprueba_pocket_pair(self, valores):
        for valor in valores:
            if valores.count(valor) == 2:
                # self.pocket_pair = True
                return True
        return False

    def comprueba_suited(self, palos):
        for palo in palos:
            if palos.count(palo) == 2:
                # self.suited = True
                return True
        return False

    def decision_flop(self):
        print("Decision Flop")

    def decision_turn(self):
        print("Decision Turn")
        pass

    def decision_river(self):
        print("Decision River")
        pass


