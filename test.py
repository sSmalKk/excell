import pandas as pd
import re

# Carrega o arquivo Excel "extrato1.xlsx" (supondo que esteja na mesma pasta)
df = pd.read_excel("extrato1.xlsx")

# Lista para armazenar os dados formatados
formatted_data = []

# Processa cada linha da tabela importada
for index, row in df.iterrows():
    # Acessa o valor da célula (assumindo que todas as informações estão na primeira coluna)
    line = str(row[0])  # Se a primeira coluna contém todos os dados
    
    # Usando regex para capturar os elementos
    match = re.match(r"(\d{1,2}\.\d{1,2}) (\d{1,2}\.\d{1,2}) (.+?) (\d{1,3}(?:\.\d{2})?) (\d{1,3}(?:\.\d{2})?)", line)
    if match:
        # Separando as partes da linha
        data_1 = match.group(1)
        data_2 = match.group(2)
        descricao = match.group(3).strip()
        valor = match.group(4)
        saldo = match.group(5)
        
        # Adiciona os dados formatados na lista
        formatted_data.append([data_1, data_2, descricao, valor, saldo])

# Criar um DataFrame com os dados formatados
df_formatado = pd.DataFrame(formatted_data, columns=["Data 1", "Data 2", "Descrição", "Valor (€)", "Saldo (€)"])

# Salva os dados em um arquivo Excel
df_formatado.to_excel("extrato_convertido.xlsx", index=False)

# Exibe o DataFrame formatado
print(df_formatado)
