import pytest
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time


@pytest.fixture(scope="session")
def driver():
    """Configurar driver do Chrome para os testes"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Executar sem interface gráfica
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--allow-running-insecure-content")
    
    try:
        # Usar webdriver-manager para compatibilidade automática
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.implicitly_wait(10)
        
        yield driver
        
        driver.quit()
    except Exception as e:
        print(f"Erro ao inicializar Chrome WebDriver: {e}")
        raise


@pytest.fixture(scope="session")
def base_url():
    """URL base da aplicação"""
    return os.getenv("FRONTEND_URL", "http://frontend:3000")


@pytest.fixture(scope="session") 
def api_url():
    """URL da API"""
    return os.getenv("API_URL", "http://backend:8000")


@pytest.fixture
def wait_for_app(driver, base_url):
    """Aguardar aplicação estar disponível"""
    max_retries = 30
    for i in range(max_retries):
        try:
            driver.get(base_url)
            # Verificar se a página carregou
            WebDriverWait(driver, 5).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            return True
        except Exception as e:
            if i == max_retries - 1:
                raise Exception(f"Aplicação não está disponível após {max_retries} tentativas: {e}")
            time.sleep(2)
    

@pytest.fixture
def clean_storage(driver):
    """Limpar localStorage e cookies antes de cada teste"""
    driver.delete_all_cookies()
    driver.execute_script("localStorage.clear();")
    driver.execute_script("sessionStorage.clear();")


@pytest.fixture
def login_user(driver, base_url, wait_for_app, clean_storage):
    """Fazer login com usuário de teste"""
    driver.get(f"{base_url}/login")
    
    # Preencher formulário de login
    email_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "email"))
    )
    password_input = driver.find_element(By.ID, "password")
    
    email_input.send_keys("admin@test.com")
    password_input.send_keys("123456")
    
    # Clicar no botão de login
    login_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Entrar na Conta')]")
    login_button.click()
    
    # Aguardar redirecionamento para dashboard
    WebDriverWait(driver, 10).until(
        EC.url_contains("/dashboard")
    )
    
    return True


class TestHelper:
    """Classe auxiliar com métodos úteis para testes"""
    
    @staticmethod
    def wait_for_element(driver, locator, timeout=10):
        """Aguardar elemento aparecer"""
        return WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located(locator)
        )
    
    @staticmethod
    def wait_for_clickable(driver, locator, timeout=10):
        """Aguardar elemento ser clicável"""
        return WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )
    
    @staticmethod
    def wait_for_text(driver, locator, text, timeout=10):
        """Aguardar texto aparecer em elemento"""
        return WebDriverWait(driver, timeout).until(
            EC.text_to_be_present_in_element(locator, text)
        )
    
    @staticmethod
    def scroll_to_element(driver, element):
        """Rolar página até elemento"""
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(0.5)


@pytest.fixture
def helper():
    """Fixture para classe auxiliar"""
    return TestHelper 