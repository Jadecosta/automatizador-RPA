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
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options
from funcoes_gerais import gravar_e_confirmar

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

            
            try:
                
                linha_excel = row.name + 2
                # Inicializa o driver do Edge
                edge_path = 'C:/GitHub/Automatizador/msedgedriver.exe'
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
                    
                driver.implicitly_wait(30)  # Espera até 30 segundos

                orgao = str(row['ORGAO'])
                driver.get(f'https://siape.sead.pi.gov.br/adm/{orgao}/pessoas')

            except:
                orgao = str(row['ORGAO'])
                driver.get(f'https://siape.sead.pi.gov.br/adm/{orgao}/pessoas')
                        
                
            # Esperar até que a página seja totalmente carregada 
            driver.implicitly_wait(30)  # Espera até 30 segundos

            #MODULO PESSOAS
            #wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="modules-list"]/li[1]/a/div'))).click()
            #time.sleep(2)              
        
            # Acessar Adicionar
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="buscarFormularioFiltro"]/div[1]/div/a/span[2]'))).click()
            time.sleep(4)

            try:
                wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_10_11_18_11_12_11_11_22_11_assistente_existente"]/div[1]/div/button/div/div/div'))).click()
                time.sleep(2)
                wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_10_11_18_11_12_11_11_22_11_assistente_existente"]/div[1]/div/div/div[1]/input'))).click()
                time.sleep(2)
                wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_10_11_18_11_12_11_11_22_11_assistente_existente"]/div[1]/div/div/div[1]/input'))).send_keys(str(row['CPF']))
                time.sleep(6)
                wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_10_11_18_11_12_11_11_22_11_assistente_existente"]/div[1]/div/div/div[2]/ul/li[2]/a/span[2]'))).click()
                time.sleep(2)

                #GRAVAR E CONFIRMAR
                wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-form-action-buttons"]/button'))).click()
                time.sleep(4)
                wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-form-confirmation-save"]'))).click()
                time.sleep(4)
                
                
            except Exception :    

                #Nova
                wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_10_11_18_11_12_11_11_22_11_assistente_existente"]/div[2]/button'))).click()
                time.sleep(4)

                #NOME
                wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_10_11_18_11_12_11_11_22_11_0_14_11"]'))).click()
                time.sleep(2)
                wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_10_11_18_11_12_11_11_22_11_0_14_11"]'))).send_keys(str(row['NOME']))
                time.sleep(2)
                
                #CPF
                wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_10_11_18_11_12_11_11_22_11_0_14_12"]'))).click()
                time.sleep(2)
                wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_10_11_18_11_12_11_11_22_11_0_14_12"]'))).send_keys(str(row['CPF']))
                time.sleep(2)

                #NACIONALIDADE
                wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_10_11_18_11_12_11_11_22_11_assistente_novo"]/div[3]/div/button/div/div/div'))).click() 
                time.sleep(2) 
                wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_10_11_18_11_12_11_11_22_11_assistente_novo"]/div[3]/div/div/div[1]/input'))).send_keys(str(row['NACIONALIDADE']))
                time.sleep(2)
                wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_10_11_18_11_12_11_11_22_11_assistente_novo"]/div[3]/div/div/div[2]/ul/li[2]/a/span[2]'))).click() 
                time.sleep(2)      

                #SEXO
                wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_10_11_18_11_12_11_11_22_11_assistente_novo"]/div[4]/div/button/div/div/div'))).click() 
                time.sleep(2)
                wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_10_11_18_11_12_11_11_22_11_assistente_novo"]/div[4]/div/div/div[1]/input'))).send_keys(str(row['SEXO']))
                time.sleep(2)
                wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_10_11_18_11_12_11_11_22_11_assistente_novo"]/div[4]/div/div/div[2]/ul/li[2]/a'))).click()
                time.sleep(2)

                #DATA NASCIMENTO
                wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_10_11_18_11_12_11_11_22_11_0_14_13"]'))).click()
                time.sleep(2)
                wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_10_11_18_11_12_11_11_22_11_0_14_13"]'))).send_keys(str(row['DATA_NASCIMENTO']))
                time.sleep(2)

                #NOME MÃE
                wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_10_11_18_11_12_11_11_22_11_0_14_24"]'))).click()
                time.sleep(2)
                wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_10_11_18_11_12_11_11_22_11_0_14_24"]'))).send_keys(str(row['MAE']))
                time.sleep(2)

                #RAÇA/COR
                wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_10_11_18_11_12_11_11_22_11_assistente_novo"]/div[8]/div/button/div/div/div'))).click() 
                time.sleep(2)
                wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_10_11_18_11_12_11_11_22_11_assistente_novo"]/div[8]/div/div/div[1]/input'))).send_keys(str(row['RACA/COR']))
                time.sleep(2)
                wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_10_11_18_11_12_11_11_22_11_assistente_novo"]/div[8]/div/div/div[2]/ul/li[2]/a'))).click()
                time.sleep(2)

                #DEFICIENCIA
                wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_10_11_18_11_12_11_11_22_11_assistente_novo"]/div[9]/div/button/div/div/div'))).click() 
                time.sleep(2)
                wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_10_11_18_11_12_11_11_22_11_assistente_novo"]/div[9]/div/div/div[1]/input'))).send_keys(str(row['DEFICIENCIA']))
                time.sleep(2)
                wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_10_11_18_11_12_11_11_22_11_assistente_novo"]/div[9]/div/div/div[2]/ul/li[2]/a'))).click()
                time.sleep(2)

                #logradouro
                wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_10_11_18_11_12_11_11_22_11_0_14_40"]'))).click()
                time.sleep(2)
                wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_10_11_18_11_12_11_11_22_11_0_14_40"]'))).send_keys(str(row['LOGRADOURO']))
                time.sleep(2)

                #UF
                wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_10_11_18_11_12_11_11_22_11_assistente_novo"]/div[19]/div/button/div/div/div'))).click() 
                time.sleep(2)
                wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_10_11_18_11_12_11_11_22_11_assistente_novo"]/div[19]/div/div/div[1]/input'))).send_keys(str(row['UF']))
                time.sleep(2)
                wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_10_11_18_11_12_11_11_22_11_assistente_novo"]/div[19]/div/div/div[2]/ul/li[2]/a'))).click()
                time.sleep(2)

                #MUNICIPIO
                wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_10_11_18_11_12_11_11_22_11_assistente_novo"]/div[20]/div/button/div/div/div'))).click() 
                time.sleep(2)
                wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_10_11_18_11_12_11_11_22_11_assistente_novo"]/div[20]/div/div/div[1]/input'))).send_keys(str(row['MUNICIPIO']))
                time.sleep(2)
                wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_10_11_18_11_12_11_11_22_11_assistente_novo"]/div[20]/div/div/div[2]/ul/li[2]/a'))).click()
                time.sleep(2)

                #PAÍS
                wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_10_11_18_11_12_11_11_22_11_assistente_novo"]/div[21]/div/button/div/div/div'))).click() 
                time.sleep(2)
                wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_10_11_18_11_12_11_11_22_11_assistente_novo"]/div[21]/div/div/div[1]/input'))).send_keys(str(row['PAIS']))
                time.sleep(2)
                wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_10_11_18_11_12_11_11_22_11_assistente_novo"]/div[21]/div/div/div[2]/ul/li[2]/a'))).click()
                time.sleep(2)
                '''
                #Data Início Endereço
                wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_10_11_18_11_12_11_11_22_11_0_14_51"]'))).click()
                time.sleep(2)
                wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_10_11_18_11_12_11_11_22_11_0_14_51"]'))).send_keys(str(row['Data_Inicio_Endereço']))
                time.sleep(2)
                '''
                #Estado Civil                 //*[@id="id_10_11_18_11_12_11_11_22_11_assistente_novo"]/div[25]/div/button/div
                wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_10_11_18_11_12_11_11_22_11_assistente_novo"]/div[25]/div/button/div'))).click() 
                time.sleep(2) 
                wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_10_11_18_11_12_11_11_22_11_assistente_novo"]/div[25]/div/div/div[1]/input'))).send_keys(str(row['ESTADO_CIVIL']))
                time.sleep(2)
                wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_10_11_18_11_12_11_11_22_11_assistente_novo"]/div[25]/div/div/div[2]/ul/li[2]/a'))).click()
                time.sleep(2)
                '''
                #Data Início Estado Civil
                wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_10_11_18_11_12_11_11_22_11_0_14_56"]'))).click()
                time.sleep(2)
                wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_10_11_18_11_12_11_11_22_11_0_14_56"]'))).send_keys(str(row['Data_Inicio_Estado_civil']))
                time.sleep(2)
                '''
                #banco //*[@id="id_10_11_18_11_12_11_11_22_11_assistente_novo"]/div[27]/div/button/div/div/div
                wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_10_11_18_11_12_11_11_22_11_assistente_novo"]/div[27]/div/button/div/div/div'))).click() 
                time.sleep(2)
                wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_10_11_18_11_12_11_11_22_11_assistente_novo"]/div[27]/div/div/div[1]/input'))).send_keys(str(row['BANCO']))
                time.sleep(2)
                wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_10_11_18_11_12_11_11_22_11_assistente_novo"]/div[27]/div/div/div[2]/ul/li[2]/a'))).click()
                time.sleep(2)
        
                #AGENCIA
                wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_10_11_18_11_12_11_11_22_11_assistente_novo"]/div[28]/div/button/div/div/div'))).click() 
                time.sleep(2)
                wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_10_11_18_11_12_11_11_22_11_assistente_novo"]/div[28]/div/div/div[1]/input'))).send_keys(str(row['AGENCIA']))
                time.sleep(2)
                wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_10_11_18_11_12_11_11_22_11_assistente_novo"]/div[28]/div/div/div[2]/ul/li[2]/a'))).click()
                time.sleep(2)
            
                

                #CONTA CORRENTE
                wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_10_11_18_11_12_11_11_22_11_0_14_64"]'))).click()
                time.sleep(2)
                wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_10_11_18_11_12_11_11_22_11_0_14_64"]'))).send_keys(str(row['CONTA_CORRENTE']))
                time.sleep(2)
                '''
                #Data Início Banco 
                wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_10_11_18_11_12_11_11_22_11_0_14_67"]'))).click()
                time.sleep(2)
                wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_10_11_18_11_12_11_11_22_11_0_14_67"]'))).send_keys(str(row['Data_Inicio_BANCO']))
                time.sleep(2)
                '''
                #OPERAÇÃO
                #wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_10_11_18_11_12_11_11_22_11_0_14_65"]'))).click()
                #time.sleep(2)
                #wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_10_11_18_11_12_11_11_22_11_0_14_65"]'))).send_keys(str(row['OPERACAO']))
                #time.sleep(2)
                try:
                    element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="id_10_11_18_11_12_11_11_22_11_0_14_65"]')))
                    element.click()
                    element.send_keys('001')
                except:
                    element.click()
                    element.clear()
                    element.send_keys('013')                   

                # GRAVAR E CONFIRMAR
                wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="vobys-form-action-buttons"]/button'))).click()
                time.sleep(4)
                wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="vobys-form-confirmation-save"]'))).click()
                time.sleep(4)
               
            ''' 
            try: 
                    element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="id_10_11_18_11_12_11_11_22_11_0_14_65"]')))
                    element.click()
                    element.send_keys('001')

                    # GRAVAR E CONFIRMAR
                    gravar_e_confirmar(driver)

                except:
                    try:
                        # Primeira tentativa falhou, tentar com '013'
                        element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="id_10_11_18_11_12_11_11_22_11_0_14_65"]')))
                        element.clear()
                        element.send_keys('051')

                        # GRAVAR E CONFIRMAR
                        gravar_e_confirmar(driver)

                    except:
                        # Segunda tentativa falhou, tentar com outro valor, por exemplo, '025'
                        element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="id_10_11_18_11_12_11_11_22_11_0_14_65"]')))
                        element.clear()
                        element.send_keys('013')

                        # GRAVAR E CONFIRMAR
                        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="vobys-form-action-buttons"]/button'))).click()
                        time.sleep(4)
                        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="vobys-form-confirmation-save"]'))).click()
                        time.sleep(4)
            '''


            # Esperar até que a página seja totalmente carregada 
            driver.implicitly_wait(30)  # Espera até 30 segundos
            
            #vinculo                      //*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div/div[2]/div/div/button/div/div/div
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div/div[2]/div/div/button/div/div/div'))).click()
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div/div[2]/div/div/div/div[1]/input'))).send_keys('Quadro de Pessoa')
            time.sleep(4)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div/div[2]/div/div/div/div[2]/ul/li[2]/a/span[2]'))).click()
            time.sleep(4)
        
            #PROXIMO
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-form-action-buttons"]/button'))).click()
            time.sleep(6) 

            ########################################################
            #INGRESSO
            ########################################################  

            #DATA ADMISSAo/POSSE/EXERCICIO  
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_10_11_18_11_15_11_11_12_12"]'))).send_keys(str(row['DATA_ADMISSAO']))
            time.sleep(2)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_10_11_18_11_15_11_11_12_13"]'))).send_keys(str(row['DATA_ADMISSAO']))
            time.sleep(2)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_10_11_18_11_15_11_11_12_14"]'))).send_keys(str(row['DATA_ADMISSAO']))
            time.sleep(2)
        
            #ESPECIALIDADE
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[3]/div[2]/div[8]/div/button/div/div/div'))).click()
            time.sleep(2)

            especialidade = (str(row['ESPECIALIDADE']))
            especialidade_buscar = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[3]/div[2]/div[8]/div/div/div[1]/input')))
            time.sleep(2)
            especialidade_buscar.send_keys(especialidade)
            time.sleep(2)
            especialidade_buscar.send_keys(Keys.SPACE)
            time.sleep(2)
            # Encontrar todos os elementos do dropdown
            #opcao_especialidade = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[3]/div[2]/div[8]/div/div/div[2]/ul/li[2]/a/span[2]')))
            #ActionChains(driver).move_to_element(opcao_especialidade).click().perform()
            #elementos_dropdown = wait.until(EC.presence_of_element_locateds(By.CLASS_NAME, "dropdown-item"))
            driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[3]/div[2]/div[8]/div/div/div[2]/ul/li[2]/a/span[2]').click() 
            '''
            # Encontrar todos os elementos do dropdown
                # Iterar sobre os elementos do dropdown
                for elemento in elementos_dropdown:
                    # Verificar se o texto desejado está presente no elemento do dropdown
                    if especialidade in elemento.text:
                        # Clicar no elemento
                        elemento.click()
                        # Se o elemento for clicado, podemos sair do loop
                        break
            ''' 
            time.sleep(2)
            #REABILITADO
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_10_11_18_11_15_11_11_13_23"]'))).click()
            time.sleep(2)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_10_11_18_11_15_11_11_13_23"]/option[3]'))).click() 
            time.sleep(2)       
            #REGIME
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[5]/div[2]/div[1]/div/button/div/div/div'))).click()
            time.sleep(2)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[5]/div[2]/div[1]/div/div/div[1]/input'))).send_keys(row['REGIME'])
            time.sleep(2)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[5]/div[2]/div[1]/div/div/div[2]/ul/li[2]/a/span[2]'))).click()
            time.sleep(2)
            #REMUNERAÇAO
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@i d="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[5]/div[2]/div[2]/div/button/div/div/div'))).click()
            time.sleep(2)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[5]/div[2]/div[2]/div/div/div[1]/input'))).send_keys('Remunerado')
            time.sleep(4)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[5]/div[2]/div[2]/div/div/div[2]/ul/li[2]/a/span[2]'))).click()
            time.sleep(2)
            #DIVIÃO
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[5]/div[2]/div[3]/div/button/div/div/div'))).click()
            time.sleep(2)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[5]/div[2]/div[3]/div/div/div[1]/input'))).send_keys(row['DIVISAO'])
            time.sleep(4)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[5]/div[2]/div[3]/div/div/div[2]/ul/li[2]a/span[2]'))).click()
            time.sleep(2) 
            
            if 'Militar' in row['DIVISAO']:
                wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[5]/div[2]/div[3]/div/div/div[2]/ul/li[4]/a'))).click()
                time.sleep(2)            
            elif():
                wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[5]/div[2]/div[3]/div/div/div[2]/ul/li[2]/a'))).click()
                time.sleep(2)    
            
        
            #CATEGORIA                     
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[5]/div[2]/div[4]/div/button/div/div/div'))).click()
            time.sleep(2)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[5]/div[2]/div[4]/div/div/div[1]/input'))).send_keys(row['CATEGORIA'])
            time.sleep(4)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[5]/div[2]/div[4]/div/div/div[2]/ul/li[2]/a/span[2]'))).click()
            time.sleep(2)
            #TIPO DE SERVIDOR
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[5]/div[2]/div[6]/div/button/div/div/div'))).click()
            time.sleep(2)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[5]/div[2]/div[6]/div/div/div[1]/input'))).send_keys(row['TIPO'])
            time.sleep(4)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[5]/div[2]/div[6]/div/div/div[2]/ul/li[2]/a/span[2]'))).click()
            time.sleep(2)
            
            #SITUAÇÃO
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[5]/div[2]/div[5]/div/button/div/div/div'))).click()
            time.sleep(2)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[5]/div[2]/div[5]/div/div/div[1]/input'))).send_keys(row['SITUACAO'])
            time.sleep(4)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[5]/div[2]/div[5]/div/div/div[2]/ul/li[2]/a/span[2]'))).click()
            time.sleep(2)
            
            #INCIDENCIA
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[5]/div[2]/div[7]/div/button/div/div/div'))).click()
            time.sleep(2)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[5]/div[2]/div[7]/div/div/div[2]/ul/li[4]/a/span[2]'))).click()
            time.sleep(2)
            
            
            #LOTAÇÃO 
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[7]/div[2]/div[1]/div/button/div/div/div'))).click()
            time.sleep(2)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[7]/div[2]/div[1]/div/div/div[1]/input'))).send_keys(row['LOTACAO'])
            time.sleep(4)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[7]/div[2]/div[1]/div/div/div[2]/ul/li[2]/a/span[2]'))).click()
            time.sleep(2)
            #CARGA HORARIA
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_10_11_18_11_15_11_11_16_15"]'))).click()
            time.sleep(2)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_10_11_18_11_15_11_11_16_15"]'))).send_keys(str(row['JORNADA DE TRABALHO']))
            time.sleep(2)
            #OBSERVACAO
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_10_11_18_11_15_11_11_25_11"]'))).click()
            time.sleep(2)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_10_11_18_11_15_11_11_25_11"]'))).send_keys(str(row['OBSERVACAO']))
            time.sleep(2)
            #GRAVAR E CONFIRMAR
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-form-action-buttons"]/button'))).click()
            time.sleep(4)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-form-confirmation-save"]'))).click()
            time.sleep(4)
            
        
            success_time = datetime.now().strftime("%H:%M")
            success_message = f"Linha Excel: {linha_excel} {row['CPF']} INCLUSO EM FOLHA às {success_time}\n"
            print(success_message)
            log_file_path.write(success_message)
            log_file_path.flush()  # Força a gravação imediata no arquivo
        except Exception as e:
            # Salva a linha que deu erro no arquivo de texto
            success_time = datetime.now().strftime("%H:%M")
            error_message = f"Linha Excel: {linha_excel} {row['CPF']} Erro às {success_time}\n"
            log_file_path.write(error_message)
            log_file_path.flush()  # Força a gravação imediata no arquivo
            print(error_message)
            pass
        finally:
            driver.quit()

    # Atualizar progresso
    #progresso = (row.name + 1) / total_linhas * 100
    #with open(progress_file_path, 'w') as progress_file:
    #    json.dump({'task_id': task_id, 'progress': progresso}, progress_file)
            
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
