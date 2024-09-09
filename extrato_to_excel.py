import pdfplumber
import pandas as pd

# Abra o arquivo PDF
with pdfplumber.open("Extrato1.pdf") as pdf:
    all_data = []
    
    # Itera por todas as páginas do PDF
    for page in pdf.pages:
        text = page.extract_text()
        lines = text.split("\n")
        
        # Processa cada linha para que as palavras fiquem em uma célula
        for line in lines:
            # Juntar todas as palavras da linha em uma única string
            data = ' '.join(line.split())  # Junta as palavras da linha
            all_data.append([data])  # Adiciona a linha como uma lista com um único elemento

# Converte para DataFrame, onde cada linha está em uma célula separada
df = pd.DataFrame(all_data, columns=["Conteúdo"])

# Salva como arquivo Excel
df.to_excel("extrato_convertido.xlsx", index=False)

print("Conversão concluída e salva em 'extrato_convertido.xlsx'")
