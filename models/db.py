"""
db.py

Este arquivo é usado somente para leitura do dataset fornecido e gravação dos dados em um arquivo
binário "data.bin". Estrutura dos objetos salvos no binário:
[ ID  | SENDER | RECEIVER ]
[ INT | STRING | LIST[]   ]

Falta:
- Tratar Sender:vazio e Receiver:vazio
    O Sender não pode ser vazio, pois assim não haverá vértice

"""

from dotenv import load_dotenv
import os
import re
import pickle

load_dotenv() # Load the .env

# Directory
PATH = os.getenv("ROOT_PATH")
dataset_directory = f'{PATH}/models/AmostraEnron-2016'
output_binary = f'{PATH}/models/data.bin'


def extract_email_addresses(text):
    """
    Extração de e-mails de uma string e remove duplicatas.
    """
    emails = set(re.findall(r'[\w\.\-\']+@[\w\.\-]+', text)) # Regex para identificar um endereço de e-mail
    return list(emails)


def extract_field(field_name, content):
    """
    Extração do conteúdo de um campo como 'To:', 'Cc:', 'Bcc:' considerando quebras de linha.
    """
    pattern = rf'{field_name}:\s*((?:.+\n?)+)'
    match = re.search(pattern, content, re.MULTILINE)

    if match:
        field_content = match.group(1)
        field_content = re.sub(r'\n\s+', ' ', field_content)  # Junta linhas quebradas
        return field_content.strip()
    return ""


def process_email_file(file_path, email_id):
    """
    Leitura de um arquivo de e-mail e extrai ID, Sender e Receivers.
    """
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            content = file.read()
    except Exception as e:
        print(f"Erro ao ler {file_path}: {e}")
        return None

    sender_match = re.search(r'From:\s*(.+?)(?=\n|$)', content)
    to_field = extract_field('To', content)
    cc_field = extract_field('Cc', content)
    bcc_field = extract_field('Bcc', content)

    sender = sender_match.group(1).strip() if sender_match else None # Evita que o programe pare caso o atributo seja None
    if sender is None : return False                                 # Desvia o fluxo caso o Sender/Vértice seja vazio

    receivers = set()

    if to_field:
        receivers.update(extract_email_addresses(to_field))
    if cc_field:
        receivers.update(extract_email_addresses(cc_field))
    if bcc_field:
        receivers.update(extract_email_addresses(bcc_field))

    content_email = {"id": email_id, "sender": sender, "receiver": list(receivers)}

    return content_email


def process_email_directory(root_dir, output_file):
    """
    Percorre todos os diretórios e processa os e-mails.
    """
    email_id = 1
    email_data = []

    for dirpath, _, filenames in os.walk(root_dir):
        for email_file in filenames:
            file_path = os.path.join(dirpath, email_file)

            if os.path.isfile(file_path):
                email_entry = process_email_file(file_path, email_id)
                if email_entry:
                    email_data.append(email_entry)
                    email_id += 1

    with open(output_file, 'wb') as bin_file:
        pickle.dump(email_data, bin_file)

    print(f"Processamento concluído. {len(email_data)} e-mails salvos em {output_file}")


# Chamada da função para gravar o binário
process_email_directory(dataset_directory, output_binary)
