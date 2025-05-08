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
            nome_pessoa = row['MATRICULA']
            try:
                # Inicializa o driver do Edge
                edge_path = 'C:/Github/App_Program/msedgedriver.exe'
                edge_options = webdriver.EdgeOptions()
                edge_options.use_chromium = True

                # Configuração do nível de log do driver do Edge
                #logging_prefs = {"browser": "ERROR"}
                #edge_options.set_capability("loggingPrefs", logging_prefs)

                # Exibe o navegador visualmente
                edge_options.add_argument('--headless')  # Comentar ou remover esta linha para desativar o modo headless
                edge_options.add_argument('--disable-gpu')  # Desabilita a aceleração de GPU
                #edge_options.add_experimental_option("excludeSwitches", ["enable-logging"])  # Desabilita o DevTools listening

                edge_service = Service(edge_path)
                driver = webdriver.Edge(service=edge_service, options=edge_options)

                # Navegar até a página de login
                driver.get('https://siape.sead.pi.gov.br')

                # Esperar até que a página seja totalmente carregada 
                driver.implicitly_wait(30)  # Espera até 30 segundos

                # Localizar os elementos de input do usuário e senha
                input_usuario = driver.find_element(By.ID, 'username')
                input_senha = driver.find_element(By.ID, 'password')
                driver.implicitly_wait(60)  # Espera até 30 segundos  

                input_senha.send_keys(Keys.RETURN)  # Enviar o formulário de login

                orgao = str(row['ORGAO'])
                driver.get(f'https://siape.sead.pi.gov.br/adm/{orgao}/pessoas')

            except:
                orgao = str(row['ORGAO'])
                driver.get(f'https://siape.sead.pi.gov.br/adm/{orgao}/pessoas')

            # Esperar até que a página seja totalmente carregada 
            driver.implicitly_wait(30)  # Espera até 30 segundos
        
            # Matricula
            driver.find_element(By.XPATH,'//*[@id="matricula"]/div/div[3]/input').click()
            time.sleep(4)
            driver.find_element(By.XPATH,'//*[@id="matricula"]/div/div[3]/input').send_keys(str(row['MATRICULA']))
            time.sleep(4)
            driver.find_element(By.XPATH,'//*[@id="pesquisaNormal"]/div/div[6]/button').click()
            time.sleep(4)
            #SERVIDOR
            driver.find_element(By.XPATH,'//*[@id="resultadoDaBuscaDePessoas"]/div[1]/table/tbody/tr/td[1]/a').click()
            time.sleep(4)
        ####    
            
            #DESLIGAMENTO
            driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div[14]/div/div[2]/div/div[11]/a').click()
            time.sleep(2)

            #ADICIONAR
            driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div[5]/form/div[1]/div/a/span[2]').click()
            time.sleep(4)

            #Forma de Extinção do Trabalho (RAIS) *
            driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[1]/div/button/div/div/div').click()
            time.sleep(2)
            driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[1]/div/div/div[1]/input').click()
            time.sleep(2)
            driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[1]/div/div/div[1]/input').send_keys(row['Forma de Extinção'])
            time.sleep(2)
            driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[1]/div/div/div[2]/ul/li[2]/a/span[2]').click()
            time.sleep(2)

            # Motivo do Desligamento do Servidor *
            driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[2]/div/button/div/div/div').click()
            time.sleep(2)
            driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[2]/div/div/div[1]/input').click()
            time.sleep(2)
            driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[2]/div/div/div[1]/input').send_keys(row['Motivo do Desligamento'])
            time.sleep(2)
            driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[2]/div/div/div[2]/ul/li[2]/a').click()
            time.sleep(2)

            # DIVISAO
            driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[4]/div/button/div/div/div').click()
            time.sleep(2)
            driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[4]/div/div/div[1]/input').click()
            time.sleep(2)
            driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[4]/div/div/div[1]/input').send_keys(row['DIVISAO'])
            time.sleep(2)
            driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[4]/div/div/div[2]/ul/li[2]/a').click()
            time.sleep(2)

            #SITUAÇAO
            driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[5]/div/button/div/div/div').click()
            time.sleep(2)
            driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[5]/div/div/div[1]/input').click()
            time.sleep(2)
            driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[5]/div/div/div[1]/input').send_keys(row['SITUAÇAO'])
            time.sleep(2)
            driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[5]/div/div/div[2]/ul/li[2]/a').click()
            time.sleep(2)

            # MOVIMENTAÇÃO SEFIP
            driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[6]/div/button/div/div/div').click()
            time.sleep(2)
            driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[6]/div/div/div[1]/input').click()
            time.sleep(2)
            driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[6]/div/div/div[1]/input').send_keys(row['MOVIMENTAÇÃO SEFIP'])
            time.sleep(2)
            driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[6]/div/div/div[2]/ul/li[2]/a/span[2]').click()
            time.sleep(2)

            # TIPO SERVIDOR *
            driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[7]/div/button/div/div/div').click()
            time.sleep(2)
            driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[7]/div/div/div[1]/input').click()
            time.sleep(2)
            driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[7]/div/div/div[1]/input').send_keys(row['TIPO SERVIDOR'])
            time.sleep(2)
            driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[7]/div/div/div[2]/ul/li[2]/a').click()
            time.sleep(2)


            # eSocial Motivo Desligamento Efetivo *
            driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[9]/div/button/div/div/div').click()
            time.sleep(2)
            driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[9]/div/div/div[1]/input').click()
            time.sleep(2)
            driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[9]/div/div/div[1]/input').send_keys(row['eSocial Motivo'])
            time.sleep(2)
            driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[9]/div/div/div[2]/ul/li[2]/a/span[2]').click()
            time.sleep(2)


            #DATA
            driver.find_element(By.XPATH,'//*[@id="id_10_11_18_11_15_11_22_12_16_12_11"]').click()
            driver.find_element(By.XPATH,'//*[@id="id_10_11_18_11_15_11_22_12_16_12_11"]').send_keys(row['DATA'])

            #observação
            driver.find_element(By.XPATH,'//*[@id="id_10_11_18_11_15_11_22_12_16_12_21"]').click()
            driver.find_element(By.XPATH,'//*[@id="id_10_11_18_11_15_11_22_12_16_12_21"]').send_keys(row['observação'])

            #fgts
            driver.find_element(By.XPATH,'//*[@id="id_10_11_18_11_15_11_22_12_16_12_20"]').click()
            driver.find_element(By.XPATH,' //*[@id="id_10_11_18_11_15_11_22_12_16_12_20"]/option[3]').click()



        ####
            ###GRAVAR E CONFIRMAR
            driver.find_element(By.XPATH,'//*[@id="vobys-form-action-buttons"]/button').click()
            time.sleep(4)
            driver.find_element(By.XPATH,'//*[@id="vobys-form-confirmation-save"]').click()
            time.sleep(4)    
            
            
            success_time = datetime.datetime.now().strftime("%H:%M")
            status = f"EXECUTADO às {success_time}"
            data.at[row.name, "Status"] = status
            print(f" EXECUTADO {linha_excel}: {success_time} {nome_pessoa}")       
            pass    
        except Exception as e:
            success_time = datetime.datetime.now().strftime("%H:%M")
            # Atualizar a coluna "Status" com a informação de erro
            status = f"ERRO: {success_time}, {nome_pessoa}, {str(e)}"
            data.at[row.name, "Status"] = status
            print(f"ERRO na linha {linha_excel}: {success_time}, {nome_pessoa}, {str(e)}")

            
            pass
        finally:
            driver.quit()



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
