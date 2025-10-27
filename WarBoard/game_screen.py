"""
Tela de Jogo
Interface principal do jogo THE RESISTANCE
"""

import pygame
from constants import BLACK, WHITE, LIGHT_GRAY, GOLD, RED, LIGHT_BLUE
from resistance_game import PlayerRole, MissionResult, Vote


class GameScreen:
    """
    Tela principal do jogo THE RESISTANCE
    """
    
    def __init__(self, screen, theme_system=None):
        self.screen = screen
        self.theme_system = theme_system
        self.font_title = pygame.font.Font(None, 56)
        self.font_large = pygame.font.Font(None, 42)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)
        
        # Estado do jogo
        self.game_state = {}
        self.selected_team = []
        self.chat_messages = []
        self.chat_input = ""
        self.chat_has_focus = False
        
        # Layout
        self.sidebar_width = 320
        self.padding = 20
    
    def add_chat_message(self, message: str):
        """Adiciona mensagem ao chat"""
        self.chat_messages.append(message)
        if len(self.chat_messages) > 200:
            self.chat_messages = self.chat_messages[-200:]
    
    def handle_event(self, event):
        """Processa eventos do jogo"""
        # Verificar ESC para configurações
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return 'settings'
        
        # Eventos do jogo
        if event.type == pygame.MOUSEBUTTONDOWN:
            layout = self._compute_layout()
            main_rect = layout['board_rect']
            
            # Verificar cliques nos botões do jogo
            action = self._handle_game_click(event, main_rect)
            if action:
                return action
        
        # Eventos do chat
        self._handle_chat_event(event)
        
        return None
    
    def _handle_game_click(self, event, main_rect):
        """Processa cliques na área do jogo"""
        if not self.game_state.get('is_active', False):
            return None
        
        # Verificar se clicou nos botões de voto
        if self.game_state.get('current_mission_team'):
            y_pos = main_rect.top + 350
            approve_rect = pygame.Rect(main_rect.left + 20, y_pos, 150, 40)
            reject_rect = pygame.Rect(main_rect.left + 180, y_pos, 150, 40)
            
            if approve_rect.collidepoint(event.pos):
                return {'type': 'vote_team', 'vote': 'approve'}
            elif reject_rect.collidepoint(event.pos):
                return {'type': 'vote_team', 'vote': 'reject'}
        
        # Verificar se é o líder e pode propor time
        if (self.game_state.get('current_leader') == 'Jogador' and 
            not self.game_state.get('current_mission_team')):
            
            y_pos = main_rect.top + 200
            for i, player in enumerate(self.game_state.get('player_names', [])):
                player_rect = pygame.Rect(main_rect.left + 30, y_pos + i * 25, 200, 25)
                if player_rect.collidepoint(event.pos):
                    return {'type': 'toggle_player', 'player': player}
            
            # Botão para confirmar time
            confirm_y = y_pos + len(self.game_state.get('player_names', [])) * 25 + 20
            confirm_rect = pygame.Rect(main_rect.left + 20, confirm_y, 200, 40)
            if confirm_rect.collidepoint(event.pos):
                return {'type': 'confirm_team'}
        
        # Verificar cliques nos botões de execução da missão
        if (self.game_state.get('current_mission_team') and 
            not self.game_state.get('mission_votes') and 
            'Jogador' in self.game_state.get('current_mission_team', [])):
            
            y_pos = main_rect.top + 440
            success_rect = pygame.Rect(main_rect.left + 20, y_pos, 150, 40)
            fail_rect = pygame.Rect(main_rect.left + 180, y_pos, 150, 40)
            
            if success_rect.collidepoint(event.pos):
                return {'type': 'execute_mission', 'result': 'success'}
            elif fail_rect.collidepoint(event.pos):
                return {'type': 'execute_mission', 'result': 'failure'}
        
        return None
    
    def _handle_chat_event(self, event):
        """Processa eventos do chat"""
        layout = self._compute_layout()
        chat_input_rect = layout['chat_input_rect']
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.chat_has_focus = chat_input_rect.collidepoint(event.pos)
        elif event.type == pygame.KEYDOWN and self.chat_has_focus:
            if event.key == pygame.K_RETURN:
                text = self.chat_input.strip()
                if text:
                    self.add_chat_message(f"Você: {text}")
                    self.chat_input = ""
            elif event.key == pygame.K_BACKSPACE:
                self.chat_input = self.chat_input[:-1]
            else:
                if event.unicode and len(self.chat_input) < 200 and ord(event.unicode) >= 32:
                    self.chat_input += event.unicode
    
    def draw_with_state(self, game_state):
        """Desenha o jogo com estado fornecido"""
        self.game_state = game_state
        self.draw()
    
    def draw(self):
        """Desenha a tela do jogo"""
        # Fundo verde de feltro (sempre verde, independente do tema)
        self.screen.fill((34, 139, 34))
        
        layout = self._compute_layout()
        board_rect = layout['board_rect']
        sidebar_rect = layout['sidebar_rect']
        
        # Tabuleiro
        self._draw_board(board_rect)
        
        # Interface do jogo
        if self.game_state.get('is_active', False):
            self._draw_game_interface(board_rect)
        else:
            self._draw_waiting_screen(board_rect)
        
        # Chat
        self._draw_chat_panel(sidebar_rect)
        
        # Controles
        self._draw_controls(board_rect)
    
    def _compute_layout(self):
        """Calcula o layout da tela"""
        screen_w = self.screen.get_width()
        screen_h = self.screen.get_height()
        
        left = self.padding
        top = self.padding + 60
        sidebar_width = max(250, min(320, screen_w // 4))
        usable_w = max(400, screen_w - self.padding * 3 - sidebar_width)
        usable_h = screen_h - self.padding * 2
        board_rect = pygame.Rect(left, top, usable_w, usable_h - top + self.padding)
        sidebar_x = left + usable_w + self.padding
        sidebar_rect = pygame.Rect(sidebar_x, self.padding, sidebar_width, screen_h - self.padding * 2)
        
        input_h = 40
        chat_input_rect = pygame.Rect(sidebar_rect.left + 12, sidebar_rect.bottom - input_h - 12, sidebar_rect.width - 24, input_h)
        messages_rect = pygame.Rect(sidebar_rect.left + 12, sidebar_rect.top + 60, sidebar_rect.width - 24, sidebar_rect.height - 60 - input_h - 24)
        
        return {
            'board_rect': board_rect,
            'sidebar_rect': sidebar_rect,
            'chat_input_rect': chat_input_rect,
            'messages_rect': messages_rect,
        }
    
    def _draw_board(self, board_rect):
        """Desenha o tabuleiro"""
        pygame.draw.rect(self.screen, (210, 180, 140), board_rect)
        pygame.draw.rect(self.screen, BLACK, board_rect, 3)
    
    def _draw_waiting_screen(self, board_rect):
        """Desenha tela de espera"""
        title = self.font_title.render("THE RESISTANCE", True, WHITE)
        self.screen.blit(title, (board_rect.left + 20, board_rect.top + 20))
        
        waiting_text = self.font_medium.render("Aguardando início do jogo...", True, WHITE)
        self.screen.blit(waiting_text, (board_rect.left + 20, board_rect.top + 100))
    
    def _draw_game_interface(self, board_rect):
        """Desenha a interface do jogo"""
        # Título
        title = self.font_title.render("THE RESISTANCE", True, WHITE)
        self.screen.blit(title, (board_rect.left + 20, board_rect.top + 20))
        
        y_pos = board_rect.top + 90
        
        # Informações gerais
        mission_info = self.font_medium.render(f"Missão {self.game_state.get('mission_number', 1)}/5", True, WHITE)
        self.screen.blit(mission_info, (board_rect.left + 20, y_pos))
        
        y_pos += 35
        leader_info = self.font_medium.render(f"Líder: {self.game_state.get('current_leader', '')}", True, (255, 215, 0))
        self.screen.blit(leader_info, (board_rect.left + 20, y_pos))
        
        y_pos += 35
        score_info = self.font_medium.render(
            f"Sucessos: {self.game_state.get('success_count', 0)} | Falhas: {self.game_state.get('failure_count', 0)}", 
            True, WHITE
        )
        self.screen.blit(score_info, (board_rect.left + 20, y_pos))
        
        # Verificar se o jogo terminou
        if self.game_state.get('game_over', False):
            y_pos += 50
            winner_text = "RESISTÊNCIA VENCEU!" if self.game_state.get('winner') == "Resistência" else "ESPIÕES VENCERAM!"
            winner_color = (0, 255, 0) if self.game_state.get('winner') == "Resistência" else (255, 0, 0)
            winner_surface = self.font_large.render(winner_text, True, winner_color)
            self.screen.blit(winner_surface, (board_rect.left + 20, y_pos))
            return
        
        y_pos += 50
        
        # Lista de jogadores
        players_title = self.font_medium.render("Jogadores:", True, WHITE)
        self.screen.blit(players_title, (board_rect.left + 20, y_pos))
        y_pos += 35
        
        for i, player in enumerate(self.game_state.get('player_names', [])):
            # Marcar se está selecionado
            marker = "[X] " if player in self.selected_team else "[ ] "
            if player == "Jogador":
                marker += "VOCÊ - "
            
            player_text = self.font_small.render(f"{marker}{player}", True, WHITE)
            self.screen.blit(player_text, (board_rect.left + 30, y_pos))
            y_pos += 25
        
        y_pos += 20
        
        # Configuração da missão atual
        mission_config = self.game_state.get('mission_config')
        if mission_config:
            mission_size_text = self.font_medium.render(
                f"Time necessário: {mission_config['mission_size']} jogadores", True, WHITE
            )
            self.screen.blit(mission_size_text, (board_rect.left + 20, y_pos))
            y_pos += 35
            
            fails_text = self.font_medium.render(
                f"Falhas para sabotar: {mission_config['fails_needed']}", True, (255, 200, 0)
            )
            self.screen.blit(fails_text, (board_rect.left + 20, y_pos))
            y_pos += 50
        
        # Time proposto
        current_mission_team = self.game_state.get('current_mission_team', [])
        if current_mission_team:
            team_title = self.font_medium.render("Time Proposto:", True, WHITE)
            self.screen.blit(team_title, (board_rect.left + 20, y_pos))
            y_pos += 35
            
            for player in current_mission_team:
                team_text = self.font_small.render(f"• {player}", True, WHITE)
                self.screen.blit(team_text, (board_rect.left + 30, y_pos))
                y_pos += 25
            
            y_pos += 20
            
            # Botões de voto
            if not self.game_state.get('leader_votes', {}):
                approve_rect = pygame.Rect(board_rect.left + 20, y_pos, 150, 40)
                reject_rect = pygame.Rect(board_rect.left + 180, y_pos, 150, 40)
                
                pygame.draw.rect(self.screen, (0, 200, 0), approve_rect, border_radius=8)
                pygame.draw.rect(self.screen, (200, 0, 0), reject_rect, border_radius=8)
                
                approve_text = self.font_small.render("Aprovar", True, WHITE)
                reject_text = self.font_small.render("Rejeitar", True, WHITE)
                
                self.screen.blit(approve_text, (approve_rect.centerx - 40, approve_rect.centery - 10))
                self.screen.blit(reject_text, (reject_rect.centerx - 40, reject_rect.centery - 10))
        
        # Botão de confirmar time
        if (self.game_state.get('current_leader') == 'Jogador' and 
            not current_mission_team and 
            len(self.selected_team) == mission_config.get('mission_size', 0)):
            
            y_pos_confirm = board_rect.top + 200 + len(self.game_state.get('player_names', [])) * 25 + 20
            confirm_rect = pygame.Rect(board_rect.left + 20, y_pos_confirm, 200, 40)
            pygame.draw.rect(self.screen, (0, 150, 255), confirm_rect, border_radius=8)
            confirm_text = self.font_small.render("Confirmar Time", True, WHITE)
            self.screen.blit(confirm_text, (confirm_rect.centerx - 60, confirm_rect.centery - 10))
    
    def _draw_chat_panel(self, sidebar_rect):
        """Desenha o painel de chat"""
        pygame.draw.rect(self.screen, (245, 245, 245), sidebar_rect, border_radius=10)
        pygame.draw.rect(self.screen, BLACK, sidebar_rect, 2, border_radius=10)
        
        title = self.font_chat_title.render("Chat", True, BLACK)
        self.screen.blit(title, title.get_rect(midtop=(sidebar_rect.centerx, sidebar_rect.top + 12)))
        
        layout = self._compute_layout()
        messages_rect = layout['messages_rect']
        chat_input_rect = layout['chat_input_rect']
        
        # Mensagens
        pygame.draw.rect(self.screen, WHITE, messages_rect)
        pygame.draw.rect(self.screen, BLACK, messages_rect, 1)
        max_lines = max(1, messages_rect.height // 22)
        lines = self.chat_messages[-max_lines:]
        y = messages_rect.top + 6
        for msg in lines:
            surface = self.font_chat_text.render(msg, True, BLACK)
            self.screen.blit(surface, (messages_rect.left + 6, y))
            y += 22
        
        # Input
        input_color = (255, 255, 255) if self.chat_has_focus else (245, 245, 245)
        border_color = (0, 150, 255) if self.chat_has_focus else BLACK
        pygame.draw.rect(self.screen, input_color, chat_input_rect, border_radius=8)
        pygame.draw.rect(self.screen, border_color, chat_input_rect, 2 if self.chat_has_focus else 1, border_radius=8)
        
        if self.chat_input:
            txt = self.font_chat_text.render(self.chat_input, True, BLACK)
        else:
            placeholder = "Digite uma mensagem..." if not self.chat_has_focus else "Digite aqui..."
            txt = self.font_chat_text.render(placeholder, True, (120, 120, 120))
        
        self.screen.blit(txt, (chat_input_rect.left + 8, chat_input_rect.top + 9))
    
    def _draw_controls(self, board_rect):
        """Desenha controles"""
        layout = self._compute_layout()
        sidebar_rect = layout['sidebar_rect']
        controls_y = sidebar_rect.top - 30
        controls_text = self.font_small.render("ESC: Configurações", True, (200, 200, 200))
        self.screen.blit(controls_text, (sidebar_rect.left, controls_y))
