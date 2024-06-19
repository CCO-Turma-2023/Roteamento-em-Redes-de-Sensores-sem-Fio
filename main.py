import numpy as np
from Metodos import MetodoMaisProximo as mp, MetodoRRCurtoAlcance as mrrc, MetodoRRLongoAlcance as mrrl, \
    MetodoMesh as mm, MetodoDijkstra as md

if __name__ == "__main__":
    quantidadeNos = input("Quantidade de dados do dataset (50, 100, 200 ou 400): ")
    arquivo = open(f"Projeto - Datasets/Cenário 5 - Rede {quantidadeNos}.txt", "r")

    tamanho = int(arquivo.readline())
    coordenadas = np.genfromtxt(arquivo, "float")

    print("Digite 1 para usar o método Dijkstra")
    print("Digite 2 para usar a rede Original")
    print("Digite 3 para usar o método Mesh")
    print("Digite 4 para usar o método de Round Robin de Curto Alcance")
    print("Digite 5 para usar o método de Round Robin de Longo Alcance")

    escolha = int(input("Digite: "))
    if escolha == 1:
        md.TesteDijkstra(coordenadas, tamanho)
    elif escolha == 2:
        mp.TesteMaisProximo(coordenadas, tamanho)
    elif escolha == 3:
        mm.TesteMesh(coordenadas, tamanho)
    elif escolha == 4:
        mrrc.testeRR_CurtoAlcance(coordenadas, tamanho)
    elif escolha == 5:
        mrrl.testeRR_LongoAlcance(coordenadas, tamanho)
    else:
        print("Opção inválida")