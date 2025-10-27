"""
Tela de menu de salas para THE RESISTANCE
"""

import pygame
from constants import BLACK, WHITE, LIGHT_GRAY, GOLD, RED, LIGHT_BLUE
from ui_components import Button


class RoomMenuScreen:
    """
    Tela de menu de salas - escolher entre entrar ou criar sala
    """
    
    def __init__(self, screen, theme_system=None):
        self.screen = screen
        self.theme_system = theme_system
        self.font_title = pygame.font.Font(None, 64)
        self.font_text = pygame.font.Font(None, 40)
        self.font_small = pygame.font.Font(None, 32)
        
        # Criar botões
        self.buttons = self._create_buttons()
        
    def _create_buttons(self):
        """Cria todos os botões da tela de menu de salas"""
        # Usar dimensões responsivas
        screen_w = self.screen.get_width()
        screen_h = self.screen.get_height()
        
        button_width = min(300, screen_w // 4)
        button_height = 60
        center_x = screen_w // 2
        start_y = screen_h // 2 - 50
        spacing = 80
        
        return {
            'create_room': Button(
                center_x - button_width // 2, start_y, button_width, button_height,
                'Criar Sala', self.font_text,
                GOLD, WHITE, BLACK
            ),
            'join_room': Button(
                center_x - button_width // 2, start_y + spacing, button_width, button_height,
                'Entrar em Sala', self.font_text,
                LIGHT_BLUE, WHITE, BLACK
            ),
            'back': Button(
                20, 20, 80, 40,  # Canto superior esquerdo
                'Voltar', self.font_small,
                RED, WHITE, BLACK
            ),
        }
    
    def handle_event(self, event):
        """Processa eventos da tela de menu de salas"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button_name, button in self.buttons.items():
                if button.handle_event(event):
                    return button_name
        return None
    
    def draw(self):
        """Desenha a tela de menu de salas"""
        # Usar cor de fundo do tema se disponível
        if self.theme_system:
            bg_color = self.theme_system.get_color('background')
            title_color = self.theme_system.get_color('text_primary')
            subtitle_color = self.theme_system.get_color('text_primary')
            info_color = self.theme_system.get_color('text_secondary')
        else:
            bg_color = (20, 24, 28)
            title_color = GOLD
            subtitle_color = WHITE
            info_color = (200, 200, 200)
            
        self.screen.fill(bg_color)
        
        # Usar dimensões responsivas
        screen_w = self.screen.get_width()
        screen_h = self.screen.get_height()
        
        # Título centralizado
        title = self.font_title.render("THE RESISTANCE", True, title_color)
        title_rect = title.get_rect(center=(screen_w // 2, 150))
        self.screen.blit(title, title_rect)
        
        # Subtítulo
        subtitle = self.font_text.render("Escolha uma opção", True, subtitle_color)
        subtitle_rect = subtitle.get_rect(center=(screen_w // 2, 200))
        self.screen.blit(subtitle, subtitle_rect)
        
        # Desenhar botões alinhados centralmente
        button_center_x = screen_w // 2
        button_y = screen_h // 2 - 50  # Posição inicial dos botões
        
        for button in self.buttons.values():
            # Reposicionar botão para ficar centralizado
            button.rect.center = (button_center_x, button_y)
            button.draw(self.screen)
            button_y += 80  # Espaçamento entre botões
        
        # Informações adicionais
        info_text = self.font_small.render("Criar Sala: Host de uma nova partida", True, info_color)
        info_rect = info_text.get_rect(center=(screen_w // 2, screen_h - 120))
        self.screen.blit(info_text, info_rect)
        
        info_text2 = self.font_small.render("Entrar em Sala: Participar de uma partida existente", True, info_color)
        info_rect2 = info_text2.get_rect(center=(screen_w // 2, screen_h - 90))
        self.screen.blit(info_text2, info_rect2)
