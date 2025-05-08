import sys
import pandas as pd
import time
import json
import os
import concurrent.futures
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

def main(file_path, username, password, task_id, log_file_name):
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_file_path = os.path.join(log_dir, log_file_name)

    # Arquivo para registrar erros
    error_file = open(log_file_path, 'w')

    progress_file_path = f'progress_{task_id}.json'


    # Leitura do arquivo Excel
    try:
        data = pd.read_excel(file_path)
        data['CODIGO'] = data['CODIGO'].astype(str)
    except Exception as e:
        print(f"Erro ao ler o arquivo Excel: {e}")
        error_file.write(f"Erro ao ler o arquivo Excel: {e}\n")
        error_file.close()
        return

    total_linhas = len(data)

    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    # chrome_options.add_argument("--headless")  # Descomente esta linha para execução sem interface gráfica

    def processar_linha(row):
        try:
            linha_excel = row.name + 2
            matricula = row['MATRICULA']

            driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
            wait = WebDriverWait(driver, 60)
            
            driver.get('https://siape.sead.pi.gov.br')
            
            wait.until(EC.presence_of_element_located((By.ID, "username"))).send_keys(username)
            driver.find_element(By.ID, "password").send_keys(password)
            driver.find_element(By.ID, "password").send_keys(Keys.RETURN)
            
            orgao_text = str(row['ORGAO'])
            driver.get(f'https://siape.sead.pi.gov.br/adm/{orgao_text}/pessoas')

            wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="matricula"]/div/div[3]/input'))).send_keys(matricula)
            driver.find_element(By.XPATH, '//*[@id="pesquisaNormal"]/div/div[6]/button').click()
            time.sleep(1)

            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="resultadoDaBuscaDePessoas"]/div[1]/table/tbody/tr[1]/td[1]/a'))).click()       
          
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="vobys-content"]/div/div/div[18]/div/div[2]/div/div[1]/a'))).click()
            
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div[2]/form/div[1]/div/a/span[2]'))).click()
            
            data_input = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="id_10_11_18_11_15_15_11_12_14_11_11"]')))
            data_input.send_keys(str(row['DATA']))
            time.sleep(1)
            driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[3]/div/button/div').click()
            time.sleep(1)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[3]/div/div/div[1]/input'))).send_keys(str(row['CODIGO']) + Keys.SPACE)
            time.sleep(1)
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[3]/div/div/div[2]/ul/li[2]/a/span[2]'))).click()
            time.sleep(1)

            # Gravar e confirmar - uncomment if needed
            wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="vobys-form-action-buttons"]/button'))).click()
            wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="vobys-form-confirmation-save"]'))).click()

        except Exception as e:
            error_msg = f"Erro na linha {linha_excel} para a Matrícula {matricula}: {e}"
            print(error_msg)
            error_file.write(error_msg + '\n')

        finally:
            driver.quit()

        # Atualizar progresso
        progresso = (row.name + 1) / total_linhas * 100
        with open(progress_file_path, 'w') as progress_file:
            json.dump({'task_id': task_id, 'progress': progresso}, progress_file)

    # Processa cada linha do Excel
    #data.apply(processar_linha, axis=5)
    # Inicializa a lista de resultados
    resultados = []

    # Cria um executor de threads com no máximo 5 workers (telas abertas)
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    #with concurrent.futures.ThreadPoolExecutor() as executor:
        for index, row in data.iterrows():
            resultado = executor.submit(processar_linha, row)
            resultados.append(resultado)

        # Aguarda a conclusão de todos os resultados
        for resultado in concurrent.futures.as_completed(resultados):
            resultado.result()

    error_file.close()

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Uso: script_ingresso_pecunia.py <caminho do arquivo Excel> <username> <password> <task_id>")
        sys.exit(1)

    file_path = sys.argv[1]
    username = sys.argv[2]
    password = sys.argv[3]
    task_id = sys.argv[4]
    log_file_name = sys.argv[5]
    main(file_path, username, password, task_id, log_file_name)