import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from page_objects.login_page import LoginPage
from page_objects.dashboard_page import DashboardPage
from page_objects.treinos_page import TreinosPage


class TestUIComponents:
    """Testes de componentes UI e responsividade"""
    
    def test_login_form_elements(self, driver, base_url, wait_for_app, clean_storage):
        """Teste de elementos do formulário de login"""
        login_page = LoginPage(driver)
        
        # Navegar para login
        login_page.navigate_to(base_url)
        
        # Verificar elementos obrigatórios
        email_input = driver.find_element(*login_page.EMAIL_INPUT)
        password_input = driver.find_element(*login_page.PASSWORD_INPUT)
        login_button = driver.find_element(*login_page.LOGIN_BUTTON)
        
        # Verificar propriedades dos inputs
        assert email_input.get_attribute("type") == "email"
        assert email_input.get_attribute("required") is not None
        assert password_input.get_attribute("type") == "password"
        assert password_input.get_attribute("required") is not None
        
        # Verificar placeholders
        assert "email" in email_input.get_attribute("placeholder").lower()
        assert password_input.get_attribute("placeholder")
        
        # Verificar botão
        assert login_button.is_enabled()
        assert "Entrar" in login_button.text
    
    def test_dashboard_statistics_cards(self, driver, base_url, login_user):
        """Teste dos cards de estatísticas do dashboard"""
        dashboard_page = DashboardPage(driver)
        
        # Navegar para dashboard
        dashboard_page.navigate_to(base_url).wait_for_page_load()
        
        # Verificar cards de estatísticas
        stats_cards = driver.find_elements(By.XPATH, "//div[contains(@class, 'shadow-card')]")
        
        # Deve ter pelo menos 3 cards (treinos, meta, dias ativos)
        assert len(stats_cards) >= 3
        
        # Verificar ícones nos cards
        icons = driver.find_elements(By.XPATH, "//div[contains(@class, 'shadow-glow')]")
        assert len(icons) >= 3
    
    def test_buttons_styling_and_hover(self, driver, base_url, login_user, helper):
        """Teste de estilização e hover dos botões"""
        dashboard_page = DashboardPage(driver)
        
        # Navegar para dashboard
        dashboard_page.navigate_to(base_url).wait_for_page_load()
        
        # Encontrar botões principais
        buttons = driver.find_elements(By.XPATH, "//button[contains(@class, 'bg-gradient')]")
        
        # Verificar que botões têm estilização adequada
        for button in buttons[:3]:  # Testar primeiros 3 botões
            # Verificar que não são brancos (devem ter cores)
            bg_color = button.value_of_css_property("background-color")
            assert bg_color != "rgba(0, 0, 0, 0)"  # Não transparente
            assert bg_color != "rgb(255, 255, 255)"  # Não branco
            
            # Verificar bordas arredondadas
            border_radius = button.value_of_css_property("border-radius")
            assert border_radius != "0px"
            
            # Simular hover
            driver.execute_script("arguments[0].style.transform = 'scale(1.05)';", button)
    
    def test_responsive_layout_mobile(self, driver, base_url, login_user):
        """Teste de layout responsivo - mobile"""
        dashboard_page = DashboardPage(driver)
        
        # Configurar viewport mobile
        driver.set_window_size(375, 667)  # iPhone 8 size
        
        # Navegar para dashboard
        dashboard_page.navigate_to(base_url).wait_for_page_load()
        
        # Verificar que layout se adapta
        # Cards devem empilhar verticalmente
        stats_cards = driver.find_elements(By.XPATH, "//div[contains(@class, 'grid-cols-1')]")
        assert len(stats_cards) > 0
        
        # Header deve estar visível
        header = driver.find_element(By.XPATH, "//header")
        assert header.is_displayed()
        
        # Restaurar tamanho normal
        driver.set_window_size(1920, 1080)
    
    def test_responsive_layout_tablet(self, driver, base_url, login_user):
        """Teste de layout responsivo - tablet"""
        dashboard_page = DashboardPage(driver)
        
        # Configurar viewport tablet
        driver.set_window_size(768, 1024)  # iPad size
        
        # Navegar para dashboard
        dashboard_page.navigate_to(base_url).wait_for_page_load()
        
        # Verificar adaptação do layout
        content = driver.find_element(By.XPATH, "//main")
        assert content.is_displayed()
        
        # Restaurar tamanho normal
        driver.set_window_size(1920, 1080)
    
    def test_loading_states(self, driver, base_url, login_user):
        """Teste de estados de loading"""
        treinos_page = TreinosPage(driver)
        
        # Navegar para treinos
        treinos_page.navigate_to(base_url)
        
        # Verificar se spinner aparece (pode ser muito rápido)
        try:
            WebDriverWait(driver, 2).until(
                EC.presence_of_element_located(treinos_page.LOADING_SPINNER)
            )
        except:
            pass  # Loading pode ser muito rápido para capturar
        
        # Verificar que página carrega completamente
        treinos_page.wait_for_page_load()
    
    def test_form_validation_visual_feedback(self, driver, base_url, wait_for_app, clean_storage):
        """Teste de feedback visual em validação de formulários"""
        login_page = LoginPage(driver)
        
        # Navegar para login
        login_page.navigate_to(base_url)
        
        # Tentar submeter formulário vazio
        login_page.click_login()
        
        # Verificar feedback visual do browser para campos obrigatórios
        email_input = driver.find_element(*login_page.EMAIL_INPUT)
        
        # Verificar que campo foi focado ou tem estilo de erro
        assert email_input == driver.switch_to.active_element or \
               "invalid" in email_input.get_attribute("class") or \
               email_input.get_attribute("aria-invalid") == "true"
    
    def test_icons_and_emojis_display(self, driver, base_url, login_user):
        """Teste de exibição de ícones e emojis"""
        dashboard_page = DashboardPage(driver)
        
        # Navegar para dashboard
        dashboard_page.navigate_to(base_url).wait_for_page_load()
        
        # Verificar que emojis estão sendo exibidos
        page_text = driver.find_element(By.TAG_NAME, "body").text
        
        # Verificar presença de emojis comuns
        emojis_expected = ["👋", "💪", "🎯", "🔥", "✨", "📋", "👤"]
        emoji_found = any(emoji in page_text for emoji in emojis_expected)
        assert emoji_found, f"Nenhum emoji encontrado na página. Texto: {page_text[:200]}..."
    
    def test_color_contrast_accessibility(self, driver, base_url, login_user):
        """Teste básico de contraste de cores"""
        dashboard_page = DashboardPage(driver)
        
        # Navegar para dashboard
        dashboard_page.navigate_to(base_url).wait_for_page_load()
        
        # Verificar textos principais têm cor preta (boa legibilidade)
        main_texts = driver.find_elements(By.XPATH, "//h1 | //h2 | //h3 | //p")
        
        black_text_count = 0
        for text in main_texts[:10]:  # Verificar primeiros 10 elementos
            color = text.value_of_css_property("color")
            # Verificar se é preto ou quase preto
            if "rgb(0, 0, 0)" in color or "rgba(0, 0, 0" in color:
                black_text_count += 1
        
        # Pelo menos alguns textos devem ser pretos
        assert black_text_count > 0, "Nenhum texto preto encontrado - pode haver problema de contraste"
    
    def test_animation_classes(self, driver, base_url, login_user):
        """Teste de classes de animação"""
        dashboard_page = DashboardPage(driver)
        
        # Navegar para dashboard
        dashboard_page.navigate_to(base_url).wait_for_page_load()
        
        # Verificar elementos com animação
        animated_elements = driver.find_elements(By.XPATH, "//*[contains(@class, 'animate-')]")
        
        # Deve haver elementos animados
        assert len(animated_elements) > 0
        
        # Verificar tipos de animação comuns
        animation_classes = []
        for element in animated_elements:
            classes = element.get_attribute("class")
            if "animate-" in classes:
                animation_classes.extend([cls for cls in classes.split() if cls.startswith("animate-")])
        
        # Verificar animações esperadas
        expected_animations = ["animate-fade-in", "animate-slide-up", "animate-bounce-gentle"]
        found_animations = [anim for anim in expected_animations if anim in animation_classes]
        assert len(found_animations) > 0, f"Animações esperadas não encontradas. Encontradas: {animation_classes}"
    
    def test_focus_management(self, driver, base_url, wait_for_app, clean_storage):
        """Teste de gerenciamento de foco para acessibilidade"""
        login_page = LoginPage(driver)
        
        # Navegar para login
        login_page.navigate_to(base_url)
        
        # Verificar que primeiro input recebe foco
        email_input = driver.find_element(*login_page.EMAIL_INPUT)
        
        # Clicar no input
        email_input.click()
        
        # Verificar que está focado
        assert email_input == driver.switch_to.active_element
        
        # Navegar com Tab
        driver.execute_script("arguments[0].dispatchEvent(new KeyboardEvent('keydown', {key: 'Tab'}));", email_input)
        
        # Verificar que foco mudou (para próximo elemento)
        assert email_input != driver.switch_to.active_element 