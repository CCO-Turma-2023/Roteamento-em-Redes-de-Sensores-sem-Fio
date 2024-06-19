import numpy as np
from OperacoesGrafos import operações_grafos as og, CriaRede as cr, plotGrafos as pg, Coordenadas as cd

matriz = []
rota = []
bateria = []
mortos = []
coordenadas_nova = []
clusterhead = []
naoIteraveis = []
inicio = 0
fim = 0
matriz_copia = []
mortosSecao = []
filaRR = []
clusterheadSecoes = []
vidaSecoes = []
inicioSecao = 0
fimSecao = 0
secoes = []
bateriaSecao = []
secao = 0
bateriaSensor = 50

BITS = 2000


def menuRR ():
    print ("Selecione o método de comunicação entre os sensores:\n1 - Retransmissão Redundante\n2 - Supressão de Transmissão Repetida")
    codigo = int(input("Digite: "))
    return codigo


def testeRR_LongoAlcance(coordenadas, tamanho):
    global matriz, rota, bateria, mortos, coordenadas_nova, clusterhead, naoIteraveis, inicio, fim, matriz_copia, \
        mortosSecao, filaRR, clusterheadSecoes, vidaSecoes, inicioSecao, secoes, bateriaSecao, secao, bateriaSensor

    cod = menuRR()
    if cod != 1 and cod != 2:
        print("Opção inválida")
        return

    secoes = cr.cria_secoes(coordenadas, tamanho)

    coordenadas_nova = [coordenadas[0]]
    for i in range(0, 4):
        for j in range(len(secoes[i])):
            coordenadas_nova.append(secoes[i][j])

    filaRR1, filaRR2, filaRR3, filaRR4 = cr.filaClusterheads(coordenadas_nova, tamanho)

    for i in range(0, tamanho + 1):
        lista_aux = [0] * (tamanho + 1)
        matriz.append(lista_aux)

    for i in range(0, tamanho + 1):
        lista_aux = [0] * (tamanho + 1)
        matriz_copia.append(lista_aux)

    bateria = [bateriaSensor] * (tamanho + 1)

    cd.preencher_matrizEnergia(matriz, tamanho, coordenadas_nova)

    rota1 = og.dijkstra(matriz, filaRR1[0])[0]
    rota2 = og.dijkstra(matriz, filaRR2[0])[0]
    rota3 = og.dijkstra(matriz, filaRR3[0])[0]
    rota4 = og.dijkstra(matriz, filaRR4[0])[0]

    nosRadioBase = []
    for i in range(1, len(coordenadas_nova)):
        distancia = cr.distancia_vertices(coordenadas_nova[0][0], coordenadas_nova[0][1], coordenadas_nova[i][0],
                                          coordenadas_nova[i][1])
        if distancia <= 200:
            matriz_copia[i] = [0] * (tamanho + 1)
            og.insereArestaDigrafo(matriz, i, 0, distancia)
            nosRadioBase.append(i)

    vidaSecoes = [True, True, True, True]

    clusterheadSecoes = [filaRR1[0], filaRR2[0], filaRR3[0], filaRR4[0]]

    filaRR1.append(filaRR1.pop(0))
    filaRR2.append(filaRR2.pop(0))
    filaRR3.append(filaRR3.pop(0))
    filaRR4.append(filaRR4.pop(0))

    bateriaSecao1 = bateriaSensor
    bateriaSecao2 = bateriaSensor
    bateriaSecao3 = bateriaSensor
    bateriaSecao4 = bateriaSensor

    mortosSecoes1 = []
    mortosSecoes2 = []
    mortosSecoes3 = []
    mortosSecoes4 = []

    inicioSecao1 = 1
    fimSecao1 = len(secoes[0])

    inicioSecao2 = len(secoes[0]) + 1
    fimSecao2 = len(secoes[0]) + len(secoes[1])

    inicioSecao3 = 1 + len(secoes[0]) + len(secoes[1])
    fimSecao3 = len(secoes[0]) + len(secoes[1]) + len(secoes[2])

    inicioSecao4 = 1 + len(secoes[0]) + len(secoes[1]) + len(secoes[2])
    fimSecao4 = len(secoes[0]) + len(secoes[1]) + len(secoes[2]) + len(secoes[3])

    primeiroMorto = False
    mortos = []
    naoIteraveis = nosRadioBase
    iteracao = 0
    while vidaSecoes.count(False) < 3:

        if (iteracao + 1) % 10000:
            matriz_copia = []
            for i in range(0, tamanho + 1):
                lista_aux = [0] * (tamanho + 1)
                matriz_copia.append(lista_aux)

        naoIteraveis = nosRadioBase

        if vidaSecoes[0]:
            if not filaRR1:
                vidaSecoes[0] = False
            else:
                inicio = inicioSecao1
                mortosSecao = mortosSecoes1
                fim = fimSecao1
                rota = rota1
                clusterhead = clusterheadSecoes[0]
                filaRR = filaRR1
                bateriaSecao = bateriaSecao1
                secao = 0

                IniciarTeste(cod)

                bateriaSecao1 = bateriaSecao
                mortosSecoes1 = mortosSecao
                filaRR1 = filaRR
                rota1 = rota

        if vidaSecoes[1]:
            if not filaRR2:
                vidaSecoes[1] = False
            else:
                inicio = inicioSecao2
                mortosSecao = mortosSecoes2
                fim = fimSecao2
                rota = rota2
                clusterhead = clusterheadSecoes[1]
                filaRR = filaRR2
                bateriaSecao = bateriaSecao2
                secao = 1

                IniciarTeste(cod)

                bateriaSecao2 = bateriaSecao
                mortosSecoes2 = mortosSecao
                filaRR2 = filaRR
                rota2 = rota

        if vidaSecoes[2]:
            if not filaRR3:
                vidaSecoes[2] = False
            else:
                inicio = inicioSecao3
                mortosSecao = mortosSecoes3
                fim = fimSecao3
                rota = rota3
                clusterhead = clusterheadSecoes[2]
                filaRR = filaRR3
                bateriaSecao = bateriaSecao3
                secao = 2

                IniciarTeste(cod)

                bateriaSecao3 = bateriaSecao
                mortosSecoes3 = mortosSecao
                filaRR3 = filaRR
                rota3 = rota

        if vidaSecoes[3]:
            if not filaRR4:
                vidaSecoes[3] = False
            else:
                inicio = inicioSecao4
                mortosSecao = mortosSecoes4
                fim = fimSecao4
                rota = rota4
                clusterhead = clusterheadSecoes[3]
                filaRR = filaRR4
                bateriaSecao = bateriaSecao4
                secao = 3

                IniciarTeste(cod)

                bateriaSecao4 = bateriaSecao
                mortosSecoes4 = mortosSecao
                filaRR4 = filaRR
                rota4 = rota

        for sensor in nosRadioBase:
            if sensor not in mortos:

                bateria[sensor] -= (matriz[sensor][0] - ((50 * 2000) / 1000000000))
                og.insereArestaDigrafo(matriz_copia, sensor, 0, 1)
                if bateria[sensor] <= 0:
                    bateria[sensor] = 0
                    og.removeVertice(matriz, sensor)
                    mortos.append(sensor)

                    if sensor in rota1[inicioSecao1: fimSecao1 + 1]:
                        rota1 = og.dijkstra(matriz, clusterheadSecoes[0])[0]

                    if sensor in rota2[inicioSecao2: fimSecao2 + 1]:
                        rota2 = og.dijkstra(matriz, clusterheadSecoes[1])[0]

                    if sensor in rota3[inicioSecao3: fimSecao3]:
                        rota3 = og.dijkstra(matriz, clusterheadSecoes[2])[0]

                    if sensor in rota4[inicioSecao4: fimSecao4 + 1]:
                        rota4 = og.dijkstra(matriz, clusterheadSecoes[3])[0]

        iteracao += 1
        if mortos and not primeiroMorto:
            primeiroMorto = True
            primeiroNoMorto = iteracao

        if iteracao % 10000 == 0 or iteracao == 1:
            for elem in mortos:
                og.removeVertice(matriz_copia, elem)
            pg.desenhar_digrafo(matriz_copia, coordenadas_nova, "Round {}".format(iteracao), clusterheadSecoes)


    # Resultados da Rede
    matriz_copia = []
    for i in range(0, tamanho + 1):
        lista_aux = [0] * (tamanho + 1)
        matriz_copia.append(lista_aux)

    for elem in mortos:
        og.removeVertice(matriz_copia, elem)

    pg.desenhar_digrafo(matriz_copia, coordenadas_nova, "Fim da Rede")

    print("\nBateria Restante da Rede:")
    print(np.array(bateria))
    print ("A rede durou {} iterações. ({} anos e {} meses)".format(iteracao,(iteracao * 2 / 24) // 365, ((iteracao * 2 / 24) % 365) // 30))
    print("Houve {} sensores mortos".format(len(mortos)))
    if primeiroMorto:
        print("O primeiro sensor a morrer foi o vértice {} e ocorreu com {} iterações.".format(mortos[0],
                                                                                               primeiroNoMorto))
    energiaTotalGasta = 0
    for elem in bateria:
        energiaTotalGasta += bateriaSensor - elem
    print("A energia total gasta foi {} joules.".format(round(energiaTotalGasta, 2)))


def IniciarTeste(cod):
    global mortosSecao, filaRR, clusterheadSecoes, vidaSecoes, secoes, bateriaSecao, secao, rota, bateria, \
        matriz, matriz_copia, coordenadas_nova, inicio, fim, clusterhead

    if mortos != mortosSecao:
        for elem in mortos:
            if elem in filaRR:
                filaRR.remove(elem)
        if not filaRR:
            return
        if clusterheadSecoes[secao] not in filaRR:
            clusterheadSecoes[secao] = filaRR[0]
            filaRR.append(filaRR.pop(0))
            bateriaSecao = bateria[clusterheadSecoes[secao]]
            clusterhead = clusterheadSecoes[secao]
        rota = og.dijkstra(matriz, clusterheadSecoes[secao])[0]

    if clusterheadSecoes[secao] in mortos or bateriaSecao - 10 > bateria[clusterheadSecoes[secao]]:
        clusterheadSecoes[secao] = filaRR[0]
        filaRR.append(filaRR.pop(0))

        rota = og.dijkstra(matriz, clusterheadSecoes[secao])[0]
        clusterhead = clusterheadSecoes[secao]
        bateriaSecao = bateria[clusterheadSecoes[secao]]

    SimulacaoRede(cod)

    for elem in mortos:
        if elem in filaRR:
            filaRR.remove(elem)

    nosSemConexao = 0
    for i in range(inicio, fim + 1):
        if rota[i] == clusterheadSecoes[secao] and matriz[i][clusterheadSecoes[secao]] <= 0:
            nosSemConexao += 1

    if (nosSemConexao >= len(secoes[secao]) * 0.80 and clusterheadSecoes[secao] not in mortos) or not filaRR:

        for elem in mortos:
            og.removeVertice(matriz_copia, elem)
        vidaSecoes[secao] = False
        return

    if clusterheadSecoes[secao] not in filaRR:
        clusterheadSecoes[secao] = filaRR[0]
        filaRR.append(filaRR.pop(0))
        bateriaSecao = bateria[clusterheadSecoes[secao]]
        rota = og.dijkstra(matriz, clusterheadSecoes[secao])[0]

    if clusterheadSecoes[secao] not in mortos:
        distancia = cr.distancia_vertices(coordenadas_nova[0][0], coordenadas_nova[0][1],
                                          coordenadas_nova[clusterheadSecoes[secao]][0],
                                          coordenadas_nova[clusterheadSecoes[secao]][1])

        og.insereArestaDigrafo(matriz_copia, clusterheadSecoes[secao], 0, distancia)

        bateria[clusterheadSecoes[secao]] -= (matriz_copia[clusterheadSecoes[secao]][0] - ((50 * 2000) / 1000000000))

        if bateria[clusterheadSecoes[secao]] <= 0:
            bateria[clusterheadSecoes[secao]] = 0
            og.removeVertice(matriz, clusterheadSecoes[secao])
            mortos.append(clusterheadSecoes[secao])


    mortosSecao = []
    for elem in mortos:
        mortosSecao.append(elem)


def SimulacaoRede(cod):
    global matriz, rota, bateria, mortos, coordenadas_nova, clusterhead, naoIteraveis, inicio, fim, matriz_copia

    def processa_rota(i, percorridos):
        global matriz, rota, bateria, mortos, clusterhead, matriz_copia
        rota_anterior = i
        percorre_rota = rota[i]
        while percorre_rota != clusterhead:
            # Se a rota chega ao clusterhead, finaliza o loop
            if matriz[rota_anterior][0] > 0:
                percorre_rota = 0
                break
            # Atualiza a bateria dos nós na rota
            bateria[rota_anterior] -= (matriz[rota_anterior][percorre_rota] - ((50 * BITS) / 1000000000))
            bateria[percorre_rota] -= (50 * BITS) / 1000000000

            # Marca a rota percorrida
            percorridos.append(rota_anterior)
            matriz_copia[rota_anterior][percorre_rota] = matriz[rota_anterior][percorre_rota]

            # Verifica se algum nó ficou sem bateria
            if bateria[rota_anterior] <= 0 or bateria[percorre_rota] <= 0:
                if bateria[rota_anterior] <= 0:
                    adiciona_morto(rota_anterior)
                if bateria[percorre_rota] <= 0:
                    adiciona_morto(percorre_rota)
                # Recalcula a rota após a remoção de nós mortos
                rota = og.dijkstra(matriz, clusterhead)[0]
                if percorre_rota in mortos:
                    break

            rota_anterior = percorre_rota
            percorre_rota = rota[percorre_rota]

        # Trata o caso em que a rota chega ao clusterhead
        if matriz[rota_anterior][0] > 0:
            percorre_rota = 0

        if percorre_rota not in mortos and matriz[rota_anterior][percorre_rota] > 0:
            bateria[rota_anterior] -= (matriz[rota_anterior][percorre_rota] - ((50 * BITS) / 1000000000))
            if percorre_rota != 0:
                bateria[percorre_rota] -= (50 * BITS) / 1000000000
            percorridos.append(rota_anterior)
            matriz_copia[rota_anterior][percorre_rota] = matriz[rota_anterior][percorre_rota]
            if bateria[rota_anterior] <= 0:
                adiciona_morto(rota_anterior)
                rota = og.dijkstra(matriz, clusterhead)[0]
            if bateria[percorre_rota] <= 0:
                adiciona_morto(percorre_rota)
                return True
        return False

    def adiciona_morto(no):
        global mortos, matriz, bateria, matriz_copia
        mortos.append(no)
        og.removeVertice(matriz, no)
        og.removeVertice(matriz_copia, no)
        bateria[no] = 0

    if cod == 2:
        percorridos = []
        for i in range(inicio, fim + 1):
            if i not in mortos and i not in percorridos and i not in naoIteraveis:
                processa_rota(i, percorridos)
    else:
        for i in range(inicio, fim + 1):
            if i not in mortos and i not in naoIteraveis:
                if processa_rota(i, []):
                    return

    return