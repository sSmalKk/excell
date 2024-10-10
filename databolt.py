import os
import shutil
import re
from PyPDF2 import PdfReader
from datetime import datetime

# Função para buscar o número da fatura e a data de emissão no PDF
def buscar_dados_fatura_pdf(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        texto_completo = ""
        
        # Extrair o texto de todas as páginas
        for page in reader.pages:
            texto = page.extract_text()
            if texto:
                texto_completo += texto.replace("\n", " ")  # Remover quebras de linha para facilitar a busca

        # Padrões de busca para diferentes tipos de fatura e data
        numero_fatura = re.search(r'Fatura nº[:]? (\S+)', texto_completo)
        data_fatura = re.search(r'Data[:]? (\d{2}-\d{2}-\d{4})', texto_completo)

        if not numero_fatura:
            numero_fatura = re.search(r'Fatura nº[:]? (\w+)', texto_completo)  # Outro padrão encontrado

        if numero_fatura and data_fatura:
            return numero_fatura.group(1), data_fatura.group(1)
    except Exception as e:
        print(f"Erro ao ler {pdf_path}: {e}")
    return None, None

# Função para mover o PDF para a pasta do mês/ano de emissão, detectando duplicatas
def mover_pdf_para_pasta_por_mes(pdf_path, numero_fatura, data_emissao, root):
    try:
        # Converter a data para o formato de mês (ex: "2024-03")
        data_obj = datetime.strptime(data_emissao, "%d-%m-%Y")
        mes_ano = data_obj.strftime("%Y-%m")
        
        # Obter a estrutura de pastas relativa ao diretório raiz
        caminho_relativo = os.path.relpath(root, start=pasta_origem)
        
        # Criar a nova pasta de destino, mantendo a estrutura de pastas
        pasta_destino = os.path.join(pasta_origem, mes_ano, caminho_relativo)
        
        # Se a pasta não existir, criá-la
        if not os.path.exists(pasta_destino):
            os.makedirs(pasta_destino)
        
        # Verificar se já existe um PDF com o mesmo número de fatura
        caminho_arquivo_destino = os.path.join(pasta_destino, f"{numero_fatura}.pdf")
        if os.path.exists(caminho_arquivo_destino):
            print(f"Fatura duplicada detectada: {numero_fatura} - movendo para pasta 'duplicatas'")
            pasta_duplicata = os.path.join(pasta_origem, "duplicatas", mes_ano, caminho_relativo)
            if not os.path.exists(pasta_duplicata):
                os.makedirs(pasta_duplicata)
            shutil.move(pdf_path, os.path.join(pasta_duplicata, os.path.basename(pdf_path)))
        else:
            shutil.move(pdf_path, caminho_arquivo_destino)
            print(f"Movido {pdf_path} para {pasta_destino}")
    except Exception as e:
        print(f"Erro ao mover {pdf_path}: {e}")

# Função para processar todos os PDFs em uma pasta (e suas subpastas)
def processar_pdfs_recursivamente_por_mes(pasta_origem):
    for root, dirs, files in os.walk(pasta_origem):  # Caminha por pastas e subpastas
        for arquivo in files:
            if arquivo.endswith(".pdf"):
                caminho_pdf = os.path.join(root, arquivo)
                numero_fatura, data_emissao = buscar_dados_fatura_pdf(caminho_pdf)
                if numero_fatura and data_emissao:
                    mover_pdf_para_pasta_por_mes(caminho_pdf, numero_fatura, data_emissao, root)

# Exemplo de uso
pasta_origem = './pdfs'  # Pasta onde estão os PDFs e subpastas
processar_pdfs_recursivamente_por_mes(pasta_origem)
