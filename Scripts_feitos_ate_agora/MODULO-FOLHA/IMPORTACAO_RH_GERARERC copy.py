import pandas as pd
import time
import os
import datetime
import concurrent.futures
import shutil  # Biblioteca para copiar arquivos
from tkinter import filedialog
import pygetwindow as gw
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from configs.config import USERNAME, PASSWORD

error_file = open('C:/Users/ADS_DFPG/Desktop/Projetos_Program/Automacao_projetos/Automacao-Python/Arquivos/importarcalcular.txt', 'w')  # Abre o arquivo para escrita

# Leitura do arquivo Excel
file_path = filedialog.askopenfilename(title="Selecione o arquivo Excel", filetypes=[("Excel files", "*.xlsx")])

if not file_path:
    print("Nenhum arquivo selecionado. Encerrando o programa.")
    exit()

try:
    data = pd.read_excel(file_path)  
except Exception as e:
    print(f"Erro ao ler o arquivo Excel: {e}")
    error_file.write(f"Erro ao ler o arquivo Excel: {e}\n")
    error_file.close()
    exit()

print("CARREGANDO..")

def processar_linha(row, quadrante):
    try:
        linha_excel = row.name + 2

        # Inicializa o driver do Chrome
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
        wait = WebDriverWait(driver, 60)

        # Navegar até a página de login
        driver.get('https://siape.sead.pi.gov.br')

        # Localizar os elementos de input do usuário e senha
        wait.until(EC.presence_of_element_located((By.ID, "username"))).send_keys(USERNAME)
        driver.find_element(By.ID, "password").send_keys(PASSWORD)
        driver.find_element(By.ID, "password").send_keys(Keys.RETURN)

        driver.get('https://siape.sead.pi.gov.br/adm/seduc/folha-funcionario/folhas/folhas')

        # Esperar até que a página seja totalmente carregada 
        driver.implicitly_wait(60)  

        # LOCALIZAR FOLHA
        wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[2]/div/div[1]/input[2]'))).send_keys(str(row['FOLHA']))
        time.sleep(2) 
        # BUSCAR                         
        wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[2]/div/div[10]/button'))).click() 
        time.sleep(2) 

        # SELECIONAR FOLHA
        wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="folhaFuncionario"]/div[1]/table/tbody/tr[1]/td[1]/a'))).click()  

        # PAGAMENTO
        wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div[5]/div/div[2]/div/div[1]/a'))).click()

        # MATRÍCULA                                      
        wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[2]/div/div[1]/input[2]'))).send_keys(str(row['MATRICULA']))
        time.sleep(1) 

        # BUSCAR  
        wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[2]/div/div[12]/button'))).click() 
        time.sleep(4) 

        # Pagamento Servidor
        wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="funcionarios"]/div[1]/table/tbody/tr[1]/td[1]/a'))).click()
        time.sleep(4)         
        # Calcular
        wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[2]/div/a[2]'))).click()  
        time.sleep(4) 

        # Gerar eventos/Rubricas/Calculos
        wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div[1]/div/div[2]/div[6]/a'))).click()  
        time.sleep(4) 

        # Manipula a janela do navegador para posicioná-la em um dos quadrantes
        window = gw.getWindowsWithTitle(driver.title)[0]  # Obtenha a janela do navegador
        screen_width, screen_height = window.width, window.height

        # Define as posições dos quadrantes
        positions = [
            (0, 0),  # Quadrante superior esquerdo
            (screen_width // 2, 0),  # Quadrante superior direito
            (0, screen_height // 2),  # Quadrante inferior esquerdo
            (screen_width // 2, screen_height // 2)  # Quadrante inferior direito
        ]

        window.moveTo(*positions[quadrante])
        window.resizeTo(screen_width // 2, screen_height // 2)

        success_time = datetime.datetime.now().strftime("%H:%M")
        success_message = f"Linha Excel: {linha_excel} {row['MATRICULA']} Execução concluída às {success_time}\n"
        print(success_message)

    except Exception as e:
        success_time = datetime.datetime.now().strftime("%H:%M")
        error_message = f"Linha Excel: {linha_excel} {row['MATRICULA']} Erro - Execução concluída às {success_time}\n"
        error_file.write(error_message)
        error_file.flush()  
        print(error_message)
    finally:
        driver.quit()

# Inicializa a lista de resultados
resultados = []

# Cria um executor de threads com no máximo 4 workers (janelas abertas)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    for index, row in data.iterrows():
        quadrante = index % 4  # Distribui as janelas entre os 4 quadrantes
        resultado = executor.submit(processar_linha, row, quadrante)
        resultados.append(resultado)

    # Aguarda a conclusão de todos os resultados
    for resultado in concurrent.futures.as_completed(resultados):
        resultado.result()

# Fecha o arquivo após o término do loop
error_file.close()
