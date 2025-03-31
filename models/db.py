import os
import re
import pickle


def extract_email_addresses(text):
    """Extrai e-mails de uma string e remove duplicatas."""
    emails = set(re.findall(r'[\w\.\-]+@[\w\.\-]+', text))
    return list(emails)


def extract_field(field_name, content):
    """
    Extrai o conteúdo de um campo como 'To:', 'Cc:', 'Bcc:' considerando quebras de linha.
    """
    pattern = rf'{field_name}:\s*((?:.+\n?)+)'
    match = re.search(pattern, content, re.MULTILINE)

    if match:
        field_content = match.group(1)
        field_content = re.sub(r'\n\s+', ' ', field_content)  # Junta linhas quebradas
        return field_content.strip()
    return ""


def process_email_file(file_path, email_id):
    """Lê um arquivo de e-mail e extrai ID, Sender e Receivers."""
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

    sender = sender_match.group(1).strip() if sender_match else ""
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
    """Percorre todos os diretórios e processa os e-mails."""
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


# Exemplo de uso
root_directory = '/Users/qrozjr/Library/CloudStorage/OneDrive-GrupoMarista/Computer Science/5_Período/Grafos/Project-Email-Network/models/AmostraEnron-2016'  # Atualize conforme necessário
output_binary = '/Users/qrozjr/Library/CloudStorage/OneDrive-GrupoMarista/Computer Science/5_Período/Grafos/Project-Email-Network/models/emails_data.bin'

process_email_directory(root_directory, output_binary)
