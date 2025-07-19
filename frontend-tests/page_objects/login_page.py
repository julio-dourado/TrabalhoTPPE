from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
    """Page Object para página de login"""
    
    def __init__(self, driver):
        self.driver = driver
        
    # Locators
    EMAIL_INPUT = (By.ID, "email")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.XPATH, "//button[contains(text(), 'Entrar na Conta')]")
    ERROR_MESSAGE = (By.XPATH, "//p[contains(text(), '❌')]")
    REGISTER_LINK = (By.XPATH, "//a[contains(text(), 'Criar conta grátis')]")
    DEMO_CREDENTIALS = (By.XPATH, "//p[contains(text(), 'Credenciais de teste')]")
    
    def navigate_to(self, base_url):
        """Navegar para página de login"""
        self.driver.get(f"{base_url}/login")
        return self
    
    def enter_email(self, email):
        """Inserir email"""
        email_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.EMAIL_INPUT)
        )
        email_input.clear()
        email_input.send_keys(email)
        return self
    
    def enter_password(self, password):
        """Inserir senha"""
        password_input = self.driver.find_element(*self.PASSWORD_INPUT)
        password_input.clear()
        password_input.send_keys(password)
        return self
    
    def click_login(self):
        """Clicar no botão de login"""
        login_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.LOGIN_BUTTON)
        )
        login_button.click()
        return self
    
    def login(self, email, password):
        """Fazer login completo"""
        return self.enter_email(email).enter_password(password).click_login()
    
    def get_error_message(self):
        """Obter mensagem de erro"""
        try:
            error_element = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(self.ERROR_MESSAGE)
            )
            return error_element.text
        except:
            return None
    
    def click_register_link(self):
        """Clicar no link de registro"""
        register_link = self.driver.find_element(*self.REGISTER_LINK)
        register_link.click()
        return self
    
    def is_demo_credentials_visible(self):
        """Verificar se credenciais demo estão visíveis"""
        try:
            self.driver.find_element(*self.DEMO_CREDENTIALS)
            return True
        except:
            return False
    
    def wait_for_redirect_to_dashboard(self):
        """Aguardar redirecionamento para dashboard"""
        WebDriverWait(self.driver, 10).until(
            EC.url_contains("/dashboard")
        )
        return True 