"""
Componentes de interface do usuário
"""

import pygame
from constants import BLACK, WHITE, LIGHT_GRAY


class Button:
    """
    Classe para botões interativos com efeito hover
    """
    
    def __init__(self, x, y, width, height, text, font, color=LIGHT_GRAY, 
                 hover_color=WHITE, text_color=BLACK):
        """
        Inicializa um botão
        
        Args:
            x, y: Posição do botão
            width, height: Dimensões do botão
            text: Texto do botão
            font: Fonte do texto
            color: Cor normal do botão
            hover_color: Cor quando o mouse está sobre o botão
            text_color: Cor do texto
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False
        
    def draw(self, screen):
        """
        Desenha o botão na tela
        """
        # Escolher cor baseada no hover
        current_color = self.hover_color if self.is_hovered else self.color
        
        # Desenhar botão com bordas arredondadas
        pygame.draw.rect(screen, current_color, self.rect, border_radius=10)
        pygame.draw.rect(screen, BLACK, self.rect, 3, border_radius=10)
        
        # Desenhar texto centralizado
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
        
    def handle_event(self, event):
        """
        Processa eventos do mouse relacionados ao botão
        
        Returns:
            bool: True se o botão foi clicado, False caso contrário
        """
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False
