import pandas as pd
import time
import os
import datetime
import concurrent.futures
import shutil  # Biblioteca para copiar arquivos
from tkinter import filedialog
from configs.config import USERNAME, PASSWORD
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options


error_file = open('C:/Users/ADS_DFPG/Desktop/Projetos_Program/Automacao_projetos/Automacao-Python/Arquivos/importarcalcular.txt', 'w')  # Abre o arquivo para escrita

# Leitura do arquivo Excel
# Usar o diálogo de seleção de arquivo do tkinter para obter o caminho do arquivo original
file_path = filedialog.askopenfilename(title="Selecione o arquivo Excel", filetypes=[("Excel files", "*.xlsx")])

# Verificar se o usuário selecionou um arquivo
if not file_path:
    print("Nenhum arquivo selecionado. Encerrando o programa.")
    exit()

try:
    data = pd.read_excel(file_path)  
except Exception as e:
    print(f"Erro ao ler o arquivo Excel: {e}")
    error_file.write(f"Erro ao ler o arquivo Excel: {e}/n")
    error_file.close()
    exit()

print("CARREGANDO..")

def processar_linha(row):
    
    try:

        linha_excel = row.name + 2
      
        # Inicializa o driver do Edge
        edge_path = 'C:/Users/ADS_DFPG/Desktop/Projetos_Program/Automacao_projetos/Automacao-Python/msedgedriver.exe'
        edge_options = webdriver.EdgeOptions()
        edge_options.use_chromium = True

        # Configuração do nível de log do driver do Edge
        #logging_prefs = {"browser": "ERROR"}
        #edge_options.set_capability("loggingPrefs", logging_prefs)

        # Exibe o navegador visualmente
        #edge_options.add_argument('--headless')  # Comentar ou remover esta linha para desativar o modo headless
        edge_options.add_argument('--disable-gpu')  # Desabilita a aceleração de GPU
        #edge_options.add_experimental_option("excludeSwitches", ["enable-logging"])  # Desabilita o DevTools listening

        edge_service = Service(edge_path)
        driver = webdriver.Edge(service=edge_service, options=edge_options)
        wait = WebDriverWait(driver, 60)


        # Navegar até a página de login
        driver.get('https://siape.sead.pi.gov.br')
        # Esperar até que a página seja totalmente carregada 
        driver.implicitly_wait(60)  # Espera até 30 segundos  

        # Localizar os elementos de input do usuário e senha
        wait.until(EC.presence_of_element_located((By.ID, "username"))).send_keys(USERNAME)
        driver.find_element(By.ID, "password").send_keys(PASSWORD)
        driver.find_element(By.ID, "password").send_keys(Keys.RETURN)
                    
        #orgao = str(row['ORGAO'])
        driver.get('https://siape.sead.pi.gov.br/adm/seduc/folha-funcionario/folhas/folhas')

        # Esperar até que a página seja totalmente carregada 
        driver.implicitly_wait(60)  # Espera até 30 segundos  

        #LOCALIZAR FOLHA
        wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[2]/div/div[1]/input[2]'))).send_keys(str(row['FOLHA']))
        time.sleep(2) 
        #BUSCAR                         
        wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[2]/div/div[10]/button'))).click() 
        time.sleep(2) 

        #SELECIONAR FOLHA
        wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="folhaFuncionario"]/div[1]/table/tbody/tr[1]/td[1]/a'))).click()  

        #PAGAMENTO
        wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div[5]/div/div[2]/div/div[1]/a'))).click()
                          
        
        #MATRICULA                                      
        wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[2]/div/div[1]/input[2]'))).send_keys(str(row['MATRICULA']))
        time.sleep(1) 
        #CPF
        #wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div[1]/form/div[2]/div/div[10]/input[2]').click()
        #wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div[1]/form/div[2]/div/div[10]/input[2]').send_keys(str(row['CPF']))
        #time.sleep(2)


        #BUSCAR  
        wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[2]/div/div[12]/button'))).click() 
        time.sleep(4) 

        #Pagamento Servidor
        wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="funcionarios"]/div[1]/table/tbody/tr[1]/td[1]/a'))).click()
        time.sleep(4)         
        #calcular
        wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[2]/div/a[2]'))).click()  
        time.sleep(4) 
        
        #importar RH
        wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div[1]/div/div[2]/div[1]/a'))).click()  
        time.sleep(4) 

        #Gerar eventos/Rubricas/Calculos
        wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div[1]/div/div[2]/div[6]/a'))).click()  
        time.sleep(4) 
                 
        success_time = datetime.datetime.now().strftime("%H:%M")
        success_message = f"Linha Excel: {linha_excel} {row['MATRICULA']} Execução concluída às {success_time}\n"
        print(success_message)
       
    except Exception as e:
        # Salva a linha que deu erro no arquivo de texto
        success_time = datetime.datetime.now().strftime("%H:%M")
        error_message = f"Linha Excel: {linha_excel} {row['MATRICULA']} Erro - Execução concluída às {success_time}\n"
        error_file.write(error_message)
        error_file.flush()  # Força a gravação imediata no arquivo
        print(error_message)
        pass
    finally:
        driver.quit()

# Inicializa a lista de resultados
resultados = []

# Cria um executor de threads
# Cria um executor de threads com no máximo 10 workers (telas abertas)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
#with concurrent.futures.ThreadPoolExecutor() as executor:
    for index, row in data.iterrows():
        resultado = executor.submit(processar_linha, row)
        resultados.append(resultado)

    # Aguarda a conclusão de todos os resultados
    for resultado in concurrent.futures.as_completed(resultados):
        resultado.result()

# Fecha o arquivo após o término do loop
error_file.close()