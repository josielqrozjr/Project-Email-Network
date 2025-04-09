#from views.gui import GUI
from controller.one_controller import gerar_grafo
from controller.two_controller import exibir_info_grafo

def main():
    #user_interface = GUI()
    while True:
        print("\nEscolha a estrutura para testar:")
        print("1 - Gerar novo")
        print("2 - Extrair informações")
        print("0 - Encerrar")

        opcao = input("\nDigite o número da opção: ")

        if opcao == "1":
            resultado = gerar_grafo()
            print(resultado)
        elif opcao == "2":
            exibir_info_grafo()
        elif opcao == "0":
            print("Encerrando o programa.")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
