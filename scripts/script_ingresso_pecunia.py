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

            wait = WebDriverWait(driver, 30)
            driver.implicitly_wait(30)  # Espera até 30 segundos

           
            driver.get('https://siape.sead.pi.gov.br/adm/reenvio/folha-funcionario/folhas/folhas')

        
            
            #SELECIONA FOLHA
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="folhaFuncionario"]/div[1]/table/tbody/tr[1]/td[1]/a'))).click()
            time.sleep(4)

            #PAGAMENTO
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div[5]/div/div[2]/div/div[1]/a'))).click()
            time.sleep(4)

            #ADICIONAR
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div[1]/form/div[1]/div/a/span[2]'))).click()
            time.sleep(4)

            #MATRICULA
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div/div/button/div'))).click()
            time.sleep(2)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div/div/button/div'))).send_keys(str(row['MATRICULA']))
            time.sleep(4)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div/div/div/div[2]/ul/li[2]/a/span[2]'))).click()
            time.sleep(2)

            #GRAVAR E CONFIRMAR
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-form-action-buttons"]/button'))).click()
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-form-confirmation-save"]'))).click()


            #RUBRICA DIGITADA (VERIFICAR XPATH)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[2]/div/a[17]'))).click()
            time.sleep(2)

            # ADICIONAR 
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div[1]/form/div[1]/div/a/span[2]'))).click()
            time.sleep(2)

            #RUBRICA
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[1]/div/button/div'))).click()
            time.sleep(2)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[1]/div/div/div[2]/ul/li[2]/a/span[2]'))).send_keys(str(row['RUBRICA1']))
            time.sleep(4)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[1]/div/div/div[2]/ul/li[2]/a/span[2]'))).click()
            time.sleep(2)

            #PARÂMENTRO 
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_20_11_11_11_11_20_12_14_11_11_18_26_12_21_13_20"]'))).click()
            time.sleep(2)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_20_11_11_11_11_20_12_14_11_11_18_26_12_21_13_20"]/option[3]'))).send_keys('Valor Informado')
            time.sleep(4)

            #VALOR
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_20_11_11_11_11_20_12_14_11_11_18_26_12_21_13_21"]'))).click()
            time.sleep(2)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_20_11_11_11_11_20_12_14_11_11_18_26_12_21_13_21"]'))).send_keys(str(row['VALOR']))
            time.sleep(4)
                
            #SUBSTITUIÇÃO
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_20_11_11_11_11_20_12_14_11_11_18_26_12_21_13_38"]'))).click()
            time.sleep(2)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_20_11_11_11_11_20_12_14_11_11_18_26_12_21_13_38"]/option[3]'))).send_keys('Não')
            time.sleep(4)

            #GRAVAR E CONFIRMAR
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-form-action-buttons"]/button'))).click()
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-form-confirmation-save"]'))).click()
            
            # Esperar até que a página seja totalmente carregada 
            driver.implicitly_wait(30)  # Espera até 30 segundos   
                
 
        
            #RUBRICAS PERMANENTES
            driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[2]/div/a[16]').click()  
            time.sleep(2)     
                    
            #RUBRICA
            for i in range(1, 5):  
                rubrica_coluna = f'RUBRICA{i}'
                valor_coluna = f'VALOR{i}'

                if rubrica_coluna in row and pd.notna(row[rubrica_coluna]):
                    rubrica = row[rubrica_coluna]
                    valor = row[valor_coluna] if valor_coluna in row and pd.notna(row[valor_coluna]) else ''

                    try:
                        driver.find_element(By.XPATH, f"//td[contains(text(), '{rubrica}')]")
                        print(f"Rubrica {rubrica} já inserida. Pulando...")
                        continue
                    except:
                        print(f"Inserindo nova rubrica: {rubrica} com valor {valor}")

                #adicionar
                driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div/a/span[2]').click()
                time.sleep(2)

                #inserir nova rubrica
                driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[1]/div/button/div/div/div').click()
                driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[1]/div/div/div[1]/input').click()
                time.sleep(2)
                driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[1]/div/div/div[1]/input').send_keys(rubrica)
                time.sleep(2)
                driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[1]/div/div/div[2]/ul/li[2]/a/span[2]').click()
                time.sleep(2)

                #parametro                    
                driver.find_element(By.XPATH,'//*[@id="id_20_11_11_11_11_20_12_14_11_11_18_25_12_21_13_20"]').click()
                driver.find_element(By.XPATH,'//*[@id="id_20_11_11_11_11_20_12_14_11_11_18_25_12_21_13_20"]/option[3]').click()
                time.sleep(1)

                #Valor / Multiplicador
                driver.find_element(By.XPATH,'//*[@id="id_20_11_11_11_11_20_12_14_11_11_18_25_12_21_13_21"]').click()
                time.sleep(1)
                driver.find_element(By.XPATH,'//*[@id="id_20_11_11_11_11_20_12_14_11_11_18_25_12_21_13_21"]').send_keys(valor)

                #Quantidade
                #driver.find_element(By.XPATH,'//*[@id="id_20_11_11_11_11_20_12_14_11_11_18_25_12_21_13_22"]').click()
                #time.sleep(1)
                #driver.find_element(By.XPATH,'//*[@id="id_20_11_11_11_11_20_12_14_11_11_18_25_12_21_13_22"]').send_keys(row['QUANTIDADE'])
                
                #Substituição
                driver.find_element(By.XPATH,'//*[@id="id_20_11_11_11_11_20_12_14_11_11_18_25_12_21_13_38"]').click()
                driver.find_element(By.XPATH,'//*[@id="id_20_11_11_11_11_20_12_14_11_11_18_25_12_21_13_38"]/option[2]').click()

                #observação
                driver.find_element(By.XPATH,'//*[@id="id_20_11_11_11_11_20_12_14_11_11_18_25_12_21_13_40"]').click()
                driver.find_element(By.XPATH,'//*[@id="id_20_11_11_11_11_20_12_14_11_11_18_25_12_21_13_40"]').send_keys(row['OBSERVAÇÃO'])
                time.sleep(1)

                #GRAVAR E CONFIRMAR
                driver.find_element(By.XPATH,'//*[@id="vobys-form-action-buttons"]/button').click()
                time.sleep(4)
                driver.find_element(By.XPATH,'//*[@id="vobys-form-confirmation-save"]').click()
                time.sleep(4)

            #calcular
            #driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[2]/div/a[2]').click()  
            #time.sleep(2) 

            #importar RH
            #driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div[1]/div/div[2]/div[1]/a').click()  
            #time.sleep(4) 

            #Gerar eventos/Rubricas/Calculos
            #driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div[1]/div/div[2]/div[6]/a').click()  
            #time.sleep(4) 

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