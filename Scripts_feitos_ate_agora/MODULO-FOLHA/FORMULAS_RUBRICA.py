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


error_file = open('C:/Users/ADS_DFPG/Desktop/Projetos_Program/Automacao_projetos/Automacao-Python/Arquivos/formula_de_rubricas.txt', 'w')  # Abre o arquivo para escrita

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
    
        # Esperar até que a página seja totalmente carregada 
        driver.implicitly_wait(30)  # Espera até 30 segundos 
        
        #orgao = str(row['ORGAO'])
        driver.get(f'https://siape.sead.pi.gov.br/adm/seduc/folha-funcionario/folhas/folhas')
                    
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
        time.sleep(4) 
        #rubricas
        driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div[7]/div/div[2]/div/div[6]/a').click()
        time.sleep(4) 
        '''
        driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div[1]/form/div[2]/div/div[1]/div/button/div/div/div').click()
        driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div[1]/form/div[2]/div/div[1]/div/div/div[1]/input').click()
        time.sleep(2)
        driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div[1]/form/div[2]/div/div[1]/div/div/div[1]/input').send_keys(str(row['RUBRICA']).replace('.0', '') )
        time.sleep(2)
        driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div[1]/form/div[2]/div/div[1]/div/div/div[2]/ul/li[2]/a/span[2]').click()
        time.sleep(2)

        #BUSCAR
        driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div[1]/form/div[2]/div/div[8]/button').click()  
        time.sleep(2)
        referencia =  driver.find_element((By.XPATH, '//*[@id="formulasDasRubricas"]/div[1]/table/tbody/tr[1]/td[1]')).text
        if referencia == str(row['RUBRICA']):
                print(f"Linha Excel: {linha_excel} {str(row['RUBRICA'])}  já lançada")
                time.sleep(2)   
         
        else:
        '''

        # ADICIONAR                                         
        #driver.find_element_by_css_selector('[data-original-title="Adicionar Rubrica"]')
        driver.find_element((By.XPATH, '/html/body/div[2]/div[1]/div[2]/div[2]/div/div/div/div/div[3]/div/div/div[1]/form/div[1]/div/a')).click()
        #elemento = driver.find_element(By.XPATH, '//button[contains(text(),"Adicionar")]')
        #elemento.click()
        time.sleep(2)
        # RUBRICA
        driver.find_element((By.XPATH, '//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div[1]/form/div[2]/div/div[1]/div/button/div/div/div')).click()
        time.sleep(2)
        rubrica_input =  driver.find_element((By.XPATH, '//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div[1]/form/div[2]/div/div[1]/div/div/div[1]/input'))
        time.sleep(2)
        rubrica_input.send_keys(str(row['RUBRICA']).replace('.0', '') )
        time.sleep(2)                                                           
        dropdown_elements =  driver.find_element((By.XPATH, '//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div[1]/form/div[2]/div/div[1]/div/div/div[2]/ul/li'))
        for element in dropdown_elements:
            if element.text == str(row['RUBRICA']).replace('.0', '') :
                element.click()
                break
        time.sleep(2)           
        driver.find_element(By.XPATH,'//*[@id="id_20_11_11_11_11_20_12_16_16_11_18_12_16"]').send_keys('1000')

        #GRAVAR E CONFIRMAR
        driver.find_element(By.XPATH,'//*[@id="vobys-form-action-buttons"]/button').click()
        time.sleep(4)
        driver.find_element(By.XPATH,'//*[@id="vobys-form-confirmation-save"]').click()
        time.sleep(4)

        success_time = datetime.datetime.now().strftime("%H:%M")
        success_message = f"Linha Excel: {linha_excel} {str(row['RUBRICA']).replace('.0', '') } {row['FOLHA']} lançada às {success_time}\n"
        print(success_message)
        #error_file.write(success_message)
        #error_file.flush()  # Força a gravação imediata no arquivo
    except Exception as e:
        # Salva a linha que deu erro no arquivo de texto
        success_time = datetime.datetime.now().strftime("%H:%M")
        error_message = f"Linha Excel: {linha_excel} {str(row['RUBRICA']).replace('.0', '') } {row['FOLHA']} Erro às {success_time}\n"
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
