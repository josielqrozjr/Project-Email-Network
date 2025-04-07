# logger.py
import logging
import os

# Arquivos
APP_LOG = '.log'

# Diretório dos logs
DIR_LOGS = "../data/logs"
os.makedirs(DIR_LOGS, exist_ok=True)  # Garante que a pasta de logs existe

# Configuração do logger principal
logger = logging.getLogger("main")  # Logger principal da aplicação
logger.setLevel(logging.INFO)

# Criar um formatter (formato do log)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

# Configurar handler para o log principal (app.log)
app_handler = logging.FileHandler(os.path.join(DIR_LOGS, APP_LOG))
app_handler.setFormatter(formatter)
logger.addHandler(app_handler)
