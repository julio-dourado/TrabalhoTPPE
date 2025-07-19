from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class NewTreinoPage:
    """Page Object para página de novo treino"""
    
    def __init__(self, driver):
        self.driver = driver
        
    # Locators
    PAGE_TITLE = (By.XPATH, "//h1[contains(text(), 'Criar Novo Treino')]")
    BACK_BUTTON = (By.XPATH, "//button[contains(text(), 'Voltar para treinos')]")
    NAME_INPUT = (By.ID, "nome")
    DESCRIPTION_INPUT = (By.ID, "descricao")
    CANCEL_BUTTON = (By.XPATH, "//button[contains(text(), 'Cancelar')]")
    CREATE_BUTTON = (By.XPATH, "//button[contains(text(), 'Criar Treino')]")
    ERROR_MESSAGE = (By.XPATH, "//p[contains(text(), '❌')]")
    LOADING_STATE = (By.XPATH, "//span[contains(text(), 'Criando...')]")
    
    def navigate_to(self, base_url):
        """Navegar para página de novo treino"""
        self.driver.get(f"{base_url}/treinos/new")
        return self
    
    def wait_for_page_load(self):
        """Aguardar página carregar"""
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.PAGE_TITLE)
        )
        return self
    
    def enter_name(self, name):
        """Inserir nome do treino"""
        name_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.NAME_INPUT)
        )
        name_input.clear()
        name_input.send_keys(name)
        return self
    
    def enter_description(self, description):
        """Inserir descrição do treino"""
        desc_input = self.driver.find_element(*self.DESCRIPTION_INPUT)
        desc_input.clear()
        desc_input.send_keys(description)
        return self
    
    def click_create(self):
        """Clicar em criar treino"""
        create_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.CREATE_BUTTON)
        )
        create_button.click()
        return self
    
    def click_cancel(self):
        """Clicar em cancelar"""
        cancel_button = self.driver.find_element(*self.CANCEL_BUTTON)
        cancel_button.click()
        return self
    
    def click_back(self):
        """Clicar em voltar"""
        back_button = self.driver.find_element(*self.BACK_BUTTON)
        back_button.click()
        return self
    
    def create_treino(self, name, description=""):
        """Criar treino completo"""
        self.enter_name(name)
        if description:
            self.enter_description(description)
        return self.click_create()
    
    def get_error_message(self):
        """Obter mensagem de erro"""
        try:
            error_element = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(self.ERROR_MESSAGE)
            )
            return error_element.text
        except:
            return None
    
    def is_loading(self):
        """Verificar se está carregando"""
        try:
            self.driver.find_element(*self.LOADING_STATE)
            return True
        except:
            return False
    
    def wait_for_redirect_to_treinos(self):
        """Aguardar redirecionamento para página de treinos"""
        WebDriverWait(self.driver, 10).until(
            EC.url_contains("/treinos")
        )
        WebDriverWait(self.driver, 10).until(
            lambda d: "/new" not in d.current_url
        )
        return True 