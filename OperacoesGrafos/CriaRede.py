import numpy as np
import math

def cria_secoes(coordenadas, tamanho):
    secao1 = [] # Primeiro quadrante
    secao2 = [] # Segundo quadrante
    secao3 = [] # Terceiro quadrante
    secao4 = [] # Quarto quadrante
    i = 0
    for i in range (1, tamanho+1):
        if coordenadas[i][0] >= 500 and coordenadas[i][1] >= 500:
            secao1.append(coordenadas[i])
        elif coordenadas[i][0] <= 500 and coordenadas[i][1] >=500:
            secao2.append(coordenadas[i])
        elif coordenadas[i][0] <= 500:
            secao3.append(coordenadas[i])
        else:
            secao4.append(coordenadas[i])
    return np.array(secao1), np.array(secao2), np.array(secao3), np.array(secao4)


def distancia_vertices (x1, y1, x2, y2):
    distancia = math.sqrt((x2 - x1)*(x2 - x1) + (y2 - y1)*(y2 - y1))
    return distancia

def filaClusterheads (coordenadas, tamanho):
    coordenadasUtilizadas = []
    filaSecao1 = []
    filaSecao2 = []
    filaSecao3 = []
    filaSecao4 = []

    flag = 1
    while flag == 1:

        menorSecao1 = [-1, 1000]
        menorSecao2 = [-1, 1000]
        menorSecao3 = [-1, 1000]
        menorSecao4 = [-1, 1000]

        for i in range(1, tamanho + 1):

            flag_coordenada = False
            for coordenada in coordenadasUtilizadas:
                if all(coordenadas[i] == coordenada):
                    flag_coordenada = True
                    break
            if not flag_coordenada:
                distancia = distancia_vertices(coordenadas[i][0], coordenadas[i][1], 750, 750)

                if distancia <= 200 and distancia < menorSecao1[1]:
                    menorSecao1 = [i, distancia]

                distancia = distancia_vertices(coordenadas[i][0], coordenadas[i][1], 250, 750)

                if distancia <= 200 and distancia < menorSecao2[1]:
                    menorSecao2 = [i, distancia]

                distancia = distancia_vertices(coordenadas[i][0], coordenadas[i][1], 250, 250)

                if distancia <= 200 and distancia < menorSecao3[1]:
                    menorSecao3 = [i, distancia]

                distancia = distancia_vertices(coordenadas[i][0], coordenadas[i][1], 750, 250)

                if distancia <= 200 and distancia < menorSecao4[1]:
                    menorSecao4 = [i, distancia]

        flag = 0
        if menorSecao1[0] != -1:
            filaSecao1.append(menorSecao1[0])
            coordenadasUtilizadas.append(coordenadas[menorSecao1[0]])
            flag = 1

        if menorSecao2[0] != -1:
            filaSecao2.append(menorSecao2[0])
            coordenadasUtilizadas.append(coordenadas[menorSecao2[0]])
            flag = 1

        if menorSecao3[0] != -1:
            filaSecao3.append(menorSecao3[0])
            coordenadasUtilizadas.append(coordenadas[menorSecao3[0]])
            flag = 1

        if menorSecao4[0] != -1:
            filaSecao4.append(menorSecao4[0])
            coordenadasUtilizadas.append(coordenadas[menorSecao4[0]])
            flag = 1

    return filaSecao1, filaSecao2, filaSecao3, filaSecao4