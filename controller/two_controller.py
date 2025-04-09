"""
two_controller.py
Controller referente a análise do grafo
--> Extração de métricas e informações da rede construída
"""

from utils.logger import logger
from models import *
from controller.one_controller import grafo

def get_numero_vertices():
    return grafo.ordem

def get_numero_arestas():
    return grafo.tamanho

def get_vertices_isolados():
    vertices_isolados = []
    for vertice in grafo.adj_list:
        if not grafo.adj_list[vertice]:
            tem_entrada = False
            for v, destinos in grafo.adj_list.items():
                if any(d[0] == vertice for d in destinos):
                    tem_entrada = True
                    break
            
            if not tem_entrada:
                vertices_isolados.append(vertice)
    
    return vertices_isolados, len(vertices_isolados)

def get_maiores_graus_saida(top=20):
    """
    d. Os 20 indivíduos que possuem maior grau de saída e os valores
    correspondentes (de maneira ordenada e decrescente de acordo com o grau)
    """
    graus_saida = {}
    for vertice, destinos in grafo.adj_list.items():
        graus_saida[vertice] = len(destinos)
    maiores_graus = sorted(graus_saida.items(), key=lambda x: x[1], reverse=True)
    return maiores_graus[:top]

def get_maiores_graus_entrada(top=20):
    """
    e. Os 20 indivíduos que possuem maior grau de entrada e os valores
    correspondentes (de maneira ordenada e decrescente de acordo com o grau)
    """
    graus_entrada = {}
    for vertice in grafo.adj_list:
        graus_entrada[vertice] = 0
    for vertice, destinos in grafo.adj_list.items():
        for dest, _ in destinos:
            if dest in graus_entrada:
                graus_entrada[dest] += 1
            else:
                graus_entrada[dest] = 1
    maiores_graus = sorted(graus_entrada.items(), key=lambda x: x[1], reverse=True)
    return maiores_graus[:top]

def exibir_info_grafo():
    """
    Função que exibe todas as informações solicitadas do grafo
    """
    print("\n=== INFORMAÇÕES DO GRAFO ===")
    print(f"Número de vértices (ordem): {get_numero_vertices()}")
    print(f"Número de arestas (tamanho): {get_numero_arestas()}")
    
    vertices_isolados, num_isolados = get_vertices_isolados()
    print(f"Número de vértices isolados: {num_isolados}")
    
    print("\n=== TOP 20 VÉRTICES COM MAIOR GRAU DE SAÍDA ===")
    for i, (vertice, grau) in enumerate(get_maiores_graus_saida(20), 1):
        print(f"{i}. {vertice}: {grau}")
    
    print("\n=== TOP 20 VÉRTICES COM MAIOR GRAU DE ENTRADA ===")
    for i, (vertice, grau) in enumerate(get_maiores_graus_entrada(20), 1):
        print(f"{i}. {vertice}: {grau}")

if __name__ == "__main__":
    exibir_info_grafo()