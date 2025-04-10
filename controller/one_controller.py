"""
one_controller.py
Controller referente a solução da questão 1
--> Criação do grafo: rotulado, direcionado e ponderado
"""

from utils.logger import logger
from models import *


global grafo
grafo = Grafo()

def gerar_grafo():
    arestas = {}

    for email in db:
        sender = email["sender"]
        receivers = email["receiver"]
        #print(sender, receivers)

        for receiver in receivers:
            conexao = (sender.lower(), receiver.lower())
            if conexao in arestas:
                arestas[conexao] += 1
            else:
                arestas[conexao] = 1

    for (sender, receiver), peso in arestas.items():
        resultado = grafo.insere_aresta(sender, receiver, peso)
        logger.debug(f"{resultado}: {sender} > {receiver} > {peso}")

    salvar_grafo_txt()

    return '\nGrafo gerado com sucesso!'


def salvar_grafo_txt(caminho_arquivo='../data/grafo.txt'):
    with open(caminho_arquivo, 'w', encoding='utf-8') as f:
        for remetente, destinos in grafo.adj_list.items():
            linha = f"{remetente}: "
            linha += " -> ".join([f"({destinatario}, {peso})" for destinatario, peso in destinos])
            f.write(linha + "\n")

    logger.info(f"Grafo salvo com sucesso em {caminho_arquivo}")


# Somente para teste
#gerar_grafo()
