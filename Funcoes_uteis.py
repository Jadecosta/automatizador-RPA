import concurrent.futures
import time
import pandas as pd

# Função simulada para processar uma linha
def processar_linha(row):
    # Simula o processamento real (substituir por lógica real)
    time.sleep(0.1)  # Tempo base de espera
    return row

# Estima o tempo esperado de execução
def estimar_tempo(data, num_workers, selenium_time=0):
    sleep_time = 0.1  # Tempo do time.sleep no processar_linha
    linhas_por_worker = len(data) / num_workers
    tempo_por_worker = linhas_por_worker * (sleep_time + selenium_time)
    
    # Tempo total aproximado (considerando execução paralela)
    tempo_total = tempo_por_worker
    return tempo_total

# Função principal
def executar_tarefas(data, min_workers=1, max_workers=4, monitor_interval=5, selenium_time=2, max_tempo_permitido=15):
    num_workers = min_workers
    primeira_execucao = True  # Flag para verificar se é a primeira execução
    linha_inicial = 0  # Para retomar do ponto onde parou
    
    while linha_inicial < len(data):  # Processa todas as linhas do DataFrame
        resultados = []
        start_time = time.time()
        
        try:
            # Cria um executor de threads com o número atual de workers
            with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
                for index, row in data.iloc[linha_inicial:].iterrows():  # Retoma da linha inicial
                    resultado = executor.submit(processar_linha, row)
                    resultados.append(resultado)

                # Aguarda a conclusão de todos os resultados
                for i, resultado in enumerate(concurrent.futures.as_completed(resultados)):
                    resultado.result()
                    linha_inicial += 1  # Atualiza a linha inicial processada

            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"Executado com {num_workers} workers em {elapsed_time:.2f} segundos.")

            # Verifica se o tempo de execução excede o limite permitido
            if primeira_execucao and elapsed_time > max_tempo_permitido:
                print("Sistema lento, tente novamente mais tarde!")
                break
            elif elapsed_time > max_tempo_permitido:
                print("Sistema lento! Aguardando estabilização...")
                time.sleep(monitor_interval)  # Aguarda antes de tentar novamente
                continue  # Retoma do ponto onde parou

            # Estima o tempo esperado com base nos parâmetros atuais
            tempo_estimado = estimar_tempo(data.iloc[linha_inicial:], num_workers, selenium_time)
            print(f"Tempo estimado para {num_workers} workers: {tempo_estimado:.2f} segundos.")

            # Ajusta o número de workers com base no desempenho
            if elapsed_time < tempo_estimado and num_workers < max_workers:  # Aumenta se o desempenho for bom
                num_workers += 1
                print("Aumentando número de workers para:", num_workers)
            elif elapsed_time >= tempo_estimado and num_workers > min_workers:  # Diminui se o desempenho for ruim
                num_workers -= 1
                print("Diminuindo número de workers para:", num_workers)
            else:
                print("Mantendo número de workers:", num_workers)

        except Exception as e:
            print(f"Erro inesperado: {e}")
            break

        primeira_execucao = False  # Após a primeira execução

# Exemplo de uso
# Simula um dataframe com 20 linhas
data = pd.DataFrame({'col1': range(20)})

# Chamando a função principal com tempo médio de Selenium de 2 segundos por linha
executar_tarefas(data, selenium_time=2, max_tempo_permitido=15)
