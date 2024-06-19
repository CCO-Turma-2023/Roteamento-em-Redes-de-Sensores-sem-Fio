import matplotlib.pyplot as plt
import igraph as ig

def desenhar_digrafo(matriz_adjacencia, coordenadas, titulo=None, clusterHeads = []):
    # Verifica se as dimensões da matriz de adjacência são consistentes com as coordenadas
    n = len(matriz_adjacencia)
    if n != len(coordenadas):
        raise ValueError("O tamanho da matriz de adjacência e a lista de coordenadas devem ser iguais.")

    # Encontra os índices dos vértices "mortos"
    vertices_mortos = [i for i in range(n) if all(x == -1 for x in matriz_adjacencia[i])]
    vertices = list(set(i for i in range(n)) - set(vertices_mortos))
    # Converte a matriz de adjacência em uma lista de arestas
    arestas = []
    for i in range(n):
        for j in range(n):
            if matriz_adjacencia[i][j] != 0 and i not in vertices_mortos and j not in vertices_mortos:
                arestas.append((i, j))

    # Cria o grafo direcionado a partir da lista de arestas
    grafo = ig.Graph(n, directed=True)
    grafo.add_edges(arestas)

    # Define as coordenadas dos vértices
    layout = coordenadas

    # Desenha o grafo usando Matplotlib
    fig, ax = plt.subplots(figsize=(12, 12))

    # Desenha os vértices "mortos"
    for idx in vertices_mortos:
        x, y = layout[idx]
        ax.scatter(x, y, s=400, c='red', edgecolors='black', zorder=2)
        ax.text(x, y, str(idx), fontsize=12, ha='center', va='center', zorder=3)

    # Desenha os vértices com conexões
    for idx, (x, y) in enumerate(layout):
        if idx not in vertices_mortos:
            ax.scatter(x, y, s=400, c='lightblue', edgecolors='black', zorder=2)
            ax.text(x, y, str(idx), fontsize=12, ha='center', va='center', zorder=3)

    for idx in clusterHeads:
        if idx not in vertices_mortos and sum(elem for elem in matriz_adjacencia[idx] if elem != -1) != 0:
            x, y = layout[idx]
            ax.scatter(x, y, s=400, c='blue', edgecolors='black', zorder=2)
            ax.text(x, y, str(idx), fontsize=12, ha='center', va='center', zorder=3)

    for v in vertices:
        if sum(elem for elem in matriz_adjacencia[v] if elem != -1) == 0:
            x, y = layout[v]
            ax.scatter(x, y, s=400, c='darkgray', edgecolors='black', zorder=2)
            ax.text(x, y, str(v), fontsize=12, ha='center', va='center', zorder=3)

    x, y = layout[0]
    ax.scatter(x, y, s=400, c='orange', edgecolors='black', zorder=2)
    ax.text(x, y, str(0), fontsize=12, ha='center', va='center', zorder=3)

    # Desenha as arestas com setas
    for i, j in arestas:
        ax.annotate("",
                    xy=(layout[j][0], layout[j][1]), xycoords='data',
                    xytext=(layout[i][0], layout[i][1]), textcoords='data',
                    arrowprops=dict(arrowstyle="->", color='black', lw=1.5, shrinkA=10, shrinkB=10),
                    zorder=1)

    # Configurações adicionais do gráfico
    ax.set_aspect('equal')
    ax.set_xticks([])
    ax.set_yticks([])

    # Ajusta os limites do gráfico
    x_coords, y_coords = zip(*layout)
    ax.set_xlim(min(x_coords) - 50, max(x_coords) + 50)
    ax.set_ylim(min(y_coords) - 50, max(y_coords) + 50)
    ax.set_title(titulo, size=32)

    plt.show()