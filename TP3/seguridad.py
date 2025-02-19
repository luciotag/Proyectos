import heapq
from collections import defaultdict, deque

def dijkstra(n, aristas):
    grafo = defaultdict(list)
    for v, w, c in aristas:
        grafo[v].append((w, c))
        grafo[w].append((v, c))
    
    distancias = [float('inf')] * n
    distancias[0] = 0
    padres = [[] for _ in range(n)]
    cola_prioridad = [(0, 0)]  
    
    while cola_prioridad:
        distancia_actual, nodo = heapq.heappop(cola_prioridad)
        if distancia_actual > distancias[nodo]:
            continue
        for vecino, peso in grafo[nodo]:
            nueva_distancia = distancias[nodo] + peso
            if nueva_distancia < distancias[vecino]:
                distancias[vecino] = nueva_distancia
                heapq.heappush(cola_prioridad, (nueva_distancia, vecino))
                padres[vecino] = [(nodo, peso)]
            elif nueva_distancia == distancias[vecino]:
                padres[vecino].append((nodo, peso))
    
    return calcular_costo_seguridad(n, padres)

def calcular_costo_seguridad(n, padres):
    visitado = [False] * n
    cola = deque([n - 1])
    visitado[n - 1] = True
    costo_total = 0
    
    while cola:
        nodo = cola.popleft()
        for padre, peso in padres[nodo]:
            costo_total += 2 * peso
            if not visitado[padre]:
                visitado[padre] = True
                cola.append(padre)
    
    return costo_total

n, m = map(int, input().split())
aristas = [tuple(map(int, input().split())) for _ in range(m)]
print(dijkstra(n, aristas))
