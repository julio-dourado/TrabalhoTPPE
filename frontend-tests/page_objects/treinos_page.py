from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TreinosPage:
    """Page Object para página de treinos"""
    
    def __init__(self, driver):
        self.driver = driver
        
    # Locators
    PAGE_TITLE = (By.XPATH, "//h1[contains(text(), 'Meus Treinos')]")
    CREATE_TREINO_BTN = (By.XPATH, "//button[contains(text(), 'Criar Treino')]")
    CREATE_FIRST_TREINO_BTN = (By.XPATH, "//button[contains(text(), 'Criar Primeiro Treino')]")
    TREINO_CARDS = (By.XPATH, "//div[contains(@class, 'cursor-pointer')]//h3")
    DELETE_BUTTONS = (By.XPATH, "//button[@title='Excluir treino']")
    NO_TREINOS_MESSAGE = (By.XPATH, "//h3[contains(text(), 'Você não possui nenhum treino ainda')]")
    LOADING_SPINNER = (By.XPATH, "//p[contains(text(), 'Carregando treinos')]")
    
    def navigate_to(self, base_url):
        """Navegar para página de treinos"""
        self.driver.get(f"{base_url}/treinos")
        return self
    
    def wait_for_page_load(self):
        """Aguardar página carregar"""
        # Aguardar either título da página ou spinner desaparecer
        WebDriverWait(self.driver, 10).until(
            lambda d: d.find_elements(*self.PAGE_TITLE) or 
                     not d.find_elements(*self.LOADING_SPINNER)
        )
        return self
    
    def click_create_treino(self):
        """Clicar em criar treino"""
        try:
            btn = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(self.CREATE_TREINO_BTN)
            )
            btn.click()
            return True
        except:
            return False
    
    def click_create_first_treino(self):
        """Clicar em criar primeiro treino"""
        try:
            btn = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(self.CREATE_FIRST_TREINO_BTN)
            )
            btn.click()
            return True
        except:
            return False
    
    def get_treino_cards(self):
        """Obter lista de cards de treinos"""
        try:
            cards = self.driver.find_elements(*self.TREINO_CARDS)
            return [card.text for card in cards]
        except:
            return []
    
    def get_treino_count(self):
        """Obter número de treinos"""
        return len(self.get_treino_cards())
    
    def click_treino_card(self, index=0):
        """Clicar em card de treino específico"""
        try:
            cards = self.driver.find_elements(*self.TREINO_CARDS)
            if index < len(cards):
                cards[index].click()
                return True
            return False
        except:
            return False
    
    def click_delete_treino(self, index=0):
        """Clicar em botão de deletar treino"""
        try:
            delete_buttons = self.driver.find_elements(*self.DELETE_BUTTONS)
            if index < len(delete_buttons):
                delete_buttons[index].click()
                return True
            return False
        except:
            return False
    
    def confirm_delete(self):
        """Confirmar exclusão na modal do navegador"""
        try:
            # Aguardar e aceitar alert do browser
            WebDriverWait(self.driver, 3).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            alert.accept()
            return True
        except:
            return False
    
    def has_no_treinos_message(self):
        """Verificar se tem mensagem de nenhum treino"""
        try:
            self.driver.find_element(*self.NO_TREINOS_MESSAGE)
            return True
        except:
            return False
    
    def wait_for_treino_deleted(self, initial_count):
        """Aguardar treino ser deletado"""
        WebDriverWait(self.driver, 10).until(
            lambda d: len(d.find_elements(*self.TREINO_CARDS)) < initial_count
        )
        return True 