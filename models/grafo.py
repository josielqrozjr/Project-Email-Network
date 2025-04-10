"""
grafo.py
"""

from collections import defaultdict
import heapq
#from utils.logger import logger


class Grafo:
    def __init__(self):
        self.ordem = 0                                          # Quantidade de vertices
        self.tamanho = 0                                        # Quantidade de arestas
        self.adj_list = defaultdict(list)                       # Lista de adjacências

    def insere_vertice(self, vertice):
        if vertice not in self.adj_list:
            self.adj_list[vertice] = []
            self.ordem += 1

    def insere_aresta(self, vertice_x, vertice_y, peso):
        if peso <= 0: return 'Pesos negativos não são permitidos!'

        vertices = [vertice_x, vertice_y]
        for vertice in vertices:                                # Validar se os vertices existem
            if vertice not in self.adj_list : self.insere_vertice(vertice)

        for i, (vertex, weight) in enumerate(self.adj_list[vertice_x]):
            if vertex == vertice_y:
                self.adj_list[vertice_x][i] = (vertice_y, peso)
                return 'Peso atualizado!'

        self.adj_list[vertice_x].append((vertice_y, peso))
        self.tamanho += 1

        return 'Aresta adicionada!'

    def dijkstra(self, origem):
        distancias = {v: float('inf') for v in self.adj_list}
        anteriores = {v: None for v in self.adj_list}
        distancias[origem] = 0

        fila = [(0, origem)]

        while fila:
            dist_atual, atual = heapq.heappop(fila)

            for vizinho, peso in self.adj_list[atual]:
                nova_dist = dist_atual + peso
                if nova_dist < distancias[vizinho]:
                    distancias[vizinho] = nova_dist
                    anteriores[vizinho] = atual
                    heapq.heappush(fila, (nova_dist, vizinho))

        return distancias, anteriores


def dijkstra_new(self, origem):
    distancias = {v: float('inf') for v in self.adj_list}
    anteriores = {v: None for v in self.adj_list}
    distancias[origem] = 0

    fila = [(0, origem)]
    visitados = set()

    while fila:
        dist_atual, atual = heapq.heappop(fila)

        if atual in visitados:
            continue
        visitados.add(atual)

        for vizinho, peso in self.adj_list[atual]:
            if vizinho in visitados:
                continue

            nova_dist = dist_atual + peso
            if nova_dist < distancias[vizinho]:
                distancias[vizinho] = nova_dist
                anteriores[vizinho] = atual
                heapq.heappush(fila, (nova_dist, vizinho))

    return distancias, anteriores
