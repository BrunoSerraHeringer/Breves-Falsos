"""
Tela de jogo do The Resistance com tabuleiro e chat
"""

import pygame
from constants import BLACK, WHITE, LIGHT_GRAY, GOLD, RED, GREEN, LIGHT_BLUE
from resistance_board import ResistanceBoard


class GameLobbyScreen:
    """
    Tela de jogo que combina o tabuleiro do The Resistance com o chat
    """
    
    def __init__(self, screen, theme_system=None):
        self.screen = screen
        self.theme_system = theme_system
        
        # Fontes
        self.font_title = pygame.font.Font(None, 48)
        self.font_text = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)
        self.font_chat_title = pygame.font.Font(None, 40)
        self.font_chat_text = pygame.font.Font(None, 28)
        
        # Tabuleiro do jogo
        self.resistance_board = ResistanceBoard(screen, theme_system)
        
        # Chat
        self.chat_messages = []
        self.chat_input = ""
        self.chat_has_focus = False
        
        # Dados do jogo
        self.players = []
        self.player_name = "Jogador"
        self.room_code = ""
        
        # Resolução escolhida para layout responsivo
        self.chosen_width = None
        self.chosen_height = None
        
        # Botão de voltar
        self.back_button = None
        self._create_buttons()
    
    def _create_buttons(self):
        """Cria botões da tela"""
        screen_w = self.screen.get_width()
        screen_h = self.screen.get_height()
        
        # Botão voltar (canto superior esquerdo)
        self.back_button = pygame.Rect(20, 20, 100, 40)
    
    def set_game_data(self, game_data):
        """Define dados do jogo"""
        self.players = game_data.get('players', [])
        self.player_name = game_data.get('player_name', 'Jogador')
        self.room_code = game_data.get('room_code', '')
        
        # Atualizar estado do tabuleiro
        board_state = {
            'players': self.players,
            'current_mission': game_data.get('current_mission', 1),
            'current_leader': game_data.get('current_leader', 0),
            'team_size': game_data.get('team_size', 0),
            'votes': game_data.get('votes', {}),
            'mission_results': game_data.get('mission_results', {})
        }
        self.resistance_board.set_game_state(board_state)
    
    def add_chat_message(self, message: str):
        """Adiciona mensagem ao chat com quebra de linha"""
        # Quebrar mensagem em linhas se for muito longa
        wrapped_message = self._wrap_text(message, 25)  # 25 caracteres por linha
        for line in wrapped_message:
            self.chat_messages.append(line)
        if len(self.chat_messages) > 100:
            self.chat_messages = self.chat_messages[-100:]
    
    def _wrap_text(self, text: str, max_length: int) -> list:
        """Quebra texto em linhas com limite de caracteres"""
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            if len(current_line + " " + word) <= max_length:
                if current_line:
                    current_line += " " + word
                else:
                    current_line = word
            else:
                if current_line:
                    lines.append(current_line)
                    current_line = word
                else:
                    # Palavra muito longa, quebrar no meio
                    lines.append(word[:max_length])
                    current_line = word[max_length:]
        
        if current_line:
            lines.append(current_line)
        
        return lines
    
    def handle_event(self, event):
        """Processa eventos da tela de jogo"""
        # Verificar ESC para configurações
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return 'settings'
        
        # Eventos do mouse
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Botão voltar
            if self.back_button.collidepoint(event.pos):
                return 'back_to_lobby'
            
            # Chat input
            layout = self._compute_layout()
            chat_input_rect = layout['chat_input_rect']
            self.chat_has_focus = chat_input_rect.collidepoint(event.pos)
        
        # Entrada de texto no chat
        if event.type == pygame.KEYDOWN and self.chat_has_focus:
            if event.key == pygame.K_RETURN:
                text = self.chat_input.strip()
                if text:
                    self.add_chat_message(f"{self.player_name}: {text}")
                    self.chat_input = ""
            elif event.key == pygame.K_BACKSPACE:
                self.chat_input = self.chat_input[:-1]
            else:
                if event.unicode and len(self.chat_input) < 200 and ord(event.unicode) >= 32:
                    self.chat_input += event.unicode
        
        # Debug: verificar se o chat está funcionando
        if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
            self.add_chat_message("Teste de chat no jogo")
        
        return None
    
    def _compute_layout(self):
        """Calcula layout responsivo da tela"""
        # Usar resolução escolhida se disponível, senão usar resolução real
        screen_w = self.chosen_width if self.chosen_width else self.screen.get_width()
        screen_h = self.chosen_height if self.chosen_height else self.screen.get_height()
        
        # Larguras mínimas mais conservadoras
        min_board_width = 250
        min_chat_width = 120
        
        # Aplicar breakpoints responsivos baseados na resolução escolhida
        if screen_w <= 640:  # Pequeno: até 640px
            layout_mode = 'small'
        elif screen_w <= 1007:  # Médio: 641-1007px
            layout_mode = 'medium'
        else:  # Grande: 1008px+
            layout_mode = 'large'
        
        # Garantir que a tela seja grande o suficiente
        if layout_mode == 'small':  # Forçar layout vertical para telas pequenas
            # Tela muito pequena - usar layout vertical
            board_width = screen_w
            chat_width = screen_w
            board_height = screen_h // 2
            chat_height = screen_h // 2
            
            board_rect = pygame.Rect(0, 0, board_width, board_height)
            chat_rect = pygame.Rect(0, board_height, chat_width, chat_height)
        else:
            # Layout horizontal normal
            # Proporção adaptativa baseada em breakpoints
            if layout_mode == 'small':
                # Pequeno: 50% tabuleiro, 50% chat
                board_ratio = 0.5
            elif layout_mode == 'medium':
                # Médio: 55% tabuleiro, 45% chat
                board_ratio = 0.55
            else:  # Grande
                # Grande: 60% tabuleiro, 40% chat
                board_ratio = 0.6
            
            board_width = int(screen_w * board_ratio)
            chat_width = screen_w - board_width
            
            # Garantir larguras mínimas
            if board_width < min_board_width:
                board_width = min_board_width
                chat_width = screen_w - board_width
            if chat_width < min_chat_width:
                chat_width = min_chat_width
                board_width = screen_w - chat_width
            
            # Área do tabuleiro (lado esquerdo)
            board_rect = pygame.Rect(0, 0, board_width, screen_h)
            
            # Área do chat (lado direito)
            chat_rect = pygame.Rect(board_width, 0, chat_width, screen_h)
        
        # Área de mensagens do chat (altura adaptativa)
        min_messages_height = 150
        max_messages_height = chat_rect.height - 100
        messages_height = max(min_messages_height, min(max_messages_height, chat_rect.height - 100))
        
        messages_rect = pygame.Rect(
            chat_rect.left + 10,
            chat_rect.top + 50,
            chat_rect.width - 20,
            messages_height
        )
        
        # Input do chat
        chat_input_rect = pygame.Rect(
            chat_rect.left + 10,
            messages_rect.bottom + 10,
            chat_rect.width - 20,
            30
        )
        
        return {
            'board_rect': board_rect,
            'chat_rect': chat_rect,
            'messages_rect': messages_rect,
            'chat_input_rect': chat_input_rect
        }
    
    def draw(self):
        """Desenha a tela de jogo"""
        # Usar cor de fundo do tema se disponível
        if self.theme_system:
            bg_color = self.theme_system.get_color('background')
        else:
            bg_color = (20, 24, 28)
            
        self.screen.fill(bg_color)
        
        # Calcular layout
        layout = self._compute_layout()
        board_rect = layout['board_rect']
        chat_rect = layout['chat_rect']
        messages_rect = layout['messages_rect']
        chat_input_rect = layout['chat_input_rect']
        
        # Desenhar tabuleiro
        self.resistance_board.draw(board_rect)
        
        # Desenhar chat
        self._draw_chat_panel(chat_rect, messages_rect, chat_input_rect)
        
        # Desenhar botão voltar
        self._draw_back_button()
        
        # Desenhar controles
        self._draw_controls()
    
    def _draw_chat_panel(self, chat_rect, messages_rect, chat_input_rect):
        """Desenha o painel de chat"""
        # Usar cores do tema se disponível
        if self.theme_system:
            chat_bg = self.theme_system.get_color('surface')
            chat_border = self.theme_system.get_color('text_primary')
            text_color = self.theme_system.get_color('text_primary')
            msg_bg = self.theme_system.get_color('surface')
            msg_border = self.theme_system.get_color('text_primary')
            msg_text_color = self.theme_system.get_color('text_primary')
            input_bg = self.theme_system.get_color('input_background')
            input_border = self.theme_system.get_color('input_focus') if self.chat_has_focus else self.theme_system.get_color('input_border')
            input_text_color = self.theme_system.get_color('text_primary')
            placeholder_color = self.theme_system.get_color('text_secondary')
        else:
            chat_bg = (40, 44, 48)
            chat_border = WHITE
            text_color = WHITE
            msg_bg = WHITE
            msg_border = BLACK
            msg_text_color = BLACK
            input_bg = (255, 255, 255)
            input_border = (0, 150, 255) if self.chat_has_focus else BLACK
            input_text_color = BLACK
            placeholder_color = (120, 120, 120)
        
        # Fundo do chat
        pygame.draw.rect(self.screen, chat_bg, chat_rect)
        pygame.draw.rect(self.screen, chat_border, chat_rect, 2)
        
        # Título do chat
        chat_title = self.font_chat_title.render("Chat do Jogo", True, text_color)
        self.screen.blit(chat_title, (chat_rect.left + 10, chat_rect.top + 10))
        
        # Área de mensagens
        pygame.draw.rect(self.screen, msg_bg, messages_rect)
        pygame.draw.rect(self.screen, msg_border, messages_rect, 1)
        
        # Calcular quantas linhas cabem na área de mensagens
        line_height = 18
        max_lines = max(1, messages_rect.height // line_height)
        lines = self.chat_messages[-max_lines:]
        
        y = messages_rect.top + 6
        for msg in lines:
            # Verificar se a linha cabe na área
            if y + line_height <= messages_rect.bottom:
                surface = self.font_chat_text.render(msg, True, msg_text_color)
                self.screen.blit(surface, (messages_rect.left + 6, y))
                y += line_height
        
        # Input do chat
        pygame.draw.rect(self.screen, input_bg, chat_input_rect, border_radius=8)
        pygame.draw.rect(self.screen, input_border, chat_input_rect, 2 if self.chat_has_focus else 1, border_radius=8)
        
        # Texto do input
        if self.chat_input:
            input_text = self.font_chat_text.render(self.chat_input, True, input_text_color)
        else:
            placeholder = "Digite uma mensagem..." if not self.chat_has_focus else "Digite aqui..."
            input_text = self.font_chat_text.render(placeholder, True, placeholder_color)
        
        input_text_rect = input_text.get_rect(center=chat_input_rect.center)
        self.screen.blit(input_text, input_text_rect)
    
    def _draw_back_button(self):
        """Desenha botão de voltar"""
        pygame.draw.rect(self.screen, RED, self.back_button, border_radius=8)
        pygame.draw.rect(self.screen, BLACK, self.back_button, 2, border_radius=8)
        
        back_text = self.font_text.render("Voltar", True, WHITE)
        back_text_rect = back_text.get_rect(center=self.back_button.center)
        self.screen.blit(back_text, back_text_rect)
    
    def set_chosen_resolution(self, width, height):
        """Define a resolução escolhida para layout responsivo"""
        self.chosen_width = width
        self.chosen_height = height
    
    def _draw_controls(self):
        """Desenha controles"""
        # Usar resolução escolhida se disponível
        screen_w = self.chosen_width if self.chosen_width else self.screen.get_width()
        screen_h = self.chosen_height if self.chosen_height else self.screen.get_height()
        
        # Controles no canto inferior esquerdo
        controls_text = self.font_small.render("F11: Fullscreen | ESC: Configurações", True, (200, 200, 200))
        self.screen.blit(controls_text, (20, screen_h - 30))
    
    def update_layout(self):
        """Atualiza o layout quando a tela é redimensionada"""
        # O layout é calculado dinamicamente no _compute_layout
        pass
