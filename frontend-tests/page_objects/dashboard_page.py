from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class DashboardPage:
    """Page Object para dashboard"""
    
    def __init__(self, driver):
        self.driver = driver
        
    # Locators
    GREETING_TITLE = (By.XPATH, "//h1[contains(text(), 'Olá,')]")
    TREINOS_COUNT = (By.XPATH, "//p[contains(text(), 'Treinos criados') or contains(text(), 'Treino criado')]")
    CREATE_FIRST_TREINO_BTN = (By.XPATH, "//button[contains(text(), 'Criar Primeiro Treino')]")
    CREATE_NEW_TREINO_BTN = (By.XPATH, "//button[contains(text(), 'Criar Novo Treino')]")
    VIEW_TREINOS_BTN = (By.XPATH, "//button[contains(text(), 'Ver Todos os Treinos')]")
    PROFILE_BTN = (By.XPATH, "//button[contains(text(), 'Meu Perfil')]")
    TREINO_ITEM = (By.XPATH, "//div[contains(@class, 'group')]//p[contains(@class, 'font-semibold')]")
    TIP_OF_DAY = (By.XPATH, "//h3[contains(text(), 'Dica do Dia')]")
    
    def navigate_to(self, base_url):
        """Navegar para dashboard"""
        self.driver.get(f"{base_url}/dashboard")
        return self
    
    def wait_for_page_load(self):
        """Aguardar página carregar"""
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.GREETING_TITLE)
        )
        return self
    
    def get_greeting_text(self):
        """Obter texto de saudação"""
        greeting = self.driver.find_element(*self.GREETING_TITLE)
        return greeting.text
    
    def get_treinos_count_text(self):
        """Obter texto da contagem de treinos"""
        try:
            count_element = self.driver.find_element(*self.TREINOS_COUNT)
            return count_element.text
        except:
            return None
    
    def click_create_first_treino(self):
        """Clicar em criar primeiro treino"""
        try:
            btn = self.driver.find_element(*self.CREATE_FIRST_TREINO_BTN)
            btn.click()
            return True
        except:
            return False
    
    def click_create_new_treino(self):
        """Clicar em criar novo treino"""
        try:
            btn = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(self.CREATE_NEW_TREINO_BTN)
            )
            btn.click()
            return True
        except:
            return False
    
    def click_view_all_treinos(self):
        """Clicar em ver todos os treinos"""
        btn = self.driver.find_element(*self.VIEW_TREINOS_BTN)
        btn.click()
        return self
    
    def click_profile(self):
        """Clicar em perfil"""
        btn = self.driver.find_element(*self.PROFILE_BTN)
        btn.click()
        return self
    
    def get_treino_items(self):
        """Obter lista de treinos"""
        try:
            items = self.driver.find_elements(*self.TREINO_ITEM)
            return [item.text for item in items]
        except:
            return []
    
    def click_treino_item(self, index=0):
        """Clicar em item de treino específico"""
        items = self.driver.find_elements(*self.TREINO_ITEM)
        if index < len(items):
            items[index].click()
            return True
        return False
    
    def is_tip_of_day_visible(self):
        """Verificar se dica do dia está visível"""
        try:
            self.driver.find_element(*self.TIP_OF_DAY)
            return True
        except:
            return False
    
    def has_no_treinos_message(self):
        """Verificar se tem mensagem de nenhum treino"""
        try:
            self.driver.find_element(*self.CREATE_FIRST_TREINO_BTN)
            return True
        except:
            return False 