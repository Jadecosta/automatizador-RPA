import json
import os
import sys
import time
from selenium.webdriver.common.by import By

PROGRESS_FOLDER = 'progress_files'

def update_progress(task_id, progresso):
    progress_file_path = os.path.join(PROGRESS_FOLDER, f'progress_{task_id}.json') # type: ignore
    with open(progress_file_path, 'w') as progress_file:
        json.dump({'task_id': task_id, 'progress': progresso}, progress_file)

# gravar, confirmar

def gravar_e_confirmar(driver):
    try:
        
        driver.find_element(By.XPATH, '//*[@id="vobys-form-action-buttons"]/button').click()
        time.sleep(4)
        
        driver.find_element(By.XPATH, '//*[@id="vobys-form-confirmation-save"]').click()
        time.sleep(4)
        
        print("Ação de gravação e confirmação realizada com sucesso.")
    except Exception as e:
        print(f"Ocorreu um erro durante a ação de gravação e confirmação: {e}")

#charma webdrive, login    driver.get('https://siape.sead.pi.gov.br')

# isolar as instancias