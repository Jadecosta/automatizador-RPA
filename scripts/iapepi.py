import os
from collections import OrderedDict

def write(caminho, texto):
    """Escreve uma linha no arquivo especificado."""
    try:
        with open(caminho, 'a') as arquivo:
            arquivo.write(texto + '\n')
        return True
    except IOError as e:
        print(f"Erro ao escrever no arquivo {caminho}: {e}")
        return False

def processar_arquivo(caminho_arquivo, caminho_temp):
    """Processa um arquivo de entrada e grava os resultados em um arquivo temporário."""
    try:
        with open(caminho_arquivo, 'r') as arquivo:
            for linha in arquivo:
                linha = linha.strip()
                vinculo = linha[:2]
                matricula = linha[5:12]
                ano = linha[-10:-6]
                mes = linha[-12:-10]
                valor = linha[-6:]

                if vinculo == "CF" and valor == "000000":
                    valor = "000100"

                linha_processada = (vinculo + matricula + ano + mes + "0000" + valor).upper()
                print(linha_processada)

                if vinculo in ("CC", "CF"):
                    write(caminho_temp, linha_processada)

    except IOError as e:
        print(f"Erro ao processar o arquivo {caminho_arquivo}: {e}")

def remover_duplicatas(caminho_temp, caminho_final):
    """Remove duplicatas do arquivo temporário e grava os resultados no arquivo final."""
    try:
        with open(caminho_temp, 'r') as arquivo:
            linhas_unicas = OrderedDict.fromkeys(arquivo.readlines())

        with open(caminho_final, 'w') as arquivo_final:
            for linha in linhas_unicas:
                arquivo_final.write(linha)

        print(f"Total de linhas no arquivo final: {len(linhas_unicas)}")

    except IOError as e:
        print(f"Erro ao remover duplicatas: {e}")

def extrair_mmaa(nome_arquivo):
    """Extrai o mês e ano do nome do arquivo."""
    return nome_arquivo[-8:-4]  # Exemplo: "mmaa" no formato 'ISEDmmaa.TXT'

def processar_arquivos(caminho1, caminho2):
    """Processa dois arquivos e gera um arquivo final."""
    mmaa_arquivo1 = extrair_mmaa(os.path.basename(caminho1))
    mmaa_arquivo2 = extrair_mmaa(os.path.basename(caminho2))

    if mmaa_arquivo1 != mmaa_arquivo2:
        raise ValueError("Os arquivos selecionados não possuem o mesmo mês e ano.")

    nome_arquivo_saida = f"MOV{mmaa_arquivo1}.txt"
    caminho_final = os.path.join(os.getcwd(), nome_arquivo_saida)
    caminho_temp = os.path.join(os.getcwd(), "PREMOV_temp.txt")

    processar_arquivo(caminho1, caminho_temp)
    processar_arquivo(caminho2, caminho_temp)
    remover_duplicatas(caminho_temp, caminho_final)

    if os.path.exists(caminho_temp):
        os.remove(caminho_temp)

    print(f"Processo concluído com sucesso. Arquivo final: {nome_arquivo_saida}")
    return nome_arquivo_saida

if __name__ == "__main__":
    # Para execução direta, substitua pelos caminhos reais.
    caminho_arquivo1 = "ISEDmmaa.TXT"
    caminho_arquivo2 = "ISPDmmaa.TXT"

    try:
        processar_arquivos(caminho_arquivo1, caminho_arquivo2)
    except ValueError as e:
        print(e)
