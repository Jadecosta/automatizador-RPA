import pandas as pd
import time
import datetime
import concurrent.futures
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from tkinter import filedialog
from configs.config import USERNAME, PASSWORD

# Usar o diálogo de seleção de arquivo do tkinter para obter o caminho do arquivo original
file_path = filedialog.askopenfilename(title="Selecione o arquivo Excel", filetypes=[("Excel files", "*.xlsx")])
error_file = open('C:/Users/ADS_DFPG/Desktop/Automacao-Python/Arquivos/rub_DIFERENCA_Log.txt', 'w')  # Abre o arquivo para escrita

# Leitura do arquivo Excel
try:
    data = pd.read_excel(file_path)
except Exception as e:
    error_file.write(f"Erro ao ler o arquivo Excel: {e}\n")
    error_file.close()
    exit()

print("CARREGANDO..")

def processar_linha(row):
    
    try:
        linha_excel = row.name + 2
        nome_pessoa = row['MATRICULA']
        try:
            # Inicializa o driver do Edge
            edge_path = 'C:/Users/ADS_DFPG/Desktop/Automacao-Python/msedgedriver.exe'
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

            # Navegar até a página de login
            driver.get('https://siape.sead.pi.gov.br')

            # Esperar até que a página seja totalmente carregada 
            driver.implicitly_wait(30)  # Espera até 30 segundos

            # Localizar os elementos de input do usuário e senha
            input_usuario = driver.find_element(By.ID, 'username')
            input_senha = driver.find_element(By.ID, 'password')

            # Preencher os campos de usuário e senha
            input_usuario.send_keys(USERNAME)
            input_senha.send_keys(PASSWORD)

            input_senha.send_keys(Keys.RETURN)  # Enviar o formulário de login
            
            orgao = str(row['ORGAO'])
            driver.get(f'https://siape.sead.pi.gov.br/adm/{orgao}/folha-funcionario/folhas/folhas')

        except:

            orgao = str(row['ORGAO'])
            driver.get(f'https://siape.sead.pi.gov.br/adm/{orgao}/folha-funcionario/folhas/folhas')
                    
        # Esperar até que a página seja totalmente carregada 
        driver.implicitly_wait(30)  # Espera até 30 segundos  

        #LOCALIZAR FOLHA
        driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[2]/div/div[1]/input[2]').click()
        driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[2]/div/div[1]/input[2]').send_keys(str(row['FOLHA']))
        time.sleep(4)
    
        #BUSCAR                         
        driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[2]/div/div[10]/button').click() 
        time.sleep(4) 

        #SELECIONAR FOLHA
        driver.find_element(By.XPATH,'//*[@id="folhaFuncionario"]/div[1]/table/tbody/tr/td[1]/a').click()  
        
        # Esperar até que a página seja totalmente carregada 
        driver.implicitly_wait(30)  # Espera até 30 segundos   
            
        #PAGAMENTO
        driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div[5]/div/div[2]/div/div[1]/a').click()
        
        # Esperar até que a página seja totalmente carregada 
        driver.implicitly_wait(30)  # Espera até 30 segundos

        #MATRICULA                                      
        driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[2]/div/div[1]/input[2]').click()
        driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[2]/div/div[1]/input[2]').send_keys(str(row['MATRICULA']))
        time.sleep(2)

        #BUSCAR  
        driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[2]/div/div[12]/button').click() 
        time.sleep(6) 

        #Pagamento Servidor
        driver.find_element(By.XPATH,'//*[@id="funcionarios"]/div[1]/table/tbody/tr/td[1]/a').click()
        time.sleep(4)

        
        

        #RUBRICAS DIFERENÇA
        driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[2]/div/a[18]').click()  
        time.sleep(2) 
        
        
        while True:
            try:
                #RUBRICA
                rubrica = row['RUBRICA'] 
                element = driver.find_element(By.XPATH,f'//*[@id="vobys-content"]/div/div/div/div[3]/div/div//*[text()="{rubrica}"]')
                element.click()
                time.sleep(2) 
                
                #EXCLUIR
                driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/nav/div[2]/a/span[2]').click()
                time.sleep(2) 

                #EXCLUSAO
                driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[10]/div/div/button/div/div/div').click()
                driver.find_element(By.XPATH,'/html/body/div[5]/div/div[1]/input').click()
                time.sleep(2)
                driver.find_element(By.XPATH,'/html/body/div[5]/div/div[1]/input').send_keys(' ')
                time.sleep(2)
                driver.find_element(By.XPATH,'/html/body/div[5]/div/div[2]/ul/li[2]/a').click()
                time.sleep(2)

                #GRAVAR E CONFIRMAR
                driver.find_element(By.XPATH,'//*[@id="vobys-form-action-buttons"]/button').click()
                time.sleep(4)
                driver.find_element(By.XPATH,'//*[@id="vobys-form-confirmation-save"]').click()
                time.sleep(4)
            except:
                break
                    
        

        #ADICIONAR                   
        driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div/a/span[2]').click()
        time.sleep(2)
        
        #RUBRICA
        driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[1]/div/button/div/div/div').click()
        driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[1]/div/div/div[1]/input').click()
        time.sleep(2)
        driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[1]/div/div/div[1]/input').send_keys(str(row['RUBRICA']))
        time.sleep(2)
        driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[1]/div/div/div[2]/ul/li[2]/a/span[2]').click()
        time.sleep(2)

        #parametro                     /           
        driver.find_element(By.XPATH,'//*[@id="id_20_11_11_11_11_20_12_14_11_11_18_27_12_21_13_20"]').click()
        driver.find_element(By.XPATH,'//*[@id="id_20_11_11_11_11_20_12_14_11_11_18_27_12_21_13_20"]/option[3]').click()

        #Valor / Multiplicador
        driver.find_element(By.XPATH,'//*[@id="id_20_11_11_11_11_20_12_14_11_11_18_27_12_21_13_21"]').click()
        time.sleep(1)
        driver.find_element(By.XPATH,'//*[@id="id_20_11_11_11_11_20_12_14_11_11_18_27_12_21_13_21"]').send_keys(row['VALOR'])

        #Substituição *
        driver.find_element(By.XPATH,'//*[@id="id_20_11_11_11_11_20_12_14_11_11_18_27_12_21_13_38"]').click()
        driver.find_element(By.XPATH,'//*[@id="id_20_11_11_11_11_20_12_14_11_11_18_27_12_21_13_38"]/option[2]').click()

        #observação
        #driver.find_element(By.XPATH,'//*[@id="id_20_11_11_11_11_20_12_14_11_11_18_27_12_21_13_40"]').click()
        #driver.find_element(By.XPATH,'//*[@id="id_20_11_11_11_11_20_12_14_11_11_18_27_12_21_13_40"]').send_keys(row['OBSERVAÇÃO'])
        #time.sleep(1)

        #GRAVAR E CONFIRMAR
        driver.find_element(By.XPATH,'//*[@id="vobys-form-action-buttons"]/button').click()
        time.sleep(4)
        driver.find_element(By.XPATH,'//*[@id="vobys-form-confirmation-save"]').click()
        time.sleep(4)

        #calcular
        driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[2]/div/a[2]').click()  
        time.sleep(2) 

        #importar RH
        driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div[1]/div/div[2]/div[1]/a').click()  
        time.sleep(4) 

        #Gerar eventos/Rubricas/Calculos
        driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div[1]/div/div[2]/div[6]/a').click()  
        time.sleep(4) 

        success_time = datetime.datetime.now().strftime("%H:%M")
        success_message = f"Linha Excel: {linha_excel} {row['MATRICULA']} VALOR ALTERADO - Execução concluída às {success_time}\n"
        print(success_message)
        error_file.write(success_message)
        error_file.flush()  # Força a gravação imediata no arquivo
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
# Cria um executor de threads com no máximo 5 workers (telas abertas)
with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
#with concurrent.futures.ThreadPoolExecutor() as executor:
    for index, row in data.iterrows():
        resultado = executor.submit(processar_linha, row)
        resultados.append(resultado)

    # Aguarda a conclusão de todos os resultados
    for resultado in concurrent.futures.as_completed(resultados):
        resultado.result()

# Fecha o arquivo após o término do loop
error_file.close()