import pickle

# Nome do arquivo binário onde os dados foram armazenados
bin_file = "/Users/qrozjr/Library/CloudStorage/OneDrive-GrupoMarista/Computer Science/5_Período/Grafos/Project-Email-Network/models/emails_data.bin"


# Ler os dados do arquivo binário
def read_binary_file(file_path, num_records=2):
    try:
        with open(file_path, "rb") as f:
            emails = pickle.load(f)  # Carrega todos os registros do arquivo
            print(f"Total de registros: {len(emails)}\n")

            # Exibir alguns registros para teste
            for i, email in enumerate(emails[:num_records]):
                print(f"ID: {email['id']}")
                print(f"Sender: {email['sender']}")
                print(f"Receiver: {email['receiver']}")
                print("-" * 50)

    except FileNotFoundError:
        print("Arquivo binário não encontrado.")
    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}")


# Chamar a função para testar
read_binary_file(bin_file)
