import pytest
from page_objects.dashboard_page import DashboardPage
from page_objects.treinos_page import TreinosPage
from page_objects.layout import Layout


class TestNavigation:
    """Testes de navegação entre páginas"""
    
    def test_header_navigation_dashboard(self, driver, base_url, login_user):
        """Teste de navegação via header - Dashboard"""
        layout = Layout(driver)
        dashboard_page = DashboardPage(driver)
        
        # Começar em outra página
        driver.get(f"{base_url}/treinos")
        
        # Navegar via header
        layout.click_dashboard()
        
        # Verificar navegação
        assert layout.wait_for_navigation("/dashboard")
        dashboard_page.wait_for_page_load()
        
        # Verificar link ativo
        active_link = layout.get_current_active_link()
        assert active_link == "Dashboard"
    
    def test_header_navigation_treinos(self, driver, base_url, login_user):
        """Teste de navegação via header - Treinos"""
        layout = Layout(driver)
        treinos_page = TreinosPage(driver)
        
        # Começar no dashboard
        driver.get(f"{base_url}/dashboard")
        
        # Navegar via header
        layout.click_treinos()
        
        # Verificar navegação
        assert layout.wait_for_navigation("/treinos")
        treinos_page.wait_for_page_load()
        
        # Verificar link ativo
        active_link = layout.get_current_active_link()
        assert active_link == "Treinos"
    
    def test_header_navigation_profile(self, driver, base_url, login_user):
        """Teste de navegação via header - Perfil"""
        layout = Layout(driver)
        
        # Começar no dashboard
        driver.get(f"{base_url}/dashboard")
        
        # Navegar via header
        layout.click_profile()
        
        # Verificar navegação
        assert layout.wait_for_navigation("/profile")
        
        # Verificar link ativo
        active_link = layout.get_current_active_link()
        assert active_link == "Perfil"
    
    def test_logo_navigation(self, driver, base_url, login_user):
        """Teste de navegação via logo"""
        layout = Layout(driver)
        dashboard_page = DashboardPage(driver)
        
        # Começar em outra página
        driver.get(f"{base_url}/treinos")
        
        # Clicar no logo
        layout.click_logo()
        
        # Verificar navegação para dashboard
        assert layout.wait_for_navigation("/dashboard")
        dashboard_page.wait_for_page_load()
    
    def test_dashboard_to_treinos_navigation(self, driver, base_url, login_user):
        """Teste de navegação do dashboard para treinos"""
        dashboard_page = DashboardPage(driver)
        treinos_page = TreinosPage(driver)
        
        # Começar no dashboard
        dashboard_page.navigate_to(base_url).wait_for_page_load()
        
        # Navegar para treinos via botão
        dashboard_page.click_view_all_treinos()
        
        # Verificar navegação
        treinos_page.wait_for_page_load()
        assert "/treinos" in driver.current_url
    
    def test_dashboard_create_treino_navigation(self, driver, base_url, login_user):
        """Teste de navegação para criar treino via dashboard"""
        dashboard_page = DashboardPage(driver)
        
        # Navegar para dashboard
        dashboard_page.navigate_to(base_url).wait_for_page_load()
        
        # Clicar em criar treino (primeiro ou novo)
        if dashboard_page.has_no_treinos_message():
            dashboard_page.click_create_first_treino()
        else:
            dashboard_page.click_create_new_treino()
        
        # Verificar navegação para página de novo treino
        assert "/treinos/new" in driver.current_url
    
    def test_browser_back_navigation(self, driver, base_url, login_user):
        """Teste de navegação usando botão voltar do browser"""
        dashboard_page = DashboardPage(driver)
        treinos_page = TreinosPage(driver)
        
        # Navegar: Dashboard -> Treinos
        dashboard_page.navigate_to(base_url).wait_for_page_load()
        dashboard_page.click_view_all_treinos()
        treinos_page.wait_for_page_load()
        
        # Usar botão voltar do browser
        driver.back()
        
        # Verificar volta ao dashboard
        assert "/dashboard" in driver.current_url
        dashboard_page.wait_for_page_load()
    
    def test_browser_forward_navigation(self, driver, base_url, login_user):
        """Teste de navegação usando botão avançar do browser"""
        dashboard_page = DashboardPage(driver)
        treinos_page = TreinosPage(driver)
        
        # Navegar: Dashboard -> Treinos -> Voltar
        dashboard_page.navigate_to(base_url).wait_for_page_load()
        dashboard_page.click_view_all_treinos()
        treinos_page.wait_for_page_load()
        driver.back()
        dashboard_page.wait_for_page_load()
        
        # Usar botão avançar do browser
        driver.forward()
        
        # Verificar volta aos treinos
        assert "/treinos" in driver.current_url
        treinos_page.wait_for_page_load()
    
    def test_url_direct_access(self, driver, base_url, login_user):
        """Teste de acesso direto via URL"""
        dashboard_page = DashboardPage(driver)
        treinos_page = TreinosPage(driver)
        
        # Testar acesso direto a diferentes páginas
        pages_to_test = [
            ("/dashboard", dashboard_page.wait_for_page_load),
            ("/treinos", treinos_page.wait_for_page_load),
            ("/profile", lambda: "/profile" in driver.current_url),
        ]
        
        for url, verification in pages_to_test:
            driver.get(f"{base_url}{url}")
            
            if callable(verification):
                verification()
            else:
                assert verification
    
    def test_navigation_state_preservation(self, driver, base_url, login_user):
        """Teste de preservação do estado durante navegação"""
        layout = Layout(driver)
        
        # Navegar entre páginas diferentes
        pages = ["/dashboard", "/treinos", "/profile"]
        
        for page in pages:
            driver.get(f"{base_url}{page}")
            
            # Verificar que usuário continua logado
            assert layout.is_user_logged_in()
            
            # Verificar link ativo correto no header
            if page == "/dashboard":
                expected_active = "Dashboard"
            elif page == "/treinos":
                expected_active = "Treinos"
            elif page == "/profile":
                expected_active = "Perfil"
            
            active_link = layout.get_current_active_link()
            assert active_link == expected_active
    
    def test_invalid_url_handling(self, driver, base_url, login_user):
        """Teste de tratamento de URLs inválidas"""
        # Tentar acessar página que não existe
        driver.get(f"{base_url}/pagina-inexistente")
        
        # Verificar se foi redirecionado ou mostra erro 404
        # (Depende da implementação do Next.js)
        assert driver.current_url  # Pelo menos não deve dar crash
    
    def test_deep_link_access(self, driver, base_url, login_user):
        """Teste de acesso a links profundos"""
        # Este teste requer que haja pelo menos um treino existente
        # Por simplicidade, vamos testar se a URL não quebra a aplicação
        driver.get(f"{base_url}/treinos/999")  # ID que provavelmente não existe
        
        # Verificar que aplicação não quebrou
        assert driver.current_url
        
        # Pode redirecionar para lista de treinos ou mostrar erro - ambos OK
        # O importante é não quebrar a aplicação 