import os
import sys
import time
import pandas as pd
import datetime
import concurrent.futures
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options
from tkinter import filedialog
from configs.config import USERNAME, PASSWORD

# Redireciona a saída de erro padrão para /dev/null para suprimir mensagens do DevTools
sys.stderr = open(os.devnull, 'w')

# Abre o arquivo para escrita
error_file = open('C:/Users/ADS_DFPG/Desktop/Automacao-Python/Arquivos/promocaoCONFERENCIA.txt', 'w')

# Usar o diálogo de seleção de arquivo do tkinter para obter o caminho do arquivo original
file_path = filedialog.askopenfilename(title="Selecione o arquivo Excel", filetypes=[("Excel files", "*.xlsx")])

# Verificar se o usuário selecionou um arquivo
if not file_path:
    print("Nenhum arquivo selecionado. Encerrando o programa.")
    exit()

# Leitura do arquivo Excel
try:
    data = pd.read_excel(file_path)
except Exception as e:
    print(f"Erro ao ler o arquivo Excel: {e}")
    error_file.write(f"Erro ao ler o arquivo Excel: {e}\n")
    error_file.close()
    exit()

# Adiciona as novas colunas ao DataFrame
data['REFERENCIA'] = ''
data['DATA'] = ''

print("CARREGANDO..")

def processar_linha(row):
    try:
        linha_excel = row.name + 2

        # Inicializa o driver do Edge
        edge_path = 'C:/Users/ADS_DFPG/Desktop/Automacao-Python/msedgedriver.exe'
        edge_options = webdriver.EdgeOptions()
        edge_options.use_chromium = True
        edge_options.add_argument('--headless')
        edge_options.add_argument("--log-level=3")  # Adiciona esta linha para suprimir os logs
        edge_service = Service(edge_path)
        driver = webdriver.Edge(service=edge_service, options=edge_options)

        wait = WebDriverWait(driver, 30)

        # Navegar até a página de login
        driver.get('https://siape.sead.pi.gov.br')
        driver.implicitly_wait(30)
        input_usuario = wait.until(EC.presence_of_element_located((By.ID, 'username')))
        input_senha = driver.find_element(By.ID, 'password')

        # Preencher os campos de usuário e senha
        input_usuario.send_keys(USERNAME)
        input_senha.send_keys(PASSWORD)
        input_senha.send_keys(Keys.RETURN)

        try:
            orgao = str(row['ORGAO'])
            driver.get(f'https://siape.sead.pi.gov.br/adm/{orgao}/pessoas')
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="matricula"]/div/div[3]/input')))
        except:
            print('Erro ao carregar página do órgão!')

        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="matricula"]/div/div[3]/input'))).click()
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="matricula"]/div/div[3]/input'))).send_keys(str(row['MATRICULA']))
        time.sleep(2)
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="pesquisaNormal"]/div/div[6]/button'))).click()
        time.sleep(4)
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="resultadoDaBuscaDePessoas"]/div[1]/table/tbody/tr/td[1]/a'))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="vobys-content"]/div/div/div[14]/div/div[2]/div/div[4]/a'))).click()

        # Captura dos dados de referência e data
        referencia = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="historicoDoDesenvolvimentoNaCarreira"]/div[1]/table/tbody/tr[1]/td[2]'))).text
        data_promo = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="historicoDoDesenvolvimentoNaCarreira"]/div[1]/table/tbody/tr[1]/td[4]'))).text

        # Atualiza as colunas do DataFrame
        data.at[row.name, 'REFERENCIA'] = referencia
        data.at[row.name, 'DATA'] = data_promo

        success_time = datetime.datetime.now().strftime("%H:%M")
        success_message = f"Linha Excel: {linha_excel} {row['MATRICULA']} {referencia} {data_promo} \n"
        print(success_message)
        error_file.write(success_message)
        error_file.flush()
    except Exception as e:
        success_time = datetime.datetime.now().strftime("%H:%M")
        error_message = f"Linha Excel: {linha_excel} {row['MATRICULA']} Erro às {success_time}: {e}\n"
        error_file.write(error_message)
        error_file.flush()
        print(error_message)
    finally:
        driver.quit()

# Inicializa a lista de resultados
resultados = []

# Cria um executor de threads com no máximo 1 worker (telas abertas)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    for index, row in data.iterrows():
        resultado = executor.submit(processar_linha, row)
        resultados.append(resultado)

    for resultado in concurrent.futures.as_completed(resultados):
        resultado.result()

# Salva o DataFrame atualizado no arquivo original
data.to_excel(file_path, index=False)

# Fecha o arquivo de erros
error_file.close()
