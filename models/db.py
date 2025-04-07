from dotenv import load_dotenv
from utils.logger import logger
import os
import pickle

load_dotenv()  #Load the .env file variables

# Nome do arquivo binário onde os dados foram armazenados
PATH = os.getenv("ROOT_PATH")
bin_file = f'{PATH}/data/data.bin'


# Ler os dados do arquivo binário
def read_binary_file(file_path):
    try:
        with open(file_path, "rb") as f:
            data_email = pickle.load(f)  # Carrega todos os registros do arquivo
            logger.info(f"Total de registros: {len(data_email)}")
            return data_email

    except FileNotFoundError:
        logger.warning("Arquivo binário não encontrado.")
    except Exception as e:
        logger.critical(f"Erro ao ler o arquivo: {e}")


# Chamar a função para testar
db = read_binary_file(bin_file)

# Teste da variavel
'''
for i, db in enumerate(db[:3]):
    #if db['sender'] is not None:
    print(f"ID: {db['id']}")
    print(f"Sender: {db['sender']}")
    print(f"Receiver: {db['receiver']}")
    print("-" * 50)
'''
