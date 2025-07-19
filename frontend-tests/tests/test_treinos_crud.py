import pytest
import time
from page_objects.dashboard_page import DashboardPage
from page_objects.treinos_page import TreinosPage
from page_objects.new_treino_page import NewTreinoPage


class TestTreinosCRUD:
    """Testes CRUD para treinos"""
    
    def test_create_first_treino_from_dashboard(self, driver, base_url, login_user):
        """Teste de criação do primeiro treino via dashboard"""
        dashboard_page = DashboardPage(driver)
        new_treino_page = NewTreinoPage(driver)
        
        # Navegar para dashboard
        dashboard_page.navigate_to(base_url).wait_for_page_load()
        
        # Se não há treinos, clicar em criar primeiro treino
        if dashboard_page.has_no_treinos_message():
            dashboard_page.click_create_first_treino()
        else:
            dashboard_page.click_create_new_treino()
        
        # Verificar redirecionamento para página de novo treino
        new_treino_page.wait_for_page_load()
        
        # Criar treino
        treino_name = f"Treino Teste {int(time.time())}"
        treino_desc = "Descrição do treino de teste"
        
        new_treino_page.create_treino(treino_name, treino_desc)
        
        # Verificar redirecionamento para lista de treinos
        new_treino_page.wait_for_redirect_to_treinos()
        
        # Verificar que treino foi criado
        treinos_page = TreinosPage(driver)
        treinos_page.wait_for_page_load()
        treinos = treinos_page.get_treino_cards()
        assert treino_name in treinos
    
    def test_create_treino_from_treinos_page(self, driver, base_url, login_user):
        """Teste de criação de treino via página de treinos"""
        treinos_page = TreinosPage(driver)
        new_treino_page = NewTreinoPage(driver)
        
        # Navegar para página de treinos
        treinos_page.navigate_to(base_url).wait_for_page_load()
        
        # Contar treinos existentes
        initial_count = treinos_page.get_treino_count()
        
        # Clicar em criar treino
        if treinos_page.has_no_treinos_message():
            treinos_page.click_create_first_treino()
        else:
            treinos_page.click_create_treino()
        
        # Criar treino
        treino_name = f"Novo Treino {int(time.time())}"
        new_treino_page.wait_for_page_load()
        new_treino_page.create_treino(treino_name, "Descrição detalhada do treino")
        
        # Verificar que treino foi adicionado
        new_treino_page.wait_for_redirect_to_treinos()
        treinos_page.wait_for_page_load()
        
        new_count = treinos_page.get_treino_count()
        assert new_count == initial_count + 1
        
        treinos = treinos_page.get_treino_cards()
        assert treino_name in treinos
    
    def test_create_treino_validation(self, driver, base_url, login_user):
        """Teste de validação na criação de treino"""
        new_treino_page = NewTreinoPage(driver)
        
        # Navegar para página de novo treino
        new_treino_page.navigate_to(base_url).wait_for_page_load()
        
        # Tentar criar treino sem nome
        new_treino_page.enter_description("Descrição sem nome")
        new_treino_page.click_create()
        
        # Verificar que permaneceu na mesma página (validação HTML5)
        assert "/treinos/new" in driver.current_url
    
    def test_cancel_treino_creation(self, driver, base_url, login_user):
        """Teste de cancelamento da criação de treino"""
        treinos_page = TreinosPage(driver)
        new_treino_page = NewTreinoPage(driver)
        
        # Navegar para treinos
        treinos_page.navigate_to(base_url).wait_for_page_load()
        initial_count = treinos_page.get_treino_count()
        
        # Ir para página de novo treino
        if treinos_page.has_no_treinos_message():
            treinos_page.click_create_first_treino()
        else:
            treinos_page.click_create_treino()
        
        # Preencher dados parciais
        new_treino_page.wait_for_page_load()
        new_treino_page.enter_name("Treino Cancelado")
        
        # Cancelar
        new_treino_page.click_cancel()
        
        # Verificar volta para página de treinos
        assert "/treinos" in driver.current_url and "/new" not in driver.current_url
        
        # Verificar que contagem não mudou
        treinos_page.wait_for_page_load()
        assert treinos_page.get_treino_count() == initial_count
    
     
    def test_view_treino_details(self, driver, base_url, login_user):
        """Teste de visualização de detalhes do treino"""
        treinos_page = TreinosPage(driver)
        
        # Criar um treino primeiro se necessário
        self._create_test_treino(driver, base_url)
        
        # Navegar para treinos
        treinos_page.navigate_to(base_url).wait_for_page_load()
        
        # Clicar no primeiro treino
        assert treinos_page.click_treino_card(0)
        
        # Verificar redirecionamento para detalhes
        assert "/treinos/" in driver.current_url
        assert driver.current_url.count("/") >= 4  # /treinos/{id}
    
    def test_treinos_page_navigation(self, driver, base_url, login_user):
        """Teste de navegação na página de treinos"""
        dashboard_page = DashboardPage(driver)
        treinos_page = TreinosPage(driver)
        
        # Navegar do dashboard para treinos
        dashboard_page.navigate_to(base_url).wait_for_page_load()
        dashboard_page.click_view_all_treinos()
        
        # Verificar página de treinos
        assert "/treinos" in driver.current_url
        treinos_page.wait_for_page_load()
    
    def _create_test_treino(self, driver, base_url):
        """Método auxiliar para criar treino de teste"""
        treinos_page = TreinosPage(driver)
        new_treino_page = NewTreinoPage(driver)
        
        treinos_page.navigate_to(base_url).wait_for_page_load()
        
        if treinos_page.has_no_treinos_message():
            treinos_page.click_create_first_treino()
        else:
            treinos_page.click_create_treino()
        
        treino_name = f"Treino Test {int(time.time())}"
        new_treino_page.wait_for_page_load()
        new_treino_page.create_treino(treino_name, "Treino para teste de exclusão")
        new_treino_page.wait_for_redirect_to_treinos()
    
    def test_back_navigation_from_new_treino(self, driver, base_url, login_user):
        """Teste de navegação de volta da página de novo treino"""
        treinos_page = TreinosPage(driver)
        new_treino_page = NewTreinoPage(driver)
        
        # Navegar para página de novo treino
        new_treino_page.navigate_to(base_url).wait_for_page_load()
        
        # Clicar em voltar
        new_treino_page.click_back()
        
        # Verificar volta para página de treinos
        assert "/treinos" in driver.current_url and "/new" not in driver.current_url
    
    def test_treinos_page_when_empty(self, driver, base_url, login_user):
        """Teste da página de treinos quando vazia"""
        treinos_page = TreinosPage(driver)
        
        # Navegar para treinos
        treinos_page.navigate_to(base_url).wait_for_page_load()
        
        # Se há treinos, este teste não se aplica
        if not treinos_page.has_no_treinos_message():
            pytest.skip("Teste não aplicável - usuário já tem treinos")
        
        # Verificar elementos da página vazia
        assert treinos_page.has_no_treinos_message()
        assert treinos_page.click_create_first_treino()  # Botão deve estar funcional 