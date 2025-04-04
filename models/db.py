from dotenv import load_dotenv
import os
import pickle

load_dotenv()  #Load the .env file variables

# Nome do arquivo binário onde os dados foram armazenados
PATH = os.getenv("ROOT_PATH")
bin_file = f'{PATH}/data/data.bin'


# Ler os dados do arquivo binário
def read_binary_file(file_path, num_records=33):
    try:
        with open(file_path, "rb") as f:
            emails = pickle.load(f)  # Carrega todos os registros do arquivo
            print(f"Total de registros: {len(emails)}\n")

            # Exibir alguns registros para teste
            for i, email in enumerate(emails[:num_records]):
                #if email['sender'] is not None:
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
