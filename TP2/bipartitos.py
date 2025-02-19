def dfs(nodo):
    stack = [(nodo, 0)]
    while stack:
        actual, color = stack.pop()
        if colores[actual] == -1:
            colores[actual] = color
            if color == 0:
                conjuntos[0].append(actual)
            else:
                conjuntos[1].append(actual)
            for vecino in listaAdy[actual]:
                if colores[vecino] == -1:
                    stack.append((vecino, 1 - color))

n = int(input())

if n == 1:
    print(0)
    exit()

listaAdy = [[] for _ in range(n + 1)]

for _ in range(n - 1):
    u, v = map(int, input().split())
    if v not in listaAdy[u]:  
        listaAdy[u].append(v)
    if u not in listaAdy[v]:  
        listaAdy[v].append(u)

colores = [-1] * (n + 1)
conjuntos = [[], []]

dfs(1)

tamañoA = len(conjuntos[0])
tamañoB = len(conjuntos[1])

aristasPosibles = tamañoA * tamañoB
aristasAdicionales = aristasPosibles - (n - 1)

print(aristasAdicionales)

