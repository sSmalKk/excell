import subprocess
import sys
from collections import defaultdict

# Função para instalar o módulo astroquery se não estiver instalado
def install_package(package):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    except Exception as e:
        print(f"Erro ao instalar o pacote {package}: {e}")
        sys.exit(1)

# Verifica se o astroquery está instalado e o instala se necessário
try:
    from astroquery.nist import Nist
    import astropy.units as u
except ModuleNotFoundError as e:
    print(f"Erro: {e}. Tentando instalar o módulo 'astroquery'...")
    install_package("astroquery")
    from astroquery.nist import Nist
    import astropy.units as u

# Função para converter comprimento de onda (nm) para RGB
def wavelength_to_rgb(wavelength):
    gamma = 0.8
    intensity_max = 255

    if 380 <= wavelength <= 440:
        r = -(wavelength - 440) / (440 - 380)
        g = 0.0
        b = 1.0
    elif 440 < wavelength <= 490:
        r = 0.0
        g = (wavelength - 440) / (490 - 440)
        b = 1.0
    elif 490 < wavelength <= 510:
        r = 0.0
        g = 1.0
        b = -(wavelength - 510) / (510 - 490)
    elif 510 < wavelength <= 580:
        r = (wavelength - 510) / (580 - 510)
        g = 1.0
        b = 0.0
    elif 580 < wavelength <= 645:
        r = 1.0
        g = -(wavelength - 645) / (645 - 580)
        b = 0.0
    elif 645 < wavelength <= 700:
        r = 1.0
        g = 0.0
        b = 0.0
    else:
        r = g = b = 0.0

    # Intensity correction
    if 380 <= wavelength <= 420:
        factor = 0.3 + 0.7 * (wavelength - 380) / (420 - 380)
    elif 420 < wavelength <= 645:
        factor = 1.0
    elif 645 < wavelength <= 700:
        factor = 0.3 + 0.7 * (700 - wavelength) / (700 - 645)
    else:
        factor = 0.0

    r = round(intensity_max * ((r * factor) ** gamma))
    g = round(intensity_max * ((g * factor) ** gamma))
    b = round(intensity_max * ((b * factor) ** gamma))

    return r, g, b

# Função para puxar os dados do NIST e organizá-los
def fetch_nist_data():
    try:
        print("Iniciando consulta ao NIST...")
        
        # Definindo o intervalo de comprimento de onda (4000 Å a 7000 Å)
        lower_wavelength = 4000 * u.AA
        upper_wavelength = 7000 * u.AA
        
        # Consultando o NIST para linhas espectrais do Hidrogênio (H I)
        result_table = Nist.query(lower_wavelength, upper_wavelength, linename="H I")
        
        # Organizando os dados
        spectral_lines = defaultdict(list)
        for row in result_table:
            wavelength_nm = row['Ritz']  # Comprimento de onda em Ångströms
            if wavelength_nm:  # Filtrar valores válidos
                wavelength_nm /= 10  # Converter de Ångströms para nanômetros
                if 380 <= wavelength_nm <= 700:  # Apenas espectro visível
                    rgb = wavelength_to_rgb(wavelength_nm)
                    spectral_lines[(wavelength_nm, rgb)].append({
                        "Transition": row['Transition'],
                        "Temperature": "Ambiente" if 4000 <= wavelength_nm <= 7000 else "Alta",
                    })
        
        # Exibindo os dados organizados
        print("\nLinhas Espectrais Organizadass:\n")
        print(f"{'Linha Espectral':<15}{'Comprimento de Onda (nm)':<25}{'RGB':<20}{'Temperatura':<15}")
        print("=" * 80)
        for (wavelength_nm, rgb), details in spectral_lines.items():
            for detail in details:
                print(f"Hydrogen Line    {wavelength_nm:<25.2f}{str(rgb):<20}{detail['Temperature']:<15}")
    
    except Exception as e:
        print(f"Erro durante a consulta ao NIST: {e}")

# Executando a função de fetch
fetch_nist_data()
