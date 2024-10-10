import os
import shutil
from PyPDF2 import PdfReader

# Função para buscar uma palavra em um PDF após remover os espaços
def buscar_palavra_pdf_sem_espacos(pdf_path, lista_palavras):
    try:
        reader = PdfReader(pdf_path)
        texto_completo = ""
        
        # Extrair o texto de todas as páginas e remover os espaços
        for page in reader.pages:
            texto = page.extract_text()
            if texto:
                texto_completo += texto.replace(" ", "").replace("\n", "")  # Remove espaços e quebras de linha
        
        # Verifica se alguma palavra da lista está no texto (case-insensitive)
        for palavra in lista_palavras:
            if palavra.lower() in texto_completo.lower():
                return palavra  # Retorna a palavra encontrada
        
    except Exception as e:
        print(f"Erro ao ler {pdf_path}: {e}")
    
    return None  # Nenhuma palavra encontrada

# Função para mover o PDF para a pasta com a palavra, mantendo a estrutura de diretórios
def mover_pdf_para_pasta(pdf_path, destino, root):
    # Obter a estrutura de pastas relativa ao diretório raiz
    caminho_relativo = os.path.relpath(root, start=pasta_origem)
    
    # Criar a nova pasta de destino, mantendo a estrutura de pastas
    pasta_destino = os.path.join(pasta_origem, destino, caminho_relativo)
    
    # Se a pasta não existir, criá-la
    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)
    
    # Mover o arquivo para a nova pasta, mantendo o nome original do arquivo
    shutil.move(pdf_path, os.path.join(pasta_destino, os.path.basename(pdf_path)))
    print(f"Movido {pdf_path} para {pasta_destino}")

# Função para processar todos os PDFs em uma pasta (e suas subpastas)
def processar_pdfs_recursivamente(pasta_origem, lista_palavras):
    for root, dirs, files in os.walk(pasta_origem):  # Caminha por pastas e subpastas
        for arquivo in files:
            if arquivo.endswith(".pdf"):
                caminho_pdf = os.path.join(root, arquivo)
                
                # Buscar palavras no PDF
                palavra_encontrada = buscar_palavra_pdf_sem_espacos(caminho_pdf, lista_palavras)
                
                # Se uma palavra foi encontrada, movê-lo para a pasta correspondente
                if palavra_encontrada:
                    mover_pdf_para_pasta(caminho_pdf, palavra_encontrada, root)
                else:
                    # Caso contrário, mover para a pasta 'nao encontrada'
                    mover_pdf_para_pasta(caminho_pdf, 'nao encontrada', root)

# Exemplo de uso
pasta_origem = './pdfs'  # Pasta onde estão os PDFs e subpastas
lista_palavras = ['518239390', '515352179']  # Lista de palavras a serem buscadas

processar_pdfs_recursivamente(pasta_origem, lista_palavras)
