from multiprocessing import Pool, cpu_count
from controller.one_controller import grafo
import time


def calcular_diametro(grafo):
    diametro = -1
    caminho_diametro = []

    for origem in grafo.adj_list:
        distancias, anteriores = grafo.dijkstra(origem)

        for destino, distancia in distancias.items():
            if origem != destino and distancia != float('inf') and distancia > diametro:
                diametro = distancia
                caminho_diametro = reconstruir_caminho(origem, destino, anteriores)

    return diametro, caminho_diametro


def reconstruir_caminho(origem, destino, anteriores):
    caminho = []
    atual = destino
    while atual is not None:
        caminho.insert(0, atual)
        if atual == origem:
            break
        atual = anteriores[atual]
    return caminho


def processar_dijkstra(origem):
    distancias, anteriores = grafo.dijkstra(origem)
    max_dist = -1
    max_dest = None

    for destino, distancia in distancias.items():
        if origem != destino and distancia != float('inf') and distancia > max_dist:
            max_dist = distancia
            max_dest = destino

    if max_dest:
        caminho = reconstruir_caminho(origem, max_dest, anteriores)
        return (max_dist, caminho)
    return (None, None)

def calcular_diametro_paralelo(grafo):
    with Pool(cpu_count()) as pool:
        resultados = pool.map(processar_dijkstra, list(grafo.adj_list.keys()))

    # Encontrar o resultado com maior distância
    diametro = -1
    caminho_diametro = []

    for dist, caminho in resultados:
        if dist is not None and dist > diametro:
            diametro = dist
            caminho_diametro = caminho

    return diametro, caminho_diametro


# Teste

'''if __name__ == '__main__':

    inicio = time.time()

    diametro, caminho = calcular_diametro_paralelo(grafo)

    fim = time.time()
    tempo_execucao = fim - inicio

    print(f"Diâmetro do grafo: {diametro}")
    print("Caminho correspondente:")
    print(" -> ".join(caminho))
    print(f"Tempo de execução: {tempo_execucao:.2f} segundos")
'''
