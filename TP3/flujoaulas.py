from collections import deque

INFINITO = float('inf')

def agregar_arista(red, capacidades, nodo_origen, nodo_destino, capacidad):
    red[nodo_origen].append(nodo_destino)
    red[nodo_destino].append(nodo_origen)
    capacidades[(nodo_origen, nodo_destino)] = capacidad
    capacidades[(nodo_destino, nodo_origen)] = 0  
    
def encontrar_camino(red, capacidades, fuente, sumidero, predecesores):
    visitados = set()
    cola = deque([fuente])
    visitados.add(fuente)

    while cola:
        nodo = cola.popleft()
        for vecino in red[nodo]:
            if vecino not in visitados and capacidades[(nodo, vecino)] > 0:
                visitados.add(vecino)
                predecesores[vecino] = nodo
                if vecino == sumidero:
                    return True
                cola.append(vecino)
    return False

def flujo_maximo(red, capacidades, fuente, sumidero):
    flujo_total = 0
    predecesores = {}

    while encontrar_camino(red, capacidades, fuente, sumidero, predecesores):
        capacidad_minima = INFINITO
        nodo_actual = sumidero

        while nodo_actual != fuente:
            nodo_anterior = predecesores[nodo_actual]
            capacidad_minima = min(capacidad_minima, capacidades[(nodo_anterior, nodo_actual)])
            nodo_actual = nodo_anterior

        nodo_actual = sumidero
        while nodo_actual != fuente:
            nodo_anterior = predecesores[nodo_actual]
            capacidades[(nodo_anterior, nodo_actual)] -= capacidad_minima
            capacidades[(nodo_actual, nodo_anterior)] += capacidad_minima
            nodo_actual = nodo_anterior

        flujo_total += capacidad_minima

    return flujo_total

def resolver_aulas_sobrecargadas(num_aulas, num_conexiones, estudiantes_iniciales, capacidad_requerida, conexiones):
    fuente = 0
    sumidero = 2 * num_aulas + 1
    red = [[] for _ in range(2 * num_aulas + 2)]
    capacidades = {}

    total_estudiantes = sum(estudiantes_iniciales)
    total_capacidades = sum(capacidad_requerida)

    for i in range(1, num_aulas + 1):
        agregar_arista(red, capacidades, fuente, i, estudiantes_iniciales[i - 1])
        agregar_arista(red, capacidades, i + num_aulas, sumidero, capacidad_requerida[i - 1])
        agregar_arista(red, capacidades, i, i + num_aulas, INFINITO)

    for aula1, aula2 in conexiones:
        agregar_arista(red, capacidades, aula1, aula2 + num_aulas, INFINITO)
        agregar_arista(red, capacidades, aula2, aula1 + num_aulas, INFINITO)

    if total_estudiantes != total_capacidades or flujo_maximo(red, capacidades, fuente, sumidero) != total_capacidades:
        return "NO"

    resultado = [[0] * num_aulas for _ in range(num_aulas)]

    for i in range(1, num_aulas + 1):
        for vecino in red[i]:
            if num_aulas + 1 <= vecino <= 2 * num_aulas:
                flujo_usado = capacidades[(vecino, i)]
                if flujo_usado > 0:
                    resultado[i - 1][vecino - num_aulas - 1] = flujo_usado

    respuesta = "YES\n" + "\n".join(" ".join(map(str, fila)) for fila in resultado)
    return respuesta


if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    datos = input().splitlines()

    n, m = map(int, datos[0].split())
    estudiantes = list(map(int, datos[1].split()))
    capacidades = list(map(int, datos[2].split()))
    conexiones = [tuple(map(int, linea.split())) for linea in datos[3:]]
    print(resolver_aulas_sobrecargadas(n, m, estudiantes, capacidades, conexiones))
