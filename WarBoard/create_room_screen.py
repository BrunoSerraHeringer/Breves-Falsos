"""
Tela de criação de sala para THE RESISTANCE
"""

import pygame
from constants import BLACK, WHITE, LIGHT_GRAY, GOLD, RED, LIGHT_BLUE
from ui_components import Button


class CreateRoomScreen:
    """
    Tela de criação de sala - selecionar número de jogadores
    """
    
    def __init__(self, screen, theme_system=None):
        self.screen = screen
        self.theme_system = theme_system
        self.font_title = pygame.font.Font(None, 64)
        self.font_text = pygame.font.Font(None, 40)
        self.font_small = pygame.font.Font(None, 32)
        self.players = 5
        
        # Criar botões
        self.buttons = self._create_buttons()
        
    def _create_buttons(self):
        """Cria todos os botões da tela de criação de sala"""
        # Usar dimensões responsivas
        screen_w = self.screen.get_width()
        screen_h = self.screen.get_height()
        
        button_width = 200
        button_height = 50
        center_x = screen_w // 2
        start_y = screen_h // 2 - 100
        spacing = 60
        
        return {
            'minus': Button(
                center_x - 150, start_y, 60, 60,
                '-', self.font_text,
                LIGHT_GRAY, WHITE, BLACK
            ),
            'plus': Button(
                center_x + 90, start_y, 60, 60,
                '+', self.font_text,
                LIGHT_GRAY, WHITE, BLACK
            ),
            'create': Button(
                center_x - button_width // 2, start_y + 120, button_width, button_height,
                'Criar Sala', self.font_text,
                GOLD, WHITE, BLACK
            ),
            'back': Button(
                20, 20, 80, 40,  # Canto superior esquerdo
                'Voltar', self.font_small,
                RED, WHITE, BLACK
            ),
        }
    
    def handle_event(self, event):
        """Processa eventos da tela de criação de sala"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button_name, button in self.buttons.items():
                if button.handle_event(event):
                    if button_name == 'minus' and self.players > 5:
                        self.players -= 1
                    elif button_name == 'plus' and self.players < 10:
                        self.players += 1
                    elif button_name == 'create':
                        return 'create_room'
                    elif button_name == 'back':
                        return 'back'
        return None
    
    def draw(self):
        """Desenha a tela de criação de sala"""
        # Usar cor de fundo do tema se disponível
        if self.theme_system:
            bg_color = self.theme_system.get_color('background')
        else:
            bg_color = (20, 24, 28)  # Fundo escuro padrão
            
        self.screen.fill(bg_color)
        
        # Usar dimensões responsivas
        screen_w = self.screen.get_width()
        screen_h = self.screen.get_height()
        
        # Usar cor do tema para títulos
        if self.theme_system:
            title_color = self.theme_system.get_color('text_primary')
            subtitle_color = self.theme_system.get_color('text_primary')
        else:
            title_color = GOLD
            subtitle_color = WHITE
            
        # Título centralizado
        title = self.font_title.render("Criar Sala", True, title_color)
        title_rect = title.get_rect(center=(screen_w // 2, 150))
        self.screen.blit(title, title_rect)
        
        # Subtítulo
        subtitle = self.font_text.render("Selecione o número de jogadores", True, subtitle_color)
        subtitle_rect = subtitle.get_rect(center=(screen_w // 2, 200))
        self.screen.blit(subtitle, subtitle_rect)
        
        # Controle de número de jogadores - centralizado
        center_x = screen_w // 2
        number_y = screen_h // 2 - 50
        
        # Centralizar botões de controle baseado no centro do número
        self.buttons['minus'].rect.center = (center_x - 80, number_y)
        self.buttons['plus'].rect.center = (center_x + 80, number_y)
        
        # Botões de controle
        pygame.draw.rect(self.screen, LIGHT_GRAY, self.buttons['minus'].rect, border_radius=8)
        pygame.draw.rect(self.screen, LIGHT_GRAY, self.buttons['plus'].rect, border_radius=8)
        
        # Usar cor do tema para os botões +/-
        if self.theme_system:
            button_text_color = self.theme_system.get_color('text_inverse')
        else:
            button_text_color = BLACK
            
        minus_txt = self.font_text.render("-", True, button_text_color)
        plus_txt = self.font_text.render("+", True, button_text_color)
        self.screen.blit(minus_txt, minus_txt.get_rect(center=self.buttons['minus'].rect.center))
        self.screen.blit(plus_txt, plus_txt.get_rect(center=self.buttons['plus'].rect.center))
        
        # Número de jogadores - centralizado, usar cor do tema
        if self.theme_system:
            text_color = self.theme_system.get_color('text_primary')
        else:
            text_color = WHITE
            
        players_txt = self.font_title.render(str(self.players), True, text_color)
        players_rect = players_txt.get_rect(center=(center_x, number_y))
        self.screen.blit(players_txt, players_rect)
        
        # Desenhar botões de ação alinhados com o número
        button_y = number_y + 100  # 100px abaixo do número
        for button_name, button in self.buttons.items():
            if button_name not in ['minus', 'plus']:
                # Reposicionar botão baseado no centro do número
                button.rect.center = (center_x, button_y)
                button.draw(self.screen)
                button_y += 60  # Espaçamento entre botões
        
        # Informações
        info_text = self.font_small.render(f"Jogadores: {self.players}", True, (200, 200, 200))
        info_rect = info_text.get_rect(center=(screen_w // 2, screen_h - 100))
        self.screen.blit(info_text, info_rect)
