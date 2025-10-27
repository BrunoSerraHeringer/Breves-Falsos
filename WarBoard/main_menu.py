"""
Menu principal do jogo
"""

import pygame
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE, DARK_BLUE, 
    GOLD, LIGHT_BLUE, RED, GRAY, BACKGROUND_IMAGE_PATH
)
from ui_components import Button


class MainMenu:
    """
    Classe responsável pelo menu principal do jogo
    """
    
    def __init__(self, screen):
        """
        Inicializa o menu principal
        
        Args:
            screen: Superfície do pygame onde o menu será desenhado
        """
        self.screen = screen
        self.font_title = pygame.font.Font(None, 72)
        self.font_button = pygame.font.Font(None, 48)
        self.font_subtitle = pygame.font.Font(None, 36)
        
        # Carregar imagem de fundo
        self.background_image = self._load_background_image()
        
        # Criar botões
        self.buttons = self._create_buttons()
        
    def _load_background_image(self):
        """
        Carrega a imagem de fundo, retorna None se não conseguir carregar
        
        Returns:
            pygame.Surface ou None: Imagem de fundo carregada
        """
        try:
            raw_image = pygame.image.load(BACKGROUND_IMAGE_PATH).convert()
            return pygame.transform.smoothscale(raw_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except Exception:
            return None
    
    def _create_buttons(self):
        """
        Cria todos os botões do menu
        
        Returns:
            dict: Dicionário com os botões do menu
        """
        button_width = 300
        button_height = 60
        button_x = (SCREEN_WIDTH - button_width) // 2
        start_y = 400
        spacing = 80
        
        return {
            'jogo_classico': Button(
                button_x, start_y, button_width, button_height,
                'THE RESISTANCE', self.font_button, GOLD, WHITE
            ),
            'jogo_estendido': Button(
                button_x, start_y + spacing, button_width, button_height,
                'THE COUNCIL', self.font_button, GOLD, WHITE
            ),
            'configuracoes': Button(
                button_x, start_y + spacing * 2, button_width, button_height,
                'CONFIGURAÇÕES', self.font_button, LIGHT_BLUE, WHITE
            ),
            'sair': Button(
                button_x, start_y + spacing * 3, button_width, button_height,
                'SAIR', self.font_button, RED, WHITE
            ),
        }
    
    def _draw_gradient_background(self):
        """
        Desenha um fundo com gradiente quando não há imagem disponível
        """
        for y in range(SCREEN_HEIGHT):
            color_ratio = y / SCREEN_HEIGHT
            r = int(DARK_BLUE[0] * (1 - color_ratio) + BLACK[0] * color_ratio)
            g = int(DARK_BLUE[1] * (1 - color_ratio) + BLACK[1] * color_ratio)
            b = int(DARK_BLUE[2] * (1 - color_ratio) + BLACK[2] * color_ratio)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))
    
    def _draw_title(self):
        """
        Desenha o título e subtítulo do jogo
        """
        # Título principal
        title_text = self.font_title.render("WAR BOARD", True, GOLD)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(title_text, title_rect)
        
        # Subtítulo
        subtitle_text = self.font_subtitle.render("Estratégia de Guerra", True, WHITE)
        subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH // 2, 200))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # Decoração - linhas douradas
        pygame.draw.line(self.screen, GOLD, 
                        (SCREEN_WIDTH // 2 - 200, 250), 
                        (SCREEN_WIDTH // 2 + 200, 250), 3)
        pygame.draw.line(self.screen, GOLD, 
                        (SCREEN_WIDTH // 2 - 150, 260), 
                        (SCREEN_WIDTH // 2 + 150, 260), 2)
    
    def _draw_footer(self):
        """
        Desenha o rodapé com informações do desenvolvedor
        """
        dev_text = pygame.font.Font(None, 24).render("Desenvolvido com Pygame", True, GRAY)
        dev_rect = dev_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
        self.screen.blit(dev_text, dev_rect)
    
    def _draw_controls(self):
        """Desenha controles"""
        # Controles no canto inferior esquerdo
        controls_text = pygame.font.Font(None, 24).render("F11: Fullscreen | ESC: Configurações", True, (200, 200, 200))
        self.screen.blit(controls_text, (20, SCREEN_HEIGHT - 60))
    
    def draw(self):
        """
        Desenha o menu principal completo
        """
        # Background: imagem se disponível, senão gradiente
        if self.background_image:
            self.screen.blit(self.background_image, (0, 0))
        else:
            self._draw_gradient_background()
        
        # Desenhar elementos do menu
        self._draw_title()
        
        # Desenhar botões
        for button in self.buttons.values():
            button.draw(self.screen)
        
        # Rodapé
        self._draw_footer()
        
        # Controles
        self._draw_controls()
        
    def handle_event(self, event):
        """
        Processa eventos do menu
        
        Args:
            event: Evento do pygame
            
        Returns:
            str ou None: Nome do botão clicado ou None
        """
        for button_name, button in self.buttons.items():
            if button.handle_event(event):
                return button_name
        return None
