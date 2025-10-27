"""
Tela de configurações do jogo
"""

import pygame
from constants import BLACK, WHITE, LIGHT_GRAY, GOLD, RED, LIGHT_BLUE
from ui_components import Button


class SettingsScreen:
    """
    Tela de configurações com opções de tamanho de tela e outras configurações
    """
    
    def __init__(self, screen, theme_system=None):
        self.screen = screen
        self.theme_system = theme_system
        self.font_title = pygame.font.Font(None, 64)
        self.font_text = pygame.font.Font(None, 40)
        self.font_small = pygame.font.Font(None, 32)
        
        # Tamanhos de tela com resoluções específicas
        self.screen_sizes = [
            {"name": "Pequeno", "size": (640, 480), "key": "small"},
            {"name": "Médio", "size": (1024, 768), "key": "medium"},
            {"name": "Grande", "size": (1600, 900), "key": "large"},
            {"name": "Tela Cheia", "size": (0, 0), "key": "fullscreen"}
        ]
        
        self.current_size_index = 1  # Médio por padrão
        self.is_fullscreen = False  # Janela normal por padrão
        self.current_theme = 'dark'  # Tema padrão
        
        # Criar botões
        self.buttons = self._create_buttons()
    
    def load_current_settings(self, settings):
        """Carrega as configurações atuais"""
        # Carregar fullscreen primeiro
        self.is_fullscreen = settings.get('fullscreen', True)
        
        # Verificar se é tela cheia real (width = 0)
        if settings.get('screen_width', 0) == 0:
            # Tela cheia real
            self.current_size_index = 3  # Índice do "Tela Cheia"
        else:
            # Tamanho específico
            screen_size = (settings.get('screen_width', 1024), settings.get('screen_height', 768))
            
            for i, size_info in enumerate(self.screen_sizes):
                if size_info['size'] == screen_size and size_info['key'] != 'fullscreen':
                    self.current_size_index = i
                    break
            else:
                # Se não encontrar, usar médio como padrão
                self.current_size_index = 1
        
        # Carregar tema
        self.current_theme = settings.get('theme', 'dark')
        
        # Recriar botões com as configurações atuais
        self.buttons = self._create_buttons()
        
        print(f"Configurações carregadas: tamanho={self.screen_sizes[self.current_size_index]['name']}, fullscreen={self.is_fullscreen}, tema={self.current_theme}")
        
    def _create_buttons(self):
        """Cria todos os botões da tela de configurações em layout vertical"""
        # Usar dimensões responsivas com fallback
        try:
            screen_w = self.screen.get_width()
            screen_h = self.screen.get_height()
        except:
            # Fallback se a tela não estiver pronta
            screen_w = 1280
            screen_h = 720
        
        # Botões responsivos baseados no tamanho da tela
        if screen_w < 800:
            button_width = min(120, screen_w // 10)
            button_height = 35
            spacing_x = 15
            spacing_y = 10
            left_section_x = screen_w // 8
            right_section_x = screen_w // 2 + 30
            center_x = screen_w // 2
            start_y = 160
        else:
            button_width = min(150, screen_w // 8)
            button_height = 45
            spacing_x = 20
            spacing_y = 15
            left_section_x = screen_w // 6
            right_section_x = screen_w // 2 + 50
            center_x = screen_w // 2
            start_y = 180
        buttons = {}
        
        # === SEÇÃO ESQUERDA: TAMANHOS DE TELA ===
        for i, size_info in enumerate(self.screen_sizes):
            x_pos = left_section_x + (i % 2) * (button_width + spacing_x)
            y_pos = start_y + (i // 2) * (button_height + spacing_y)
            buttons[f"size_{size_info['key']}"] = Button(
                x_pos, y_pos, button_width, button_height,
                size_info['name'], self.font_small,
                LIGHT_GRAY, WHITE, BLACK
            )
        
        
        # === SEÇÃO DIREITA: TEMA ===
        theme_y = start_y
        buttons['theme_dark'] = Button(
            right_section_x, theme_y, button_width, button_height,
            'Tema Escuro', self.font_small,
            LIGHT_GRAY, WHITE, BLACK
        )
        
        buttons['theme_light'] = Button(
            right_section_x + button_width + spacing_x, theme_y, button_width, button_height,
            'Tema Claro', self.font_small,
            LIGHT_GRAY, WHITE, BLACK
        )
        
        # === BOTÕES DE AÇÃO (CENTRO) ===
        action_y = screen_h - 120
        buttons['apply'] = Button(
            center_x - button_width - spacing_x//2, action_y, button_width, button_height,
            'Aplicar', self.font_text,
            GOLD, WHITE, BLACK
        )
        
        buttons['back'] = Button(
            center_x + spacing_x//2, action_y, button_width, button_height,
            'Voltar', self.font_text,
            RED, WHITE, BLACK
        )
        
        return buttons
    
    def handle_event(self, event):
        """Processa eventos da tela de configurações"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button_name, button in self.buttons.items():
                if button.handle_event(event):
                    if button_name.startswith('size_'):
                        # Atualizar seleção de tamanho
                        size_key = button_name.replace('size_', '')
                        for i, size_info in enumerate(self.screen_sizes):
                            if size_info['key'] == size_key:
                                self.current_size_index = i
                                # Apenas "Tela Cheia" é fullscreen
                                self.is_fullscreen = (size_key == 'fullscreen')
                                break
                        return None
                    elif button_name == 'theme_dark':
                        self.current_theme = 'dark'
                        return None
                    elif button_name == 'theme_light':
                        self.current_theme = 'light'
                        return None
                    elif button_name == 'apply':
                        return {
                            'action': 'apply_settings',
                            'settings': self.get_current_settings()
                        }
                    elif button_name == 'back':
                        return 'back'
        
        return None
    
    def get_current_settings(self):
        """Retorna as configurações atuais"""
        current_size = self.screen_sizes[self.current_size_index]
        
        if current_size['key'] == 'fullscreen':
            # Tela cheia real - usar toda a tela disponível
            return {
                'screen_width': 0,  # 0 indica tela cheia real
                'screen_height': 0,
                'fullscreen': True,
                'theme': self.current_theme
            }
        else:
            # Tamanho específico com resolução (janela normal)
            return {
                'screen_width': current_size['size'][0],
                'screen_height': current_size['size'][1],
                'fullscreen': False,  # Janela normal
                'theme': self.current_theme
            }
    
    def update_layout(self):
        """Atualiza o layout quando a tela é redimensionada"""
        self.buttons = self._create_buttons()
    
    def draw(self):
        """Desenha a tela de configurações"""
        # Usar dimensões responsivas com fallback
        try:
            screen_w = self.screen.get_width()
            screen_h = self.screen.get_height()
        except:
            # Fallback se a tela não estiver pronta
            screen_w = 1280
            screen_h = 720
        
        # Usar cores do tema se disponível
        if self.theme_system:
            bg_color = self.theme_system.get_color('background')
            title_color = self.theme_system.get_color('text_primary')
            subtitle_color = self.theme_system.get_color('text_secondary')
        else:
            bg_color = (20, 24, 28)
            title_color = GOLD
            subtitle_color = WHITE
        
        # Fundo
        self.screen.fill(bg_color)
        
        # Título centralizado
        title = self.font_title.render("Configurações", True, title_color)
        title_rect = title.get_rect(center=(screen_w // 2, 80))
        self.screen.blit(title, title_rect)
        
        # Subtítulos alinhados com as opções
        # Tamanho da tela (esquerda) - alinhado com os botões
        left_section_x = screen_w // 6 if screen_w >= 800 else screen_w // 8
        subtitle1 = self.font_text.render("Tamanho da Tela", True, subtitle_color)
        subtitle1_rect = subtitle1.get_rect(center=(left_section_x + 75, 140))  # 75px = metade da largura do botão
        self.screen.blit(subtitle1, subtitle1_rect)
        
        # Tema (direita) - alinhado com os botões
        right_section_x = screen_w // 2 + 50 if screen_w >= 800 else screen_w // 2 + 30
        subtitle2 = self.font_text.render("Tema", True, subtitle_color)
        subtitle2_rect = subtitle2.get_rect(center=(right_section_x + 75, 140))  # 75px = metade da largura do botão
        self.screen.blit(subtitle2, subtitle2_rect)
        
        # Desenhar botões de tamanho
        for i, (button_name, button) in enumerate(self.buttons.items()):
            if button_name.startswith('size_'):
                # Destacar o tamanho selecionado
                if i == self.current_size_index:
                    button.color = GOLD
                    button.hover_color = WHITE
                else:
                    button.color = LIGHT_GRAY
                    button.hover_color = WHITE
            elif button_name == 'fullscreen':
                # Destacar se tela cheia está ativada
                if self.is_fullscreen:
                    button.color = GOLD
                    button.hover_color = WHITE
                else:
                    button.color = LIGHT_GRAY
                    button.hover_color = WHITE
            elif button_name == 'theme_dark':
                # Destacar se tema escuro está selecionado
                if self.current_theme == 'dark':
                    button.color = GOLD
                    button.hover_color = WHITE
                else:
                    button.color = LIGHT_GRAY
                    button.hover_color = WHITE
            elif button_name == 'theme_light':
                # Destacar se tema claro está selecionado
                if self.current_theme == 'light':
                    button.color = GOLD
                    button.hover_color = WHITE
                else:
                    button.color = LIGHT_GRAY
                    button.hover_color = WHITE
            
            button.draw(self.screen)
        
        # Informações adicionais (canto inferior esquerdo)
        info_x = 50
        info_y = screen_h - 150
        info_text = self.font_small.render("Controles:", True, WHITE)
        self.screen.blit(info_text, (info_x, info_y))
        
        controls = [
            "ESC - Voltar ao jogo",
            "Aplicar - Salvar configurações",
            "Voltar - Retornar à tela anterior"
        ]
        
        for i, control in enumerate(controls):
            control_text = self.font_small.render(control, True, LIGHT_GRAY)
            self.screen.blit(control_text, (info_x + 20, info_y + 25 + i * 20))
        
        # Mostrar configuração atual (canto inferior direito)
        current_settings = self.get_current_settings()
        theme_name = "Escuro" if current_settings['theme'] == 'dark' else "Claro"
        current_text = self.font_small.render(
            f"Atual: {current_settings['screen_width']}x{current_settings['screen_height']} {'(Tela Cheia)' if current_settings['fullscreen'] else ''} | Tema: {theme_name}",
            True, GOLD
        )
        current_rect = current_text.get_rect(bottomright=(screen_w - 50, screen_h - 50))
        self.screen.blit(current_text, current_rect)
