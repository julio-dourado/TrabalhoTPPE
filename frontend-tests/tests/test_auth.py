import pytest
from page_objects.login_page import LoginPage
from page_objects.register_page import RegisterPage
from page_objects.dashboard_page import DashboardPage
from page_objects.layout import Layout


class TestAuthentication:
    """Testes de autenticação"""
    
    def test_successful_login(self, driver, base_url, wait_for_app, clean_storage):
        """Teste de login bem-sucedido"""
        login_page = LoginPage(driver)
        dashboard_page = DashboardPage(driver)
        
        # Navegar para página de login
        login_page.navigate_to(base_url)
        
        # Verificar se credenciais demo estão visíveis
        assert login_page.is_demo_credentials_visible()
        
        # Fazer login
        login_page.login("admin@test.com", "123456")
        
        # Verificar redirecionamento para dashboard
        assert login_page.wait_for_redirect_to_dashboard()
        
        # Verificar se dashboard carregou
        dashboard_page.wait_for_page_load()
        assert "Olá," in dashboard_page.get_greeting_text()
    
    def test_invalid_credentials_login(self, driver, base_url, wait_for_app, clean_storage):
        """Teste de login com credenciais inválidas"""
        login_page = LoginPage(driver)
        
        # Navegar para página de login
        login_page.navigate_to(base_url)
        
        # Tentar login com credenciais inválidas
        login_page.login("invalid@email.com", "wrongpassword")
        
        # Verificar mensagem de erro
        error_message = login_page.get_error_message()
        assert error_message is not None
        assert "inválidos" in error_message.lower()
    
    def test_empty_fields_login(self, driver, base_url, wait_for_app, clean_storage):
        """Teste de login com campos vazios"""
        login_page = LoginPage(driver)
        
        # Navegar para página de login
        login_page.navigate_to(base_url)
        
        # Tentar login sem preencher campos
        login_page.click_login()
        
        # Verificar que não redirecionou
        assert "/login" in driver.current_url
    
    def test_logout_functionality(self, driver, base_url, login_user):
        """Teste de logout"""
        layout = Layout(driver)
        
        # Verificar que usuário está logado
        assert layout.is_user_logged_in()
        assert "/dashboard" in driver.current_url
        
        # Fazer logout
        layout.click_logout()
        
        # Verificar redirecionamento para login
        assert "/login" in driver.current_url
        
        # Tentar acessar dashboard sem login
        driver.get(f"{base_url}/dashboard")
        
        # Deve redirecionar para login
        assert "/login" in driver.current_url
    
    def test_register_new_user(self, driver, base_url, wait_for_app, clean_storage):
        """Teste de registro de novo usuário"""
        register_page = RegisterPage(driver)
        
        # Navegar para página de registro
        register_page.navigate_to(base_url)
        
        # Verificar se dica de senha está visível
        assert register_page.is_password_hint_visible()
        
        # Registrar novo usuário com dados únicos
        import time
        timestamp = str(int(time.time()))
        email = f"teste{timestamp}@test.com"
        
        register_page.register(
            name=f"Usuário Teste {timestamp}",
            email=email,
            password="123456"
        )
        
        # Verificar redirecionamento para dashboard
        assert register_page.wait_for_redirect_to_dashboard()
    
    def test_register_with_existing_email(self, driver, base_url, wait_for_app, clean_storage):
        """Teste de registro com email já existente"""
        register_page = RegisterPage(driver)
        
        # Navegar para página de registro
        register_page.navigate_to(base_url)
        
        # Tentar registrar com email já existente
        register_page.register(
            name="Outro Usuário",
            email="admin@test.com",  # Email já existe
            password="123456"
        )
        
        # Verificar mensagem de erro
        error_message = register_page.get_error_message()
        assert error_message is not None
        assert "já está em uso" in error_message or "já existe" in error_message.lower()
    
    def test_navigation_between_login_and_register(self, driver, base_url, wait_for_app, clean_storage):
        """Teste de navegação entre páginas de login e registro"""
        login_page = LoginPage(driver)
        register_page = RegisterPage(driver)
        
        # Começar na página de login
        login_page.navigate_to(base_url)
        assert "/login" in driver.current_url
        
        # Navegar para registro
        login_page.click_register_link()
        assert "/register" in driver.current_url
        
        # Voltar para login
        register_page.click_login_link()
        assert "/login" in driver.current_url
    
    def test_authentication_redirect(self, driver, base_url, wait_for_app, clean_storage):
        """Teste de redirecionamento automático quando não autenticado"""
        # Tentar acessar páginas protegidas sem login
        protected_pages = ["/dashboard", "/treinos", "/profile"]
        
        for page in protected_pages:
            driver.get(f"{base_url}{page}")
            
            # Deve redirecionar para login
            assert "/login" in driver.current_url
    
    def test_auto_redirect_when_logged_in(self, driver, base_url, login_user):
        """Teste de redirecionamento automático quando já logado"""
        # Tentar acessar páginas de auth quando já logado
        auth_pages = ["/login", "/register"]
        
        for page in auth_pages:
            driver.get(f"{base_url}{page}")
            
            # Deve redirecionar para dashboard
            assert "/dashboard" in driver.current_url 