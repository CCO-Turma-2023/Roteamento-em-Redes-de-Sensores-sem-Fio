import numpy as np
from OperacoesGrafos import operações_grafos as og, plotGrafos as pg, Coordenadas as cd

bateriaSensor = 50

def TesteMaisProximo (coordenadas, tamanho):
    global bateriaSensor
    matriz = []
    listaAdj = cd.preencher_listaDistancia(tamanho, coordenadas)
    for i in range(0, tamanho + 1):
        lista_aux = [0] * (tamanho + 1)
        matriz.append(lista_aux)
    cd.preencher_matrizDistancia(matriz, tamanho, coordenadas)
    nao_mandou = 0
    bateria = [bateriaSensor] * (tamanho + 1)
    matriz_Representa_Caminho = []
    iteracoes = 0
    primeroNoMorto = 0
    while nao_mandou + bateria.count(0) < tamanho * 0.80:
        sensor = 1

        if iteracoes % 5000 == 0:
            matriz_Representa_Caminho = []
            for i in range(0, tamanho + 1):
                lista_aux = [0] * (tamanho + 1)
                matriz_Representa_Caminho.append(lista_aux)
        nao_mandou = 0
        while sensor != tamanho:

            atual = sensor
            proximo = -1
            visitados = []

            while proximo != 0 and matriz[sensor][0] != -1:
                visitados.append(atual)
                menor = 1000
                if matriz[atual][0] > 0:
                    break
                else:
                    for i in listaAdj[atual]:
                        if menor > matriz[atual][i] > 0 and i not in visitados:
                            menor = matriz[atual][i]
                            proximo = i
                if proximo != -1:

                    bateria[proximo] = bateria[proximo] - ((50 * 2000)/1000000000)
                    bateria[atual] = bateria[atual] - (((50 * 2000) + (0.010 * 2000 *
                                    (matriz[atual][proximo]*matriz[atual][proximo])))/1000000000)

                    if bateria[atual] <= 0:
                        og.removeVertice(matriz, atual)
                        bateria[atual] = 0

                    if bateria[proximo] <= 0:
                        og.removeVertice(matriz, proximo)
                        bateria[proximo] = 0
                        break
                    matriz_Representa_Caminho[atual][proximo] = matriz[atual][proximo]
                    atual = proximo
                else:
                    nao_mandou += 1
                    break

                proximo = -1

            if matriz[atual][0] > 0:
                bateria[atual] = bateria[atual] - (((50 * 2000) + (0.010 * 2000 *
                                                                  (matriz[atual][0] * matriz[atual][
                                                                      0])))/1000000000)
                if bateria[atual] <= 0:
                    og.removeVertice(matriz, atual)
                    bateria[atual] = 0
                matriz_Representa_Caminho[atual][0] = matriz[atual][0]

            sensor = sensor + 1
        if bateria.count(0) > 0 and primeroNoMorto == 0:
            for i in range (1, len(bateria)):
                if bateria[i] == 0:
                    iteracaoPrimeiroMorto = iteracoes
                    primeroNoMorto = i

        if iteracoes % 1000 == 0:
            for i in range(tamanho + 1):
                if matriz[i][0] == -1:
                    og.removeVertice(matriz_Representa_Caminho, i)
            pg.desenhar_digrafo(matriz_Representa_Caminho, coordenadas, "Round {}".format(iteracoes) if iteracoes != 0 else "Início da Rede")
        iteracoes += 1

    matriz_Representa_Caminho = []
    for i in range(0, tamanho + 1):
        lista_aux = [0] * (tamanho + 1)
        matriz_Representa_Caminho.append(lista_aux)
    for i in range(tamanho + 1):
        if matriz[i][0] == -1:
            og.removeVertice(matriz_Representa_Caminho, i)

    pg.desenhar_digrafo(matriz_Representa_Caminho, coordenadas, "Fim da Rede")
    print ("Bateria Restante da Rede: ")
    print(np.array(bateria))
    print ("A rede durou {} iterações. ({} anos e {} meses)".format(iteracoes,(iteracoes * 2 / 24) // 365, ((iteracoes * 2 / 24) % 365) // 30))
    print ("O primeiro sensor a morrer foi o {} e morreu com {} iterações.".format(primeroNoMorto, iteracaoPrimeiroMorto))
    energiaTotalGasta = 0
    for elem in bateria:
        energiaTotalGasta += bateriaSensor - elem
    print ("A energia total gasta foi {} joules.".format(round(energiaTotalGasta, 2)))
    return