import pdfplumber
import pandas as pd
import re

# Lista para armazenar os dados formatados
formatted_data = []

# Parte 1: Processar o PDF e extrair os dados de crédito
with pdfplumber.open("Extrato1.pdf") as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        lines = text.split("\n")
        
        # Processa cada linha e filtra as linhas que contêm valores de crédito
        for line in lines:
            # Ignora linhas como "A TRANSPORTAR" ou "TRANSPORTE"
            if "A TRANSPORTAR" in line or "TRANSPORTE" in line:
                continue  # Pula essas linhas
            
            # Ignora títulos como "SALDO INICIAL", "DATA", "DESCRITIVO", etc.
            if "SALDO" in line or "DATA" in line or "DESCRITIVO" in line:
                continue  # Pula essas linhas
            
            # Tenta capturar os elementos da linha que possuem datas, descrição, valor e saldo
            match = re.match(r"(\d{1,2}\.\d{1,2}) (\d{1,2}\.\d{1,2}) (.+?) (\d{1,3}(?:\.\d{2})?) (\d{1,3}(?:\.\d{2})?)", line)
            if match:
                # Separando as partes da linha
                data_1 = match.group(1)
                data_2 = match.group(2)
                descricao = match.group(3).strip()
                valor = match.group(4)
                saldo = match.group(5)
                
                # Adiciona os dados formatados à lista
                formatted_data.append([data_1, data_2, descricao, valor, saldo])

# Parte 2: Criar um DataFrame com os dados formatados
df_formatado = pd.DataFrame(formatted_data, columns=["Data 1", "Data 2", "Descrição", "Valor (€)", "Saldo (€)"])

# Parte 3: Salva os dados formatados em um arquivo Excel
df_formatado.to_excel("extrato_convertido.xlsx", index=False)

# Exibe uma confirmação
print("Dados de crédito extraídos, formatados e salvos em 'extrato_convertido.xlsx'")
