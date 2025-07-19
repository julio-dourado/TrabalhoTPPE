from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Layout:
    """Page Object para Layout da aplicação"""
    
    def __init__(self, driver):
        self.driver = driver
        
    # Locators
    LOGO = (By.XPATH, "//h1[contains(text(), 'Crie Seu Treino')]")
    DASHBOARD_LINK = (By.XPATH, "//button[contains(text(), 'Dashboard')]")
    TREINOS_LINK = (By.XPATH, "//button[contains(text(), 'Treinos')]")
    PROFILE_LINK = (By.XPATH, "//button[contains(text(), 'Perfil')]")
    LOGOUT_BUTTON = (By.XPATH, "//button[contains(text(), 'Sair')]")
    
    def click_logo(self):
        """Clicar no logo para ir ao dashboard"""
        logo = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.LOGO)
        )
        logo.click()
        return self
    
    def click_dashboard(self):
        """Navegar para dashboard"""
        dashboard_link = self.driver.find_element(*self.DASHBOARD_LINK)
        dashboard_link.click()
        return self
    
    def click_treinos(self):
        """Navegar para treinos"""
        treinos_link = self.driver.find_element(*self.TREINOS_LINK)
        treinos_link.click()
        return self
    
    def click_profile(self):
        """Navegar para perfil"""
        profile_link = self.driver.find_element(*self.PROFILE_LINK)
        profile_link.click()
        return self
    
    def click_logout(self):
        """Fazer logout"""
        logout_button = self.driver.find_element(*self.LOGOUT_BUTTON)
        logout_button.click()
        return self
    
    def wait_for_navigation(self, expected_url_part):
        """Aguardar navegação para URL específica"""
        WebDriverWait(self.driver, 10).until(
            EC.url_contains(expected_url_part)
        )
        return True
    
    def get_current_active_link(self):
        """Obter qual link está ativo no momento"""
        try:
            # Procurar por links com background colorido (ativo)
            active_elements = self.driver.find_elements(By.XPATH, 
                "//button[contains(@class, 'bg-primary-500')]")
            if active_elements:
                return active_elements[0].text
            return None
        except:
            return None
    
    def is_user_logged_in(self):
        """Verificar se usuário está logado (header visível)"""
        try:
            self.driver.find_element(*self.LOGO)
            self.driver.find_element(*self.LOGOUT_BUTTON)
            return True
        except:
            return False 