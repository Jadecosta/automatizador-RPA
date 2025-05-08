import pandas as pd
import datetime
import concurrent.futures
from datetime import datetime
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from tkinter import filedialog
import shutil
from configs.config import USERNAME, PASSWORD
import psutil
import requests

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

        
        
        # Inicializa o driver do Edge
        edge_path = 'C:/Users/ADS_DFPG/Desktop/Projetos_Program/Automacao_projetos/Automacao-Python/msedgedriver.exe'
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
        wait = WebDriverWait(driver, 60)

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
        
        #driver.get('https://siape.sead.pi.gov.br/adm/sesapi/folha-funcionario/folhas/folhas/folha-de-pagamento/1004260/funcionarios/pagamento')

        
        orgao = str(row['ORGAO'])
        driver.get(f'https://siape.sead.pi.gov.br/adm/{orgao}/folha-funcionario/folhas/folhas')

        # Localizar folha
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[2]/div/div[1]/input[2]'))).click()
        driver.find_element(By.XPATH, '//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[2]/div/div[1]/input[2]').send_keys(str(row['FOLHA']))
        time.sleep(1)
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[2]/div/div[10]/button'))).click()
        time.sleep(2)
        # Selecionar folha
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="folhaFuncionario"]/div[1]/table/tbody/tr[1]/td[1]/a'))).click()
        time.sleep(2)
        # Pagamento
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="vobys-content"]/div/div/div[5]/div/div[2]/div/div[1]/a'))).click()
        
        # Matrícula
        matricula_input = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[2]/div/div[1]/input[2]')))
        matricula_input.click()
        matricula_input.send_keys(str(row['MATRICULA']))

        # Clicar no botão para prosseguir
        submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[2]/div/div[12]/button')))
        submit_button.click()
        time.sleep(4)
        # Aguardar o carregamento da tabela de funcionários e clicar no primeiro link de pagamento
        pagamento_link = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="funcionarios"]/div[1]/table/tbody/tr[1]/td[1]/a')))
        pagamento_link.click()

        # Rubricas Permanentes
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="vobys-content"]/div/div/div/div[2]/div/a[16]'))).click()

        while True:
            try:
                rubrica = row['RUBRICA']
                element = driver.find_element(By.XPATH, f'//*[@id="vobys-content"]/div/div/div/div[3]/div/div//*[text()="{rubrica}"]')
                element.click()

                # Excluir
                wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="vobys-content"]/div/div/div/div[3]/div/div/nav/div[2]/a/span[2]'))).click()

                # Exclusão
                wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[10]/div/div/button/div/div/div'))).click()
                time.sleep(1)

                motivo = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Buscar..."]')))
                motivo.click()
                time.sleep(2)

                motivo.send_keys(Keys.SPACE)
                time.sleep(1)

                opcao = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[5]/div/div[2]/ul/li[2]/a')))
                opcao.click()
                time.sleep(1)

                # Gravar e Confirmar
                wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="vobys-form-action-buttons"]/button'))).click()
                wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="vobys-form-confirmation-save"]'))).click()
                time.sleep(4)
            except:
                break

        try:
            # Calcular
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="vobys-content"]/div/div/div/div[2]/div/a[2]'))).click()

            # Gerar eventos/Rubricas/Cálculos
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="vobys-content"]/div/div/div/div[3]/div/div[1]/div/div[2]/div[6]/a'))).click()
            time.sleep(2)
        except:
            msg_erro = 'Não calculado!'
            print(msg_erro)

        success_time = datetime.now().strftime("%H:%M")
        status = f"EXECUTADO às {success_time}"
        data.at[row.name, "Status"] = status
        status_list.append(status)
        print(f"EXECUTADO {linha_excel}: {success_time} {nome_pessoa}")
    except Exception as e:
        success_time = datetime.now().strftime("%H:%M")
        status = f"ERRO: {success_time}, {nome_pessoa}, {str(e)}"
        data.at[row.name, "Status"] = status
        status_list.append(status)
        print(f"ERRO na linha {linha_excel}: {success_time}, {nome_pessoa}, {str(e)}")
    finally:
        driver.quit()


# Inicializa a lista de resultados
resultados = []

# Cria um executor de threads com número de workers baseado nos recursos do sistema
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    for index, row in data.iterrows():
        resultado = executor.submit(processar_linha, row)
        resultados.append(resultado)

    # Aguarda a conclusão de todos os resultados
    for resultado in concurrent.futures.as_completed(resultados):
        resultado.result()

# Salvar o DataFrame com a coluna "Status" no arquivo copiado
data.to_excel(copy_file_path, index=False)

# Exibir a lista de status
for status in status_list:
    print(status)