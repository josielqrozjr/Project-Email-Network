"""
third_controller.py
Controller referente a solução da questão 3
--> Grafo Euleriano
Em grafos não direcionados ele precisa ser: conexo e cada nó deve ter grau par
Em grafos direcionados deve ser fortemente conexo e o grau de entrada = grau de saída

"""
from controller.one_controller import grafo
from models import *

#for directed graphs


def grafo_euleriano_direcionado():
    eh_balanceado = True
    tem_vertice_isolado = False

    com_entrada = set()
    com_saida = set()

    # Um único laço principal sobre as arestas
    for origem, destinos in grafo.adj_list.items():
        if destinos:
            com_saida.add(origem)

        entradas_por_vertice = {}
        for destino, _ in destinos:
            com_entrada.add(destino)
            entradas_por_vertice[destino] = entradas_por_vertice.get(destino, 0) + 1

        

        # Verifica se origem está balanceado (entrada == saída) de forma parcial
        # Aqui só podemos afirmar algo sobre a saída; entrada será validada depois

    # Segundo e último laço apenas para checar propriedades finais
    for vertice in grafo.adj_list:
        grau_saida = len(grafo.adj_list[vertice])
        grau_entrada = (vertice in com_entrada)  # sabemos apenas se tem entrada

        if grau_entrada and grau_saida == 0:
            eh_balanceado = False
        elif not grau_entrada and grau_saida > 0:
            eh_balanceado = False

        if vertice not in com_entrada and vertice not in com_saida:
            tem_vertice_isolado = True

        

    return eh_balanceado, tem_vertice_isolado

    not_valid_nodes = [] #array to store any node with invalid degree

    

    return