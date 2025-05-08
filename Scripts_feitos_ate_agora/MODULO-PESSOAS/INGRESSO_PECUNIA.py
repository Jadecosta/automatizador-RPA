import pandas as pd
import time
import os
import datetime
import concurrent.futures
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from tkinter import filedialog, simpledialog
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from configs.config import USERNAME, PASSWORD
from selenium.webdriver.support.ui import WebDriverWait


# Usar o diálogo de seleção de arquivo do tkinter para obter o caminho do arquivo original
file_path = filedialog.askopenfilename(title="Selecione o arquivo Excel", filetypes=[("Excel files", "*.xlsx")])

# Verificar se o usuário selecionou um arquivo
if not file_path:
    print("Nenhum arquivo selecionado. Encerrando o programa.")
    exit()

# Obter o nome do arquivo e o diretório do arquivo de origem
file_name = os.path.basename(file_path)
file_directory = os.path.dirname(file_path)

# Caminho para o arquivo de log de erro no mesmo diretório do arquivo de origem
log_file_path = os.path.join(file_directory, f"{os.path.splitext(file_name)[0]}_log.txt")

try:
    data = pd.read_excel(file_path)  
except Exception as e:
    print(f"Erro ao ler o arquivo Excel: {e}")
    log_file_path.write(f"Erro ao ler o arquivo Excel: {e}/n")
    log_file_path.close()
    exit()

# Solicitar login e senha usando a caixa de diálogo do tkinter
#USERNAME = simpledialog.askstring("Login", "Digite seu usuário:")
#PASSWORD = simpledialog.askstring("Senha", "Digite sua senha:", show='*')  # O 'show'='*' esconde a senha


print("CARREGANDO..")

def processar_linha(row):
    
    try:
        linha_excel = row.name + 2

        try:
            # Inicializa o driver do Edge
            edge_path = 'C:/Github/App_Program/msedgedriver.exe'
            edge_options = webdriver.EdgeOptions()
            edge_options.use_chromium = True

            # Configurações para ignorar certificados inseguros
            edge_options.add_argument('--ignore-certificate-errors')
            edge_options.add_argument('--ignore-ssl-errors')
            edge_options.add_argument('--disable-web-security')
            
            # Exibe o navegador visualmente
            #edge_options.add_argument('--headless')  # Comentar ou remover esta linha para desativar o modo headless
            edge_options.add_argument('--disable-gpu')  # Desabilita a aceleração de GPU

            edge_service = Service(edge_path)
            driver = webdriver.Edge(service=edge_service, options=edge_options)

            wait = WebDriverWait(driver, 30)

            # Navegar até a página de login
            driver.get('https://siape.sead.pi.gov.br')
            driver.implicitly_wait(30)
            input_usuario = wait.until(EC.presence_of_element_located((By.ID, 'username')))
            input_senha = driver.find_element(By.ID, 'password')

            # Preencher os campos de usuário e senha
            input_usuario.send_keys(USERNAME)
            input_senha.send_keys(PASSWORD)
            input_senha.send_keys(Keys.RETURN)
            
            driver.implicitly_wait(30)  # Espera até 30 segundos

            driver.get('https://siape.sead.pi.gov.br/org/sead/empresa/empresa/selecionar-empresa/')

        except:
            driver.get('https://siape.sead.pi.gov.br/org/sead/empresa/empresa/selecionar-empresa/')

            # Esperar até que a página seja totalmente carregada 
            driver.implicitly_wait(30)  # Espera até 30 segundos
        
        try:
            #BUSCAR PELA FOLHA DIVERSOS 
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div[1]/form/div[2]/div/div[3]/input[2]'))).send_keys("diversos")
            time.sleep(2)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div[1]/form/div[2]/div/div[4]/button'))).click()
            time.sleep(4)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="selecaoDaEmpresa"]/div[1]/table/tbody/tr/td[1]/a'))).click()
            time.sleep(4)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="modules-list"]/li[1]/a/div'))).click()
            time.sleep(4)

            #ADICIONAR
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="buscarFormularioFiltro"]/div[1]/div/a/span[2]'))).click()
            time.sleep(4)
        
        except Exception:
            #CPF
            CPF_INPUT = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_10_11_18_11_12_11_11_22_11_assistente_existente"]/div[1]/div/button/div/div/div')))
            CPF_INPUT.send_keys(str(row['CPF']))
            time.sleep(10)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_10_11_18_11_12_11_11_22_11_assistente_existente"]/div[1]/div/div/div[2]/ul/li[2]/a/span[2]'))).click()
            time.sleep(4)

            #GRAVAR E CONFIRMAR
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-form-action-buttons"]/button'))).click()
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-form-confirmation-save"]'))).click()

            #VÍNCULO
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div/div[2]/div/div/button/div/div/div'))).click()
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div/div[2]/div/div/div/div[1]/input'))).send_keys('Quadro de Pessoa')
            time.sleep(4)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div/div[2]/div/div/div/div[2]/ul/li[2]/a/span[2]'))).click()
            time.sleep(4)

            #PROXIMO
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-form-action-buttons"]/button'))).click()
            time.sleep(6)

            #OBSERVAÇÃO
            OBSERVACAO_INPUT = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_10_11_18_11_15_11_11_11_11"]')))
            OBSERVACAO_INPUT.send_keys(str(row['OBSERVAÇÃO']))
            time.sleep(4)
            
            #MATRICULA
            MATRICULA_INPUT = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_10_11_18_11_15_11_11_11_12"]')))
            MATRICULA_INPUT.send_keys(str(row['MATRICULA']))
            time.sleep(4)

            #DATA NOMEAÇÃO/POSSE/EXECUÇÃO 
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_10_11_18_11_15_11_11_12_12"]'))).send_keys(str(row['DATA_NOMEAÇÃO']))
            time.sleep(2)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_10_11_18_11_15_11_11_12_13"]'))).send_keys(str(row['DATA_POSSE']))
            time.sleep(2)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_10_11_18_11_15_11_11_12_14"]'))).send_keys(str(row['DATA_EXECUÇÃO']))
            time.sleep(2)

            #ESPECIALIDADE
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_10_11_18_11_15_11_11_13_23"]'))).click()
            time.sleep(2)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[5]/div[2]/div[2]/div/div/div[1]/input'))).send_keys('1 - APOSENTADO')
            time.sleep(4)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[3]/div[2]/div[8]/div/button/div/div/div'))).click()
            time.sleep(2)

            #SERVIDOR
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[5]/div[2]/div[2]/div/button/div/div/div'))).click()
            time.sleep(2)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_10_11_18_11_15_11_11_13_23"]/option[3]'))).send_keys('NÃO')
            time.sleep(4)

            #REGIME
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[5]/div[2]/div[2]/div/button/div/div/div//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[5]/div[2]/div[1]/div/button/div'))).click()
            time.sleep(2)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[5]/div[2]/div[1]/div/div/div[2]/ul/li[4]/a/span[2]'))).send_keys('Estatutário Efetivo')
            time.sleep(4)

            #REMUNERAÇAO
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[5]/div[2]/div[2]/div/div'))).click()
            time.sleep(2)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[5]/div[2]/div[2]/div/div/div[2]/ul/li[2]/a/span[2]'))).send_keys('Remunerado')
            time.sleep(4)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[5]/div[2]/div[2]/div/div/div[2]/ul/li[2]/a/span[2]'))).click()
            time.sleep(2)

            #DIVIÃO
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[5]/div[2]/div[3]/div/button/div'))).click()
            time.sleep(2)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[5]/div[2]/div[3]/div/div/div[2]/ul/li[2]/a/span[2]'))).send_keys('Servidor')
            time.sleep(4)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[5]/div[2]/div[3]/div/div/div[2]/ul/li[2]/a'))).click()
            time.sleep(2) 

            #CATEGORIA
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[5]/div[2]/div[4]/div/button/div'))).click()
            time.sleep(2)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[5]/div[2]/div[4]/div/button/div/div/div'))).send_keys('301 – Servidor Público Titular de Cargo Efetivo, Magistrado, Ministro de Tribunal de Contas, Conselheiro de Tribunal de Contas e Membro do Ministério Público ')
            time.sleep(4)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[5]/div[2]/div[3]/div/div/div[2]/ul/li[2]/a'))).click()
            time.sleep(2)

            #DIVISÃO
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[5]/div[2]/div[5]/div/div/div[1]/input'))).click()
            time.sleep(2)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[5]/div[2]/div[5]/div/button/div/div/div'))).send_keys('Credito Pecuniario Aposentado')
            time.sleep(4)

            #TIPO DE SERVIDOR 
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[5]/div[2]/div[6]/div/button/div'))).click()
            time.sleep(2)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[5]/div[2]/div[6]/div/button/div/div/div'))).send_keys('Aposentado')
            time.sleep(4)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[5]/div[2]/div[6]/div/div/div[2]/ul/li[2]/a'))).click()
            time.sleep(2)

            #CLASSE DE INCIDENTE
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[5]/div[2]/div[7]/div/button/div'))).click()
            time.sleep(2)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[5]/div[2]/div[7]/div/button/div/div/div'))).send_keys('IR')
            time.sleep(4)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[5]/div[2]/div[7]/div/div/div[2]/ul/li[4]/a'))).click()
            time.sleep(2)

            #LOCAL
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[7]/div[2]/div[1]/div/button/div'))).click()
            time.sleep(2)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[7]/div[2]/div[1]/div/button/div/div/div'))).send_keys('SEM CORRESPONDENTE')
            time.sleep(4)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[7]/div[2]/div[1]/div/div/div[2]/ul/li[2]/a/span[2]'))).click()
            time.sleep(2)

            #JORNADA
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_10_11_18_11_15_11_11_16_15"]'))).click()
            time.sleep(2)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_10_11_18_11_15_11_11_16_15"]'))).send_keys('0')
            time.sleep(4)

            #GRAVAR E CONFIRMAR
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-form-action-buttons"]/button'))).click()
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-form-confirmation-save"]'))).click()

        try:
            driver.get('https://siape.sead.pi.gov.br/adm/reenvio/folha-funcionario/folhas/folhas')

        except Exception:
            #FOLHA
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="folhaFuncionario"]/div[1]/table/tbody/tr[1]/td[1]/a'))).click()
            time.sleep(4)

            #PAGAMENTO
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div[5]/div/div[2]/div/div[1]/a'))).click()
            time.sleep(4)

            #ADICIONAR
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div[1]/form/div[1]/div/a/span[2]'))).click()
            time.sleep(4)

            #MATRICULA
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div/div/button/div'))).click()
            time.sleep(2)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div/div/button/div'))).send_keys(str(row['MATRICULA']))
            time.sleep(4)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div/div/div/div[2]/ul/li[2]/a/span[2]'))).click()
            time.sleep(2)

            #GRAVAR E CONFIRMAR
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-form-action-buttons"]/button'))).click()
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-form-confirmation-save"]'))).click()


        #RUBRICA DIGITADA
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[2]/div/a[17]'))).click()
            time.sleep(2)

            # ADICIONAR 
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div[1]/form/div[1]/div/a/span[2]'))).click()
            time.sleep(2)

            #RUBRICA
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[1]/div/button/div'))).click()
            time.sleep(2)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[1]/div/div/div[2]/ul/li[2]/a/span[2]'))).send_keys(str(row['RUBRICA']))
            time.sleep(4)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[1]/div/div/div[2]/ul/li[2]/a/span[2]'))).click()
            time.sleep(2)

            #PARÂMENTRO 
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_20_11_11_11_11_20_12_14_11_11_18_26_12_21_13_20"]'))).click()
            time.sleep(2)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_20_11_11_11_11_20_12_14_11_11_18_26_12_21_13_20"]/option[3]'))).send_keys('Valor Informado')
            time.sleep(4)

            #VALOR
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_20_11_11_11_11_20_12_14_11_11_18_26_12_21_13_21"]'))).click()
            time.sleep(2)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_20_11_11_11_11_20_12_14_11_11_18_26_12_21_13_21"]'))).send_keys(str(row['VALOR']))
            time.sleep(4)
                
            #SUBSTITUIÇÃO
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_20_11_11_11_11_20_12_14_11_11_18_26_12_21_13_38"]'))).click()
            time.sleep(2)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id_20_11_11_11_11_20_12_14_11_11_18_26_12_21_13_38"]/option[3]'))).send_keys('Não')
            time.sleep(4)

            #GRAVAR E CONFIRMAR
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-form-action-buttons"]/button'))).click()
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-form-confirmation-save"]'))).click()
            
            #CALCULAR
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[2]/div/a[2]'))).click()
            time.sleep(2)

            #IMPORTA DADOS RH
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div[1]/div/div[2]/div[1]/a'))).click()
            time.sleep(2)

            #GERAR EVENTOS, RUBRICA E CALCULAR
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vobys-content"]/div/div/div/div[3]/div/div[1]/div/div[2]/div[6]/a'))).click()
            time.sleep(2)


    except Exception as e:
        # Salva a linha que deu erro no arquivo de texto
        success_time = datetime.datetime.now().strftime("%H:%M")
        error_message = f"Linha Excel: {linha_excel} {row['CPF']} Erro às {success_time}\n"
        log_file_path.write(error_message)
        log_file_path.flush()  # Força a gravação imediata no arquivo
        print(error_message)
        pass
    finally:
        driver.quit()