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
        data['MATRICULA'] = data['MATRICULA'].astype(str)
        
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
            #edge_options.add_experimental_option('excludeSwitches', ['enable-automation'])
            #edge_options.add_experimental_option('useAutomationExtension', False)
            
            #edge_options.add_experimental_option("excludeSwitches", ["enable-logging"])  # Desabilita o DevTools listenin
            edge_service = Service(edge_path)
            driver = webdriver.Edge(service=edge_service, options=edge_options)

            wait = WebDriverWait(driver, 60)

            try:
                driver.get('https://siape.sead.pi.gov.br')
                driver.implicitly_wait(30)
                wait.until(EC.presence_of_element_located((By.ID, "username"))).send_keys(username)
                driver.find_element(By.ID, "password").send_keys(password)
                driver.find_element(By.ID, "password").send_keys(Keys.RETURN)    

                # Espere até que o login seja concluído com sucesso
                WebDriverWait(driver, 30).until(EC.url_changes('https://siape.sead.pi.gov.br'))
                  
            except:
                print("Erro de login ou timeout!")      
            
            try:
                #orgao = str(row['ORGAO'])
                #url = f'https://siape.sead.pi.gov.br/adm/{orgao}/pessoas'
                # Força o redirecionamento usando JavaScript
                #driver.execute_script(f"window.location.href='{url}';")
                wait.until(EC.presence_of_element_located((By.XPATH, "//div[text()='Pessoas']"))).click()
                driver.implicitly_wait(30)  # Espera até 30 segundos
                
            except Exception as e:
                print(f'Erro ao forçar redirecionamento: {e}')
            
        
            #MATRÍCULA
            driver.find_element(By.XPATH,'//*[@id="matricula"]/div/div[3]/input').click()
            time.sleep(2)
            driver.find_element(By.XPATH,'//*[@id="matricula"]/div/div[3]/input').send_keys(str(row['MATRICULA']))
            time.sleep(2)
            driver.find_element(By.XPATH,'//*[@id="pesquisaNormal"]/div/div[5]/button[2]').click()
            time.sleep(4)
            
            #SERVIDOR
            driver.find_element(By.XPATH,'//*[@id="resultadoDaBuscaDePessoas"]/div[1]/table/tbody/tr/td[1]/a').click()
            time.sleep(4)
        
            #INGRESSO
            driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div[14]/div/div[2]/div/div[1]/a').click()
            time.sleep(4)
        
            #ALTERAR
            driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/nav/div/a/span[2]').click()
            time.sleep(4)
                    
            #REABILITADO
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_10_11_18_11_15_11_11_13_23"]'))).click()
            time.sleep(2)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_10_11_18_11_15_11_11_13_23"]/option[3]'))).click() 
            time.sleep(2) 

            #REGIME                        
            driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[4]/div[2]/div[1]/div/button/div/div/div').click()
            time.sleep(1)
            driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[4]/div[2]/div[1]/div/div/div[1]/input').send_keys(row['REGIME'])
            time.sleep(1)
            driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[4]/div[2]/div[1]/div/div/div[2]/ul/li[2]/a/span[2]').click()
            time.sleep(1)
                        
            #REMUNERAÇAO                                          //*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[4]/div[2]/div[2]/div/button/div/div/div
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[4]/div[2]/div[2]/div/button/div/div/div'))).click()
            time.sleep(2)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[4]/div[2]/div[2]/div/div/div[1]/input'))).send_keys('Remunerado')
            time.sleep(4)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[4]/div[2]/div[2]/div/div/div[2]/ul/li[2]/a/span[2]'))).click()
            time.sleep(2)
            
            #DIVIÃO
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[4]/div[2]/div[3]/div/button/div/div/div'))).click()
            time.sleep(2)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[4]/div[2]/div[3]/div/div/div[1]/input'))).send_keys(row['DIVISAO'])
            time.sleep(4)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[4]/div[2]/div[3]/div/div/div[2]/ul/li[2]/a'))).click()
            time.sleep(2) 

            #CATEGORIA                     
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[4]/div[2]/div[4]/div/button/div/div/div'))).click()
            time.sleep(2)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[4]/div[2]/div[4]/div/div/div[1]/input'))).send_keys(row['CATEGORIA'])
            time.sleep(4)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[4]/div[2]/div[4]/div/div/div[2]/ul/li[2]/a/span[2]'))).click()
            time.sleep(2)
           
            #TIPO DE SERVIDOR
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[4]/div[2]/div[6]/div/button/div/div/div'))).click()
            time.sleep(2)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[4]/div[2]/div[6]/div/div/div[1]/input'))).send_keys(row['TIPO'])
            time.sleep(4)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[4]/div[2]/div[6]/div/div/div[2]/ul/li[2]/a'))).click()
            time.sleep(2)
            
            #SITUAÇÃO
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[4]/div[2]/div[5]/div/button/div/div/div'))).click()
            time.sleep(2)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[4]/div[2]/div[5]/div/div/div[1]/input'))).send_keys(row['SITUACAO'])
            time.sleep(4)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[4]/div[2]/div[5]/div/div/div[2]/ul/li[2]/a'))).click()
            time.sleep(2)
            
            #INCIDENCIA
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[4]/div[2]/div[7]/div/button/div/div/div'))).click()
            time.sleep(2)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[4]/div[2]/div[7]/div/div/div[2]/ul/li[4]/a'))).click()
            time.sleep(2)

            #LOTAÇÃO 
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[6]/div[2]/div[1]/div/button/div/div/div'))).click()
            time.sleep(2)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[6]/div[2]/div[1]/div/div/div[1]/input'))).send_keys(row['LOTACAO'])
            time.sleep(4)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[6]/div[2]/div[1]/div/div/div[2]/ul/li[2]/a'))).click()
            time.sleep(2)
            
            #CARGA HORARIA
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_10_11_18_11_15_11_11_16_15"]'))).click()
            time.sleep(2)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_10_11_18_11_15_11_11_16_15"]'))).send_keys(str(row['JORNADA DE TRABALHO']))
            time.sleep(2)

            #REMUNERAÇAO
            driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[4]/div[2]/div[2]/div/button/div/div/div').click()
            time.sleep(1)
            driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[4]/div[2]/div[2]/div/div/div[1]/input').send_keys('Remunerado')
            time.sleep(1)
            driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[4]/div[2]/div[2]/div/div/div[2]/ul/li[2]/a/span[2]').click()
            time.sleep(1)

            #DIVISÃO
            driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[4]/div[2]/div[3]/div/button/div/div/div').click()
            time.sleep(1)
            driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[4]/div[2]/div[3]/div/div/div[1]/input').send_keys(row['DIVISAO'])
            time.sleep(2)
            driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[4]/div[2]/div[3]/div/div/div[2]/ul/li[2]/a').click()
            time.sleep(1)
            
            #CATEGORIA
            driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[4]/div[2]/div[4]/div/button/div/div/div').click()
            time.sleep(1)
            driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[4]/div[2]/div[4]/div/div/div[1]/input').send_keys(row['CATEGORIA'])
            time.sleep(2)
            driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[4]/div[2]/div[4]/div/div/div[2]/ul/li[2]/a/span[2]').click()
            time.sleep(1)

            #TIPO DE SERVIDOR
            driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[4]/div[2]/div[6]/div/button/div/div/div').click()
            time.sleep(1)
            driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[4]/div[2]/div[6]/div/div/div[1]/input').send_keys(row['TIPO'])
            time.sleep(2)
            driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[4]/div[2]/div[6]/div/div/div[2]/ul/li[2]/a').click()
            time.sleep(1)

            #SITUAÇÃO
            driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[4]/div[2]/div[5]/div/button/div/div/div').click()
            time.sleep(1)
            driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[4]/div[2]/div[5]/div/div/div[1]/input').send_keys(row['SITUACAO'])
            time.sleep(2)
            driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[4]/div[2]/div[5]/div/div/div[2]/ul/li[2]/a').click()
            time.sleep(1)

            #INCIDENCIA
            driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[4]/div[2]/div[7]/div/button/div/div/div').click()
            time.sleep(1)
            driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[4]/div[2]/div[7]/div/div/div[2]/ul/li[3]/a/span[2]').click()
            time.sleep(1)

            ## #GRAVAR E CONFIRMAR
            driver.find_element(By.XPATH,'//*[@id="vobys-form-action-buttons"]/button').click()
            time.sleep(4)
            driver.find_element(By.XPATH,'//*[@id="vobys-form-confirmation-save"]').click()
            time.sleep(4)    


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