from controller.one_controller import grafo

# Dijkstra com limite de distância.
def vertices_ate_distancia(vertice_origem, limite_distancia):
    # Dicionário que armazena as menores distâncias encontradas até o momento que não tenham superado o limite_distancia.
    distancias = {}

    # Fila que contém o valor acumulado e nome do vértice.
    fila = [(0, vertice_origem)]

    # Lista dos vértices que estão dentro do limite (até a distância D).
    dentro_do_limite = []

    # Enquanto houver elementos na fila...
    while fila:
        # Encontra o vértice com menor distância acumulada
        menor_indice = 0

        # Percorre todos os elementos da fila e utiliza a lógica do alg. de Dijkstra (encontrar o vérice com menor distância para prossguir com o algoritmo de Dijkstra). 
        for i in range(1, len(fila)):
            # Caso a distância acumulada seja menor no caminho calculado...
            if fila[i][0] < fila[menor_indice][0]:
                # Armazena o índice do caminho com menor custo.
                menor_indice = i

        # Remove e processa o próximo vértice de menor custo.
        distancia_atual, vertice = fila.pop(menor_indice)

        if vertice in distancias:
            continue # Caso já tenhamos calculado a menor distância para este vértice, ignoramos o processamento, ou seja, pulamos e voltamos para o início do While e capturamos o próximo vértice da fila.

        # Armazenamos no dicionário de distâncias o vértice e a menor distância encontrada até o momento.
        distancias[vertice] = distancia_atual

        # Caso a distância acumulada não tenha passado do limite passado como parâmetro, armazenamos na lista de distâncias dentro_do_limite.
        if 0 < distancia_atual <= limite_distancia:
            dentro_do_limite.append(vertice)

        if distancia_atual >= limite_distancia:
            continue # Caso a distância tenha passado do limite, reinicia o laço While com o próximo elemento da fila.

        # Verificando os vizinhos
        if vertice in grafo.adj_list:
            # Percorre os vizinhos do vértice atual.
            for vizinho, peso in grafo.adj_list[vertice]:
                # Se o vizinho ainda não tiver sido visitado (sem distância registrada no dicionário "distancias")
                if vizinho not in distancias:
                        nova_distancia = distancia_atual + peso
                        # Calculamos a distância acumulada dos vizinhos e caso esteja dentro do limite, incluímos na fila de prioridades.
                        if nova_distancia <= limite_distancia:
                            fila.append((nova_distancia, vizinho))

    return dentro_do_limite

def verificar_menor_caminho():
    origem = input("Qual o vértice de origem: ")
    
    if origem not in grafo.adj_list:
        print("Vértice de origem não encontrado no grafo!")
        return

    # Aqui tratamos tanto números negativos como número não inteiros.
    try:
        distancia_maxima = int(input("Qual a distância máxima: "))
        if distancia_maxima < 0:
            print("A distância máxima deve ser um inteiro não negativo!")
            return
    except ValueError:
        print("Entrada inválida! Digite um número inteiro para a distância.")
        return
    print(f"\nVÉRTICES COM MENOR CAMINHO ATÉ A DISTÂNCIA ACUMULADA DE {distancia_maxima}:")
    print(vertices_ate_distancia(origem, distancia_maxima))

# Teste
verificar_menor_caminho()