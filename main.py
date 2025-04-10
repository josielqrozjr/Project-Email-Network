#from views.gui import GUI
from controller.one_controller import gerar_grafo
from controller.third_controller import grafo_euleriano_direcionado
from controller.two_controller import exibir_info_grafo


def main():
    #user_interface = GUI()
    while True:
        print("\nEscolha a estrutura para testar:")
        print("1 - Gerar novo")
        print("2 - Extrair informações")
        print("3 - Euleriano")

        print("0 - Encerrar")

        opcao = input("\nDigite o número da opção: ")

        if opcao == "1":
            resultado = gerar_grafo()
            print(resultado)
        elif opcao == "2":
            exibir_info_grafo()
        elif opcao == "3":
            eh_euleriano, condicoes = grafo_euleriano_direcionado()
            if eh_euleriano:
                print(condicoes)
            else:
                print("O grafo não é euleriano. Condições não satisfeitas:")
                for condicao in condicoes:
                    print(f"- {condicao}")

        elif opcao == "0":
            print("Encerrando o programa.")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
