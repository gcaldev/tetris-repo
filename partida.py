import csv
import gamelib
import tetris
grilla_guardada_vacia=""

def guardar_puntaje(juego,puntuacion_jugador):
    """Recibe la puntuacion del jugador y el juego,
    le pide al usuario que ingrese su nombre y lo almacena"""
    lista_puntuaciones=[]
    username=gamelib.input("Ingrese su nombre de usuario")
    if not username:
        username="Unnamed"
    username=username.replace(","," ")#En caso de que el usuario ingrese una coma se reemplaza por un espacio para evitar errores al cargar los puntajes
    try:
        with open("puntuaciones.txt","r")as mejores_puntuaciones:
            puntuaciones_anteriores=csv.reader(mejores_puntuaciones)
            for i in puntuaciones_anteriores:
                lista_puntuaciones.append(i)
    except FileNotFoundError:
        pass
    lista_puntuaciones.append([username,puntuacion_jugador])
    lista_puntuaciones=sorted(lista_puntuaciones,key=lambda puntos:int(puntos[1]), reverse=True)#La funcion lambda permite transformar los numeros recibidos a entero y ordenar los puntajes en base a estos
    if len(lista_puntuaciones)==11:
        lista_puntuaciones.pop(len(lista_puntuaciones)-1)
    with open("puntuaciones.txt","w")as puntuaciones:
        for i in range(0,len(lista_puntuaciones)):
            puntuaciones.write(f"{lista_puntuaciones[i][0]},{lista_puntuaciones[i][1]}\n")
    return lista_puntuaciones
          
def guardar_partida(juego,puntuacion):
    """Recibe el estado de juego actual y la puntuacion actual
    y los guarda
    """
    posiciones_ocupadas=""
    pieza_posicion=""
    with open("savedata.txt","w")as f_guardar:
        for y in range(0,len(juego[0])):
            for x in range(0,len(juego[0][1])):
                if juego[0][y][x]==2: #Se almacena unicamente los lugares ocupados en la grilla
                    posiciones_ocupadas+=f"{x},{y};"
        for i in tetris.pieza_actual(juego):
            pieza_posicion+=f"{i[0]},{i[1]};"
        posiciones_ocupadas=posiciones_ocupadas[:-1]
        pieza_posicion=pieza_posicion[:-1]
        f_guardar.write(f"{posiciones_ocupadas}-{pieza_posicion}-{puntuacion}")

def cargar_partida():
    """Lee el archivo en el que se guardo la partida
    y carga el estado de juego actual y la puntuacion actual"""
    grilla_vacia=[]
    for filas in range(0,tetris.ALTO_JUEGO):
        grilla_vacia.append([0]*tetris.ANCHO_JUEGO)
    try:
        with open("savedata.txt")as f_cargar:
            data=f_cargar.read().split("-")
            posiciones_ocupadas=data[0]
            puntos=int(data[2])
            posiciones_ocupadas=posiciones_ocupadas.split(";")
            posiciones_lista=[]
            if posiciones_ocupadas!=grilla_guardada_vacia:
                for porciones_ocupadas in posiciones_ocupadas: #Se coloca cada porcion de la superficie consolidada en una grilla vacia
                    porciones_ocupadas=porciones_ocupadas.split(",")
                    eje_x,eje_y=(int(porciones_ocupadas[0]),int(porciones_ocupadas[1]))
                    for y in range(0,len(grilla_vacia)):
                        for x in range(0,len(grilla_vacia[0])):
                            if y==eje_y and x==eje_x:
                                grilla_vacia[y][x]+=2       
            pieza_guardada=data[1].split(";")
            pieza_lista=[]
            for porcion_pieza in pieza_guardada: #Se hace entero cada parte de la pieza guardada
                porcion_pieza=porcion_pieza.split(",") 
                pieza_lista.append((int(porcion_pieza[0]),int(porcion_pieza[1])))
            return (grilla_vacia,tuple(pieza_lista)),puntos
    except FileNotFoundError:
        gamelib.say("Debe guardar una partida para poder cargarla")
