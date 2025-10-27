"""
Tela de seleção de nome do jogador
"""

import pygame
from constants import BLACK, WHITE, LIGHT_GRAY, GOLD, RED, LIGHT_BLUE
from ui_components import Button


class PlayerNameScreen:
    """
    Tela de seleção de nome do jogador (máximo 12 caracteres)
    """
    
    def __init__(self, screen, theme_system=None):
        self.screen = screen
        self.theme_system = theme_system
        self.font_title = pygame.font.Font(None, 64)
        self.font_text = pygame.font.Font(None, 40)
        self.font_small = pygame.font.Font(None, 32)
        self.player_name = ""
        self.has_focus = False
        self.max_length = 12
        
        # Criar botões
        self.buttons = self._create_buttons()
        
    def _create_buttons(self):
        """Cria todos os botões da tela de nome do jogador"""
        # Usar dimensões responsivas
        screen_w = self.screen.get_width()
        screen_h = self.screen.get_height()
        
        button_width = 200
        button_height = 50
        center_x = screen_w // 2
        start_y = screen_h // 2 + 50
        spacing = 60
        
        return {
            'confirm': Button(
                center_x - button_width // 2, start_y, button_width, button_height,
                'Confirmar', self.font_text,
                GOLD, WHITE, BLACK
            ),
            'back': Button(
                20, 20, 80, 40,  # Canto superior esquerdo
                'Voltar', self.font_small,
                RED, WHITE, BLACK
            ),
        }
    
    def handle_event(self, event):
        """Processa eventos da tela de nome do jogador"""
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
                    if button_name == 'confirm' and self.player_name.strip():
                        return 'confirm'
                    elif button_name == 'back':
                        return 'back'
        
        elif event.type == pygame.KEYDOWN and self.has_focus:
            try:
                if event.key == pygame.K_RETURN:
                    if self.player_name.strip():
                        print(f"Confirmando nome: '{self.player_name}'")
                        return 'confirm'
                elif event.key == pygame.K_BACKSPACE:
                    self.player_name = self.player_name[:-1]
                else:
                    if event.unicode and len(self.player_name) < self.max_length:
                        # Aceitar apenas caracteres imprimíveis básicos
                        char = event.unicode
                        if char.isprintable() and char not in ['\n', '\r', '\t']:
                            self.player_name += char
                            print(f"Adicionando caractere: '{char}', nome atual: '{self.player_name}'")
            except Exception as e:
                print(f"Erro ao processar tecla: {e}")
                # Continuar funcionando mesmo com erro
        
        return None
    
    def draw(self):
        """Desenha a tela de nome do jogador"""
        # Usar cor de fundo do tema se disponível
        if self.theme_system:
            bg_color = self.theme_system.get_color('background')
        else:
            bg_color = (20, 24, 28)  # Fundo escuro padrão
            
        self.screen.fill(bg_color)
        
        # Usar dimensões responsivas
        screen_w = self.screen.get_width()
        screen_h = self.screen.get_height()
        
        # Título centralizado
        title = self.font_title.render("Nome do Jogador", True, GOLD)
        title_rect = title.get_rect(center=(screen_w // 2, 150))
        self.screen.blit(title, title_rect)
        
        # Subtítulo
        subtitle = self.font_text.render("Digite seu nome (máximo 12 caracteres, letras e números)", True, WHITE)
        subtitle_rect = subtitle.get_rect(center=(screen_w // 2, 200))
        self.screen.blit(subtitle, subtitle_rect)
        
        # Campo de input
        input_rect = pygame.Rect(screen_w // 2 - 200, screen_h // 2 - 25, 400, 50)
        input_color = (255, 255, 255) if self.has_focus else (245, 245, 245)
        border_color = (0, 150, 255) if self.has_focus else BLACK
        
        pygame.draw.rect(self.screen, input_color, input_rect, border_radius=8)
        pygame.draw.rect(self.screen, border_color, input_rect, 2 if self.has_focus else 1, border_radius=8)
        
        # Centralizar botões baseado no centro da caixa de input
        input_center_x = input_rect.centerx
        input_center_y = input_rect.centery
        
        # Texto do input
        if self.player_name:
            txt = self.font_text.render(self.player_name, True, BLACK)
        else:
            placeholder = "Digite seu nome..." if not self.has_focus else "Digite aqui..."
            txt = self.font_text.render(placeholder, True, (120, 120, 120))
        
        txt_rect = txt.get_rect(center=input_rect.center)
        self.screen.blit(txt, txt_rect)
        
        # Contador de caracteres
        char_count = f"{len(self.player_name)}/{self.max_length}"
        count_text = self.font_small.render(char_count, True, (200, 200, 200))
        count_rect = count_text.get_rect(center=(screen_w // 2, screen_h // 2 + 40))
        self.screen.blit(count_text, count_rect)
        
        # Desenhar botões alinhados com a caixa de input
        button_y = input_center_y + 80  # 80px abaixo da caixa de input
        for button in self.buttons.values():
            # Reposicionar botão baseado no centro da caixa de input
            button.rect.center = (input_center_x, button_y)
            button.draw(self.screen)
            button_y += 60  # Espaçamento entre botões
        
        # Informações
        info_text = self.font_small.render("O nome será exibido para outros jogadores", True, (200, 200, 200))
        info_rect = info_text.get_rect(center=(screen_w // 2, screen_h - 100))
        self.screen.blit(info_text, info_rect)
