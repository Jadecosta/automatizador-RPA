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
            matricula = row['MATRICULA'] 
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
            driver.implicitly_wait(60)  # Espera até 30 segundos  

            driver.get('https://siape.sead.pi.gov.br') 
            wait.until(EC.presence_of_element_located((By.ID, "username"))).send_keys(username)
            driver.find_element(By.ID, "password").send_keys(password)
            driver.find_element(By.ID, "password").send_keys(Keys.RETURN)
            driver.implicitly_wait(60)  # Espera até 30 segundos  

            orgao_text = str(row['ORGAO'])
            driver.get(f'https://siape.sead.pi.gov.br/adm/{orgao_text}/pessoas')
            driver.implicitly_wait(60)  # Espera até 30 segundos  

            wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="matricula"]/div/div[3]/input'))).send_keys(matricula)
            time.sleep(1)
            driver.find_element(By.XPATH, '//*[@id="pesquisaNormal"]/div/div[5]/button[2]').click()
            time.sleep(2)

            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="resultadoDaBuscaDePessoas"]/div[1]/table/tbody/tr[1]/td[1]/a'))).click()       
            
            #aposentadoria 
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="vobys-content"]/div/div/div[27]/div/div[2]/div/div[1]/a'))).click()
            time.sleep(1)        

            try:
                  elemento = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="informacoesParaPrevidencia"]/div[1]/table/tbody/tr/td[1]')))
                     # Se o elemento existir, pule para a próxima interação
                  print("Elemento encontrado. Pulando para a próxima interação.")

            except:  

                
                wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div[1]/form/div[1]/div/a/span[2]'))).click()

                #plano
                wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[1]/div/button/div/div/div'))).click()
                time.sleep(1)
                wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[1]/div/div/div[1]/input'))).send_keys(str(row['PLANO']) + Keys.SPACE)
                time.sleep(1)
                wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[1]/div/div/div[2]/ul/li[2]/a/span[2]'))).click()
                time.sleep(1)

                #empresa
                wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[2]/div/button/div'))).click()
                time.sleep(1)
                wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[2]/div/div/div[1]/input'))).send_keys(str(row['EMPRESA']) + Keys.SPACE)
                time.sleep(1)
                wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[2]/div/div/div[2]/ul/li[2]/a/span[2]'))).click()
                time.sleep(1)
                
                #ORGAO EXTERNO
                wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[3]/div/button/div'))).click()
                time.sleep(1)
                wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[3]/div/div/div[1]/input'))).send_keys(str(row['ORGAO_EXTERNO']) + Keys.SPACE)
                time.sleep(1)
                wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[3]/div/div/div[2]/ul/li[2]/a/span[2]'))).click()
                time.sleep(1)

                #Empresa Pagamento
                wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[4]/div/button/div'))).click()
                time.sleep(1)
                wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[4]/div/div/div[1]/input'))).send_keys(str('FUNPREV') + Keys.SPACE)
                time.sleep(1)
                wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[4]/div/div/div[2]/ul/li[2]/a/span[2]'))).click()
                time.sleep(1)
                
                # Categoria Funcional
                wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[5]/div/button/div/div/div'))).click()
                time.sleep(1)
                wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[5]/div/div/div[1]/input'))).send_keys(str(row['CATEGORIA FUNCIONAL']) + Keys.SPACE)
                time.sleep(1)
                wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[5]/div/div/div[2]/ul/li[2]/a/span[2]'))).click()
                time.sleep(1)

                # Referência
                wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[6]/div/button/div/div/div'))).click()
                time.sleep(1)
                wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[6]/div/div/div[1]/input'))).send_keys(str(row['REFERENCIA']) + Keys.SPACE)
                time.sleep(1)
                wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[6]/div/div/div[2]/ul/li[2]/a/span[2]'))).click()
                time.sleep(1)
            
                #Observação
                observacao = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="id_10_11_18_11_15_27_11_12_18_11_17"]')))
                observacao.send_keys(str(row['OBSERVAÇÃO']))
                time.sleep(1)
                
                # Gravar e confirmar - uncomment if needed
                wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="vobys-form-action-buttons"]/button'))).click()
                time.sleep(2)
                wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="vobys-form-confirmation-save"]'))).click()
                time.sleep(4)

            #voltar rh
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="vobys-content"]/div/ol/li[2]/a'))).click()

            #aposentadoria propria
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="vobys-content"]/div/div/div[26]/div/div[2]/div/div[1]/a'))).click()
            time.sleep(1)
           
            try:
                  elemento = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="aposentadoriaPropria"]/div[1]/table/tbody/tr/td[1]')))
                     # Se o elemento existir, pule para a próxima interação
                  print("Elemento encontrado. Pulando para a próxima interação.")
                

            except:  
                wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div[1]/form/div[1]/div/a/span[2]'))).click()

                #DataRequerimento
                requerimento = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="id_10_11_18_11_15_22_40_12_16_11_16"]')))
                requerimento.send_keys(str(row['DATA REQUERIMENTO E APOSENTADORIA']))
                time.sleep(1)
                
                #DataAposentadoria
                aposent_data = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="id_10_11_18_11_15_22_40_12_16_11_11"]')))
                aposent_data.send_keys(str(row['DATA REQUERIMENTO E APOSENTADORIA']))
                time.sleep(1)  
                
            
                #Proventos
                if 'INTEGRAL' in row['PROVENTOS']:
                    # Quantidade field for Auxílio Transporte 
                    wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="id_10_11_18_11_15_22_40_12_16_11_24"]'))).click()
                    driver.find_element(By.XPATH,f'//*[@id="id_10_11_18_11_15_22_40_12_16_11_24"]/option[2]').click()
                elif 'PROPORCIONAL' in row['PROVENTOS']:
                    # Valor field for Auxílio Alimentação
                    wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="id_10_11_18_11_15_22_40_12_16_11_24"]'))).click()
                    driver.find_element(By.XPATH,f'//*[@id="id_10_11_18_11_15_22_40_12_16_11_24"]/option[3]').click()

                # Modalidade Aposentadoria
                wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[2]/div[2]/div[7]/div/button/div/div/div'))).click()
                time.sleep(1)
                wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[2]/div[2]/div[7]/div/div/div[1]/input'))).send_keys(str(row['MODALIDADE APOSENTADORIA']) + Keys.SPACE)
                time.sleep(1)
                wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[2]/div[2]/div[7]/div/div/div[2]/ul/li[2]/a/span[2]'))).click()
                time.sleep(1)

                # Migrar para Órgão de Pagamento 
                if 'S' in row['MIGRAR']:
                    # Quantidade field for Auxílio Transporte 
                    wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="id_10_11_18_11_15_22_40_12_16_11_65"]'))).click()
                    driver.find_element(By.XPATH,f'//*[@id="id_10_11_18_11_15_22_40_12_16_11_65"]/option[2]').click()
                elif 'N' in row['MIGRAR']:
                    # Valor field for Auxílio Alimentação
                    wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="id_10_11_18_11_15_22_40_12_16_11_65"]'))).click()
                    driver.find_element(By.XPATH,f'//*[@id="id_10_11_18_11_15_22_40_12_16_11_65"]/option[3]').click()

                #Observação
                observacao1 = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="id_10_11_18_11_15_22_40_12_16_11_19"]')))
                observacao1.send_keys(str(row['OBSERVAÇÃO']))
                time.sleep(1)
            
                # Informações para Previdência
                wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="id_10_11_18_11_15_22_40_12_16_31_66_assistente_existente"]/div[1]/div/button/div/div/div'))).click()
                time.sleep(1)
                wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_10_11_18_11_15_22_40_12_16_31_66_assistente_existente"]/div[1]/div/div/div[1]/input'))).send_keys(Keys.SPACE)
                time.sleep(1)
                wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="id_10_11_18_11_15_22_40_12_16_31_66_assistente_existente"]/div[1]/div/div/div[2]/ul/li[2]/a/span[2]'))).click()
                time.sleep(1)
                        
                # DIVISAO
                wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[3]/div[4]/div[1]/div/button/div/div/div'))).click()
                time.sleep(1)
                divisao = str(row['DIVISÃO']) 
                campo_input_divisao =  wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[3]/div[4]/div[1]/div/div/div[1]/input')))
                campo_input_divisao.send_keys(divisao)
                time.sleep(1)
                campo_input_divisao.send_keys(Keys.SPACE)
                time.sleep(1)

                # Esperar o dropdown aparecer
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[3]/div[4]/div[1]/div/div/div[2]/ul'))
                )
                time.sleep(1)

                # Encontrar todos os elementos do dropdown
                elementos_dropdown = driver.find_elements(By.XPATH, '//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[3]/div[4]/div[1]/div/div/div[2]/ul/li')
                time.sleep(1)

                # Iterar sobre os elementos do dropdown
                for elemento in elementos_dropdown:
                    # Verificar se o texto desejado está presente no elemento do dropdown
                    if divisao in elemento.text:
                        # Clicar no elemento
                        elemento.click()
                        # Se o elemento for clicado, podemos sair do loop
                        break

                # Situacao
                wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[3]/div[4]/div[2]/div/button/div/div/div'))).click()
                time.sleep(1)
                Situacao = str(row['SITUAÇÃO']) 
                campo_input_Situacao =  wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[3]/div[4]/div[2]/div/div/div[1]/input')))
                campo_input_Situacao.send_keys(Situacao)
                time.sleep(1)
                campo_input_Situacao.send_keys(Keys.SPACE)
                time.sleep(1)

                # Esperar o dropdown aparecer 
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[3]/div[4]/div[2]/div/div/div[2]/ul'))
                )
                time.sleep(1)

                # Encontrar todos os elementos do dropdown
                elementos_dropdown = driver.find_elements(By.XPATH, '//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[3]/div[4]/div[2]/div/div/div[2]/ul/li')
                time.sleep(1)

                # Iterar sobre os elementos do dropdown
                for elemento in elementos_dropdown:
                    # Verificar se o texto desejado está presente no elemento do dropdown
                    if Situacao in elemento.text:
                        # Clicar no elemento
                        elemento.click()
                        # Se o elemento for clicado, podemos sair do loop
                        break
                
                #FormaPrevidencia
                wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="id_10_11_18_11_15_22_40_12_16_22_16"]'))).click()
                driver.find_element(By.XPATH,'//*[@id="id_10_11_18_11_15_22_40_12_16_22_16"]/option[3]').click()

                #Categoria da Aposentadoria
                if 'Militares' in row['CATEGORIA']:            
                    wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="id_10_11_18_11_15_22_40_12_16_22_21"]'))).click()
                    driver.find_element(By.XPATH,f'//*[@id="id_10_11_18_11_15_22_40_12_16_22_21"]/option[3]').click()
                elif 'Civil' in row['CATEGORIA']:              
                    wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="id_10_11_18_11_15_22_40_12_16_22_21"]'))).click()
                    driver.find_element(By.XPATH,f'//*[@id="id_10_11_18_11_15_22_40_12_16_22_21"]/option[2]').click()
                elif 'Docente' in row['CATEGORIA']:
                    wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="id_10_11_18_11_15_22_40_12_16_22_21"]'))).click()
                    driver.find_element(By.XPATH,f'//*[@id="id_10_11_18_11_15_22_40_12_16_22_21"]/option[4]').click()
                elif 'Segurança Pública' in row['CATEGORIA']:
                    wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="id_10_11_18_11_15_22_40_12_16_22_21"]'))).click()
                    driver.find_element(By.XPATH,f'//*[@id="id_10_11_18_11_15_22_40_12_16_22_21"]/option[5]').click()   
                elif 'Outras Especial' in row['CATEGORIA']:
                    wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="id_10_11_18_11_15_22_40_12_16_22_21"]'))).click()
                    driver.find_element(By.XPATH,f'//*[@id="id_10_11_18_11_15_22_40_12_16_22_21"]/option[6]').click()      

                #poder
                wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="id_10_11_18_11_15_22_40_12_16_22_27"]'))).click()
                driver.find_element(By.XPATH,'//*[@id="id_10_11_18_11_15_22_40_12_16_22_27"]/option[2]').click()

                #Tipo de Cálculo
                if 'Integralidade' in row['TIPO DE CALCULO']:            
                    wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="id_10_11_18_11_15_22_40_12_16_22_23"]'))).click()
                    driver.find_element(By.XPATH,f'//*[@id="id_10_11_18_11_15_22_40_12_16_22_23"]/option[2]').click()
                elif 'Por Média' in row['TIPO DE CALCULO']:              
                    wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="id_10_11_18_11_15_22_40_12_16_22_23"]'))).click()
                    driver.find_element(By.XPATH,f'//*[@id="id_10_11_18_11_15_22_40_12_16_22_23"]/option[3]').click()

                    
                #Forma de Revisão
                if 'Paridade' in row['FORMA DE REVISÃO']:            
                    wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="id_10_11_18_11_15_22_40_12_16_22_51"]'))).click()
                    driver.find_element(By.XPATH,f'//*[@id="id_10_11_18_11_15_22_40_12_16_22_51"]/option[2]').click()
                elif 'Reajuste Anual' in row['FORMA DE REVISÃO']:              
                    wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="id_10_11_18_11_15_22_40_12_16_22_51"]'))).click()
                    driver.find_element(By.XPATH,f'//*[@id="id_10_11_18_11_15_22_40_12_16_22_51"]/option[3]').click()

                #Tipo
                if 'Integral' in row['TIPO']:            
                    wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="id_10_11_18_11_15_22_40_12_16_22_52"]'))).click()
                    driver.find_element(By.XPATH,f'//*[@id="id_10_11_18_11_15_22_40_12_16_22_52"]/option[2]').click()
                elif 'Proporcional' in row['TIPO']:              
                    wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="id_10_11_18_11_15_22_40_12_16_22_52"]'))).click()
                    driver.find_element(By.XPATH,f'//*[@id="id_10_11_18_11_15_22_40_12_16_22_52"]/option[3]').click()

                #Cálculo
                if 'Remuneração' in row['CALCULO']:            
                    wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="id_10_11_18_11_15_22_40_12_16_22_53"]'))).click()
                    driver.find_element(By.XPATH,f'//*[@id="id_10_11_18_11_15_22_40_12_16_22_53"]/option[2]').click()
                elif 'Com Paridade' in row['CALCULO']:              
                    wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="id_10_11_18_11_15_22_40_12_16_22_53"]'))).click()
                    driver.find_element(By.XPATH,f'//*[@id="id_10_11_18_11_15_22_40_12_16_22_53"]/option[3]').click()
                elif 'Benefício Médio' in row['CALCULO']:              
                    wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="id_10_11_18_11_15_22_40_12_16_22_53"]'))).click()
                    driver.find_element(By.XPATH,f'//*[@id="id_10_11_18_11_15_22_40_12_16_22_53"]/option[4]').click()

                #Data Inicío
                wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="id_10_11_18_11_15_22_40_12_16_25_20"]'))).click()
                driver.find_element(By.XPATH,'//*[@id="id_10_11_18_11_15_22_40_12_16_25_20"]/option[3]').click()

                #Situação Benefício Orgão Declarante
                wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="id_10_11_18_11_15_22_40_12_16_25_21"]'))).click()
                driver.find_element(By.XPATH,'//*[@id="id_10_11_18_11_15_22_40_12_16_25_21"]/option[2]').click()

                #Número Benefício
                wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="id_10_11_18_11_15_22_40_12_16_25_22"]'))).click()
                driver.find_element(By.XPATH,'//*[@id="id_10_11_18_11_15_22_40_12_16_25_22"]').send_keys(str(row['MATRICULA']))

                #Data Inicío Beneficio
                data_inicio = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="id_10_11_18_11_15_22_40_12_16_25_23"]')))
                data_inicio.send_keys(str(row['DATA REQUERIMENTO E APOSENTADORIA']))
                time.sleep(1)

                #Tipo de Plano de Segregação
                wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="id_10_11_18_11_15_22_40_12_16_25_25"]'))).click()
                driver.find_element(By.XPATH,'//*[@id="id_10_11_18_11_15_22_40_12_16_25_25"]/option[2]').click()

                #Indicador de Benefício por Decisão Judicial
                if 'S' in row['Indicador']:            
                    wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="id_10_11_18_11_15_22_40_12_16_25_27"]'))).click()
                    driver.find_element(By.XPATH,f'//*[@id="id_10_11_18_11_15_22_40_12_16_25_27"]/option[2]').click()
                elif 'N' in row['Indicador']:              
                    wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="id_10_11_18_11_15_22_40_12_16_25_27"]'))).click()
                    driver.find_element(By.XPATH,f'//*[@id="id_10_11_18_11_15_22_40_12_16_25_27"]/option[3]').click()

                # Tipo de Benefício 
                wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[5]/div[2]/div[9]/div/button/div/div/div'))).click()
                time.sleep(1)
                wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[5]/div[2]/div[9]/div/div/div[1]/input'))).send_keys(str(row['Tipo de Benefício']) + Keys.SPACE)
                time.sleep(1)
                wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[5]/div[2]/div[9]/div/div/div[2]/ul/li[2]/a'))).click()
                time.sleep(1)

                # ESOCIAL
                wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[5]/div[2]/div[11]/div/button/div/div/div'))).click()
                time.sleep(1)
                wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[5]/div[2]/div[11]/div/div/div[1]/input'))).send_keys(str(row['E-Social']) + Keys.SPACE)
                time.sleep(1)
                wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[5]/div[2]/div[11]/div/div/div[2]/ul/li[2]/a/span[2]'))).click()
                time.sleep(1)

                #REGIME
                wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="id_10_11_18_11_15_22_40_12_16_25_32"]'))).click()
                driver.find_element(By.XPATH,'//*[@id="id_10_11_18_11_15_22_40_12_16_25_32"]/option[3]').click()

                # Gravar e confirmar - uncomment if needed
                wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="vobys-form-action-buttons"]/button'))).click()
                time.sleep(2)
                wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="vobys-form-confirmation-save"]'))).click()
                time.sleep(2)
                '''
        #ADICIONAR NA FOLHA
        
                driver.get('https://siape.sead.pi.gov.br/adm/funprev/folha-funcionario/folhas/folhas')
                    
                # Esperar até que a página seja totalmente carregada 
                driver.implicitly_wait(30)  # Espera até 30 segundos                      
                                                
                driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[2]/div/div[1]/input[2]').send_keys(str(row['FOLHA']))
                time.sleep(4)

                driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[2]/div/div[10]/button').click()
                time.sleep(4)

                driver.find_element(By.XPATH,'//*[@id="folhaFuncionario"]/div[1]/table/tbody/tr/td[1]/a').click()
                time.sleep(4)
                
                #pagamento
                driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div[5]/div/div[2]/div/div[1]/a').click()
                time.sleep(4)        

                #adicionar
                driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div/a/span[2]').click()
                time.sleep(4)

                #matricula
                driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div/div/button/div/div/div').click()
                time.sleep(4)                
                driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div/div/div/div[1]/input').click()
                time.sleep(4)
                driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div/div/div/div[1]/input').send_keys(str(row['MATRICULA']))
                time.sleep(4)
                driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div/div/div/div[2]/ul/li[2]/a/span[2]').click()
                time.sleep(4)

                #GRAVAR E CONFIRMAR
                driver.find_element(By.XPATH,'//*[@id="vobys-form-action-buttons"]/button').click()
                time.sleep(4)
                driver.find_element(By.XPATH,'//*[@id="vobys-form-confirmation-save"]').click()
                time.sleep(4)
                '''
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
