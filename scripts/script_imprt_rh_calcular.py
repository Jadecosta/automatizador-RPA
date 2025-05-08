import sys
import pandas as pd
import time
import json
import os
import concurrent.futures
from playwright.sync_api import sync_playwright
from datetime import datetime

def main(file_path, username, password, task_id, log_file_name):
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_file_path = os.path.join(log_dir, log_file_name)

    # Arquivo para registrar erros
    error_file = open(log_file_path, 'w')

    progress_file_path = f'progress_{task_id}.json'


    # Leitura do arquivo Excel
    try:
        data = pd.read_excel(file_path)
    except Exception as e:
        print(f"Erro ao ler o arquivo Excel: {e}")
        error_file.write(f"Erro ao ler o arquivo Excel: {e}\n")
        error_file.close()
        return

    total_linhas = len(data)

    def processar_linha(row):
        with sync_playwright() as p:
            try:
                linha_excel = row.name + 2
                browser = p.chromium.launch(headless=True)  # Remova headless=True para exibir o navegador visualmente
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
                page.goto(f'https://siape.sead.pi.gov.br/adm/{orgao}/folha-funcionario/folhas/folhas')


                # Esperar até que a página seja totalmente carregada 
                page.wait_for_load_state("load", timeout=60000)

                page.locator('//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[2]/div/div[1]/input[2]').fill(str(row['FOLHA']))

                page.locator('//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div/form/div[2]/div/div[10]/button').click()
                page.wait_for_timeout(4000)

                page.locator('//*[@id="folhaFuncionario"]/div[1]/table/tbody/tr/td[1]/a').click()

                # pagamento
                page.locator('//*[@id="vobys-content"]/div/div/div[5]/div/div[2]/div/div[1]/a').click()

            
                # matricula
                page.locator('//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div[1]/form/div[2]/div/div[1]/input[2]').click()
                page.locator('//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div[1]/form/div[2]/div/div[1]/input[2]').fill(str(row['MATRICULA']))
            
                page.locator('//*[@id="vobys-content"]/div/div/div/div[3]/div/div/div[1]/form/div[2]/div/div[12]/button').click()
                page.wait_for_timeout(4000)

                page.locator('//*[@id="funcionarios"]/div[1]/table/tbody/tr[1]/td[1]/a').click()
            
            
                # calcular
                page.locator('//*[@id="vobys-content"]/div/div/div/div[2]/div/a[2]').click()
                page.wait_for_timeout(4000)

                # importar RH
                page.locator('//*[@id="vobys-content"]/div/div/div/div[3]/div/div[1]/div/div[2]/div[1]/a').click()
                page.wait_for_timeout(5000)

                # Gerar eventos/Rubricas/Calculos
                page.locator('//*[@id="vobys-content"]/div/div/div/div[3]/div/div[1]/div/div[2]/div[6]/a').click()
                page.wait_for_timeout(5000)

            except Exception as e:
                # Salva a linha que deu erro no arquivo de texto
                success_time = datetime.datetime.now().strftime("%H:%M")
                error_message = f"Linha Excel: {linha_excel} {row['MATRICULA']} {row['FOLHA']} Erro às {success_time}\n"
                with open(log_file_path, 'a') as error_file:
                    error_file.write(error_message)
                    error_file.flush()  # Força a gravação imediata no arquivo
                print(error_message)
            finally:
                browser.close()

        # Atualizar progresso
        progresso = (row.name + 1) / total_linhas * 100
        with open(progress_file_path, 'w') as progress_file:
            json.dump({'task_id': task_id, 'progress': progresso}, progress_file)

    # Inicializa a lista de resultados
    resultados = []

    # Cria um executor de threads com no máximo 5 workers (telas abertas)
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    #with concurrent.futures.ThreadPoolExecutor() as executor:
        for index, row in data.iterrows():
            resultado = executor.submit(processar_linha, row)
            resultados.append(resultado)

        # Aguarda a conclusão de todos os resultados
        for resultado in concurrent.futures.as_completed(resultados):
            resultado.result()

    error_file.close()

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Uso: script_ingresso_pecunia.py <caminho do arquivo Excel> <username> <password> <task_id>")
        sys.exit(1)

    file_path = sys.argv[1]
    username = sys.argv[2]
    password = sys.argv[3]
    task_id = sys.argv[4]
    log_file_name = sys.argv[5]
    main(file_path, username, password, task_id, log_file_name)
