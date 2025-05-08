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

error_file = open('C:/Users/ADS_DFPG/Desktop/Projetos_Program/Automacao_projetos/Automacao-Python/Arquivos/alterarmatricula.txt', 'w')  # Abre o arquivo para escrita

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
    error_file.write(f"Erro ao ler o arquivo Excel: {e}\n")
    error_file.close()
    exit()

print("CARREGANDO..")

def processar_linha(row):
    
    try:
        linha_excel = row.name + 2
        nome_pessoa = row['MATRICULA DESLIGADO']
        try:
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
        time.sleep(2)
        driver.find_element(By.XPATH,'//*[@id="matricula"]/div/div[3]/input').send_keys(str(row['MATRICULA NOVA']))
        time.sleep(2)
        #BUSCAR
        driver.find_element(By.XPATH,'//*[@id="pesquisaNormal"]/div/div[5]/button[2]').click()
        time.sleep(5)
        #SERVIDOR
        driver.find_element(By.XPATH,'//*[@id="resultadoDaBuscaDePessoas"]/div[1]/table/tbody/tr[1]/td[1]/a').click()
        
        # Esperar até que a página seja totalmente carregada 
        driver.implicitly_wait(30)  # Espera até 30 segundos
       
        #VINCULO
        driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div[7]/div/div[2]/div/div[1]/a').click()
        time.sleep(4)

        # Valor da matrícula que estamos procurando
        matricula_procurada = str(row['MATRICULA NOVA'])

        # Localiza a tabela
        tabela = driver.find_element(By.XPATH, '//*[@id="vinculoInstitucional"]/div[1]/table/tbody')

        # Itera sobre as linhas da tabela
        linhas = tabela.find_elements(By.TAG_NAME, "tr")
        for linha in linhas:
            colunas = linha.find_elements(By.TAG_NAME, "td")
            if colunas:
                matricula = colunas[2].text  # Supondo que a coluna "Matrícula" seja a terceira
                if matricula == matricula_procurada:
                    # Clica na célula da coluna "Vínculo" correspondente (primeira coluna)
                    colunas[0].find_element(By.TAG_NAME, "a").click()
                    break

        # Espera para ver o resultado antes de fechar
        time.sleep(4)
        #QUADRO DE PESSOA
        #driver.find_element(By.XPATH,'//*[@id="vinculoInstitucional"]/div[1]/table/tbody/tr/td[1]/a').click()
        #time.sleep(4)
        #ALTERAR
        driver.find_element(By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/nav/div/a/span[2]').click()
        time.sleep(2)
        #agencia
        driver.find_element(By.XPATH,'//*[@id="id_10_11_18_11_12_15_11_12_17_12_12"]').click()
        driver.find_element(By.XPATH,'//*[@id="id_10_11_18_11_12_15_11_12_17_12_12"]').clear()
        driver.find_element(By.XPATH,'//*[@id="id_10_11_18_11_12_15_11_12_17_12_12"]').send_keys(str(row['MATRICULA DESLIGADO']))
        time.sleep(2)
        
        #GRAVAR E CONFIRMAR
        driver.find_element(By.XPATH,'//*[@id="vobys-form-action-buttons"]/button').click()
        time.sleep(4)
        driver.find_element(By.XPATH,'//*[@id="vobys-form-confirmation-save"]').click()
        time.sleep(4) 

       
      
        success_time = datetime.datetime.now().strftime("%H:%M")
        success_message = f"Linha Excel: {linha_excel} {row['MATRICULA DESLIGADO']} ALTERADA às {success_time}\n"
        print(success_message)
        error_file.write(success_message)
        error_file.flush()  # Força a gravação imediata no arquivo
    except Exception as e:
        # Salva a linha que deu erro no arquivo de texto
        success_time = datetime.datetime.now().strftime("%H:%M")
        error_message = f"Linha Excel: {linha_excel} {row['MATRICULA DESLIGADO']} Erro às {success_time}\n"
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