import os
import shutil
from PyPDF2 import PdfReader

# Função para buscar uma palavra em um PDF após remover os espaços
def buscar_palavra_pdf_sem_espacos(pdf_path, palavra):
    try:
        reader = PdfReader(pdf_path)
        texto_completo = ""
        
        # Extrair o texto de todas as páginas e remover os espaços
        for page in reader.pages:
            texto = page.extract_text()
            if texto:
                texto_completo += texto.replace(" ", "").replace("\n", "")  # Remove espaços e quebras de linha
        
        # Busca a palavra no texto sem espaços
        if palavra.lower() in texto_completo.lower():  # Busca case-insensitive
            return True
    except Exception as e:
        print(f"Erro ao ler {pdf_path}: {e}")
    return False

# Função para mover o PDF para a pasta com a palavra, mantendo a estrutura de diretórios
def mover_pdf_para_pasta(pdf_path, palavra, root):
    # Obter a estrutura de pastas relativa ao diretório raiz
    caminho_relativo = os.path.relpath(root, start=pasta_origem)
    
    # Criar a nova pasta de destino, mantendo a estrutura de pastas
    pasta_destino = os.path.join(pasta_origem, palavra, caminho_relativo)
    
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
                for palavra in lista_palavras:
                    if buscar_palavra_pdf_sem_espacos(caminho_pdf, palavra):
                        mover_pdf_para_pasta(caminho_pdf, palavra, root)
                        break  # Se encontrar a palavra, mover e parar a busca nesse PDF

# Exemplo de uso
pasta_origem = './pdfs'  # Pasta onde estão os PDFs e subpastas
lista_palavras = ['Quintanilha', 'LOGICO']  # Lista de palavras a serem buscadas

processar_pdfs_recursivamente(pasta_origem, lista_palavras)
