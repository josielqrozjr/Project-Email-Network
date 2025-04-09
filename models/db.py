from dotenv import load_dotenv
from utils.logger import logger
import os
import pickle

load_dotenv()

PATH = os.getenv("ROOT_PATH", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
bin_file = f'{PATH}/data/data.bin'

if not os.path.exists(bin_file):
    bin_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'data.bin')
    logger.warning(f"Usando caminho alternativo para o arquivo binário: {bin_file}")


def read_binary_file(file_path):
    try:
        with open(file_path, "rb") as f:
            data_email = pickle.load(f)  # Carrega todos os registros do arquivo
            logger.info(f"Total de registros: {len(data_email)}")
            return data_email

    except FileNotFoundError:
        logger.warning(f"Arquivo binário não encontrado: {file_path}")
    except Exception as e:
        logger.critical(f"Erro ao ler o arquivo: {e}")


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
