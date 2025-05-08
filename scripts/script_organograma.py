import sys
import pandas as pd
import time
import json
import os
from playwright.sync_api import sync_playwright
from datetime import datetime


def main(file_path, username, password, task_id):
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file_name = f'log_organograma_{timestamp}.txt'
    log_file_path = os.path.join(log_dir, log_file_name)

    # Arquivo para registrar erros
    error_file = open(log_file_path, 'w')

    progress_file_path = f'progress_{task_id}.json'

    # Leitura do arquivo Excel
    try:
        data = pd.read_excel(file_path)
        data['CODIGO'] = data['CODIGO'].astype(str)
    except Exception as e:
        print(f"Erro ao ler o arquivo Excel: {e}")
        error_file.write(f"Erro ao ler o arquivo Excel: {e}\n")
        error_file.close()
        return

    total_linhas = len(data)


    # chrome_options.add_argument("--headless")  # Descomente esta linha para execução sem interface gráfica

    def processar_linha(row):
        with sync_playwright() as p:
            try:
                linha_excel = row.name + 2
                nome = row['NOME']
                browser = p.chromium.launch(headless=False)  # Remova headless=True para exibir o navegador visualmente
                context = browser.new_context()
        
                page = context.new_page()
                page.goto('https://siape.sead.pi.gov.br')
                page.wait_for_load_state("load")

                try:
                    # Localizar os elementos de input do usuário e senha
                    input_usuario = page.locator('#username')
                    input_senha = page.locator('#password')

                    # Preencher os campos de usuário e senha
                    input_usuario.type(username)
                    input_senha.type(password)

                    input_senha.press('Enter')  # Enviar o formulário de login
                except:
                    print("Erro de credenciais!")
                
                orgao = str(row['ORGAO'])
                page.goto(f'https://siape.sead.pi.gov.br/adm/{orgao}/tabelas-basicas/lotacao-centro-custo/lotacoes')             

                # Esperar até que a página seja totalmente carregada
                page.wait_for_load_state("load", timeout=30000)
 
                page.click('//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div[1]/form/div[1]/div/a')   

                page.click('//*[@id="id_7_11_21_12_11_28_11_11"]')
                codigo_institucional = str(row['CODIGO'])
                campo_input_cod = page.locator('//*[@id="id_7_11_21_12_11_28_11_11"]')
                campo_input_cod.clear()
                campo_input_cod.fill(codigo_institucional)  

                page.click('//*[@id="id_7_11_21_12_11_28_11_12"]')
                campo_input_nome = page.locator('//*[@id="id_7_11_21_12_11_28_11_12"]')
                campo_input_nome.clear()
                campo_input_nome.fill(nome)

                page.click('//*[@id="id_7_11_21_12_11_28_11_13"]')
                sigla = str(row['SIGLA'])
                campo_input_sigla = page.locator('//*[@id="id_7_11_21_12_11_28_11_13"]')
                campo_input_sigla.clear()
                campo_input_sigla.fill(sigla)  

                page.click('//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[5]/div/button')
                page.click('//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[5]/div/div/div[1]/input') 
                time.sleep(1)
                campo_input_eSocial = page.locator('//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[5]/div/div/div[1]/input')
                campo_input_eSocial.press('Space')
                time.sleep(1)
                page.click('//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[5]/div/div/div[2]/ul/li[2]/a/span[2]')

                page.click('//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[6]/div/button/div/div/div')
                page.click('//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[6]/div/div/div[1]/input') 
                time.sleep(1)
                campo_input_lotacaoeSocial = page.locator('//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[6]/div/div/div[1]/input')
                campo_input_lotacaoeSocial.press('Space')
                time.sleep(1)
                page.click('//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[6]/div/div/div[2]/ul/li[2]/a/span[2]')
                
            
                page.click('//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[14]/div/button/div')
                page.click('//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[14]/div/div/div[1]/input') 
                time.sleep(1)
                hierarquicamente_superior = str(row['LOTACAO HIERARQUICAMENTE SUPERIOR'])
                 # Insira o valor no campo de entrada
                campo_input = page.locator('//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[14]/div/div/div[1]/input')
                campo_input.fill(hierarquicamente_superior)
                time.sleep(1)
                # Simulate backspace key press
                campo_input.press('Space')
                time.sleep(1)
                page.click('//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[14]/div/div/div[2]/ul/li[2]/a/span[2]')


                page.click('//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[16]/div/button/div/div/div')

                municipio = str(row['MUNICIPIO'])

                # Preencher o campo de entrada com o município
                campo_input_municipio = page.locator('//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[16]/div/div/div[1]/input')
                campo_input_municipio.fill(municipio)
                time.sleep(1)
                campo_input_municipio.press('Space')
                time.sleep(1)
                page.wait_for_selector('//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[16]/div/div/div[2]/ul')
                time.sleep(1)
                # Encontrar todos os elementos do dropdown
                elementos_dropdown = page.query_selector_all('//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div[16]/div/div/div[2]/ul/li')
                time.sleep(1)
                # Iterar sobre os elementos do dropdown
                for elemento in elementos_dropdown:
                    # Verificar se o texto desejado está presente no elemento do dropdown
                    if municipio in elemento.text_content():
                        # Clicar no elemento
                        elemento.click()
                        # Se o elemento for clicado, podemos sair do loop
                        break

                    # Executar JavaScript para preencher o campo de data
                page.evaluate('''() => {
                    document.querySelector('#id_7_11_21_12_11_28_11_14').value = '24/06/2024';
                }''')
                #page.click('//*[@id="id_7_11_21_12_11_28_11_14"]')
                #page.locator('//*[@id="id_7_11_21_12_11_28_11_14"]').fill('01/04/2024')
                
                #time.sleep(2)

                # GRAVAR E CONFIRMAR
                # Clicar no botão GRAVAR
                page.click('//*[@id="vobys-form-action-buttons"]/button')
                page.wait_for_timeout(5000)  # Aguardar por 4 segundos (equivale ao seu time.sleep(4))

                # Clicar no botão CONFIRMAR
                page.click('//*[@id="vobys-form-confirmation-save"]')
                page.wait_for_timeout(5000)  # Aguardar por 4 segundos (equivale ao seu time.sleep(4))
            
            except Exception as e:
                error_msg = f"Erro na linha {linha_excel} para a codigo {str(row['CODIGO'])}: {e}"
                print(error_msg)
                error_file.write(error_msg + '\n')

            finally:
                browser.close()

        # Atualizar progresso
        progresso = (row.name + 1) / total_linhas * 100
        with open(progress_file_path, 'w') as progress_file:
            json.dump({'task_id': task_id, 'progress': progresso}, progress_file)

    # Processa cada linha do Excel
    data.apply(processar_linha, axis=1)

    error_file.close()

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Uso: script_organograma.py <caminho do arquivo Excel> <username> <password> <task_id>")
        sys.exit(1)

    file_path = sys.argv[1]
    username = sys.argv[2]
    password = sys.argv[3]
    task_id = sys.argv[4]
    main(file_path, username, password, task_id)
