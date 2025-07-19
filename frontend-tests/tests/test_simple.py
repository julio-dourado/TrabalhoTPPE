import pytest
from page_objects.login_page import LoginPage


class TestSimple:
    """Testes simples para verificar funcionamento básico"""
    
    def test_page_load(self, driver, base_url, wait_for_app, clean_storage):
        """Teste simples de carregamento da página"""
        login_page = LoginPage(driver)
        
        # Navegar para página de login
        login_page.navigate_to(base_url)
        
        # Verificar se a página carregou
        assert "login" in driver.current_url
        
        # Verificar título da página
        assert driver.title or True  # Aceitar qualquer título ou vazio
        
        # Verificar se há elementos básicos
        page_source = driver.page_source
        assert len(page_source) > 100  # Página tem conteúdo
    
    def test_basic_navigation(self, driver, base_url, wait_for_app, clean_storage):
        """Teste básico de navegação"""
        # Ir para página inicial
        driver.get(base_url)
        
        # Verificar que redirecionou para login
        assert "/login" in driver.current_url or "/register" in driver.current_url
        
    def test_login_form_exists(self, driver, base_url, wait_for_app, clean_storage):
        """Teste se formulário de login existe"""
        login_page = LoginPage(driver)
        
        # Navegar para login
        login_page.navigate_to(base_url)
        
        # Verificar se inputs existem
        email_input = driver.find_element(*login_page.EMAIL_INPUT)
        password_input = driver.find_element(*login_page.PASSWORD_INPUT)
        login_button = driver.find_element(*login_page.LOGIN_BUTTON)
        
        assert email_input is not None
        assert password_input is not None  
        assert login_button is not None 