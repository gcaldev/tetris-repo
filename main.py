import tetris
import gamelib
import csv
import partida
ESPERA_DESCENDER = 8
PUNTUACION_PIEZA_UBICADA=5

def dibujar_grilla(juego):  
    """Dibuja la grilla utilizando las
    dimensiones dadas en el archivo tetris"""
    posicion_pieza=tetris.pieza_actual(juego)
    ancho,alto=tetris.dimensiones(juego)
    gamelib.draw_image('img/background_piedra3.gif', 0, 0)
    numero_fila=0
    numero_columna=0
    gamelib.title("Tetris")
    for fila in range(0,alto):
        for columna in range(0,ancho):
            gamelib.draw_rectangle(30*columna+60, 30*fila+60, 30*columna+90, 30*fila+90, outline="white", fill="black")
            numero_columna+=1
            if juego[0][numero_fila][numero_columna-1]==2: #Esta condicion chequea si hay superficie consolidada en el lugar
                gamelib.draw_rectangle(30*(columna)+60, 30*(fila)+60, 30*(columna)+90, 30*(fila)+90, outline="white", fill="violet")

            if not tetris.terminado(juego):     
                if (numero_columna-1,numero_fila) in posicion_pieza:
                    gamelib.draw_rectangle(30*columna+60, 30*fila+60, 30*columna+90, 30*fila+90, outline="white", fill="green")
            else:
                if (numero_columna-1,numero_fila) in posicion_pieza:
                    gamelib.draw_rectangle(30*columna+60, 30*fila+60, 30*columna+90, 30*fila+90, outline="white", fill="red")
        numero_fila+=1
        numero_columna=0     
    gamelib.draw_image('img/marcov5.gif', -15, 12)

def dibujar_siguiente(juego,siguiente_pieza):
    """Recibe la siguiente pieza y la dibuja"""
    ancho,alto=tetris.dimensiones(juego)
    numero_fila=0
    numero_columna=0
    for fila in range(0,alto):
        for columna in range(0,ancho):
            numero_columna+=1
            if (numero_columna-1,numero_fila) in siguiente_pieza:
                gamelib.draw_rectangle(15*columna+175, 15*fila+625, 15*columna+190, 15*fila+640, outline="white", fill="grey")
        numero_fila+=1
        numero_columna=0 

def dibujar_score(lista):
    """Recibe la lista de los 10 mejores puntajes
    y la muestra en pantalla"""
    gamelib.draw_image('img/background_piedra3.gif', 0, 0)
    gamelib.draw_text("TOP 10", 197, 125, 50)
    gamelib.draw_text("JUGADORES", 197, 180, 35)
    for i in range(0,len(lista)):
        gamelib.draw_text(f"{1+i}-{lista[i][0]}-{lista[i][1]} pts.", 195, 230+i*30, 17)

def funcion_teclas():
    """Recorre el archivo, omite los espacios vacíos y se
    almacenan las teclas y sus acciones en un diccionario"""
    lista={}
    with open("teclas.txt") as f_teclas:
        for linea in f_teclas:
            linea=linea.strip()
            if linea!="":
                x=linea.split("=")
                lista[x[0].rstrip()]=x[1].lstrip()
        return lista



def main():
    # Inicializar el estado del juego
    validador=False
    top=None
    puntuacion_total=0
    gamelib.resize(395, 700)
    juego=tetris.crear_juego(tetris.generar_pieza())
    timer_bajar = ESPERA_DESCENDER
    rotaciones=tetris.lector_rotacion()
    siguiente_pieza=tetris.generar_pieza()  
    while gamelib.loop(fps=30):
        gamelib.draw_begin()
        # Dibujar la pantalla
        dibujar_grilla(juego)
        dibujar_siguiente(juego,siguiente_pieza)
        gamelib.draw_text("Puntuacion", 300, 645, fill='white', size=17)
        gamelib.draw_text(f"Total: {puntuacion_total}", 300, 665, fill='white', size=17)
        if tetris.terminado(juego) and not validador:  #Esta validación chequea si ya ingreso el usuario para que no pida mas veces el gamelib.input
            top=partida.guardar_puntaje(juego,puntuacion_total)
            validador=True
        if validador:
            dibujar_score(top)
        gamelib.draw_end()
        for event in gamelib.get_events():
            if not event:
              break
            if event.type == gamelib.EventType.KeyPress:
                tecla = event.key
                teclas=funcion_teclas()
                if tecla in teclas.keys():
                    if not tetris.terminado(juego):
                        if teclas[tecla]=="IZQUIERDA":
                            juego=tetris.mover(juego,tetris.IZQUIERDA)
                        if teclas[tecla]=="DERECHA":
                            juego=tetris.mover(juego,tetris.DERECHA)
                        if teclas[tecla]=="DESCENDER":
                            juego,cambiar_pieza=tetris.avanzar(juego,siguiente_pieza)
                            if cambiar_pieza:
                                siguiente_pieza=tetris.generar_pieza()
                                puntuacion_total+=PUNTUACION_PIEZA_UBICADA
                        if teclas[tecla]=="SALIR":
                            return
                        if teclas[tecla]=="GUARDAR":
                            partida.guardar_partida(juego,puntuacion_total)
                        if teclas[tecla]=="CARGAR":
                            if partida.cargar_partida()!=None: #Esta condición evita que se intente desempaquetar ya que no se guardo una partida antes
                                juego,puntuacion_total=partida.cargar_partida()
                        if teclas[tecla]=="ROTAR":
                            juego=tetris.rotar(juego, rotaciones)

                    else:
                        if teclas[tecla]=="SALIR":
                            return
              # Actualizar el juego, según la tecla presionada
        timer_bajar -= 1
        if timer_bajar == 0:
            timer_bajar = ESPERA_DESCENDER
            juego,cambiar_pieza=tetris.avanzar(juego,siguiente_pieza)
            if cambiar_pieza:
                siguiente_pieza=tetris.generar_pieza()
                puntuacion_total+=PUNTUACION_PIEZA_UBICADA
            # Descender la pieza automáticamente

            
gamelib.init(main)