import os
import shutil
import re
from PyPDF2 import PdfReader
from datetime import datetime

# Função para buscar dados da fatura e outras variantes
def buscar_dados_fatura_pdf(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        texto_completo = ""
        
        # Extrair o texto de todas as páginas
        for page in reader.pages:
            texto = page.extract_text()
            if texto:
                texto_completo += texto.replace("\n", " ")  # Remover quebras de linha para facilitar a busca
        
        # Usar regex para encontrar diferentes variações de faturas e datas
        numero_documento_externo = re.search(r'Nº do documento externo (\S+)', texto_completo)
        numero_fatura = re.search(r'Fatura Nº[:]? (\S+)', texto_completo) or re.search(r'FT \S+/(\S+)', texto_completo)
        referencia = re.search(r'Referência[:]? (\S+)', texto_completo)
        data_fatura = re.search(r'Data[:]? (\d{2}-\d{2}-\d{4}|\d{1,2}/\d{1,2}/\d{4})', texto_completo) or re.search(r'Doc. Nr (\d{4}-\d{2}-\d{2})', texto_completo)
        data_emissao = re.search(r'Emitida em[:]? (\d{2}-\d{2}-\d{4}|\d{1,2}/\d{1,2}/\d{4})', texto_completo) or data_fatura
        
        # Tentativa de encontrar qualquer informação relevante
        numero_id = numero_documento_externo or numero_fatura or referencia
        if numero_id and data_emissao:
            numero_id = numero_id.group(1)
            data_str = data_emissao.group(1)
            
            # Tentar diferentes formatos de data
            try:
                data_obj = datetime.strptime(data_str, "%d-%m-%Y")
            except ValueError:
                try:
                    data_obj = datetime.strptime(data_str, "%Y-%m-%d")
                except ValueError:
                    print(f"Formato de data não reconhecido: {data_str}")
                    return None, None
            
            # Retornar o número relevante (documento externo, fatura ou referência) e a data formatada
            return numero_id, data_obj.strftime("%d-%m-%Y")
        
    except Exception as e:
        print(f"Erro ao ler {pdf_path}: {e}")
    return None, None

# Função para mover o PDF para a pasta do mês/ano de emissão, detectando duplicatas
def mover_pdf_para_pasta_por_mes(pdf_path, numero_documento_externo, data_emissao, root):
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
        
        # Verificar se já existe um PDF com o mesmo número de documento/fatura/referência
        caminho_arquivo_destino = os.path.join(pasta_destino, f"{numero_documento_externo}.pdf")
        if os.path.exists(caminho_arquivo_destino):
            print(f"Fatura duplicada detectada: {numero_documento_externo} - movendo para pasta 'duplicatas'")
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
                numero_documento_externo, data_emissao = buscar_dados_fatura_pdf(caminho_pdf)
                if numero_documento_externo and data_emissao:
                    mover_pdf_para_pasta_por_mes(caminho_pdf, numero_documento_externo, data_emissao, root)

# Exemplo de uso
pasta_origem = './pdfs'  # Pasta onde estão os PDFs e subpastas
processar_pdfs_recursivamente_por_mes(pasta_origem)
