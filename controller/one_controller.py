"""
one_controller.py
Controller referente a solução da questão 1
--> Criação do grafo: rotulado, direcionado e ponderado
"""

from utils.logger import logger
from models import *


global grafo
grafo = Grafo()

<<<<<<< HEAD

# Função para gerar o grafo e salvá-lo automaticamente no diretório padrão
def gerar_grafo():
    arestas = {}                        # Armazenar arestas
=======
>>>>>>> e448fc7528551384ffb6594ac69215a50956bad4

# Função para gerar o grafo e salvá-lo automaticamente no diretório padrão
def gerar_grafo():
    arestas = {}                        # Armazenar arestas, adiante serão armazenados como pares de chave -> valor

    for email in db:                    # Percorrer todos os dados de DB armazenando nas
        sender = email["sender"]        # variáveis os valores desejados
        receivers = email["receiver"]
        #print(sender, receivers)       # Fins de Debug

        for receiver in receivers:
            conexao = (sender.lower(), receiver.lower())    # Lower() para tratar emails com uniformidade
            if conexao in arestas:
                arestas[conexao] += 1                       # Caso a aresta/conexão já exista, então incrementa o peso
            else:
                arestas[conexao] = 1                        # Caso seja não exista, define peso 1 (primeiro envio)


    for (sender, receiver), peso in arestas.items():        # Para cada par de chave -> valor do dicionário "arestas"
        resultado = grafo.insere_aresta(sender, receiver, peso)     # Insere cada aresta no Grafo
        logger.warning(f"{resultado}: {sender} > {receiver} > {peso}")

    salvar_grafo_txt() # Chamada da função para salvar o grafo em formato de texto

    return '\nGrafo gerado com sucesso!'


# Função para salvar o grafo em um arquivo txt
def salvar_grafo_txt(nome_arquivo='grafo.txt'):                 # Nome do arquivo pode ser alterado via parâmetro
    caminho_arquivo = f'../data/{nome_arquivo}'
    with open(caminho_arquivo, 'w', encoding='utf-8') as f:
        for remetente, destinos in grafo.adj_list.items():      # Itera sobre a lista de adjacências
            linha = f"{remetente}: "                            # Configurar a saída
            linha += " -> ".join([f"({destinatario}, {peso})" for destinatario, peso in destinos])
            f.write(linha + "\n")   # Gravar no arquivo

    logger.info(f"Grafo salvo com sucesso em {caminho_arquivo}")    # Controle de logs


# Gerar o grafo para disponibilizar para as outros controllers
gerar_grafo()


# Testes
#file = "teste.txt"
#salvar_grafo_txt(file)
