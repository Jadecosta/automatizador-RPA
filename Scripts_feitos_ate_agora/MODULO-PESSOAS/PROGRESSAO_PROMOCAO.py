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


error_file = open('C:/Users/ADS_DFPG/Desktop/Automacao-Python/Arquivos/promocao.txt', 'w')  # Abre o arquivo para escrita

# Leitura do arquivo Excel
# Usar o diálogo de seleção de arquivo do tkinter para obter o caminho do arquivo original
file_path = filedialog.askopenfilename(title="Selecione o arquivo Excel", filetypes=[("Excel files", "*.xlsx")])
# Verificar se o usuário selecionou um arquivo
if not file_path:
    print("Nenhum arquivo selecionado. Encerrando o programa.")
    exit()
# Leitura do arquivo Excel
try:
    data = pd.read_excel(file_path)  
except Exception as e:
    print(f"Erro ao ler o arquivo Excel: {e}")
    error_file.write(f"Erro ao ler o arquivo Excel: {e}\n")
    error_file.close()
    exit()

print("CARREGANDO..")

def processar_linha(row):

    try:
        linha_excel = row.name + 2
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
            
            # Esperar até que a página seja totalmente carregada 
            driver.implicitly_wait(30)  # Espera até 30 segundos                       

        except:
            print('Erro de credenciais!')
        
        try:
            orgao = str(row['ORGAO'])
            driver.get(f'https://siape.sead.pi.gov.br/adm/{orgao}/pessoas')
       
            # Esperar até que a página seja totalmente carregada 
            driver.implicitly_wait(30)  # Espera até 30 segundos       
        except:
            print('Erro ao carregar página do órgão!')


        # Matricula
        driver.find_element(By.XPATH,'//*[@id="matricula"]/div/div[3]/input').send_keys(str(row['MATRICULA']))
        time.sleep(4)
        driver.find_element(By.XPATH,'//*[@id="pesquisaNormal"]/div/div[6]/button').click()
        time.sleep(4)
        
        #SERVIDOR
        servidor = driver.find_element(By.XPATH,'//*[@id="resultadoDaBuscaDePessoas"]/div[1]/table/tbody/tr/td[1]/a')
        servidor.click()
        time.sleep(4)
        
        #PROMOÇOES
        promocao = driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div[14]/div/div[2]/div/div[4]/a')
        promocao.click()
        time.sleep(4)
        
        #ADICIONAR
        adicionar = driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div[2]/form/div[1]/div/a/span[2]')
        adicionar.click()
        time.sleep(4)
        
        #CARREIRA################################################################################
        driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[1]/div/button/div/div/div').click()
        time.sleep(2)
        driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[1]/div/div/div[1]/input').send_keys(str(row['CARREIRA']))
        time.sleep(2)
        driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[1]/div/div/div[2]/ul/li[2]/a/span[2]').click()
        time.sleep(2)
        
        
        #CARGO EFETIVO
       
        driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[2]/div/button/div/div/div').click()
        time.sleep(2)
        driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[2]/div/div/div[1]/input').send_keys(str(row['CARGO_EFETIVO']))
        time.sleep(2)
        dropdown_elements = driver.find_elements(By.XPATH, '//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[2]/div/div/div[2]/ul/li')
        for element in dropdown_elements:
            if element.text == str(row['CARGO_EFETIVO']):
                element.click()
                break
        #driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[2]/div/div/div[2]/ul/li[2]/a').click()
        '''
        # Clica no botão para abrir as opções
        driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[2]/div/button/div/div/div').click()
        time.sleep(2)
        driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[2]/div/div/div[1]/input').send_keys(str(row['CARGO_EFETIVO']))
        time.sleep(2)
        # Localiza todos os elementos da lista de opções
        options = driver.find_elements(By.XPATH, '//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[2]/div/div/div[2]/ul/li/a')

        # Itera sobre os elementos e clica no texto correspondente
        for option in options:
            if option.text == "CARGO EFETIVO":  # Substitua "CARGO EFETIVO" pelo texto que deseja clicar
                option.click()
                break  # Termina o loop depois de clicar no texto correspondente
         '''
        #REFERENCIA
        driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[3]/div/button/div/div/div').click()
        time.sleep(2)
        driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[3]/div/div/div[1]/input').send_keys(str(row['REFERENCIA']))
        time.sleep(2)
        dropdown_elements = driver.find_elements(By.XPATH, '//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[3]/div/div/div[2]/ul/li')
        for element in dropdown_elements:
            if element.text == str(row['REFERENCIA']):
                element.click()
                break
        #driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[3]/div/div/div[2]/ul/li[2]/a/span[2]').click()
    
        #ESPECIALIDADE
        driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[4]/div/button/div/div/div').click()
        time.sleep(2)
        driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[4]/div/div/div[1]/input').send_keys(str(row['ESPECIALIDADE']))
        time.sleep(2)
        driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[4]/div/div/div[2]/ul/li[2]/a/span[2]').click()

        #INICIO VIGENCIA
        driver.find_element(By.XPATH,'//*[@id="id_10_11_18_11_15_11_14_12_16_11_14"]').click()
        time.sleep(2)
        driver.find_element(By.XPATH,'//*[@id="id_10_11_18_11_15_11_14_12_16_11_14"]').send_keys(str('01/08/2024'))

        #OBSERVACAO
        driver.find_element(By.XPATH,'//*[@id="id_10_11_18_11_15_11_14_12_16_11_22"]').click()
        time.sleep(2)
        driver.find_element(By.XPATH,'//*[@id="id_10_11_18_11_15_11_14_12_16_11_22"]').send_keys(str(row['OBSERVAÇÃO']))
        time.sleep(2)

        ###GRAVAR E CONFIRMAR
        #driver.find_element(By.XPATH,'//*[@id="vobys-form-action-buttons"]/button').click()
        #time.sleep(4)
        #driver.find_element(By.XPATH,'//*[@id="vobys-form-confirmation-save"]').click()
        #time.sleep(4)



        success_time = datetime.datetime.now().strftime("%H:%M")
        success_message = f"Linha Excel: {linha_excel} {row['MATRICULA']} PROMOÇÃO concluída às {success_time}\n"
        print(success_message)
        error_file.write(success_message)
        error_file.flush()  # Força a gravação imediata no arquivo
    except Exception as e:
        # Salva a linha que deu erro no arquivo de texto
        success_time = datetime.datetime.now().strftime("%H:%M")
        error_message = f"Linha Excel: {linha_excel} {row['MATRICULA']} Erro às {success_time}\n"
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