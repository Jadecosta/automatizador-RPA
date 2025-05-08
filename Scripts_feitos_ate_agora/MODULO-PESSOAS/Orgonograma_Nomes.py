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
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

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
        cod = row['Código']
        nome = row['Nome']
      
        # Inicializa o driver do Edge
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        #chrome_options.add_argument("--headless")  # Descomente esta linha para execução sem interface gráfica
        
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
        wait = WebDriverWait(driver, 60)


        # Navegar até a página de login
        driver.get('https://siape.sead.pi.gov.br')


        # Localizar os elementos de input do usuário e senha
        wait.until(EC.presence_of_element_located((By.ID, "username"))).send_keys(USERNAME)
        driver.find_element(By.ID, "password").send_keys(PASSWORD)
        driver.find_element(By.ID, "password").send_keys(Keys.RETURN)


        orgao = str(row['ORGAO'])
        driver.get(f'https://siape.ati.pi.gov.br/adm/{orgao}/tabelas-basicas/lotacao-centro-custo/lotacoes')

        # Esperar até que a página seja totalmente carregada 
        driver.implicitly_wait(30)  # Espera até 30 segundos
    
              
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div[1]/form/div[2]/div/div[1]/input[2]'))).send_keys(cod)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div[1]/form/div[2]/div/div[11]/button'))).click()

        # Clicar no link encontrado
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="lotacoes"]/div[1]/table/tbody/tr/td[1]/a'))).click()

        # Limpar e preencher o nome
        campo_input_nome = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="id_7_11_21_12_11_28_11_12"]')))
        campo_input_nome.clear()
        campo_input_nome.send_keys(f"{cod}-{nome}")

        # Gravar e confirmar
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="vobys-form-action-buttons"]/button'))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="vobys-form-confirmation-save"]'))).click()

        
        success_time = datetime.datetime.now().strftime("%H:%M")
        status = f"EXECUTADO às {success_time}"
        data.at[row.name, "Status"] = status
        status_list.append(status)
        print(f" EXECUTADO {linha_excel}: {success_time} {cod}")        

    except Exception as e:
        success_time = datetime.datetime.now().strftime("%H:%M")
         # Atualizar a coluna "Status" com a informação de erro
        status = f"ERRO: {success_time}, {row['MATRICULA']}, {str(e)}"
        data.at[row.name, "Status"] = status
        status_list.append(status)
        print(f"ERRO na linha {linha_excel}: {success_time}, {cod}, {str(e)}")

        
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
