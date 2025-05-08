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


error_file = open('C:/Users/ADS_DFPG/Desktop/Projetos_Program/Automacao_projetos/Automacao-Python/Arquivos/rubricadigitada.txt', 'w')  # Abre o arquivo para escrita

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
        mat = '366974-2'
        #rubrica = str(row['RUBRICA']).replace('.0', '') 
        try:
            # Inicializa o driver do Edge
            edge_path = 'C:/Users/ADS_DFPG/Desktop/Projetos_Program/Automacao_projetos/Automacao-Python/msedgedriver.exe'
            edge_options = webdriver.EdgeOptions()
            edge_options.use_chromium = True

            # Configuração do nível de log do driver do Edge
            #logging_prefs = {"browser": "ERROR"}
            #edge_options.set_capability("loggingPrefs", logging_prefs)

            # Configurações para ignorar certificados inseguros
            edge_options.add_argument('--ignore-certificate-errors')
            edge_options.add_argument('--ignore-ssl-errors')
            edge_options.add_argument('--disable-web-security')

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
            try:
                # Localizar os elementos de input do usuário e senha
                input_usuario = driver.find_element(By.ID, 'username')
                input_senha = driver.find_element(By.ID, 'password')

                # Preencher os campos de usuário e senha
                input_usuario.send_keys(USERNAME)
                input_senha.send_keys(PASSWORD)

                input_senha.send_keys(Keys.RETURN)  # Enviar o formulário de login
            except:
                print("Erro de credenciais!")

            #orgao = str(row['ORGAO'])
            driver.get(f'https://siape.sead.pi.gov.br/adm/sead/folha-funcionario/folhas/folhas')
        except:
            orgao = str(row['ORGAO'])
            driver.get(f'https://siape.sead.pi.gov.br/adm/sead/folha-funcionario/folhas/folhas')
                    
        # Esperar até que a página seja totalmente carregada 
        driver.implicitly_wait(30)  # Espera até 30 segundos     
                    

        #LOCALIZAR FOLHA
        driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[2]/div/div[1]/input[2]').click()
        driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[2]/div/div[1]/input[2]').send_keys('11/2024-250')
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
        driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[2]/div/div[1]/input[2]').send_keys(mat)
        time.sleep(2)

        #BUSCAR  
        driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[2]/div/div[12]/button').click() 
        time.sleep(6) 

        #Pagamento Servidor
        driver.find_element(By.XPATH,'//*[@id="funcionarios"]/div[1]/table/tbody/tr/td[1]/a').click()
        time.sleep(4)

           
        
        #RUBRICAS DIGITADA
        driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[2]/div/a[17]').click()
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
                            
                            #ADICIONAR
                            driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div/a/span[2]').click()
                            time.sleep(2)

                            #inserindo nova rubrica //*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[1]/div/button
                            driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[1]/div/button/div/div/div').click()
                            driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[1]/div/div/div[1]/input').click()
                            time.sleep(2)
                            driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[1]/div/div/div[1]/input').send_keys(rubrica)
                            time.sleep(2)
                            driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[1]/div/div/div[2]/ul/li[2]/a/span[2]').click()
                            time.sleep(2)

                            #parametro                    
                            driver.find_element(By.XPATH,'//*[@id="id_20_11_11_11_11_20_12_14_11_11_18_26_12_21_13_20"]').click()
                            driver.find_element(By.XPATH,'//*[@id="id_20_11_11_11_11_20_12_14_11_11_18_26_12_21_13_20"]/option[3]').click()
                            time.sleep(1)
                            #Valor / Multiplicador
                            driver.find_element(By.XPATH,'//*[@id="id_20_11_11_11_11_20_12_14_11_11_18_26_12_21_13_21"]').click()
                            time.sleep(1)
                            driver.find_element(By.XPATH,'//*[@id="id_20_11_11_11_11_20_12_14_11_11_18_26_12_21_13_21"]').send_keys(valor)

                            #Quantidade
                            #driver.find_element(By.XPATH,'//*[@id="id_20_11_11_11_11_20_12_14_11_11_18_25_12_21_13_22"]').click()
                            #time.sleep(1)
                            #driver.find_element(By.XPATH,'//*[@id="id_20_11_11_11_11_20_12_14_11_11_18_25_12_21_13_22"]').send_keys(row['QUANTIDADE'])
                            
                            #Substituição *
                            driver.find_element(By.XPATH,'//*[@id="id_20_11_11_11_11_20_12_14_11_11_18_26_12_21_13_38"]').click()
                            driver.find_element(By.XPATH,'//*[@id="id_20_11_11_11_11_20_12_14_11_11_18_26_12_21_13_38"]/option[2]').click()


    except Exception as e:
        # Salva a linha que deu erro no arquivo de texto
        success_time = datetime.datetime.now().strftime("%H:%M")
        error_message = f"Linha Excel: {linha_excel} Erro às {success_time}\n"
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