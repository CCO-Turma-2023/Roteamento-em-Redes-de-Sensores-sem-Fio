import numpy as np
from OperacoesGrafos import operações_grafos as og, CriaRede as cr, plotGrafos as pg

bateriaSensor = 50

def menuMesh():
    print("Quanto de bateria as meshs irão ter?")
    print("-1 Para infinito")
    qtdBaterias = int(input("Digite: "))
    return 1000000000000 if qtdBaterias == -1 else qtdBaterias

# Atualiza bateria das meshs
def atualizarBateriaMesh(bateria, matriz):
    for i in range(1, 5):
        if bateria[i] > 0:
            consumo = (100 * 2000 + 0.02 * 2000 * (matriz[i][0] ** 2)) / 1000000000
            bateria[i] = max(bateria[i] - consumo, 0)
            if bateria[i] == 0:
                og.removeVertice(matriz, i)

def atualizarBateriaNos(bateria, matriz, tamanho): # Atualiza bateria dos nos
    for i in range(5, tamanho + 5):
        if bateria[i] > 0:
            for j in range(5):
                if matriz[i][j] > 0 and bateria[j] > 0:
                    # Formula para recepção de sinal
                    consumo_i = (50 * 2000 + 0.010 * 2000 * (matriz[i][j] ** 2)) / 1000000000

                    # Formula para envio de sinal
                    consumo_j = 100 * 2000 / 1000000000

                    # Desconta do receptor
                    bateria[i] = max(bateria[i] - consumo_i, 0)

                    if j != 0:
                        # Desconta do enviador
                        bateria[j] = max(bateria[j] - consumo_j, 0)
                        if bateria[j] == 0:
                            # Desconecta os nós zerados da rede
                            og.removeVertice(matriz, j)
                    if bateria[i] == 0:
                        # Desconecta os nós zerados da rede
                        og.removeVertice(matriz, i)
                        break

def encontrar_primeiro_no_morto(bateria, primeiroNoMorto):
    if bateria.count(0) > 0:
        for i in range(1, len(bateria)):
            if bateria[i] == 0:
                return i
    return primeiroNoMorto


def simulacao_bateria(bateria, matriz, qtdBaterias, tamanho, coordenadas_nova): # Simulação da bateria usada no processo
    for i in range(1, 5):
        bateria[i] = qtdBaterias

    primeiroNoMorto = 0
    iteracoes = 0

    while bateria.count(0) < tamanho and bateria[1:5].count(0) <= 3 and bateria.count(0) <= (tamanho * 0.80):
        atualizarBateriaNos(bateria, matriz, tamanho)
        atualizarBateriaMesh(bateria, matriz)

        if bateria.count(0) > 0 and primeiroNoMorto == 0:
            primeiroNoMorto = encontrar_primeiro_no_morto(bateria, primeiroNoMorto)
            iteracoesMorto = iteracoes

        iteracoes += 1
        if iteracoes % 10000 == 0:
            pg.desenhar_digrafo(matriz, coordenadas_nova, "Round {}".format(iteracoes), [1, 2, 3, 4])

    return iteracoes, primeiroNoMorto, iteracoesMorto


def printResultados(iteracoes, bateria, primeiroNoMorto, iteracoesMorto, qtdBaterias):
    dias = (iteracoes * 2) // 24  # Iterações em dias
    horas = (iteracoes * 2) % 24  # Iterações em horas

    print(f"Bateria Restante da Rede: \n {np.array(bateria)}")
    print ("A rede durou {} iterações. ({} anos e {} meses)".format(iteracoes,(iteracoes * 2 / 24) // 365, ((iteracoes * 2 / 24) % 365) // 30))
    print(f"Morreram {bateria.count(0)} sensores.")
    print(f"O primeiro Nó a morrer foi {primeiroNoMorto} e morreu com {iteracoesMorto}.")

    # Bateria total gasta pelos nos
    energiaNos = sum(bateriaSensor - elem for elem in bateria[5:])
    print(f"Energia gasta apenas por Nos: {round(energiaNos, 2)} joules.")

    # Bateria total gasta pelas Meshs
    energiaMesh = sum(qtdBaterias - elem for elem in bateria[1:5])
    print(f"Energia gasta apenas por Meshs: {round(energiaMesh, 2)} joules.")

    # Bateria total gasta
    energiaTotal = energiaNos + energiaMesh
    print(f"A energia total gasta é: {round(energiaTotal, 2)} joules.")


def TesteMesh(coordenadas, tamanho):
    secoes = cr.cria_secoes(coordenadas, tamanho)
    matriz = [[0] * (tamanho + 5) for _ in range(tamanho + 5)]
    quantidadeNos = tamanho + 5
    qtdBaterias = menuMesh()
    bateria = [bateriaSensor] * quantidadeNos

    # Setando conexão entre os meshs e a radio base
    coordenadas_mesh = [[750, 750], [250, 750], [250, 250], [750, 250]]
    for i, (x, y) in enumerate(coordenadas_mesh, start=1):
        matriz[i][0] = cr.distancia_vertices(x, y, coordenadas[0][0], coordenadas[0][1])

    # Localização das meshs
    indice = 5
    for i in range(4):
        for coordenada in secoes[i]:
            #Calcula a distancia com a Rádio Base
            dist_rb = cr.distancia_vertices(coordenadas[0][0], coordenadas[0][1], coordenada[0], coordenada[1])

            #Calcula a distancia com a Mesh
            dist_mesh = cr.distancia_vertices(coordenadas_mesh[i][0], coordenadas_mesh[i][1], coordenada[0],
                                              coordenada[1])
            if dist_rb > 200: #Manda direto para o Mesh
                matriz[indice][i + 1] = dist_mesh
            else: #Manda direto para a Rádio Base
                matriz[indice][0] = dist_rb
            indice += 1

    # Adiciona as coordenadas da radio base, das meshs e de todos nos
    coordenadas_nova = [coordenadas[0]] + coordenadas_mesh + [j for secao in secoes for j in secao]

    #Plota os grafos
    pg.desenhar_digrafo(matriz, coordenadas_nova, "Início da Rede", [1, 2, 3, 4])

    #Simula o consumo de energia da rede
    iteracoes, primeiroNoMorto, iteracoesMorto = simulacao_bateria(bateria, matriz, qtdBaterias, tamanho, coordenadas_nova)

    #Plota o último grafo
    pg.desenhar_digrafo(matriz, coordenadas_nova, "Fim da Rede", [1, 2, 3, 4])
    printResultados(iteracoes, bateria, primeiroNoMorto, iteracoesMorto, qtdBaterias)


