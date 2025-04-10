from models import *
from models import *
from controller.one_controller import grafo

def dfs(v, visited, adj_list):
    visited.add(v)
    for (neighbour, _) in adj_list[v]:
        if neighbour not in visited:
            dfs(neighbour, visited, adj_list)

# Verifica se o grafo é fortemente conexo
def is_strongly_connected():
    visited = set()
    vertices = list(grafo.adj_list.keys())
    if not vertices:
        return False

    # DFS no grafo original
    dfs(vertices[0], visited, grafo.adj_list)
    if len(visited) != len(vertices):
        return False

    # Cria grafo transposto
    transposed = {v: [] for v in vertices}
    for origem, destinos in grafo.adj_list.items():
        for destino, peso in destinos:
            transposed[destino].append((origem, peso))

    # DFS no transposto
    visited.clear()
    dfs(vertices[0], visited, transposed)
    return len(visited) == len(vertices)

# Verifica se o grafo direcionado é euleriano
def grafo_euleriano_direcionado():
    condicoes_nao_satisfeitas = []

    # Verifica conectividade
    if not is_strongly_connected():
        condicoes_nao_satisfeitas.append("O grafo não é fortemente conexo.")

    eh_balanceado = True
    tem_isolado = False

    grau_entrada = {}
    grau_saida = {}

    # Inicializa os graus
    for vertice in grafo.adj_list:
        grau_entrada[vertice] = 0
        grau_saida[vertice] = len(grafo.adj_list[vertice])

    # Conta entradas
    for origem in grafo.adj_list:
        for destino, _ in grafo.adj_list[origem]:
            grau_entrada[destino] = grau_entrada.get(destino, 0) + 1

    # Verifica condições
    for vertice in grafo.adj_list:
        entrada = grau_entrada.get(vertice, 0)
        saida = grau_saida.get(vertice, 0)

        if entrada != saida:
            eh_balanceado = False

        if entrada == 0 and saida == 0:
            tem_isolado = True

    if not eh_balanceado:
        condicoes_nao_satisfeitas.append("O grafo possui vértices com grau de entrada diferente do grau de saída.")
    if tem_isolado:
        condicoes_nao_satisfeitas.append("O grafo possui vértices isolados.")

    if condicoes_nao_satisfeitas:
        return False, condicoes_nao_satisfeitas

    return True, "O grafo é euleriano."
