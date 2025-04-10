"""
two_controller.py
Controller referente a solução da questão 1 (análise do grafo)
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
    vertices_com_entrada = set()

    for vertice, destinos in grafo.adj_list.items():
        for destino in destinos:
            vertices_com_entrada.add(destino)
    
    for vertice in grafo.adj_list:
        if not grafo.adj_list[vertice] and vertice not in vertices_com_entrada:
            vertices_isolados.append(vertice)
    
    return vertices_isolados, len(vertices_isolados)

def get_vertices_com_loops():
    vertices_com_loops = []
    
    for vertice, destinos in grafo.adj_list.items():
        if any(d[0] == vertice for d in destinos):
            vertices_com_loops.append(vertice)
    
    return vertices_com_loops, len(vertices_com_loops)

def get_maiores_graus_saida(top=20):
    graus_saida = {}
    
    for vertice, destinos in grafo.adj_list.items():
        graus_saida[vertice] = len(destinos)
    maiores_graus = sorted(graus_saida.items(), key=lambda x: x[1], reverse=True)
    return maiores_graus[:top]

def get_maiores_graus_entrada(top=20):
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
    print("\n=== INFORMAÇÕES DO GRAFO ===")
    print(f"Número de vértices (ordem): {get_numero_vertices()}")
    print(f"Número de arestas (tamanho): {get_numero_arestas()}")
    
    vertices_isolados, num_isolados = get_vertices_isolados()
    print(f"Número de vértices isolados: {num_isolados}")
    if num_isolados > 0:
        print("Exemplos de vértices isolados:")
        for i, v in enumerate(vertices_isolados[:5], 1):
            print(f"  {i}. {v}")
        if num_isolados > 5:
            print(f"  ... e mais {num_isolados - 5} vértices")
    
    vertices_com_loops, num_loops = get_vertices_com_loops()
    print(f"Número de vértices com loops (auto-arestas): {num_loops}")
    if num_loops > 0:
        print("Exemplos de vértices com loops:")
        for i, v in enumerate(vertices_com_loops[:5], 1):
            print(f"  {i}. {v}")
        if num_loops > 5:
            print(f"  ... e mais {num_loops - 5} vértices")
    
    print("\n=== TOP 20 VÉRTICES COM MAIOR GRAU DE SAÍDA ===")
    for i, (vertice, grau) in enumerate(get_maiores_graus_saida(20), 1):
        print(f"{i}. {vertice}: {grau}")
    
    print("\n=== TOP 20 VÉRTICES COM MAIOR GRAU DE ENTRADA ===")
    for i, (vertice, grau) in enumerate(get_maiores_graus_entrada(20), 1):
        print(f"{i}. {vertice}: {grau}")

if __name__ == "__main__":
    exibir_info_grafo()