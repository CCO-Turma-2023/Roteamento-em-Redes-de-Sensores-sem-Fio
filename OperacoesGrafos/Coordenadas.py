import math
from OperacoesGrafos import operações_grafos as og

def distancia_vertices (x1, y1, x2, y2):
    distancia = math.sqrt((x2 - x1)*(x2 - x1) + (y2 - y1)*(y2 - y1))
    return distancia


def preencher_matrizEnergia (matriz, qtd_vertices, coord):
    for i in range(0, qtd_vertices+1):
        for j in range(qtd_vertices + 1):
            aux_1 = coord[i]
            aux_2 = coord[j]
            distancia = distancia_vertices(aux_1[0], aux_1[1], aux_2[0], aux_2[1])
            if distancia <= 200 and i != j:
                if og.verificaAdjacencia(matriz, i, j) == False:
                    og.insereArestaEnergia(matriz, i, j, distancia)
    return

def preencher_matrizDistancia (matriz, qtd_vertices, coord):
    for i in range(0, qtd_vertices+1):
        for j in range (qtd_vertices + 1):
            aux_1 = coord[i]
            aux_2 = coord[j]
            distancia = distancia_vertices(aux_1[0], aux_1[1], aux_2[0], aux_2[1])
            if distancia <= 200 and i != j:
                if og.verificaAdjacencia(matriz, i, j) == False:
                    og.insereArestaDistancia(matriz, i, j, distancia)
    return


def preencher_listaDistancia (qtd_vertices, coord):
    listaAdj = {}
    for i in range(qtd_vertices + 1):
        listaAdj[i] = []
    for i in range(0, qtd_vertices + 1):
        for j in range(qtd_vertices + 1):
            aux_1 = coord[i]
            aux_2 = coord[j]
            distancia = distancia_vertices(aux_1[0], aux_1[1], aux_2[0], aux_2[1])
            if distancia <= 200 and i != j:
                listaAdj[i].append(j)
    return listaAdj