from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class RegisterPage:
    """Page Object para página de registro"""
    
    def __init__(self, driver):
        self.driver = driver
        
    # Locators
    NAME_INPUT = (By.ID, "nome")
    EMAIL_INPUT = (By.ID, "email")
    PASSWORD_INPUT = (By.ID, "password")
    REGISTER_BUTTON = (By.XPATH, "//button[contains(text(), 'Criar Minha Conta')]")
    ERROR_MESSAGE = (By.XPATH, "//p[contains(text(), '❌')]")
    LOGIN_LINK = (By.XPATH, "//a[contains(text(), 'Fazer login')]")
    PASSWORD_HINT = (By.XPATH, "//p[contains(text(), 'Use no mínimo 6 caracteres')]")
    
    def navigate_to(self, base_url):
        """Navegar para página de registro"""
        self.driver.get(f"{base_url}/register")
        return self
    
    def enter_name(self, name):
        """Inserir nome"""
        name_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.NAME_INPUT)
        )
        name_input.clear()
        name_input.send_keys(name)
        return self
    
    def enter_email(self, email):
        """Inserir email"""
        email_input = self.driver.find_element(*self.EMAIL_INPUT)
        email_input.clear()
        email_input.send_keys(email)
        return self
    
    def enter_password(self, password):
        """Inserir senha"""
        password_input = self.driver.find_element(*self.PASSWORD_INPUT)
        password_input.clear()
        password_input.send_keys(password)
        return self
    
    def click_register(self):
        """Clicar no botão de registro"""
        register_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.REGISTER_BUTTON)
        )
        register_button.click()
        return self
    
    def register(self, name, email, password):
        """Fazer registro completo"""
        return self.enter_name(name).enter_email(email).enter_password(password).click_register()
    
    def get_error_message(self):
        """Obter mensagem de erro"""
        try:
            error_element = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(self.ERROR_MESSAGE)
            )
            return error_element.text
        except:
            return None
    
    def click_login_link(self):
        """Clicar no link de login"""
        login_link = self.driver.find_element(*self.LOGIN_LINK)
        login_link.click()
        return self
    
    def is_password_hint_visible(self):
        """Verificar se dica de senha está visível"""
        try:
            self.driver.find_element(*self.PASSWORD_HINT)
            return True
        except:
            return False
    
    def wait_for_redirect_to_dashboard(self):
        """Aguardar redirecionamento para dashboard"""
        WebDriverWait(self.driver, 10).until(
            EC.url_contains("/dashboard")
        )
        return True 