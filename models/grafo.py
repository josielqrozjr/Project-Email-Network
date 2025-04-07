"""
grafo.py
"""

from collections import defaultdict
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
