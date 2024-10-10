import os
import shutil
import re
from PyPDF2 import PdfReader
from datetime import datetime

# Função para buscar dados de emissão e nome do emitente
def buscar_dados_emissao_nome_pdf(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        texto_completo = ""
        
        # Extrair o texto de todas as páginas
        for page in reader.pages:
            texto = page.extract_text()
            if texto:
                texto_completo += texto.replace("\n", " ")  # Remover quebras de linha para facilitar a busca
        
        # Usar regex para encontrar a "Data de Emissão" e "Nome"
        data_emissao = re.search(r'DATA DE EMISSÃO.*? (\d{2}/\d{2}/\d{4})', texto_completo)
        nome_emitente = re.search(r'NOME\s+([A-Z ]+)', texto_completo)
        
        if data_emissao and nome_emitente:
            data_str = data_emissao.group(1)  # Captura a data
            nome = nome_emitente.group(1).strip()  # Captura o nome do emitente
            
            # Tentar converter a data para objeto datetime
            try:
                data_obj = datetime.strptime(data_str, "%d/%m/%Y")
                return nome, data_obj.strftime("%Y-%m")
            except ValueError:
                print(f"Erro ao converter a data: {data_str}")
                return None, None
        else:
            print(f"Dados não encontrados no arquivo: {pdf_path}")
    except Exception as e:
        print(f"Erro ao ler {pdf_path}: {e}")
    return None, None

# Função para mover o PDF para a pasta de ano/mês/nome do emitente
def mover_pdf_para_pasta_por_ano_mes_emitente(pdf_path, nome_emitente, ano_mes, root):
    try:
        # Obter a estrutura de pastas relativa ao diretório raiz
        caminho_relativo = os.path.relpath(root, start=pasta_origem)
        
        # Criar a nova pasta de destino no formato "ano/mes/nome_emitente", mantendo a estrutura de pastas
        pasta_destino = os.path.join(pasta_origem, ano_mes, nome_emitente, caminho_relativo)
        
        # Se a pasta não existir, criá-la
        if not os.path.exists(pasta_destino):
            os.makedirs(pasta_destino)
        
        # Mover o arquivo para a nova pasta, mantendo o nome original do arquivo
        shutil.move(pdf_path, os.path.join(pasta_destino, os.path.basename(pdf_path)))
        print(f"Movido {pdf_path} para {pasta_destino}")
    except Exception as e:
        print(f"Erro ao mover {pdf_path}: {e}")

# Função para processar todos os PDFs em uma pasta (e suas subpastas)
def processar_pdfs_recursivamente_por_emitente(pasta_origem):
    for root, dirs, files in os.walk(pasta_origem):  # Caminha por pastas e subpastas
        for arquivo in files:
            if arquivo.endswith(".pdf"):
                caminho_pdf = os.path.join(root, arquivo)
                nome_emitente, ano_mes = buscar_dados_emissao_nome_pdf(caminho_pdf)
                if nome_emitente and ano_mes:
                    mover_pdf_para_pasta_por_ano_mes_emitente(caminho_pdf, nome_emitente, ano_mes, root)

# Exemplo de uso
pasta_origem = './pdfs'  # Pasta onde estão os PDFs e subpastas
processar_pdfs_recursivamente_por_emitente(pasta_origem)
