from grafo.grafo import Grafo

class GUI:
    def __init__(self):
        self.grafo = None

    def testar_grafo(self):
        print("\n--- CONSTRUINDO O GRAFO ---")
        self.grafo = Grafo()

        while True:
            print("\nOperações no Grafo:")
            print("1 - Adicionar vértice")
            print("2 - Adicionar aresta")
            print("3 - Remover vértice")
            print("4 - Remover aresta")
            print("5 - Grau de um vértice")
            print("6 - Grau de entrada")
            print("7 - Grau de saída")
            print("8 - Peso de uma aresta")
            print("9 - Verificar se existe aresta")
            print("10 - Verificar ordem")
            print("11 - Verificar tamanho")
            print("12 - Imprimir lista de adjacências")
            print("0 - Voltar")

            opcao = input("\nDigite o número da opção: ")

            if opcao == "1":
                vertice = input("\nDigite o nome do vértice: ")
                resultado = self.grafo.insere_vertice(vertice)
                print(f"RESULTADO: {resultado}")

            elif opcao == "2":
                u = input("\nDigite o primeiro vértice: ")
                v = input("Digite o segundo vértice: ")
                peso = int(input("Digite o peso da aresta: "))
                resultado = self.grafo.insere_aresta(u, v, peso)
                print(f"RESULTADO: {resultado}")

            elif opcao == "3":
                vertice = input("\nDigite o vértice a ser removido: ")
                resultado = self.grafo.remove_vertice(vertice)
                print(f"RESULTADO: {resultado}")

            elif opcao == "4":
                u = input("\nDigite o primeiro vértice: ")
                v = input("Digite o segundo vértice: ")
                resultado = self.grafo.remove_aresta(u, v)
                print(f"RESULTADO: {resultado}")

            elif opcao == "5":
                vertice = input("\nDigite o vértice: ")
                print(f"Graus do vértice: {vertice}")
                print(f"Entrada: {self.grafo.grau_entrada(vertice)}")
                print(f"Saída: {self.grafo.grau_saida(vertice)}")
                print(f"Total: {self.grafo.grau(vertice)}")

            elif opcao == "6":
                vertice = input("\nDigite o vértice: ")
                print(f"Grau de entrada de {vertice}: {self.grafo.grau_entrada(vertice)}")

            elif opcao == "7":
                vertice = input("\nDigite o vértice: ")
                print(f"Grau de saída de {vertice}: {self.grafo.grau_saida(vertice)}")

            elif opcao == "8":
                u = input("\nDigite o primeiro vértice: ")
                v = input("Digite o segundo vértice: ")
                resultado = self.grafo.get_peso(u, v)
                print(f"RESULTADO: {resultado}")

            elif opcao == "9":
                u = input("\nDigite o primeiro vértice: ")
                v = input("Digite o segundo vértice: ")
                resultado = self.grafo.tem_aresta(u, v)
                print(f"RESULTADO: {resultado}")

            elif opcao == "10":
                print(f"Ordem: {self.grafo.ordem}")

            elif opcao == "11":
                print(f"Tamanho: {self.grafo.tamanho}")

            elif opcao == "12":
                self.grafo.imprime_lista_adjacencias()

            elif opcao == "0":
                print("Voltando ao menu principal...")
                break

            else:
                print("Opção inválida. Tente novamente.")
