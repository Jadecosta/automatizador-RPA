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
import shutil  # Biblioteca para copiar arquivos
from selenium.common.exceptions import NoSuchElementException  # Importe a exceção
from configs.config import USERNAME, PASSWORD


# Usar o diálogo de seleção de arquivo do tkinter para obter o caminho do arquivo original
file_path = filedialog.askopenfilename(title="Selecione o arquivo Excel", filetypes=[("Excel files", "*.xlsx")])


# Verificar se o usuário selecionou um arquivo
if not file_path:
    print("Nenhum arquivo selecionado. Encerrando o programa.")
    exit()

# Extrair o diretório e o nome do arquivo do caminho selecionado
directory, original_filename = file_path.rsplit("/", 1)
original_filename_no_extension = original_filename.split(".")[0]

# Copiar o arquivo Excel original para uma nova localização
copy_file_path = f"{directory}/{original_filename_no_extension}_status.xlsx"
shutil.copy(file_path, copy_file_path)

# Abra a cópia usando a biblioteca pandas
try:
    data = pd.read_excel(copy_file_path)
except Exception as e:
    print(f"Erro ao ler o arquivo Excel: {e}")
    exit()
# Adicionar uma coluna "Status" ao DataFrame
data["Status"] = ""

# Lista para armazenar o status de cada linha
status_list = []



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

        #CPF
        #driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div[1]/form/div[2]/div/div[10]/input[2]').click()
        #driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div[1]/form/div[2]/div/div[10]/input[2]').send_keys(str(row['CPF']))
        #ime.sleep(2)


        #BUSCAR  
        driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[2]/div/div[12]/button').click() 
        time.sleep(6) 

        #Pagamento Servidor
        driver.find_element(By.XPATH,'//*[@id="funcionarios"]/div[1]/table/tbody/tr/td[1]/a').click()
        time.sleep(4)

        
        

        #RUBRICAS PERMANENTES
        driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[2]/div/a[16]').click()  
        time.sleep(2)           
        
        #RUBRICA
        rubrica = str(int(row['RUBRICA'])) 
        element = driver.find_element(By.XPATH,f'//*[@id="vobys-content"]/div/div/div/div[3]/div/div//*[text()="{rubrica}"]')
        element.click()
        time.sleep(2) 

        

        #ALTERAR
        driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/nav/div[1]/a/span[2]').click()
        time.sleep(2)
        

        #Valor / Multiplicador
        driver.find_element(By.XPATH,'//*[@id="id_20_11_11_11_11_20_12_14_11_11_18_25_12_21_13_21"]').click()
        driver.find_element(By.XPATH,'//*[@id="id_20_11_11_11_11_20_12_14_11_11_18_25_12_21_13_21"]').clear()
        time.sleep(1)
        driver.find_element(By.XPATH,'//*[@id="id_20_11_11_11_11_20_12_14_11_11_18_25_12_21_13_21"]').send_keys(str(row['VALOR']))
        time.sleep(1)

        #observação
        driver.find_element(By.XPATH,'//*[@id="id_20_11_11_11_11_20_12_14_11_11_18_25_12_21_13_40"]').click()
        driver.find_element(By.XPATH,'//*[@id="id_20_11_11_11_11_20_12_14_11_11_18_25_12_21_13_40"]').clear()
        time.sleep(1)
        driver.find_element(By.XPATH,'//*[@id="id_20_11_11_11_11_20_12_14_11_11_18_25_12_21_13_40"]').send_keys(row['OBSERVAÇÃO'])
        time.sleep(1)

        #GRAVAR E CONFIRMAR
        driver.find_element(By.XPATH,'//*[@id="vobys-form-action-buttons"]/button').click()
        time.sleep(4)
        driver.find_element(By.XPATH,'//*[@id="vobys-form-confirmation-save"]').click()
        time.sleep(4)

        #calcular
        driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[2]/div/a[2]').click()  
        time.sleep(2) 

        #Gerar eventos/Rubricas/Calculos
        driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div[1]/div/div[2]/div[6]/a').click()  
        time.sleep(4) 

        success_time = datetime.datetime.now().strftime("%H:%M")
        status = f"EXECUTADO às {success_time}"
        data.at[row.name, "Status"] = status
        status_list.append(status)
        print(f" EXECUTADO {linha_excel}: {success_time} {nome_pessoa}")        
    except NoSuchElementException as e:
        success_time = datetime.datetime.now().strftime("%H:%M")
         # Atualizar a coluna "Status" com a informação de erro
        status = f"ERRO: {success_time}, {nome_pessoa}, {str(e)}"
        data.at[row.name, "Status"] = status
        status_list.append(status)
        print(f"ERRO na linha {linha_excel}: {success_time}, {nome_pessoa}, {str(e)}")

        pass    
    except Exception as e:
        success_time = datetime.datetime.now().strftime("%H:%M")
         # Atualizar a coluna "Status" com a informação de erro
        status = f"ERRO: {success_time}, {nome_pessoa}, {str(e)}"
        data.at[row.name, "Status"] = status
        status_list.append(status)
        print(f"ERRO na linha {linha_excel}: {success_time}, {nome_pessoa}, {str(e)}")

        
        pass
    finally:
        driver.quit()

# Salvar o DataFrame com a coluna "Status" no arquivo copiado
data.to_excel(copy_file_path, index=False)

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

# Exibir a lista de status
for status in status_list:
    print(status)
