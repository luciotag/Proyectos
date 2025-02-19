from collections import deque

def minimaEnergia(n, atajos):
    distancias = [float('inf')] * n
    distancias[0] = 0
    cola = deque([0])
    
    while cola:
        aulaActual = cola.popleft()
        
        if aulaActual + 1 < n and distancias[aulaActual + 1] > distancias[aulaActual] + 1:
            distancias[aulaActual + 1] = distancias[aulaActual] + 1
            cola.append(aulaActual + 1)

        if aulaActual - 1 >= 0 and distancias[aulaActual - 1] > distancias[aulaActual] + 1:
            distancias[aulaActual - 1] = distancias[aulaActual] + 1
            cola.append(aulaActual - 1)

        aulaAtada = atajos[aulaActual] - 1
        if distancias[aulaAtada] > distancias[aulaActual] + 1:
            distancias[aulaAtada] = distancias[aulaActual] + 1
            cola.append(aulaAtada)

    return distancias

n = int(input())
atajos = list(map(int, input().split()))
resultado = minimaEnergia(n, atajos)
print(" ".join(map(str, resultado)))
