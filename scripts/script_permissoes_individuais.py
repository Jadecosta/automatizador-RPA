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
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options

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
    except Exception as e:
        print(f"Erro ao ler o arquivo Excel: {e}")
        error_file.write(f"Erro ao ler o arquivo Excel: {e}\n")
        error_file.close()
        return

    total_linhas = len(data)

    
    def processar_linha(row):
        try:
            linha_excel = row.name + 2
            login = row['LOGIN']

            edge_path = 'C:/Github/App_Program/msedgedriver.exe'
            edge_options = webdriver.EdgeOptions()
            edge_options.use_chromium = True
            edge_options.add_argument("--log-level=3")  # Adiciona esta linha para suprimir os logs
            #edge_options.add_argument('--headless')  # Comentar ou remover esta linha para desativar o modo headless
            edge_options.add_argument('--disable-gpu')  # Desabilita a aceleração de GPU

            # Configurações para ignorar certificados inseguros
            edge_options.add_argument('--ignore-certificate-errors')
            edge_options.add_argument('--ignore-ssl-errors')
            edge_options.add_argument('--disable-web-security')
            
            #edge_options.add_experimental_option("excludeSwitches", ["enable-logging"])  # Desabilita o DevTools listenin
            edge_service = Service(edge_path)
            driver = webdriver.Edge(service=edge_service, options=edge_options)
            wait = WebDriverWait(driver, 60)
            
            driver.get('https://siape.sead.pi.gov.br')
            
            wait.until(EC.presence_of_element_located((By.ID, "username"))).send_keys(username)
            driver.find_element(By.ID, "password").send_keys(password)
            driver.find_element(By.ID, "password").send_keys(Keys.RETURN)
            
            orgao = str(row['ORGAO'])
            driver.get(f'https://siape.sead.pi.gov.br/adm/{orgao}/seguranca-de-acesso')
            
            #USUÁRIOS
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="vobys-content"]/div/div/div[2]/div/div[2]/div/div[1]/a'))).click
            time.sleep(1)

            #LOGIN
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div[1]/form/div[2]/div/div[1]/input[2]'))).click
            time.sleep(1)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div[1]/form/div[2]/div/div[1]/input[2]'))).send_keys(str(row['LOGIN']))
            
            #BUSCAR
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div[1]/form/div[2]/div/div[4]/button'))).click
            time.sleep(4)

            #USUÁRIO
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="selecionarUsuario"]/div[1]/table/tbody/tr/td[1]/a'))).click
            time.sleep(1)

            #PERMISSÕES
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="vobys-content"]/div/div/div/div[2]/div/a[3]'))).click
            time.sleep(1)

            #ADICIONAR
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div[1]/form/div[1]/div/a/span[2]'))).click
            time.sleep(1)

            #MIGALHA
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[1]/div/button/div/div/div'))).click
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[1]/div/button/div'))).send_keys(str(row['MIGALHA']))
            time.sleep(4)

            #TIPO
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="id_2_11_11_11_11_16_17_12_13_11_13"]'))).click
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="id_2_11_11_11_11_16_17_12_13_11_13"]/option[2]'))).click
            time.sleep(4)

            #VISUALIZAR
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="id_2_11_11_11_11_16_17_12_13_11_14"]'))).click
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="id_2_11_11_11_11_16_17_12_13_11_14"]/option[2]'))).click
            time.sleep(4)

            #ALTERAR
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="id_2_11_11_11_11_16_17_12_13_11_15"]'))).click
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="id_2_11_11_11_11_16_17_12_13_11_15"]/option[3]'))).click
            time.sleep(4)

            #ADICIONAR
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="id_2_11_11_11_11_16_17_12_13_11_16"]'))).click
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="id_2_11_11_11_11_16_17_12_13_11_16"]/option[3]'))).click
            time.sleep(4)

            #EXCLUIR
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="id_2_11_11_11_11_16_17_12_13_11_17"]"]'))).click
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="id_2_11_11_11_11_16_17_12_13_11_17"]/option[3]'))).click
            time.sleep(4)

            #VIUALIZAR NA GRID
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="id_2_11_11_11_11_16_17_12_13_11_18"]"]'))).click
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="id_2_11_11_11_11_16_17_12_13_11_18"]/option[2]'))).click
            time.sleep(4)

            #PESQUISAR
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="id_2_11_11_11_11_16_17_12_13_11_19"]"]'))).click
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="id_2_11_11_11_11_16_17_12_13_11_19"]/option[2]'))).click
            time.sleep(4)

            #GRAVAR E CONFIRMAR
            wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="vobys-form-action-buttons"]/button'))).click()
            wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="vobys-form-confirmation-save"]'))).click()
            time.sleep(4)

        except Exception as e:
            error_msg = f"Erro na linha {linha_excel} para o login {login}: {e}"
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
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
    #with concurrent.futures.ThreadPoolExecutor() as executor:
        for index, row in data.iterrows():
            resultado = executor.submit(processar_linha, row)
            resultados.append(resultado)

        # Aguarda a conclusão de todos os resultados
        for resultado in concurrent.futures.as_completed(resultados):
            resultado.result()

    error_file.close()

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Uso: script_permissoes_individuais.py <caminho do arquivo Excel> <username> <password> <task_id>")
        sys.exit(1)

    file_path = sys.argv[1]
    username = sys.argv[2]
    password = sys.argv[3]
    task_id = sys.argv[4]
    main(file_path, username, password, task_id)

       



