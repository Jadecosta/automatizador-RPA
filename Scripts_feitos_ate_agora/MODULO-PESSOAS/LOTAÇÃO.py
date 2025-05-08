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
copy_file_path = f"{directory}/{original_filename_no_extension}_log.xlsx"
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

            # Preencher os campos de usuário e senha
            input_usuario.send_keys(USERNAME)
            input_senha.send_keys(PASSWORD)

            input_senha.send_keys(Keys.RETURN)  # Enviar o formulário de login
            
            orgao = str(row['ORGAO'])
            driver.get(f'https://siape.sead.pi.gov.br/adm/{orgao}/pessoas')

        except:
            orgao = str(row['ORGAO'])
            driver.get(f'https://siape.sead.pi.gov.br/adm/{orgao}/pessoas')
                    
        # Esperar até que a página seja totalmente carregada 
        driver.implicitly_wait(30)  # Espera até 30 segundos  

        #MATRICULA
        driver.find_element(By.XPATH,'//*[@id="matricula"]/div/div[3]/input').click()
        driver.find_element(By.XPATH,'//*[@id="matricula"]/div/div[3]/input').send_keys(str(row['MATRICULA']))
        time.sleep(4)
    
        #BUSCAR                         
        driver.find_element(By.XPATH,'//*[@id="pesquisaNormal"]/div/div[6]/button').click() 
        time.sleep(4) 

        #SELECIONAR SERVIDOR
        driver.find_element(By.XPATH,'//*[@id="resultadoDaBuscaDePessoas"]/div[1]/table/tbody/tr[1]/td[1]/a').click()  
        time.sleep(4)
            
        #LOTACAO
        driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div[18]/div/div[2]/div/div[1]/a').click()   
        time.sleep(4)
        
        #adicionar lotação
        driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div[2]/form/div[1]/div/a/span[2]').click()
        time.sleep(4)

        #data
        driver.find_element(By.XPATH,'//*[@id="id_10_11_18_11_15_15_11_12_14_11_11"]').send_keys(('21/06/2024'))
        time.sleep(2)
        

        driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[3]/div/button/div').click()
        time.sleep(1)
        driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[3]/div/div/div[1]/input').click()
        time.sleep(1)
        driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[3]/div/div/div[1]/input').send_keys(str(row['CODIGO']))
        time.sleep(4)
        driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[3]/div/div/div[2]/ul/li[2]/a/span[2]').click()
        time.sleep(1)
        '''
        #ALTERAL LOTACAO                                  
        driver.find_element(By.XPATH,'//*[@id="lotacao"]/div[1]/table/tbody/tr/td[1]/a').click()
        time.sleep(4) 
        driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/nav/div[1]/a/span[2]').click()
        time.sleep(4)

        #ALTERANDO LOTAÇÃO
        driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[3]/div/button/div/div/div').click()
        driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[3]/div/div/div[1]/input').click()
        # Converta o valor numérico para uma string antes de inserir no campo
        codigo_folha = str(int(row['CODIGO FOLHA']))

        # Insira o valor no campo de entrada
        campo_input = driver.find_element(By.XPATH, '//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[3]/div/div/div[1]/input')
        campo_input.click()
        campo_input.clear()  # Limpa o campo se houver algum valor prévio
        time.sleep(1)
        campo_input.send_keys(codigo_folha)
        time.sleep(4)

        driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[3]/div/div/div[2]/ul/li[2]/a/span[2]').click()
        time.sleep(1)
        '''
        #GRAVAR E CONFIRMAR
        driver.find_element(By.XPATH,'//*[@id="vobys-form-action-buttons"]/button').click()
        time.sleep(4)
        driver.find_element(By.XPATH,'//*[@id="vobys-form-confirmation-save"]').click()
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



# Adicione a coluna de status ao DataFrame da cópia
data['Status'] = status_list

# Salve a cópia atualizada com a coluna de status
data.to_excel(copy_file_path, index=False)
