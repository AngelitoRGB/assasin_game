# El juego consiste en hacer jugar a mayores de edad por un lado y menores de edad por
# otro. En cada etapa de jugada se deberían hacer las asignaciones en forma aleatoria
# teniendo en cuenta que si hay dos personas que residen en la misma ciudad deberían
# asignarse. En caso de que una persona no tenga otra persona residente en la misma
# localidad para enfrentarse se le debe asignar alguien de la localidad más cercana a la
# suya. Por supuesto que siempre se debe respetar la limitación del N ingresado. Puede
# ser que un participante quede libre en alguna ronda porque no tiene con quién enfrentarse
# en el radio en el que vive. Además, cada enfrentamiento debería consisitir en elegir un
# ganador en forma aleatoria. El proceso continúa hasta que se tiene un único sobreviviente
# en cada categoria (mayores y menores de edad) o, quienes sobrevivieron están a una
# distancia mayor a N dos a dos.

from random import*

# ingresar_jugadores: None -> List(tuples)
# Se ingresa la lista de jugadores (Un archivo.txt)
# Cada jugador es ("Nombre_Jugador,Edad,Ciudad")
def ingresar_jugadores():
    archivo  =  input("Ingrese los jugadores: ")
    jugadores  =  open(archivo) 
    nombres  =  jugadores.readlines()
    return nombres  

# ingresar_distancias: None -> List(Strings)
#Se ingresa la lista de distancias entre 2 ciudades
# Cada elemento de la lista es ("Ciudad,ciudad2,distancia")
def ingresar_distancias():
    archivo2 = input("Ingrese las distancias: ")
    distancias = open(archivo2)
    dist = distancias.readlines()
    return dist


# ingresar_N: None -> Number
# Se ingresa la distancia maxima en la que se pueden enfrentar los jugadores
def ingresar_N():
    N = float(input("Distancia maxima de enfrentamiento: "))
    return N


# clasificacion: None -> List(Tuples), List(Tuples)
# Clasifica a los jugadores según si son mayores o menores de edad
def clasificacion():
    
    players_adults = []
    players_youngers = []
    
    for info_jugador in ingresar_jugadores():
        jugador = tuple(info_jugador.split(","))
        if int(jugador[1]) >= 18:
            players_adults.append(jugador)
        else:
            players_youngers.append(jugador)
    
    return players_youngers,players_adults

# distancias_ciudades: None -> List(Tuples)
# Devuelve una lista de tuplas con las distancias de las ciudades
# invocando a la funcion ingresar_distancias()
# Cada tupla seria ("Ciudad", "Ciudad2", "Distancia")
def distancias_ciudades():
    citys = []
    for info_ciudad in ingresar_distancias():
        ciudad = tuple(info_ciudad.split(", "))
        citys.append(ciudad)
    return citys

# enfrentt: Tuple, Tuple, List(Tuples), List(Strings) -> List(Tuples), List(Strings)
# Toma dos jugadores, y las respectivas listas, luego enfrenta a ambos jugadores
# eligiendo un ganador aleatorio, al ganador lo agrega a winners y agrega
# a output el resultado del enfrentamiento
def enfrentt(J1,J2,winners,output):
    x = randint(1, 2)
    if x == 1:
        winners.append(J1)
        output.append(J1[0]+ "  elimino a " + J2[0]+ "\n")
    else:
        winners.append(J2)
        output.append(J2[0]+ "  elimino a " + J1[0]+ "\n")
    return winners, output


# misma_city: List(Tuples), List(Tuples), List(Strings) -> List(Tuples), List(Tuples), List(Strings)
# Toma la lista de los jugadores, y compara el primer jugador con el segundo, si son de la misma ciudad
# los enfrenta y saca ambos jugadores de la lista, caso contrario sigue iterando.

def misma_city(list_players,winners,output):
    index1 = 0
    index2 = index1 + 1
    while index1 < (len(list_players)-1) and list_players:
        valor = False
        while index2 < len(list_players) and not(valor):
            J1 = list_players[index1]
            J2 = list_players[index2]
            if J1[2] == J2[2]:
                enfrentt(J1, J2, winners,output)
                list_players.remove(J1)
                list_players.remove(J2)
                valor = True
                index2 = index1 + 1
            else:   
                index2 += 1
        if not(valor):
            index1 += 1
            index2 = index1 + 1
    
    return list_players,winners,output


# menores_N: list(tuples), number -> list(tuples)
# toma la lista de distancias y elimina dichas distancias menores a N.
# luego ordena la lista actualizada.
def menores_N(distancias,N):
    aux = []
    for ciudades in distancias:
        if float(ciudades[2]) <= N:
            aux.append(ciudades)
    distancias = aux
    distancias.sort(key = lambda x: float(x[2]))
    return distancias

# busqueda_descartados: List(Tuples), List(Tuples), List(Strings) , number, List(Tuples), List(Strings) -> List(Tuples), List(Tuples), List(Strings)
# toma la lista de los jugadores que no encontraron otro jugador de la misma ciudad,
# itera sobre la lista de distancias para encontrar 2 jugadores que cumplen con dicha distancia.
# una vez encontrados los enfrenta, sino, sigue iterando.


def busqueda_descartados(list_players, distancias, N,winners,output):
    dist = menores_N(distancias, N)
    for info_ciudades in dist:
        valor = False
        for j1 in list_players:
            if valor:
                break
            for j2 in list_players[(list_players.index(j1))+1:]:
                if (j1[2][:-1] == info_ciudades[0] and j2[2][:-1] == info_ciudades[1])\
                    or (j1[2][:-1] == info_ciudades[1] and j2[2][:-1] == info_ciudades[0]):
                    valor = True
                    enfrentt(j1, j2, winners, output)
                    list_players.remove(j1)
                    list_players.remove(j2)

    return list_players,winners,output

# juego: list(tuples),list(strings),number,list(tuples) -> list(strings)
# toma la lista de jugadores y mientras list_players se modifique va seguir enfrentando a los jugadores,
# caso contrario quiere decir que terminó y se obtuvieron el o los ganador/es agreandolos a output.
# winners: Lista de jugadores que pasaran a la siguiente ronda
def juego(list_players,output,N,distancias):
    valor = False
    winners = [] 
    while not(valor):
        a = list_players
        misma_city(list_players,winners,output) 
        busqueda_descartados(list_players,distancias,N,winners,output)
        winners += list_players
        list_players = winners
        winners = []
        if a == list_players:
            valor = True   
        output.append("\n")
    if len(list_players) == 1:
        WINNER = list_players[0]
        output.append(WINNER[0]+ " es el ganador")
    else:
        for winner in list_players:
            output.append(winner[0]+ " Ganador regional de " + winner[2])
    return output

# general: none -> string
# funcion de partida del juego, hace jugar a los mayores de edad y luego a los menores.
# imprime en pantalla cuando se escribió el archivo.
# output: # Lista de logs de cada que vez que un jugador elimina a otro
# players_adults: Lista de jugadores mayores de edad
# players_youngers: lista de jugadores menores de edad


def general():
    jugadores = clasificacion()
    distancias = distancias_ciudades()
    N = ingresar_N()
    arch_output = open("resultados.txt", "w")
    players_adults = jugadores[1]  
    players_younger = jugadores[0] 
    output = [] 
    output.append("Mayores de edad\n\n")
    juego(players_adults,output,N,distancias)
    output.append("\n\nMenores de edad\n\n")
    juego(players_younger,output,N,distancias)

    for archivo in output:
        arch_output.write(archivo)
    print("Se ha escrito el archivo")

general()
