
def verificaAdjacencia(matriz, vi, vj):
    return bool(matriz[vi][vj])


def insereArestaEnergia(matriz, vi, vj, distancia):
    # Calculando a energia e transformando em joule
    matriz[vi][vj] = ((50 * 2000) + (0.010 * 2000 * (distancia*distancia)) + (50 * 2000))/1000000000
    matriz[vj][vi] = ((50 * 2000) + (0.010 * 2000 * (distancia*distancia)) + (50 * 2000))/1000000000
    return matriz

def insereArestaDistancia(matriz, vi, vj, distancia):
    matriz[vi][vj] = distancia
    matriz[vj][vi] = distancia
    return matriz

def insereArestaDigrafo(matriz, vi, vj, distancia):
    # Calculando a energia e transformando em joule
    matriz[vi][vj] = ((50 * 2000) + (0.010 * 2000 * (distancia*distancia)) + (50 * 2000))/1000000000
    return matriz


def removeVertice(matriz, v):
    dimensoes = [len(matriz), len(matriz[0])]
    for i in range(0, dimensoes[0]):
        matriz[i][v] = -1
        matriz[v][i] = -1
    return matriz

def TransformaEmDigrafo(rota, tamanho, matriz_principal, clusterhead, mortos = [], soma = 0):
    matriz_digrafo = []
    for i in range(0, tamanho+1):
        lista_aux = [0] * (tamanho+1)
        matriz_digrafo.append(lista_aux)

    for i in range(0, tamanho+1):
        percorre_rota_ant = i
        percorre_rota = rota[i]
        while percorre_rota != clusterhead and percorre_rota != -1:
            matriz_digrafo[percorre_rota_ant][percorre_rota] = matriz_principal[percorre_rota_ant][percorre_rota]
            percorre_rota_ant = percorre_rota
            percorre_rota = rota[percorre_rota]
        matriz_digrafo[percorre_rota_ant][percorre_rota] = matriz_principal[percorre_rota_ant][percorre_rota]
    for i in mortos:
        removeVertice(matriz_digrafo, i)
    return matriz_digrafo


def menorcusto(custo, Fechados, Abertos):
    menor = Abertos[0]
    for i in range(len(custo)):
        if i not in Fechados:
            if custo[i] < custo[menor]:
                menor = i
    return menor


def dijkstra(matriz, vOrigem):
    custo = [float('inf')] * len(matriz)
    rota = [vOrigem] * len(matriz)
    custo[vOrigem] = 0
    Abertos = []
    for i in range(len(matriz)):
        if matriz[i][0] != -1:
            Abertos.append(i)
    Fechados = []
    while len(Abertos) > 1:
        v = menorcusto(custo,Fechados, Abertos)
        Fechados.append(v)
        for i in range(len(Abertos)):
            if Abertos[i] == v:
                Abertos.pop(i)
                break
        Adjacentes = []
        for i in range(len(matriz)):
            if matriz[v][i] > 0:
                Adjacentes.append(i)
        Adjacentes = list(set(Adjacentes) - set(Fechados))
        for i in Adjacentes:
            if custo[v] + (matriz[v][i]) < custo[i]:
                rota[i] = v
                custo[i] = custo[v] + matriz[v][i]
    rota_custo = [rota, custo]
    return rota_custo