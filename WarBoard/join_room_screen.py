"""
Tela para entrar em sala existente
"""

import pygame
from constants import BLACK, WHITE, LIGHT_GRAY, GOLD, RED, LIGHT_BLUE
from ui_components import Button


class JoinRoomScreen:
    """
    Tela para inserir código da sala e entrar
    """
    
    def __init__(self, screen, theme_system=None):
        self.screen = screen
        self.theme_system = theme_system
        self.font_title = pygame.font.Font(None, 64)
        self.font_text = pygame.font.Font(None, 40)
        self.font_small = pygame.font.Font(None, 32)
        self.room_code = ""
        self.has_focus = False
        self.max_length = 5
        
        # Criar botões
        self.buttons = self._create_buttons()
        
    def _create_buttons(self):
        """Cria todos os botões da tela"""
        # Usar dimensões responsivas
        screen_w = self.screen.get_width()
        screen_h = self.screen.get_height()
        
        button_width = 200
        button_height = 50
        center_x = screen_w // 2
        start_y = screen_h // 2 + 50
        spacing = 60
        
        return {
            'join': Button(
                center_x - 100, start_y, 200, 50,
                'Entrar na Sala', self.font_text,
                LIGHT_BLUE, WHITE, BLACK
            ),
            'back': Button(
                20, 20, 80, 40,  # Canto superior esquerdo
                'Voltar', self.font_small,
                RED, WHITE, BLACK
            ),
        }
    
    def handle_event(self, event):
        """Processa eventos da tela"""
        # Usar dimensões responsivas
        screen_w = self.screen.get_width()
        screen_h = self.screen.get_height()
        
        # Campo de input
        input_rect = pygame.Rect(screen_w // 2 - 200, screen_h // 2 - 25, 400, 50)
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Verificar se clicou no campo de input
            if input_rect.collidepoint(event.pos):
                self.has_focus = True
            else:
                self.has_focus = False
            
            # Verificar botões
            for button_name, button in self.buttons.items():
                if button.handle_event(event):
                    if button_name == 'join' and self.room_code.strip():
                        return 'join_room'
                    elif button_name == 'back':
                        return 'back'
        
        elif event.type == pygame.KEYDOWN and self.has_focus:
            if event.key == pygame.K_RETURN:
                if self.room_code.strip():
                    return 'join_room'
            elif event.key == pygame.K_BACKSPACE:
                self.room_code = self.room_code[:-1]
            else:
                if event.unicode and len(self.room_code) < self.max_length:
                    # Aceitar apenas letras maiúsculas e números
                    char = event.unicode.upper()
                    if char.isalnum():
                        self.room_code += char
        
        return None
    
    def draw(self):
        """Desenha a tela"""
        # Usar dimensões responsivas
        screen_w = self.screen.get_width()
        screen_h = self.screen.get_height()
        
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
        title = self.font_title.render("Entrar em Sala", True, title_color)
        title_rect = title.get_rect(center=(screen_w // 2, 150))
        self.screen.blit(title, title_rect)
        
        # Subtítulo
        subtitle = self.font_text.render("Digite o código da sala", True, subtitle_color)
        subtitle_rect = subtitle.get_rect(center=(screen_w // 2, 200))
        self.screen.blit(subtitle, subtitle_rect)
        
        # Campo de input
        input_rect = pygame.Rect(screen_w // 2 - 200, screen_h // 2 - 25, 400, 50)
        
        # Usar cores do tema para input
        if self.theme_system:
            input_bg = self.theme_system.get_color('input_background')
            input_border = self.theme_system.get_color('input_focus') if self.has_focus else self.theme_system.get_color('input_border')
            input_text_color = self.theme_system.get_color('text_primary')
            placeholder_color = self.theme_system.get_color('text_muted')
        else:
            input_bg = (255, 255, 255) if self.has_focus else (245, 245, 245)
            input_border = (0, 150, 255) if self.has_focus else BLACK
            input_text_color = BLACK
            placeholder_color = (120, 120, 120)
        
        pygame.draw.rect(self.screen, input_bg, input_rect, border_radius=8)
        pygame.draw.rect(self.screen, input_border, input_rect, 2 if self.has_focus else 1, border_radius=8)
        
        # Texto do input
        if self.room_code:
            txt = self.font_text.render(self.room_code, True, input_text_color)
        else:
            placeholder = "Digite o código..." if not self.has_focus else "Digite aqui..."
            txt = self.font_text.render(placeholder, True, placeholder_color)
        
        txt_rect = txt.get_rect(center=input_rect.center)
        self.screen.blit(txt, txt_rect)
        
        # Contador de caracteres
        char_count = f"{len(self.room_code)}/{self.max_length}"
        count_text = self.font_small.render(char_count, True, (200, 200, 200))
        count_rect = count_text.get_rect(center=(screen_w // 2, screen_h // 2 + 40))
        self.screen.blit(count_text, count_rect)
        
        # Desenhar botões
        for button in self.buttons.values():
            button.draw(self.screen)
        
        # Informações
        info_text = self.font_small.render("O código deve ter 5 caracteres (letras e números)", True, (200, 200, 200))
        info_rect = info_text.get_rect(center=(screen_w // 2, screen_h - 100))
        self.screen.blit(info_text, info_rect)
    
    def get_room_code(self):
        """Retorna o código da sala inserido"""
        return self.room_code.strip().upper()
