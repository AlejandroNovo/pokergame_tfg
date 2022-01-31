from JUEGOIA import *

print("-------------------------------------------")
print("          POKER TEXAS HOLD'EM")
print("-------------------------------------------")

respuesta = Utilidades.preguntar_opcion_num("1. Partida convecional con multiples jugadores.\n"
                                            "2. Partida contra Inteligencia Artificial.\n"
                                            "Elija el modo de juego: ", [1, 2])
print("")
if respuesta == 1:
    print("++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("     Partida convecional con multiples jugadores")
    print("++++++++++++++++++++++++++++++++++++++++++++++++++")

    print("")
    juego = Juego()
    juego.orquestar()
    print("Gracias por jugar.")

if respuesta == 2:
    print("++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("    Partida contra Inteligencia Artificial")
    print("++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("")
    juego = JuegoIA()
    juego.orquestar()

    print("Gracias por jugar.")


