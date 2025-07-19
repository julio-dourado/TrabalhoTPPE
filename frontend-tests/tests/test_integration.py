import pytest
import time
from page_objects.login_page import LoginPage
from page_objects.register_page import RegisterPage
from page_objects.dashboard_page import DashboardPage
from page_objects.treinos_page import TreinosPage
from page_objects.new_treino_page import NewTreinoPage
from page_objects.layout import Layout


class TestIntegration:
    """Testes de integração end-to-end"""
    
    def test_complete_user_journey_new_user(self, driver, base_url, wait_for_app, clean_storage):
        """Teste completo da jornada de um novo usuário"""
        register_page = RegisterPage(driver)
        dashboard_page = DashboardPage(driver)
        treinos_page = TreinosPage(driver)
        new_treino_page = NewTreinoPage(driver)
        layout = Layout(driver)
        
        # 1. Registrar novo usuário
        timestamp = str(int(time.time()))
        user_data = {
            "name": f"Usuário Teste {timestamp}",
            "email": f"teste{timestamp}@integration.com",
            "password": "123456"
        }
        
        register_page.navigate_to(base_url)
        register_page.register(user_data["name"], user_data["email"], user_data["password"])
        register_page.wait_for_redirect_to_dashboard()
        
        # 2. Verificar dashboard vazio
        dashboard_page.wait_for_page_load()
        assert user_data["name"].split()[0] in dashboard_page.get_greeting_text()
        assert dashboard_page.has_no_treinos_message()
        
        # 3. Criar primeiro treino
        dashboard_page.click_create_first_treino()
        
        treino_name = f"Meu Primeiro Treino {timestamp}"
        treino_desc = "Treino de integração completo"
        
        new_treino_page.wait_for_page_load()
        new_treino_page.create_treino(treino_name, treino_desc)
        new_treino_page.wait_for_redirect_to_treinos()
        
        # 4. Verificar treino na lista
        treinos_page.wait_for_page_load()
        treinos = treinos_page.get_treino_cards()
        assert treino_name in treinos
        
        # 5. Navegar de volta ao dashboard
        layout.click_dashboard()
        dashboard_page.wait_for_page_load()
        
        # 6. Verificar que dashboard agora mostra o treino
        assert not dashboard_page.has_no_treinos_message()
        dashboard_treinos = dashboard_page.get_treino_items()
        assert len(dashboard_treinos) > 0
        
        # 7. Fazer logout
        layout.click_logout()
        assert "/login" in driver.current_url
    
    def test_complete_user_journey_existing_user(self, driver, base_url, login_user):
        """Teste completo da jornada de usuário existente"""
        dashboard_page = DashboardPage(driver)
        treinos_page = TreinosPage(driver)
        new_treino_page = NewTreinoPage(driver)
        layout = Layout(driver)
        
        # 1. Verificar dashboard do usuário logado
        dashboard_page.navigate_to(base_url).wait_for_page_load()
        initial_greeting = dashboard_page.get_greeting_text()
        assert "Olá," in initial_greeting
        
        # 2. Contar treinos existentes
        initial_treinos = dashboard_page.get_treino_items()
        initial_count = len(initial_treinos)
        
        # 3. Criar novo treino
        if dashboard_page.has_no_treinos_message():
            dashboard_page.click_create_first_treino()
        else:
            dashboard_page.click_create_new_treino()
        
        timestamp = str(int(time.time()))
        treino_name = f"Treino Integração {timestamp}"
        
        new_treino_page.wait_for_page_load()
        new_treino_page.create_treino(treino_name, "Descrição de teste")
        new_treino_page.wait_for_redirect_to_treinos()
        
        # 4. Verificar na página de treinos
        treinos_page.wait_for_page_load()
        page_treinos = treinos_page.get_treino_cards()
        assert treino_name in page_treinos
        
        # 5. Voltar ao dashboard e verificar atualização
        layout.click_dashboard()
        dashboard_page.wait_for_page_load()
        
        updated_treinos = dashboard_page.get_treino_items()
        assert len(updated_treinos) == initial_count + 1
        
        # 6. Testar navegação entre todas as páginas
        pages_to_test = [
            (layout.click_treinos, "/treinos"),
            (layout.click_profile, "/profile"),
            (layout.click_dashboard, "/dashboard")
        ]
        
        for nav_action, expected_url in pages_to_test:
            nav_action()
            assert expected_url in driver.current_url
    
    def test_crud_treino_complete_flow(self, driver, base_url, login_user):
        """Teste completo do fluxo CRUD de treinos"""
        treinos_page = TreinosPage(driver)
        new_treino_page = NewTreinoPage(driver)
        layout = Layout(driver)
        
        # 1. Ir para página de treinos
        treinos_page.navigate_to(base_url).wait_for_page_load()
        initial_count = treinos_page.get_treino_count()
        
        # 2. CREATE - Criar novo treino
        timestamp = str(int(time.time()))
        treino_name = f"Treino CRUD {timestamp}"
        
        if treinos_page.has_no_treinos_message():
            treinos_page.click_create_first_treino()
        else:
            treinos_page.click_create_treino()
        
        new_treino_page.wait_for_page_load()
        new_treino_page.create_treino(treino_name, "Teste CRUD completo")
        new_treino_page.wait_for_redirect_to_treinos()
        
        # 3. READ - Verificar treino criado
        treinos_page.wait_for_page_load()
        treinos = treinos_page.get_treino_cards()
        assert treino_name in treinos
        assert treinos_page.get_treino_count() == initial_count + 1
        
        # 4. VIEW - Visualizar detalhes do treino
        treino_index = treinos.index(treino_name)
        treinos_page.click_treino_card(treino_index)
        assert "/treinos/" in driver.current_url
        
        # 5. Voltar para lista
        layout.click_treinos()
        treinos_page.wait_for_page_load()
        
        # 6. DELETE - Deletar o treino
        treinos = treinos_page.get_treino_cards()
        treino_index = treinos.index(treino_name)
        
        treinos_page.click_delete_treino(treino_index)
        treinos_page.confirm_delete()
        treinos_page.wait_for_treino_deleted(len(treinos))
        
        # 7. Verificar remoção
        final_treinos = treinos_page.get_treino_cards()
        assert treino_name not in final_treinos
        assert treinos_page.get_treino_count() == initial_count
    
    def test_session_persistence_across_navigation(self, driver, base_url, login_user):
        """Teste de persistência de sessão durante navegação"""
        dashboard_page = DashboardPage(driver)
        treinos_page = TreinosPage(driver)
        layout = Layout(driver)
        
        # 1. Verificar estado inicial logado
        dashboard_page.navigate_to(base_url).wait_for_page_load()
        initial_greeting = dashboard_page.get_greeting_text()
        
        # 2. Navegar entre várias páginas
        navigation_sequence = [
            (layout.click_treinos, treinos_page.wait_for_page_load),
            (layout.click_profile, lambda: "/profile" in driver.current_url),
            (layout.click_dashboard, dashboard_page.wait_for_page_load)
        ]
        
        for nav_action, verification in navigation_sequence:
            nav_action()
            verification()
            
            # Verificar que usuário continua logado
            assert layout.is_user_logged_in()
        
        # 3. Verificar que dados persistem
        final_greeting = dashboard_page.get_greeting_text()
        assert final_greeting == initial_greeting
    
    def test_error_handling_and_recovery(self, driver, base_url, login_user):
        """Teste de tratamento de erros e recuperação"""
        treinos_page = TreinosPage(driver)
        new_treino_page = NewTreinoPage(driver)
        
        # 1. Tentar criar treino com dados inválidos
        new_treino_page.navigate_to(base_url).wait_for_page_load()
        
        # Tentar criar sem nome (validação client-side)
        new_treino_page.enter_description("Apenas descrição")
        new_treino_page.click_create()
        
        # Verificar que permanece na página
        assert "/new" in driver.current_url
        
        # 2. Corrigir e criar corretamente
        timestamp = str(int(time.time()))
        treino_name = f"Treino Recuperado {timestamp}"
        new_treino_page.enter_name(treino_name)
        new_treino_page.click_create()
        
        # Verificar sucesso
        new_treino_page.wait_for_redirect_to_treinos()
        treinos_page.wait_for_page_load()
        
        treinos = treinos_page.get_treino_cards()
        assert treino_name in treinos
    
    def test_multiple_browser_tabs_session(self, driver, base_url, login_user):
        """Teste de comportamento com múltiplas abas"""
        dashboard_page = DashboardPage(driver)
        
        # 1. Estado inicial
        dashboard_page.navigate_to(base_url).wait_for_page_load()
        initial_greeting = dashboard_page.get_greeting_text()
        
        # 2. Abrir nova aba
        driver.execute_script("window.open('');")
        tabs = driver.window_handles
        assert len(tabs) == 2
        
        # 3. Alternar para nova aba
        driver.switch_to.window(tabs[1])
        
        # 4. Navegar na nova aba
        dashboard_page.navigate_to(base_url).wait_for_page_load()
        second_tab_greeting = dashboard_page.get_greeting_text()
        
        # 5. Verificar que sessão funciona em ambas as abas
        assert second_tab_greeting == initial_greeting
        
        # 6. Fechar segunda aba
        driver.close()
        driver.switch_to.window(tabs[0])
        
        # 7. Verificar que primeira aba ainda funciona
        driver.refresh()
        dashboard_page.wait_for_page_load()
        final_greeting = dashboard_page.get_greeting_text()
        assert final_greeting == initial_greeting
    
    def test_data_consistency_across_pages(self, driver, base_url, login_user):
        """Teste de consistência de dados entre páginas"""
        dashboard_page = DashboardPage(driver)
        treinos_page = TreinosPage(driver)
        new_treino_page = NewTreinoPage(driver)
        layout = Layout(driver)
        
        # 1. Contar treinos no dashboard
        dashboard_page.navigate_to(base_url).wait_for_page_load()
        dashboard_treinos = dashboard_page.get_treino_items()
        dashboard_count = len(dashboard_treinos)
        
        # 2. Contar treinos na página de treinos
        layout.click_treinos()
        treinos_page.wait_for_page_load()
        page_treinos = treinos_page.get_treino_cards()
        page_count = len(page_treinos)
        
        # 3. Verificar consistência
        assert dashboard_count == page_count, f"Dashboard: {dashboard_count}, Página: {page_count}"
        
        # 4. Criar novo treino
        timestamp = str(int(time.time()))
        treino_name = f"Treino Consistência {timestamp}"
        
        if treinos_page.has_no_treinos_message():
            treinos_page.click_create_first_treino()
        else:
            treinos_page.click_create_treino()
        
        new_treino_page.wait_for_page_load()
        new_treino_page.create_treino(treino_name)
        new_treino_page.wait_for_redirect_to_treinos()
        
        # 5. Verificar atualização na página
        treinos_page.wait_for_page_load()
        updated_page_treinos = treinos_page.get_treino_cards()
        assert len(updated_page_treinos) == page_count + 1
        assert treino_name in updated_page_treinos
        
        # 6. Verificar atualização no dashboard
        layout.click_dashboard()
        dashboard_page.wait_for_page_load()
        
        updated_dashboard_treinos = dashboard_page.get_treino_items()
        assert len(updated_dashboard_treinos) == dashboard_count + 1 