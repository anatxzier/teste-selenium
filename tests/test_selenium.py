import pytest
import openpyxl
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

caminho_arquivo = 'tests/Pasta1.xlsx'

def ler_dados_excel(caminho_arquivo):
    wb = openpyxl.load_workbook(caminho_arquivo)
    sheet = wb.active
    
    dados = []
    for row in sheet.iter_rows(min_row=2, values_only=True):
        dados.append({
            'nome': row[0],
            'senha': row[1],
        })
    
    return dados

def preencher_formulario(driver, dados):
    for dado in dados:
        # Preencher o formulário
        nome_input = driver.find_element(By.ID, "input-nome")
        senha_input = driver.find_element(By.ID, "input-senha")
        
        nome_input.clear()
        nome_input.send_keys(dado['nome'])
        
        senha_input.clear()
        senha_input.send_keys(dado['senha'])
        
        # Enviar o formulário
        submit_button = driver.find_element(By.ID, "btn-sublogin")
        submit_button.click()
        
        # Espera até que o URL da página seja alterado após o envio do formulário
        WebDriverWait(driver, 10).until(
            EC.url_contains("/novaturma/")
        )

@pytest.mark.selenium
def test_selenium():
    driver = webdriver.Chrome()
    
    try:
        driver.get("http://127.0.0.1:8000/")
        
        # Verifique se o título da página contém um texto específico
        assert "" in driver.title  # Substitua "Texto Esperado" pelo título esperado
        
        element1 = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "btnLink1"))
        )
        element1.click()

        # Ler os dados do Excel
        dados = ler_dados_excel(caminho_arquivo)
        
        if dados:
            preencher_formulario(driver, dados)
        else:
            print("Nenhum dado encontrado para preencher o formulário.")
        
        # Verifique se a navegação foi bem-sucedida
        WebDriverWait(driver, 10).until(
            EC.url_contains("/novaturma/")
        )
        

    finally:
        driver.quit()
