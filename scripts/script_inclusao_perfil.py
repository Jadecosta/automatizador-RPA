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
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
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
        data['MATRICULA'] = data['MATRICULA'].astype(str)
    except Exception as e:
        print(f"Erro ao ler o arquivo Excel: {e}")
        error_file.write(f"Erro ao ler o arquivo Excel: {e}\n")
        error_file.close()
        return

    total_linhas = len(data)

    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    #chrome_options.add_argument("--headless")  # Descomente esta linha para execução sem interface gráfica

    def processar_linha(row):
    
        try:
            linha_excel = row.name + 2
            matricula = row['MATRICULA']
        
            # Inicializa o driver do Edge
            chrome_options = Options()
            chrome_options.add_argument("--start-maximized")
            #chrome_options.add_argument("--headless")  # Descomente esta linha para execução sem interface gráfica
            driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
            wait = WebDriverWait(driver, 60)


            # Navegar até a página de login
            driver.get('https://siape.sead.pi.gov.br')

            wait.until(EC.presence_of_element_located((By.ID, "username"))).send_keys(username)
            driver.find_element(By.ID, "password").send_keys(password)
            driver.find_element(By.ID, "password").send_keys(Keys.RETURN)


            #orgao = str(row['ORGAO'])
            driver.get('https://siape.sead.pi.gov.br/adm/sesapi/pessoas')

            # Esperar até que a página seja totalmente carregada 
            driver.implicitly_wait(30)  # Espera até 30 segundos
        
            # Matricula 
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="matricula"]/div/div[3]/input'))).click()
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="matricula"]/div/div[3]/input'))).send_keys(str(row['MATRICULA']))
            time.sleep(1)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="pesquisaNormal"]/div/div[6]/button'))).click()
            time.sleep(4)
            #SERVIDOR
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="resultadoDaBuscaDePessoas"]/div[1]/table/tbody/tr/td[1]/a'))).click()      
            #PERFIL
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div[14]/div/div[2]/div/div[3]/a'))).click()
            time.sleep(2)
            ##ADICIONAR                                            
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div[3]/form/div[1]/div/a/span[2]'))).click()
            ###MOVIMENTAÇÃO
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[1]/div/button/div/div/div'))).click()
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[1]/div/div/div[1]/input'))).click()
            time.sleep(1)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[1]/div/div/div[1]/input'))).send_keys(str(row['MOVIMENTACAO']))
            time.sleep(1)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[1]/div/div/div[2]/ul/li[2]/a/span[2]'))).click()
            time.sleep(1)
            ###DIVISAO
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[2]/div/button/div/div/div'))).click()
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[2]/div/div/div[1]/input'))).click()
            time.sleep(1)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[2]/div/div/div[1]/input'))).send_keys(Keys.SPACE)
            time.sleep(1)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[2]/div/div/div[2]/ul/li[2]/a/span[2]'))).click()
            time.sleep(1)
            ###CATEGORIA DO TRABALHADOR
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[3]/div/button/div/div/div'))).click()
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[3]/div/div/div[1]/input'))).click()
            time.sleep(1)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[3]/div/div/div[1]/input'))).send_keys(str(row['CATEGORIA_DO_TRABALHADOR']))
            time.sleep(1)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[3]/div/div/div[2]/ul/li[2]/a/span[2]'))).click()
            time.sleep(1)
            ###SITUAÇÃO
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[4]/div/button/div/div/div'))).click()
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[4]/div/div/div[1]/input'))).click()
            time.sleep(1)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[4]/div/div/div[1]/input'))).send_keys(str(row['SITUACAO']))
            time.sleep(1)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[4]/div/div/div[2]/ul/li[2]/a/span[2]'))).click()
            time.sleep(1)
            ###TIPO DE SERVIDOR
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[5]/div/button/div/div/div'))).click()
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[5]/div/div/div[1]/input'))).click()
            time.sleep(1)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[5]/div/div/div[1]/input'))).send_keys(str(row['TIPO']))
            time.sleep(1)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[5]/div/div/div[2]/ul/li[2]/a/span[2]'))).click()
            time.sleep(1)
            ###REMUNERAÇÃO
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[6]/div/button/div/div/div'))).click()
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[6]/div/div/div[1]/input'))).click()
            time.sleep(1)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[6]/div/div/div[1]/input'))).send_keys(str(row['REMUNERACAO']))
            time.sleep(1)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[6]/div/div/div[2]/ul/li[2]/a/span[2]'))).click()
            time.sleep(1)
            ###TIPO DE INCIDENCIA
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[7]/div/button/div/div/div'))).click()
            time.sleep(1)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[7]/div/div/div[1]/input'))).send_keys(str(row['TIPO_DE_INCIDENCIA']))
            time.sleep(1)
            dropdown_elements = driver.find_elements(By.XPATH, '//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[7]/div/div/div[2]/ul/li')
            for element in dropdown_elements:
                if element.text == str(row['TIPO DE INCIDENCIA']):
                    element.click()
                    break
            '''
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[7]/div/button/div/div/div').click()
            time.sleep(1)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[7]/div/div/div[1]/input').click()
            time.sleep(1)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[7]/div/div/div[1]/input').send_keys(str(row['TIPO DE INCIDENCIA']))
            time.sleep(1)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[7]/div/div/div[2]/ul/li[2]/a/span[2]').click()
            time.sleep(1)
            '''
            
            ###OBSERVAÇÃO
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_10_11_18_11_15_11_13_12_17_12_21"]'))).click()
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_10_11_18_11_15_11_13_12_17_12_21"]'))).send_keys(str(row['OBSERVAÇÃO']))

        
            ###DATA
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_10_11_18_11_15_11_13_12_17_12_16"]'))).click()
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_10_11_18_11_15_11_13_12_17_12_16"]'))).send_keys(str(row['DATA']))

            ###GRAVAR E CONFIRMAR
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-form-action-buttons"]/button'))).click()
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-form-confirmation-save"]'))).click()
            time.sleep(2)    
        

        except Exception as e:
            error_msg = f"Erro na linha {linha_excel} para a Matrícula {matricula}: {e}"
            print(error_msg)
            error_file.write(error_msg + '\n')
        finally:
            driver.quit()
        
        progresso = (row.name + 1) / total_linhas * 100
        with open(progress_file_path, 'w') as progress_file:
            json.dump({'task_id': task_id, 'progress': progresso}, progress_file)

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