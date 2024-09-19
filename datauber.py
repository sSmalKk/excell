import os
import shutil
import re
from PyPDF2 import PdfReader
from datetime import datetime

# Função para buscar a data de emissão após a palavra "Data da fatura"
def buscar_data_emissao_pdf(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        texto_completo = ""
        
        # Extrair o texto de todas as páginas
        for page in reader.pages:
            texto = page.extract_text()
            if texto:
                texto_completo += texto.replace("\n", " ")  # Remover quebras de linha para facilitar a busca
        
        # Usar regex para encontrar a data de emissão abaixo da "Data da fatura"
        match = re.search(r'Data da fatura: (\d{2}-\d{2}-\d{4})', texto_completo)
        if match:
            data_str = match.group(1)  # Capturar a data
            return data_str
    except Exception as e:
        print(f"Erro ao ler {pdf_path}: {e}")
    return None

# Função para mover o PDF para a pasta do mês de emissão, mantendo a estrutura de diretórios
def mover_pdf_para_pasta_por_mes(pdf_path, data_emissao, root):
    try:
        # Converter a data para o formato de mês (ex: "2024-07")
        data_obj = datetime.strptime(data_emissao, "%d-%m-%Y")
        mes_ano = data_obj.strftime("%Y-%m")
        
        # Obter a estrutura de pastas relativa ao diretório raiz
        caminho_relativo = os.path.relpath(root, start=pasta_origem)
        
        # Criar a nova pasta de destino, mantendo a estrutura de pastas
        pasta_destino = os.path.join(pasta_origem, mes_ano, caminho_relativo)
        
        # Se a pasta não existir, criá-la
        if not os.path.exists(pasta_destino):
            os.makedirs(pasta_destino)
        
        # Mover o arquivo para a nova pasta, mantendo o nome original do arquivo
        shutil.move(pdf_path, os.path.join(pasta_destino, os.path.basename(pdf_path)))
        print(f"Movido {pdf_path} para {pasta_destino}")
    except Exception as e:
        print(f"Erro ao mover {pdf_path}: {e}")

# Função para processar todos os PDFs em uma pasta (e suas subpastas)
def processar_pdfs_recursivamente_por_mes(pasta_origem):
    for root, dirs, files in os.walk(pasta_origem):  # Caminha por pastas e subpastas
        for arquivo in files:
            if arquivo.endswith(".pdf"):
                caminho_pdf = os.path.join(root, arquivo)
                data_emissao = buscar_data_emissao_pdf(caminho_pdf)
                if data_emissao:
                    mover_pdf_para_pasta_por_mes(caminho_pdf, data_emissao, root)

# Exemplo de uso
pasta_origem = './pdfs'  # Pasta onde estão os PDFs e subpastas
processar_pdfs_recursivamente_por_mes(pasta_origem)
