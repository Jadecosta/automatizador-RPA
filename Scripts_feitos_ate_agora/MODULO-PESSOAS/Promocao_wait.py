import time
import pandas as pd
import datetime
import concurrent.futures
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options
from tkinter import filedialog
from configs.config import USERNAME, PASSWORD

# Abre o arquivo para escrita
error_file = open('C:/Users/ADS_DFPG/Desktop/Projetos_Program/Automacao_projetos/Automacao-Python/Arquivos/promocao.txt', 'w')

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

        # Inicializa o driver do Edge
        edge_path = 'C:/Users/ADS_DFPG/Desktop/Projetos_Program/Automacao_projetos/Automacao-Python/msedgedriver.exe'
        edge_options = webdriver.EdgeOptions()
        edge_options.use_chromium = True
        edge_options.add_argument("--log-level=3")  # Adiciona esta linha para suprimir os logs
        edge_options.add_argument('--headless')  # Comentar ou remover esta linha para desativar o modo headless
        edge_options.add_argument('--disable-gpu')  # Desabilita a aceleração de GPU
        
        #edge_options.add_experimental_option("excludeSwitches", ["enable-logging"])  # Desabilita o DevTools listenin
        edge_service = Service(edge_path)
        driver = webdriver.Edge(service=edge_service, options=edge_options)

        wait = WebDriverWait(driver, 60)



        # Navegar até a página de login
        driver.get('https://siape.sead.pi.gov.br')
        # Espera até que o overlay desapareça
        wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.blockUI.blockOverlay")))
        driver.implicitly_wait(60)  # Espera até 30 segundos
        # Localizar os elementos de input do usuário e senha
        input_usuario = wait.until(EC.presence_of_element_located((By.ID, 'username')))
        input_senha = driver.find_element(By.ID, 'password')

        # Preencher os campos de usuário e senha
        input_usuario.send_keys(USERNAME)
        input_senha.send_keys(PASSWORD)
        input_senha.send_keys(Keys.RETURN)

        try:
            orgao = str(row['ORGAO'])
            driver.get(f'https://siape.sead.pi.gov.br/adm/{orgao}/pessoas')
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="matricula"]/div/div[3]/input')))
        except:
            print('Erro ao carregar página do órgão!')

        wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="matricula"]/div/div[3]/input'))).click()
        wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="matricula"]/div/div[3]/input'))).send_keys(str(row['MATRICULA']))
        time.sleep(2)
        wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="pesquisaNormal"]/div/div[5]/button[2]'))).click()
        time.sleep(4)
        #SERVIDOR
        wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="resultadoDaBuscaDePessoas"]/div[1]/table/tbody/tr/td[1]/a'))).click()   
        # PROMOÇOES
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="vobys-content"]/div/div/div[14]/div/div[2]/div/div[4]/a'))).click()
        
        referencia = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="historicoDoDesenvolvimentoNaCarreira"]/div[1]/table/tbody/tr[1]/td[2]'))).text
        if referencia == str(row['REFERENCIA']):
            print(f"Linha Excel: {linha_excel} {row['MATRICULA']} Promoção já lançada")
        
        else:
            # ADICIONAR                                         
            adicionar_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div[2]/form/div[1]/div/a/span[2]')))
            driver.execute_script("arguments[0].click();", adicionar_button)

            # CARREIRA
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[1]/div/button/div/div/div'))).click()
            time.sleep(2)
            carreira_input = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[1]/div/div/div[1]/input')))
            time.sleep(2)
            carreira_input.send_keys(str(row['CARREIRA']))
            time.sleep(2)
            dropdown_elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[1]/div/div/div[2]/ul/li')))
            for element in dropdown_elements:
                if element.text == str(row['CARREIRA']):
                    element.click()
                    break

            # CARGO EFETIVO
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[2]/div/button/div/div/div'))).click()
            time.sleep(2)
            cargo_efetivo_input = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[2]/div/div/div[1]/input')))
            cargo_efetivo_input.send_keys(str(row['CARGO_EFETIVO']))
            time.sleep(2)
            cargo_efetivo_input.send_keys(Keys.SPACE)
            time.sleep(2)
            dropdown_elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[2]/div/div/div[2]/ul/li')))
            for element in dropdown_elements:
                if element.text == str(row['CARGO_EFETIVO']):
                    element.click()
                    break

            # REFERENCIA
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[3]/div/button/div/div/div'))).click()
            time.sleep(2)
            referencia_input = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[3]/div/div/div[1]/input')))
            referencia_input.send_keys(str(row['REFERENCIA']))
            time.sleep(2)
            referencia_input.send_keys(Keys.SPACE)
            time.sleep(2)
            dropdown_elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[3]/div/div/div[2]/ul/li')))
            for element in dropdown_elements:
                if element.text == str(row['REFERENCIA']):
                    element.click()
                    break
            #wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[3]/div/div/div[2]/ul/li[2]/a/span[2]'))).click()


            # ESPECIALIDADE
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[4]/div/button/div/div/div'))).click()
            time.sleep(2)
            especialidade_input = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[4]/div/div/div[1]/input')))
            especialidade_input.send_keys(str(row['ESPECIALIDADE']))
            time.sleep(2)
            especialidade_input.send_keys(Keys.SPACE)
            time.sleep(2)
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[4]/div/div/div[2]/ul/li[2]/a/span[2]'))).click()
            #dropdown_elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[4]/div/div/div[2]/ul/li')))
            #for element in dropdown_elements:
            #    if element.text == str(row['ESPECIALIDADE']):
            #        element.click()
            #        break

            # INICIO VIGENCIA
            vigencia_input = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="id_10_11_18_11_15_11_14_12_16_11_14"]')))
            vigencia_input.click()
            vigencia_input.send_keys('14/08/2024')

            # OBSERVACAO
            observacao_input = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="id_10_11_18_11_15_11_14_12_16_11_22"]')))
            observacao_input.click()
            observacao_input.send_keys(str(row['OBSERVAÇÃO']))
            time.sleep(2)
            ###GRAVAR E CONFIRMAR
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-form-action-buttons"]/button'))).click()
            time.sleep(2)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-form-confirmation-save"]'))).click()
            time.sleep(2)

            success_time = datetime.datetime.now().strftime("%H:%M")
            success_message = f"Linha Excel: {linha_excel} {row['MATRICULA']} PROMOÇÃO concluída às {success_time}\n"
            print(success_message)
            error_file.write(success_message)
            error_file.flush()  # Força a gravação imediata no arquivo
    except Exception as e:
        success_time = datetime.datetime.now().strftime("%H:%M")
        error_message = f"Linha Excel: {linha_excel} {row['MATRICULA']} Erro às {success_time}: {e}\n"
        error_file.write(error_message)
        error_file.flush()  # Força a gravação imediata no arquivo
        print(error_message)
    finally:
        driver.quit()

# Inicializa a lista de resultados
resultados = []

# Cria um executor de threads com no máximo 10 workers (telas abertas)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    for index, row in data.iterrows():
        resultado = executor.submit(processar_linha, row)
        resultados.append(resultado)

    # Aguarda a conclusão de todos os resultados
    for resultado in concurrent.futures.as_completed(resultados):
        resultado.result()

# Fecha o arquivo após o término do loop
error_file.close()
