import numpy as np
from OperacoesGrafos import operações_grafos as og, CriaRede as cr, plotGrafos as pg, Coordenadas as cd


def SimulacaoRede(matriz, rota, bateria, matriz_principal, mortos, cod):
    percorridos = []
    for i in range(1, len(matriz)):
        if i not in mortos and (i not in percorridos or cod == 1):

            rota_anterior = i
            percorre_rota = rota[i]
            # rota anterior vai para percorre_rota
            bits = 2000

            while percorre_rota != 0:
                bateria[rota_anterior] -= (matriz[rota_anterior][percorre_rota] - ((50 * bits) / 1000000000))
                bateria[percorre_rota] -= (50 * bits) / 1000000000
                percorridos.append(rota_anterior)

                if bateria[rota_anterior] <= 0 or bateria[percorre_rota] <= 0:
                    if bateria[rota_anterior] <= 0:
                        mortos.append(rota_anterior)
                        og.removeVertice(matriz_principal, rota_anterior)
                        bateria[rota_anterior] = 0
                    if bateria[percorre_rota] <= 0:
                        mortos.append(percorre_rota)
                        og.removeVertice(matriz_principal, percorre_rota)
                        bateria[percorre_rota] = 0

                    rota = og.dijkstra(matriz_principal, 0)[0]

                    matriz = og.TransformaEmDigrafo(rota, len(matriz_principal) - 1, matriz_principal, 0, mortos)

                    if percorre_rota in mortos:
                        break
                rota_anterior = percorre_rota
                percorre_rota = rota[percorre_rota]
            if percorre_rota not in mortos and matriz[rota_anterior][0] > 0:
                bateria[rota_anterior] -= (matriz[rota_anterior][percorre_rota] - ((50 * bits) / 1000000000))
                percorridos.append(rota_anterior)
                if bateria[rota_anterior] <= 0:
                    mortos.append(rota_anterior)
                    og.removeVertice(matriz_principal, rota_anterior)
                    bateria[rota_anterior] = 0
                    rota = og.dijkstra(matriz_principal, 0)[0]
    return matriz_principal, matriz, rota, mortos, bateria


def menuDijkstra ():
    print ("Selecione o método de comunicação entre os sensores:\n1 - Retransmissão Redundante\n"
           "2 - Supressão de Transmissão Repetida")
    codigo = int(input("Digite: "))
    print ("Digite a quantidade de bateria que os nós em volta da rádio base devem ter. (Padrão: 50)")
    bateriaExtra = int (input("Digite: "))
    return codigo, bateriaExtra


def TesteDijkstra(coordenadas, tamanho):
    cod, bateriaExtra = menuDijkstra()
    if cod != 1 and cod != 2:
        print ("Código inválido")
        return
    matriz = []
    for i in range(0, tamanho + 1):
        lista_aux = [0] * (tamanho + 1)
        matriz.append(lista_aux)
    bateria = [50] * (tamanho + 1)
    for i in range(1, tamanho + 1):
        if cr.distancia_vertices(coordenadas[0][0], coordenadas[0][1], coordenadas[i][0], coordenadas[i][1]) <= 200:
            bateria[i] = bateriaExtra
    cd.preencher_matrizEnergia(matriz, tamanho, coordenadas)
    matriz_copia = np.copy(matriz)
    rota = og.dijkstra(matriz_copia, 0)[0]
    matriz_copia = og.TransformaEmDigrafo(rota, tamanho, matriz, 0)
    pg.desenhar_digrafo(matriz_copia, coordenadas, "Início da Rede")
    mortos = []
    primeiro_morto = 0
    iteracao = 0
    nosSemConexao = 0
    while nosSemConexao <= tamanho * 0.80:
        matriz, matriz_copia, rota, mortos, bateria = SimulacaoRede(matriz_copia, rota, bateria, matriz, mortos, cod)
        iteracao += 1

        nosSemConexao = 0
        for i in range(1, tamanho + 1):
            if rota[i] == 0 and matriz[i][0] <= 0:
                nosSemConexao += 1

        if iteracao % 1000 == 0:
            rota = og.dijkstra(matriz, 0)[0]

            matriz_copia = og.TransformaEmDigrafo(rota, len(matriz) - 1, matriz, 0, mortos)

        if iteracao % 10000 == 0:
            pg.desenhar_digrafo(matriz_copia, coordenadas, "Round {}".format(iteracao))
        if mortos and primeiro_morto == 0:
            primeiro_morto = mortos[0]
            iteracaoMorto = iteracao
    matriz_copia = []
    for i in range(0, tamanho + 1):
        lista_aux = [0] * (tamanho + 1)
        matriz_copia.append(lista_aux)
    for elem in mortos:
        og.removeVertice(matriz_copia, elem)
    pg.desenhar_digrafo(matriz_copia, coordenadas, "Fim da Rede")
    bateria_arrendondada = [round(elem, 2) for elem in bateria]
    print("Bateria Restante da Rede:")
    print(np.array(bateria_arrendondada))
    print ("A rede durou {} iterações. ({} anos e {} meses)".format(iteracao,(iteracao * 2 / 24) // 365, ((iteracao * 2 / 24) % 365) // 30))
    print("Houve {} sensores mortos.".format(len(mortos)))
    print("O primeiro sensor a morrer foi o vértice {} e ocorreu com {} iterações.".format(mortos[0], iteracaoMorto))
    energiaTotalGasta = 0
    for i in range(1, tamanho + 1):
        if cr.distancia_vertices(coordenadas[0][0], coordenadas[0][1], coordenadas[i][0], coordenadas[i][1]) <= 200:
            energiaTotalGasta += bateriaExtra - bateria[i]
        else:
            energiaTotalGasta += 100 - bateria[i]
    print("A energia total gasta foi {} joules.".format(round(energiaTotalGasta, 2)))
    return
