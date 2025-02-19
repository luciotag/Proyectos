def solucion(act):
    cantActs = 0
    ultimoEvento = 0
    act_ordenada = sorted(act, key=lambda x: x[1])

    for tupla in act_ordenada:
        if tupla[0] >= ultimoEvento:
            cantActs += 1
            ultimoEvento = tupla[1]

    return cantActs

T = int(input())

for _ in range(T):
    
    N = int(input())
    lista_de_tuplas = []

    
    for _ in range(N):
        m, n = map(int, input().split())
        lista_de_tuplas.append((m, n))

    print(solucion(lista_de_tuplas))
