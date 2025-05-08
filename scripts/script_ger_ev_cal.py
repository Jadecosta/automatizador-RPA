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
        data['RUBRICA'] = data['RUBRICA'].astype(str)
        data['VALOR'] = data['VALOR'].astype(str)
    except Exception as e:
        print(f"Erro ao ler o arquivo Excel: {e}")
        error_file.write(f"Erro ao ler o arquivo Excel: {e}\n")
        error_file.close()
        return

    total_linhas = len(data)

    

    def processar_linha(row):
        try:
            linha_excel = row.name + 2
            # Inicializa o driver do Edge
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
            time.sleep(2)
            wait.until(EC.presence_of_element_located((By.ID, "username"))).send_keys(username)
            driver.find_element(By.ID, "password").send_keys(password)
            driver.find_element(By.ID, "password").send_keys(Keys.RETURN)      

            orgao = str(row['ORGAO'])
            driver.get(f'https://siape.sead.pi.gov.br/adm/{orgao}/folha-funcionario/folhas/folhas')
            driver.implicitly_wait(30)  # Espera até 30 segundos     

            driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[2]/div/div[1]/input[2]').send_keys(str(row['FOLHA']))
            time.sleep(4)

            driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[2]/div/div[10]/button').click()
            time.sleep(4)

            driver.find_element(By.XPATH,'//*[@id="folhaFuncionario"]/div[1]/table/tbody/tr/td[1]/a').click()
            time.sleep(4)

            #PAGAMENTO
            driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div[5]/div/div[2]/div/div[1]/a').click()
            time.sleep(4)

            #MATRICULA
            driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div[1]/form/div[2]/div/div[1]/input[2]').click()
            time.sleep(4)
            driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div[1]/form/div[2]/div/div[1]/input[2]').send_keys(str(row['MATRICULA']))
            time.sleep(4)
            driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div[1]/form/div[2]/div/div[12]/button').click()
            time.sleep(4)

            #CALCULAR
            driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[2]/div/a[2]').click()
            time.sleep(4)

            #IMPORTAR RH
            driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div[1]/div/div[2]/div[1]/a').click()
            time.sleep(4)

            #IMPORTAR RH
            driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div[1]/div/div[2]/div[1]/a').click()
            time.sleep(4)

            #GERAR EVENTOS/RUBRICA/CALCULO
            driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div[1]/div/div[2]/div[6]/a').click()
            time.sleep(4)
       
            wait = WebDriverWait(driver, 30)

        except Exception as e:
            error_msg = f"Erro na linha {linha_excel}: {e}"
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