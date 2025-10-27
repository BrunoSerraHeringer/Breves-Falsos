"""
Tela de pausa do jogo THE RESISTANCE
"""

import pygame
from constants import BLACK, WHITE, GOLD, RED, GREEN, LIGHT_GRAY, DARK_GRAY
from ui_components import Button


class PauseScreen:
    """
    Tela de pausa que aparece quando o jogo é pausado
    """
    
    def __init__(self, screen, theme_system=None):
        self.screen = screen
        self.theme_system = theme_system
        
        # Fontes
        self.font_title = pygame.font.Font(None, 64)
        self.font_text = pygame.font.Font(None, 40)
        self.font_small = pygame.font.Font(None, 32)
        
        # Botões
        self.buttons = self._create_buttons()
        
        # Estado anterior (para voltar)
        self.previous_state = None
    
    def _create_buttons(self):
        """Cria botões da tela de pausa"""
        screen_w = self.screen.get_width()
        screen_h = self.screen.get_height()
        
        button_width = 300
        button_height = 60
        center_x = screen_w // 2
        start_y = screen_h // 2 - 50
        spacing = 80
        
        return {
            'resume': Button(
                center_x - button_width // 2, start_y, button_width, button_height,
                'Continuar Jogo', self.font_text,
                GREEN, WHITE, BLACK
            ),
            'settings': Button(
                center_x - button_width // 2, start_y + spacing, button_width, button_height,
                'Configurações', self.font_text,
                LIGHT_GRAY, WHITE, BLACK
            ),
            'main_menu': Button(
                center_x - button_width // 2, start_y + spacing * 2, button_width, button_height,
                'Menu Principal', self.font_text,
                RED, WHITE, BLACK
            ),
        }
    
    def set_previous_state(self, state):
        """Define o estado anterior para voltar"""
        self.previous_state = state
    
    def handle_event(self, event):
        """Processa eventos da tela de pausa"""
        # Verificar ESC para continuar
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return 'resume'
        
        # Eventos do mouse
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button_name, button in self.buttons.items():
                if button.handle_event(event):
                    return button_name
        
        return None
    
    def draw(self):
        """Desenha a tela de pausa"""
        # Usar cor de fundo do tema se disponível
        if self.theme_system:
            bg_color = self.theme_system.get_color('background')
            title_color = self.theme_system.get_color('text_primary')
            subtitle_color = self.theme_system.get_color('text_secondary')
        else:
            bg_color = (20, 24, 28)
            title_color = GOLD
            subtitle_color = WHITE
        
        # Fundo semi-transparente
        overlay = pygame.Surface(self.screen.get_size())
        overlay.set_alpha(128)
        overlay.fill(bg_color)
        self.screen.blit(overlay, (0, 0))
        
        # Usar dimensões responsivas
        screen_w = self.screen.get_width()
        screen_h = self.screen.get_height()
        
        # Título
        title = self.font_title.render("JOGO PAUSADO", True, title_color)
        title_rect = title.get_rect(center=(screen_w // 2, screen_h // 2 - 150))
        self.screen.blit(title, title_rect)
        
        # Subtítulo
        subtitle = self.font_text.render("Pressione ESC ou clique em 'Continuar' para retomar", True, subtitle_color)
        subtitle_rect = subtitle.get_rect(center=(screen_w // 2, screen_h // 2 - 100))
        self.screen.blit(subtitle, subtitle_rect)
        
        # Desenhar botões
        for button in self.buttons.values():
            button.draw(self.screen)
        
        # Instruções adicionais
        instructions = [
            "ESC: Continuar jogo",
            "Clique nos botões para navegar",
            "O jogo permanece pausado até você continuar"
        ]
        
        y_offset = screen_h // 2 + 200
        for instruction in instructions:
            text = self.font_small.render(instruction, True, subtitle_color)
            text_rect = text.get_rect(center=(screen_w // 2, y_offset))
            self.screen.blit(text, text_rect)
            y_offset += 30

