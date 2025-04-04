from controller.controller import Controller

def main():
    controller = Controller()

    while True:
        print("\nEscolha a estrutura para testar:")
        print("1 - Grafo")
        print("0 - Encerrar")

        opcao = input("\nDigite o número da opção: ")

        if opcao == "1":
            controller.testar_grafo()
        elif opcao == "0":
            print("Encerrando o programa.")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
