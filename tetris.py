ANCHO_JUEGO, ALTO_JUEGO = 9, 18
IZQUIERDA, DERECHA = -1, 1
CUBO = 0
Z = 1
S = 2
I = 3
L = 4
L_INV = 5
T = 6


SUPERFICIE=2
VACIO=0
PARED_IZQUIERDA=0
PARED_DERECHA=ANCHO_JUEGO-1



def lector_rotacion():
    """Recibe las rotaciones de un archivo y las
    devuelve en una lista"""
    with open("piezas.txt") as f_rotacion:
        archivo=f_rotacion.readlines()
        diccionario={}
        total_piezas=[]
        pieza_transformada=[]
        pieza_actual=[]
        for i in archivo:
            i=(i.rstrip("\n").split("#"))
            piezas=i[0].split()
            pieza_transformada=[]
            for x in piezas:
                pieza_actual=[]
                x=x.split(";")
                for y in x:
                    if y[2]=="-":
                        y=int(y[0]),int(y[2]+y[3])
                    else:
                        y=int(y[0]),int(y[2])
                    pieza_actual.append(y)
                pieza_transformada.append(tuple(pieza_actual)) 
            total_piezas.append(pieza_transformada)
        return total_piezas

        

def lectura_piezas():
    """Recibe todas las rotaciones y carga unicamente las iniciales"""
    rotacion=lector_rotacion()
    lista=[]
    for i in range(0,len(rotacion)):
        lista.append(rotacion[i][0])
    return tuple(lista)
    
import random
def generar_pieza(pieza=None):
    """
    Genera una nueva pieza de entre PIEZAS al azar. Si se especifica el parámetro pieza
    se generará una pieza del tipo indicado. Los tipos de pieza posibles
    están dados por las constantes CUBO, Z, S, I, L, L_INV, T.

    El valor retornado es una tupla donde cada elemento es una posición
    ocupada por la pieza, ubicada en (0, 0). Por ejemplo, para la pieza
    I se devolverá: ( (0, 0), (0, 1), (0, 2), (0, 3) ), indicando que 
    ocupa las posiciones (x = 0, y = 0), (x = 0, y = 1), ..., etc.
    """
    lista_piezas=(CUBO, Z, S, I, L, L_INV, T)
    if pieza in lista_piezas:
        return lectura_piezas()[pieza]
    pieza=random.choice(lectura_piezas()) 
    return pieza
    


def trasladar_pieza(pieza, dx, dy):
    """
    Traslada la pieza de su posición actual a (posicion + (dx, dy)).

    La pieza está representada como una tupla de posiciones ocupadas,
    donde cada posición ocupada es una tupla (x, y). 
    Por ejemplo para la pieza ( (0, 0), (0, 1), (0, 2), (0, 3) ) y
    el desplazamiento dx=2, dy=3 se devolverá la pieza 
    ( (2, 3), (2, 4), (2, 5), (2, 6) ).
    """
    pieza_trasladada=[]
    for i in range(0, len(pieza)):
        lista=list(pieza[i])
        lista[0]+=dx
        lista[1]+=dy
        pieza_trasladada.append(tuple(lista))   
    return tuple(pieza_trasladada)


def crear_juego(pieza_inicial):
    """
    Crea un nuevo juego de Tetris.

    El parámetro pieza_inicial es una pieza obtenida mediante 
    pieza.generar_pieza. Ver documentación de esa función para más información.

    El juego creado debe cumplir con lo siguiente:
    - La grilla está vacía: hay_superficie da False para todas las ubicaciones
    - La pieza actual está arriba de todo, en el centro de la pantalla.
    - El juego no está terminado: terminado(juego) da False

    Que la pieza actual esté arriba de todo significa que la coordenada Y de 
    sus posiciones superiores es 0 (cero).
    """
    grilla=[]
    pieza_centrada=trasladar_pieza(pieza_inicial, ANCHO_JUEGO//2, 0)
    for filas in range(0,ALTO_JUEGO):
        grilla.append([0]*ANCHO_JUEGO)
    juego=grilla,pieza_centrada 
    return juego

def dimensiones(juego):
    ancho, alto=len(juego[0][0]), len(juego[0])
    """
    Devuelve las dimensiones de la grilla del juego como una tupla (ancho, alto).
    """
    return (ancho, alto)



def pieza_actual(juego):
    """
    Devuelve una tupla de tuplas (x, y) con todas las posiciones de la
    grilla ocupadas por la pieza actual.

    Se entiende por pieza actual a la pieza que está cayendo y todavía no
    fue consolidada con la superficie.

    La coordenada (0, 0) se refiere a la posición que está en la esquina 
    superior izquierda de la grilla.
    """
    pieza_actual=juego[1]
    return pieza_actual



def hay_superficie(juego, x, y):
    """
    Devuelve True si la celda (x, y) está ocupada por la superficie consolidada.
    
    La coordenada (0, 0) se refiere a la posición que está en la esquina 
    superior izquierda de la grilla.
    """
    if juego[0][y][x]==SUPERFICIE:
        return True
    return False


def mover(juego, direccion):
    """
    Mueve la pieza actual hacia la derecha o izquierda, si es posible.
    Devuelve un nuevo estado de juego con la pieza movida o el mismo estado 
    recibido si el movimiento no se puede realizar.

    El parámetro direccion debe ser una de las constantes DERECHA o IZQUIERDA.
    """
    pieza_baja=trasladar_pieza(pieza_actual(juego), direccion, 0)
    piezas_habilitadas=0
    for i in range(0,len(juego[1])):
        if direccion==IZQUIERDA:
            if pieza_baja[i][0]>=PARED_IZQUIERDA and juego[0][pieza_baja[i][1]][pieza_baja[i][0]]!=SUPERFICIE:
                # pieza_baja[i][0] es la coordenada x de la pieza y juego[0][juego[1][i][1]][juego[1][i][0]-1] es un casillero a la izquierda de la pieza
                piezas_habilitadas+=1
                if piezas_habilitadas==len(pieza_actual(juego)):                    
                    pieza_movida=trasladar_pieza(juego[1],IZQUIERDA, 0)
                    juego=juego[0],pieza_movida
     
        else:
            if pieza_baja[i][0]<=PARED_DERECHA and juego[0][pieza_baja[i][1]][pieza_baja[i][0]]!=SUPERFICIE:
                # juego[0][juego[1][i][1]][juego[1][i][0]+1] es un casillero a la derecha de la pieza
                piezas_habilitadas+=1
                if piezas_habilitadas==len(pieza_actual(juego)):
                    pieza_movida=trasladar_pieza(juego[1],DERECHA, 0)
                    juego=juego[0],pieza_movida          
    return juego        
    
def avanzar(juego, siguiente_pieza):
    """
    Avanza al siguiente estado de juego a partir del estado actual.
    
    Devuelve una tupla (juego_nuevo, cambiar_pieza) donde el primer valor
    es el nuevo estado del juego y el segundo valor es un booleano que indica
    si se debe cambiar la siguiente_pieza (es decir, se consolidó la pieza
    actual con la superficie).
    
    Avanzar el estado del juego significa:
     - Descender una posición la pieza actual.
     - Si al descender la pieza no colisiona con la superficie, simplemente
       devolver el nuevo juego con la pieza en la nueva ubicación.
     - En caso contrario, se debe
       - Consolidar la pieza actual con la superficie.
       - Eliminar las líneas que se hayan completado.
       - Cambiar la pieza actual por siguiente_pieza.

    Si se debe agregar una nueva pieza, se utilizará la pieza indicada en
    el parámetro siguiente_pieza. El valor del parámetro es una pieza obtenida 
    llamando a generar_pieza().

    **NOTA:** Hay una simplificación respecto del Tetris real a tener en
    consideración en esta función: la próxima pieza a agregar debe entrar 
    completamente en la grilla para poder seguir jugando, si al intentar 
    incorporar la nueva pieza arriba de todo en el medio de la grilla se
    pisara la superficie, se considerará que el juego está terminado.

    Si el juego está terminado (no se pueden agregar más piezas), la funcion no hace nada, 
    se debe devolver el mismo juego que se recibió.
    """
    cambiar_pieza=False
    piezas_habilitadas=0
    pieza_baja=trasladar_pieza(pieza_actual(juego), 0, 1)
    
    if not terminado(juego):
        for partes in range(0, len(pieza_actual(juego))):
            if pieza_baja[partes][1]<ALTO_JUEGO and juego[0][pieza_baja[partes][1]][pieza_baja[partes][0]]!=SUPERFICIE:
                #pieza_baja es la posicion a la que se desplazara la pieza
                piezas_habilitadas+=1
                if piezas_habilitadas==len(pieza_actual(juego)):
                    juego=juego[0],pieza_baja
                    return juego, cambiar_pieza
            else:
                juego=consolidar(juego)[0],trasladar_pieza(siguiente_pieza, ANCHO_JUEGO//2, 0)
                #la funcion consolidar, transforma la pieza en superficie y elimina filas si se encuentran todos los casilleros ocupados por superficie.
                cambiar_pieza=True
                return juego,cambiar_pieza
    return juego, cambiar_pieza

def consolidar(juego):
    for partes in range(0, len(pieza_actual(juego))):
        juego[0][pieza_actual(juego)[partes][1]][pieza_actual(juego)[partes][0]]+=SUPERFICIE
    for filas in range(0,ALTO_JUEGO):
        if all(juego[0][filas]):
            juego[0].pop(filas)
            juego[0].insert(0,[0]*ANCHO_JUEGO)
    return juego        
  
    
def terminado(juego):
    """
    Devuelve True si el juego terminó, es decir no se pueden agregar
    nuevas piezas, o False si se puede seguir jugando.
    """

    for partes in range(0,len(pieza_actual(juego))):
        if juego[0][pieza_actual(juego)[partes][1]][pieza_actual(juego)[partes][0]]==SUPERFICIE:
            return True

    return False
    
    
def rotar(juego, rotaciones):
    pieza_sin_rotar=pieza_actual(juego)
    pieza_ordenada=sorted(pieza_actual(juego))
    primera_posicion=pieza_ordenada[0]
    pieza_origen=trasladar_pieza(pieza_ordenada, -primera_posicion[0], -primera_posicion[1])
    for x in rotaciones:
        for i in range(0,len(x)):
            if x[i]==pieza_origen:
                if i+1==len(x):
                    siguiente_rotacion=x[0]
                else:
                    siguiente_rotacion=x[i+1]     
                pieza_rotada=trasladar_pieza(siguiente_rotacion, primera_posicion[0], primera_posicion[1])
                for y in range(0,len(siguiente_rotacion)):
                    if pieza_rotada[y][0]>PARED_DERECHA or pieza_rotada[y][0]<PARED_IZQUIERDA or juego[0][pieza_rotada[y][1]][pieza_rotada[y][0]]==SUPERFICIE or pieza_rotada[y][1]>=ALTO_JUEGO-1:                            
                        juego=juego[0],pieza_sin_rotar
                        return juego
                juego=juego[0],pieza_rotada
                return juego

