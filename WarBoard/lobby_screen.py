"""
Tela de Lobby
Interface do lobby de jogo
"""

import pygame
from constants import BLACK, WHITE, LIGHT_GRAY, GOLD, RED, LIGHT_BLUE, BOARD_IMAGE_PATH
from ui_components import Button


class LobbyScreen:
    """
    Tela de lobby para THE RESISTANCE
    """
    
    def __init__(self, screen, theme_system=None):
        self.screen = screen
        self.theme_system = theme_system
        self.font_title = pygame.font.Font(None, 48)
        self.font_text = pygame.font.Font(None, 40)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 32)
        self.font_chat_title = pygame.font.Font(None, 40)
        self.font_chat_text = pygame.font.Font(None, 28)
        
        # Dados do lobby
        self.room_code = ""
        self.player_name = "Jogador"
        self.num_players = 5
        self.connected_players = []
        self.host_name = ""  # Nome do host
        self.is_host = False  # Se o jogador atual é o host
        self.chat_messages = []
        self.chat_input = ""
        self.chat_input_lines = []  # Linhas do input atual
        self.chat_has_focus = False
        self.chat_scroll_offset = 0  # Offset para scroll do chat
        
        # Resolução escolhida para layout responsivo
        self.chosen_width = None
        self.chosen_height = None
        
        # Sistema de arrastar
        self.dragging = False
        self.drag_offset = (0, 0)
        self.draggable_elements = []
        
        # Imagem do tabuleiro
        self.board_image = None
        self._load_board_image()
        
        # Layout
        self.sidebar_width = 320
        self.padding = 20
        
        # Botões
        self.start_rect = pygame.Rect(0, 0, 250, 60)
        self.back_rect = pygame.Rect(0, 0, 200, 50)
        self.voltar_rect = pygame.Rect(0, 0, 80, 40)  # Botão voltar no canto superior esquerdo
        
        # Inicializar linhas do input
        self._update_input_lines()
    
    def set_room_data(self, room_code: str, player_name: str, num_players: int):
        """Define dados da sala"""
        self.room_code = room_code
        self.player_name = player_name
        self.num_players = num_players
        self.connected_players = [player_name] + [f"Jogador {i+1}" for i in range(1, num_players)]
    
    def add_chat_message(self, message: str):
        """Adiciona mensagem ao chat com quebra de linha"""
        # Quebrar mensagem em linhas se for muito longa
        wrapped_message = self._wrap_text(message, 40)  # 40 caracteres por linha
        for line in wrapped_message:
            self.chat_messages.append(line)
        if len(self.chat_messages) > 300:
            self.chat_messages = self.chat_messages[-300:]
    
    def _wrap_text(self, text: str, max_length: int) -> list:
        """Quebra texto em linhas com limite de caracteres (máximo 300 caracteres total)"""
        if not text:
            return []
        
        # Limitar texto total a 300 caracteres
        if len(text) > 300:
            text = text[:300]
            
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            # Calcular tamanho da linha com a nova palavra
            test_line = current_line + (" " if current_line else "") + word
            
            if len(test_line) <= max_length:
                # Palavra cabe na linha atual
                current_line = test_line
            else:
                # Palavra não cabe, finalizar linha atual
                if current_line:
                    lines.append(current_line)
                    current_line = word
                else:
                    # Palavra muito longa, quebrar no meio
                    while len(word) > max_length:
                        lines.append(word[:max_length])
                        word = word[max_length:]
                    current_line = word
        
        # Adicionar última linha se houver conteúdo
        if current_line:
            lines.append(current_line)
        
        return lines
    
    def _update_input_lines(self):
        """Atualiza as linhas do input do chat automaticamente"""
        if not self.chat_input:
            self.chat_input_lines = [""]
            return
        
        # Limitar a 300 caracteres
        text = self.chat_input[:300]
        
        # Quebrar em linhas de 40 caracteres
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + (" " if current_line else "") + word
            if len(test_line) <= 40:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                    current_line = word
                else:
                    # Palavra muito longa, quebrar no meio
                    while len(word) > 40:
                        lines.append(word[:40])
                        word = word[40:]
                    current_line = word
        
        if current_line:
            lines.append(current_line)
        
        # Garantir que sempre há pelo menos uma linha vazia
        if not lines:
            lines = [""]
        
        self.chat_input_lines = lines
        
    
    def handle_event(self, event):
        """Processa eventos do lobby"""
        # Verificar ESC para configurações
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return 'settings'
        
        # Verificar P para pausar/continuar (apenas no chat)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_p and self.chat_has_focus:
            return 'pause_chat'
        
        # Atalho para testar a tela de jogo (Ctrl+R+S)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_s and pygame.key.get_pressed()[pygame.K_LCTRL] and pygame.key.get_pressed()[pygame.K_r]:
            return 'test_game_screen'
        
        # Controle de scroll do chat
        if event.type == pygame.KEYDOWN and not self.chat_has_focus:
            if event.key == pygame.K_UP:
                self.chat_scroll_offset = max(0, self.chat_scroll_offset - 1)
            elif event.key == pygame.K_DOWN:
                self.chat_scroll_offset += 1
        
        
        # Scroll com roda do mouse (mais responsivo)
        if event.type == pygame.MOUSEWHEEL and not self.chat_has_focus:
            scroll_amount = event.y * 3
            self.chat_scroll_offset = max(0, self.chat_scroll_offset - scroll_amount)
        
        # Eventos do mouse
        if event.type == pygame.MOUSEBUTTONDOWN:
            layout = self._compute_layout()
            board_rect = layout['board_rect']
            
            # Botão voltar (canto superior esquerdo)
            self.voltar_rect.topleft = (20, 20)
            if self.voltar_rect.collidepoint(event.pos):
                return 'back'
            
            # Verificar se clicou em elemento arrastável (código da sala)
            if self.room_code:
                code_font = pygame.font.Font(None, 48)
                code_text = code_font.render(f"Código da Sala: {self.room_code}", True, GOLD)
                code_rect = code_text.get_rect(center=(board_rect.centerx, 80))
                bg_rect = code_rect.inflate(20, 10)
                
                if bg_rect.collidepoint(event.pos):
                    self.dragging = True
                    self.drag_offset = (event.pos[0] - code_rect.centerx, event.pos[1] - code_rect.centery)
                    return None
            
            # Botão iniciar (no centro do tabuleiro)
            center_x = board_rect.centerx
            center_y = board_rect.centery
            self.start_rect.center = (center_x, center_y)
            
            if self.start_rect.collidepoint(event.pos):
                # Só permite iniciar se for o host e tiver jogadores suficientes
                if self.is_host and len(self.connected_players) >= self.num_players:
                    return 'start_game'
            
            # Chat input
            chat_input_rect = layout['chat_input_rect']
            self.chat_has_focus = chat_input_rect.collidepoint(event.pos)
        
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            # Atualizar posição do elemento arrastado
            pass
        
        # Entrada de texto no chat
        if event.type == pygame.KEYDOWN and self.chat_has_focus:
            if event.key == pygame.K_RETURN:
                text = self.chat_input.strip()
                if text:
                    self.add_chat_message(f"{self.player_name}: {text}")
                    self.chat_input = ""
                    self._update_input_lines()  # Atualizar linhas automaticamente
            elif event.key == pygame.K_BACKSPACE:
                self.chat_input = self.chat_input[:-1]
                self._update_input_lines()  # Atualizar linhas automaticamente
            else:
                if event.unicode and len(self.chat_input) < 300 and ord(event.unicode) >= 32:
                    self.chat_input += event.unicode
                    self._update_input_lines()  # Atualizar linhas automaticamente
        
        # Debug: verificar se o chat está funcionando
        if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
            self.add_chat_message("Esta é uma mensagem muito longa que deve ser quebrada em múltiplas linhas para testar o sistema de quebra de linha do chat com limite de 300 caracteres e quebra a cada 40 caracteres para permitir mensagens mais longas e melhor formatação do texto")
        
        # Debug: atalho para testar tela de jogo
        if event.type == pygame.KEYDOWN and event.key == pygame.K_t:
            self.add_chat_message("Use Ctrl+R+S para ir direto para a tela de jogo (teste)")
        
        return None
    
    def draw_with_data(self, player_data):
        """Desenha o lobby com dados do jogador"""
        # Atualizar dados
        self.room_code = player_data.get('room_code', '')
        self.player_name = player_data.get('username', 'Jogador')
        self.num_players = player_data.get('num_players', 5)
        self.is_host = player_data.get('is_host', False)
        
        # Definir host (primeiro jogador é sempre o host)
        if not self.host_name:
            self.host_name = self.player_name
        
        # Atualizar lista de jogadores
        if not self.connected_players or self.connected_players[0] != self.player_name:
            self.connected_players = [self.player_name] + [f"Jogador {i+1}" for i in range(1, self.num_players)]
        
        # Desenhar lobby
        self.draw()
    
    def draw(self):
        """Desenha a tela do lobby"""
        # Usar cor de fundo do tema se disponível
        if self.theme_system:
            bg_color = self.theme_system.get_color('background')
        else:
            bg_color = (34, 139, 34)  # Verde de feltro padrão
            
        self.screen.fill(bg_color)
        
        layout = self._compute_layout()
        board_rect = layout['board_rect']
        sidebar_rect = layout['sidebar_rect']
        
        # Botão voltar (canto superior esquerdo)
        self._draw_back_button()
        
        # Tabuleiro
        self._draw_board(board_rect)
        
        # Cabeçalho
        self._draw_header(board_rect)
        
        # Código da sala
        self._draw_room_code(board_rect)
        
        # Botão Iniciar Jogo
        self._draw_start_button(board_rect)
        
        # Chat
        self._draw_chat_panel(sidebar_rect)
        
        # Lista de jogadores
        self._draw_players_list(board_rect)
        
        # Controles
        self._draw_controls(board_rect)
    
    def _compute_layout(self):
        """Calcula o layout da tela de forma responsiva"""
        # Usar resolução escolhida se disponível, senão usar resolução real
        screen_w = self.chosen_width if self.chosen_width else self.screen.get_width()
        screen_h = self.chosen_height if self.chosen_height else self.screen.get_height()
        
        # Larguras mínimas mais conservadoras
        min_board_width = 250
        min_sidebar_width = 150
        
        # Padding adaptativo baseado em breakpoints
        if screen_w <= 640:  # Pequeno
            self.padding = 10
        elif screen_w <= 1007:  # Médio
            self.padding = 15
        else:  # Grande
            self.padding = 20
        
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
            board_width = screen_w - self.padding * 2
            sidebar_width = screen_w - self.padding * 2
            # Usar mais espaço para o tabuleiro em telas pequenas
            board_height = int((screen_h - self.padding * 3) * 0.6)  # 60% para tabuleiro
            sidebar_height = screen_h - board_height - self.padding * 3  # Resto para chat
            
            board_rect = pygame.Rect(self.padding, self.padding + 40, board_width, board_height)
            sidebar_rect = pygame.Rect(self.padding, board_rect.bottom + self.padding, sidebar_width, sidebar_height)
        else:
            # Layout horizontal normal
            total_width = screen_w - self.padding * 2
            available_width = total_width
            
            # Proporção adaptativa baseada em breakpoints
            if layout_mode == 'small':
                # Pequeno: 50% tabuleiro, 50% sidebar
                board_ratio = 0.5
            elif layout_mode == 'medium':
                # Médio: 55% tabuleiro, 45% sidebar
                board_ratio = 0.55
            else:  # Grande
                # Grande: 60% tabuleiro, 40% sidebar
                board_ratio = 0.6
            
            board_width = int(available_width * board_ratio)
            sidebar_width = available_width - board_width
            
            # Garantir larguras mínimas mais conservadoras
            min_board_width = 200
            min_sidebar_width = 120
            board_width = max(min_board_width, board_width)
            sidebar_width = max(min_sidebar_width, sidebar_width)
            
            # Ajustar se exceder a largura total
            if board_width + sidebar_width > total_width:
                excess = (board_width + sidebar_width) - total_width
                if board_width > min_board_width:
                    board_width -= excess // 2
                if sidebar_width > min_sidebar_width:
                    sidebar_width -= excess // 2
            
            # Posicionamento
            left = self.padding
            top = self.padding + 60
            board_rect = pygame.Rect(left, top, board_width, screen_h - self.padding * 2 - top + self.padding)
            sidebar_x = left + board_width + self.padding
            sidebar_rect = pygame.Rect(sidebar_x, self.padding, sidebar_width, screen_h - self.padding * 2)
        
        # Área de mensagens (altura adaptativa baseada no conteúdo)
        input_h = 60  # Altura fixa menor para o input
        min_messages_height = 150
        max_messages_height = sidebar_rect.height - 80 - input_h  # Deixar espaço para título e input
        
        # Calcular altura necessária baseada no número de mensagens
        # Altura da linha adaptativa baseada em breakpoints
        screen_w = self.screen.get_width()
        if screen_w <= 640:  # Pequeno
            line_height = 14
        elif screen_w <= 1007:  # Médio
            line_height = 16
        else:  # Grande
            line_height = 18
        num_messages = len(self.chat_messages)
        content_height = num_messages * line_height + 20  # 20px de padding
        
        # Usar altura do conteúdo ou altura máxima disponível
        messages_height = max(
            min_messages_height,
            min(max_messages_height, content_height)
        )
        
        # Garantir que o input não saia da tela
        input_y = sidebar_rect.top + 60 + messages_height + 10
        if input_y + input_h > sidebar_rect.bottom:
            input_y = sidebar_rect.bottom - input_h - 10
            messages_height = input_y - sidebar_rect.top - 70
        
        messages_rect = pygame.Rect(sidebar_rect.left + 12, sidebar_rect.top + 60, sidebar_rect.width - 24, messages_height)
        chat_input_rect = pygame.Rect(sidebar_rect.left + 12, input_y, sidebar_rect.width - 24, input_h)
        
        return {
            'board_rect': board_rect,
            'sidebar_rect': sidebar_rect,
            'chat_input_rect': chat_input_rect,
            'messages_rect': messages_rect,
        }
    
    def set_chosen_resolution(self, width, height):
        """Define a resolução escolhida para layout responsivo"""
        self.chosen_width = width
        self.chosen_height = height
    
    def update_layout(self):
        """Atualiza o layout quando a tela é redimensionada"""
        # O layout é calculado dinamicamente no _compute_layout
        pass
    
    def _draw_board(self, board_rect):
        """Desenha o tabuleiro"""
        if self.board_image:
            scaled = pygame.transform.smoothscale(self.board_image, (board_rect.width, board_rect.height))
            self.screen.blit(scaled, board_rect.topleft)
            pygame.draw.rect(self.screen, BLACK, board_rect, 3)
        else:
            pygame.draw.rect(self.screen, (210, 180, 140), board_rect)
            pygame.draw.rect(self.screen, BLACK, board_rect, 3)
    
    def _draw_header(self, board_rect):
        """Desenha o cabeçalho"""
        # Centralizar o cabeçalho
        header_text = f"Sala de Espera - Jogadores: {len(self.connected_players)}/{self.num_players}"
        
        # Fonte adaptativa baseada em breakpoints
        screen_w = self.screen.get_width()
        if screen_w <= 640:  # Pequeno
            header_font = pygame.font.Font(None, 32)
        elif screen_w <= 1007:  # Médio
            header_font = pygame.font.Font(None, 40)
        else:  # Grande
            header_font = self.font_title
            
        header = header_font.render(header_text, True, WHITE)
        # Posicionamento baseado em breakpoints
        if screen_w <= 640:  # Pequeno
            y_pos = 25
        elif screen_w <= 1007:  # Médio
            y_pos = 30
        else:  # Grande
            y_pos = 40
        header_rect = header.get_rect(center=(board_rect.centerx, y_pos))
        self.screen.blit(header, header_rect)
    
    def _draw_room_code(self, board_rect):
        """Desenha o código da sala"""
        if self.room_code:
            # Fonte adaptativa baseada em breakpoints
            screen_w = self.screen.get_width()
            if screen_w <= 640:  # Pequeno
                code_font = pygame.font.Font(None, 28)
                y_pos = 50
            elif screen_w <= 1007:  # Médio
                code_font = pygame.font.Font(None, 36)
                y_pos = 60
            else:  # Grande
                code_font = pygame.font.Font(None, 48)
                y_pos = 80
                
            code_text = code_font.render(f"Código da Sala: {self.room_code}", True, GOLD)
            
            # Fundo para destacar o código
            code_rect = code_text.get_rect(center=(board_rect.centerx, y_pos))
            bg_rect = code_rect.inflate(20, 10)
            pygame.draw.rect(self.screen, (0, 0, 0, 180), bg_rect, border_radius=8)
            pygame.draw.rect(self.screen, GOLD, bg_rect, 2, border_radius=8)
            
            self.screen.blit(code_text, code_rect)
    
    def _draw_start_button(self, board_rect):
        """Desenha o botão de iniciar jogo"""
        center_x = board_rect.centerx
        # Posicionar mais embaixo, próximo à parte inferior do tabuleiro
        screen_w = self.screen.get_width()
        if screen_w <= 640:  # Pequeno
            center_y = board_rect.bottom - 30
        elif screen_w <= 1007:  # Médio
            center_y = board_rect.bottom - 50
        else:  # Grande
            center_y = board_rect.bottom - 80
        self.start_rect.center = (center_x, center_y)
        
        # Verificar se o mouse está sobre o botão
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = self.start_rect.collidepoint(mouse_pos)
        
        # Verificar se pode iniciar (host + jogadores suficientes)
        can_start = self.is_host and len(self.connected_players) >= self.num_players
        
        if can_start:
            if is_hovered:
                # Botão ativo com hover - verde mais escuro
                pygame.draw.rect(self.screen, (0, 150, 0), self.start_rect, border_radius=15)
                pygame.draw.rect(self.screen, BLACK, self.start_rect, 3, border_radius=15)
            else:
                # Botão ativo normal - verde sólido
                pygame.draw.rect(self.screen, (0, 200, 0), self.start_rect, border_radius=15)
                pygame.draw.rect(self.screen, BLACK, self.start_rect, 3, border_radius=15)
            start_text = self.font_text.render("INICIAR JOGO", True, WHITE)
        elif self.is_host:
            # Host mas não tem jogadores suficientes
            pygame.draw.rect(self.screen, (100, 100, 100), self.start_rect, border_radius=15)
            pygame.draw.rect(self.screen, BLACK, self.start_rect, 3, border_radius=15)
            start_text = self.font_text.render(
                f"Esperando ({len(self.connected_players)}/{self.num_players})", 
                True, (200, 200, 200)
            )
        else:
            # Não é host - botão translúcido que fica opaco no hover
            if is_hovered:
                # Hover - botão mais opaco
                pygame.draw.rect(self.screen, (0, 200, 0), self.start_rect, border_radius=15)
                pygame.draw.rect(self.screen, BLACK, self.start_rect, 3, border_radius=15)
                start_text = self.font_text.render("Apenas o Host pode iniciar", True, WHITE)
            else:
                # Normal - botão translúcido
                # Criar uma superfície com transparência
                button_surface = pygame.Surface(self.start_rect.size, pygame.SRCALPHA)
                pygame.draw.rect(button_surface, (0, 200, 0, 100), button_surface.get_rect(), border_radius=15)
                pygame.draw.rect(button_surface, (0, 0, 0, 100), button_surface.get_rect(), 3, border_radius=15)
                self.screen.blit(button_surface, self.start_rect.topleft)
                start_text = self.font_text.render("Apenas o Host pode iniciar", True, (200, 200, 200))
        
        self.screen.blit(start_text, start_text.get_rect(center=self.start_rect.center))
    
    def _draw_chat_panel(self, sidebar_rect):
        """Desenha o painel de chat"""
        # Usar cores do tema se disponível
        if self.theme_system:
            chat_bg = self.theme_system.get_color('chat_background')
            chat_border = self.theme_system.get_color('chat_border')
        else:
            chat_bg = (245, 245, 245)
            chat_border = BLACK
            
        pygame.draw.rect(self.screen, chat_bg, sidebar_rect, border_radius=10)
        pygame.draw.rect(self.screen, chat_border, sidebar_rect, 2, border_radius=10)
        
        # Usar cor de texto do tema
        if self.theme_system:
            text_color = self.theme_system.get_color('text_primary')
        else:
            text_color = BLACK
            
        # Fonte adaptativa baseada em breakpoints
        screen_w = self.screen.get_width()
        if screen_w <= 640:  # Pequeno
            title_font = pygame.font.Font(None, 24)
        elif screen_w <= 1007:  # Médio
            title_font = pygame.font.Font(None, 28)
        else:  # Grande
            title_font = self.font_chat_title
            
        title = title_font.render("Chat", True, text_color)
        # Posicionamento baseado em breakpoints
        if screen_w <= 640:  # Pequeno
            y_offset = 6
        elif screen_w <= 1007:  # Médio
            y_offset = 8
        else:  # Grande
            y_offset = 12
        self.screen.blit(title, title.get_rect(midtop=(sidebar_rect.centerx, sidebar_rect.top + y_offset)))
        
        layout = self._compute_layout()
        messages_rect = layout['messages_rect']
        chat_input_rect = layout['chat_input_rect']
        
        # Mensagens - usar cores do tema
        if self.theme_system:
            msg_bg = self.theme_system.get_color('surface')
            msg_border = self.theme_system.get_color('text_primary')
            msg_text_color = self.theme_system.get_color('text_primary')
        else:
            msg_bg = WHITE
            msg_border = BLACK
            msg_text_color = BLACK
            
        pygame.draw.rect(self.screen, msg_bg, messages_rect)
        pygame.draw.rect(self.screen, msg_border, messages_rect, 1)
        
        # Calcular quantas linhas cabem na área de mensagens
        # Altura da linha adaptativa baseada em breakpoints
        screen_w = self.screen.get_width()
        if screen_w <= 640:  # Pequeno
            line_height = 14
        elif screen_w <= 1007:  # Médio
            line_height = 16
        else:  # Grande
            line_height = 18
        max_lines = max(1, messages_rect.height // line_height)
        total_lines = len(self.chat_messages)
        
        # Desenhar barra de scroll se necessário
        if total_lines > max_lines:
            scroll_bar_width = 12  # Mais larga para melhor visibilidade
            scroll_bar_x = messages_rect.right - scroll_bar_width - 2
            scroll_bar_rect = pygame.Rect(scroll_bar_x, messages_rect.top + 2, scroll_bar_width, messages_rect.height - 4)
            
            # Usar cores do tema para barra de scroll
            if self.theme_system:
                scroll_bg = self.theme_system.get_color('surface')
                scroll_indicator = self.theme_system.get_color('text_secondary')
            else:
                scroll_bg = (220, 220, 220)
                scroll_indicator = (100, 100, 100)
            
            # Fundo da barra de scroll
            pygame.draw.rect(self.screen, scroll_bg, scroll_bar_rect, border_radius=6)
            
            # Indicador da posição atual
            scroll_ratio = self.chat_scroll_offset / max(1, total_lines - max_lines)
            indicator_height = max(30, int(scroll_bar_rect.height * (max_lines / total_lines)))
            indicator_y = scroll_bar_rect.top + int(scroll_ratio * (scroll_bar_rect.height - indicator_height))
            indicator_rect = pygame.Rect(scroll_bar_x + 2, indicator_y, scroll_bar_width - 4, indicator_height)
            pygame.draw.rect(self.screen, scroll_indicator, indicator_rect, border_radius=4)
        
        # Aplicar scroll - pegar linhas baseadas no offset
        start_line = max(0, total_lines - max_lines - self.chat_scroll_offset)
        end_line = min(total_lines, start_line + max_lines)
        lines = self.chat_messages[start_line:end_line]
        
        y = messages_rect.top + 6
        for i, msg in enumerate(lines):
            # Verificar se a linha cabe na área
            if y + line_height <= messages_rect.bottom:
                # Truncar mensagem se for muito longa para a largura da caixa
                max_chars = (messages_rect.width - 12) // 8  # Aproximadamente 8 pixels por caractere
                if len(msg) > max_chars:
                    msg = msg[:max_chars-3] + "..."
                
                # Fonte adaptativa baseada em breakpoints
                screen_w = self.screen.get_width()
                if screen_w <= 640:  # Pequeno
                    font_chat_text = pygame.font.Font(None, 20)
                elif screen_w <= 1007:  # Médio
                    font_chat_text = pygame.font.Font(None, 24)
                else:  # Grande
                    font_chat_text = self.font_chat_text
                surface = font_chat_text.render(msg, True, msg_text_color)
                self.screen.blit(surface, (messages_rect.left + 6, y))
                y += line_height
            else:
                # Se não cabe mais, parar de desenhar
                break
        
        # Input - usar cores do tema
        if self.theme_system:
            input_bg = self.theme_system.get_color('input_background')
            input_border = self.theme_system.get_color('input_focus') if self.chat_has_focus else self.theme_system.get_color('input_border')
        else:
            input_bg = (255, 255, 255) if self.chat_has_focus else (245, 245, 245)
            input_border = (0, 150, 255) if self.chat_has_focus else BLACK
            
        pygame.draw.rect(self.screen, input_bg, chat_input_rect, border_radius=8)
        pygame.draw.rect(self.screen, input_border, chat_input_rect, 2 if self.chat_has_focus else 1, border_radius=8)
        
        # Usar cor de texto do tema para input
        if self.theme_system:
            input_text_color = self.theme_system.get_color('text_primary')
            placeholder_color = self.theme_system.get_color('text_muted')
        else:
            input_text_color = BLACK
            placeholder_color = (120, 120, 120)
            
        if self.chat_input:
            # Desenhar as linhas quebradas do input
            # Altura da linha adaptativa baseada em breakpoints
            screen_w = self.screen.get_width()
            if screen_w <= 640:  # Pequeno
                line_height = 14
            elif screen_w <= 1007:  # Médio
                line_height = 16
            else:  # Grande
                line_height = 18
            y_offset = chat_input_rect.top + 9
            
            for line in self.chat_input_lines:
                if y_offset + line_height <= chat_input_rect.bottom - 5:  # Deixar espaço para o contador
                    # Fonte adaptativa baseada em breakpoints
                    screen_w = self.screen.get_width()
                    if screen_w <= 640:  # Pequeno
                        font_chat_text = pygame.font.Font(None, 20)
                    elif screen_w <= 1007:  # Médio
                        font_chat_text = pygame.font.Font(None, 24)
                    else:  # Grande
                        font_chat_text = self.font_chat_text
                    txt = font_chat_text.render(line, True, input_text_color)
                    self.screen.blit(txt, (chat_input_rect.left + 8, y_offset))
                    y_offset += line_height
        else:
            placeholder = "Digite uma mensagem..." if not self.chat_has_focus else "Digite aqui..."
            # Fonte adaptativa baseada em breakpoints
            screen_w = self.screen.get_width()
            if screen_w <= 640:  # Pequeno
                font_chat_text = pygame.font.Font(None, 20)
            elif screen_w <= 1007:  # Médio
                font_chat_text = pygame.font.Font(None, 24)
            else:  # Grande
                font_chat_text = self.font_chat_text
            txt = font_chat_text.render(placeholder, True, placeholder_color)
            self.screen.blit(txt, (chat_input_rect.left + 8, chat_input_rect.top + 9))
        
        # Barra de progresso de caracteres
        char_count = len(self.chat_input)
        char_text = f"{char_count}/300"
        char_color = input_text_color if char_count < 240 else (255, 100, 100) if char_count < 300 else (255, 0, 0)
        
        # Desenhar barra de progresso
        progress_width = chat_input_rect.width - 16
        progress_height = 4
        progress_x = chat_input_rect.left + 8
        progress_y = chat_input_rect.bottom - 25
        
        # Fundo da barra
        progress_bg_rect = pygame.Rect(progress_x, progress_y, progress_width, progress_height)
        pygame.draw.rect(self.screen, (200, 200, 200), progress_bg_rect, border_radius=2)
        
        # Barra de progresso
        if char_count > 0:
            progress_ratio = min(1.0, char_count / 300.0)
            progress_fill_width = int(progress_width * progress_ratio)
            progress_fill_rect = pygame.Rect(progress_x, progress_y, progress_fill_width, progress_height)
            
            # Cor da barra baseada no progresso
            if char_count < 240:
                progress_color = (100, 200, 100)  # Verde
            elif char_count < 300:
                progress_color = (255, 200, 100)  # Amarelo
            else:
                progress_color = (255, 100, 100)  # Vermelho
            
            pygame.draw.rect(self.screen, progress_color, progress_fill_rect, border_radius=2)
        
        # Contador de caracteres
        # Fonte adaptativa baseada em breakpoints
        screen_w = self.screen.get_width()
        if screen_w <= 640:  # Pequeno
            font_chat_text = pygame.font.Font(None, 20)
        elif screen_w <= 1007:  # Médio
            font_chat_text = pygame.font.Font(None, 24)
        else:  # Grande
            font_chat_text = self.font_chat_text
        char_surface = font_chat_text.render(char_text, True, char_color)
        char_rect = char_surface.get_rect()
        char_rect.bottomright = (chat_input_rect.right - 8, chat_input_rect.bottom - 5)
        self.screen.blit(char_surface, char_rect)
        
    
    def _draw_players_list(self, board_rect):
        """Desenha lista de jogadores"""
        # Posicionar no canto superior esquerdo do tabuleiro
        y_pos = board_rect.top + 20
        x_pos = board_rect.left + 20
        
        players_title = self.font_small.render("Jogadores:", True, WHITE)
        self.screen.blit(players_title, (x_pos, y_pos))
        y_pos += 25
        
        # Lista de jogadores alinhada à esquerda
        for i, player in enumerate(self.connected_players):
            # Determinar cor e texto baseado no status
            if player == self.host_name:
                # Host
                if player == self.player_name:
                    player_text = self.font_small.render(f"• {player} (Host - Você)", True, (255, 215, 0))  # Dourado
                else:
                    player_text = self.font_small.render(f"• {player} (Host)", True, (255, 215, 0))  # Dourado
            elif player == self.player_name:
                # Você (não host)
                player_text = self.font_small.render(f"• {player} (Você)", True, (255, 255, 100))  # Amarelo
            else:
                # Outros jogadores
                player_text = self.font_small.render(f"• {player}", True, (100, 255, 100))  # Verde
            
            self.screen.blit(player_text, (x_pos, y_pos))
            y_pos += 20
    
    def _draw_back_button(self):
        """Desenha o botão voltar no canto superior esquerdo"""
        # Posicionar no canto superior esquerdo
        self.voltar_rect.topleft = (20, 20)
        
        # Verificar se está sendo hovered
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = self.voltar_rect.collidepoint(mouse_pos)
        
        # Cor do botão (vermelho)
        if is_hovered:
            button_color = (200, 0, 0)  # Vermelho mais claro no hover
        else:
            button_color = (150, 0, 0)  # Vermelho normal
        
        # Desenhar botão
        pygame.draw.rect(self.screen, button_color, self.voltar_rect, border_radius=8)
        pygame.draw.rect(self.screen, WHITE, self.voltar_rect, 2, border_radius=8)
        
        # Texto do botão
        voltar_text = self.font_small.render("Voltar", True, WHITE)
        text_rect = voltar_text.get_rect(center=self.voltar_rect.center)
        self.screen.blit(voltar_text, text_rect)
    
    def _draw_controls(self, board_rect):
        """Desenha controles"""
        layout = self._compute_layout()
        sidebar_rect = layout['sidebar_rect']
        # Posicionar mais longe do chat, no canto inferior esquerdo
        controls_y = sidebar_rect.bottom + 20
        controls_text = self.font_small.render("ESC: Configurações | F11: Fullscreen", True, (200, 200, 200))
        self.screen.blit(controls_text, (board_rect.left + 20, controls_y))
        
        # Instrução para teste da tela de jogo (canto superior direito, discreto)
        test_text = self.font_small.render("Ctrl+R+S: Teste", True, (150, 150, 150))
        screen_w = self.screen.get_width()
        test_rect = test_text.get_rect()
        self.screen.blit(test_text, (screen_w - test_rect.width - 10, 10))
        
        # Instrução para scroll do chat (canto superior direito, abaixo do teste)
        scroll_text = self.font_small.render("↑↓: Scroll chat", True, (150, 150, 150))
        scroll_rect = scroll_text.get_rect()
        self.screen.blit(scroll_text, (screen_w - scroll_rect.width - 10, 35))
    
    def _load_board_image(self):
        """Carrega a imagem do tabuleiro"""
        try:
            self.board_image = pygame.image.load(BOARD_IMAGE_PATH).convert_alpha()
        except pygame.error:
            self.board_image = None
    
    def remove_player(self, player_name):
        """Remove um jogador da lista e reorganiza"""
        if player_name in self.connected_players:
            self.connected_players.remove(player_name)
            
            # Se o host saiu, transferir para o próximo jogador
            if player_name == self.host_name and self.connected_players:
                self.host_name = self.connected_players[0]
                # Atualizar se o jogador atual é o novo host
                if self.connected_players[0] == self.player_name:
                    self.is_host = True
                else:
                    self.is_host = False
            elif player_name == self.player_name:
                # Se você saiu, não é mais host
                self.is_host = False
    
    def add_player(self, player_name):
        """Adiciona um jogador à lista"""
        if player_name not in self.connected_players:
            self.connected_players.append(player_name)
    
    def set_host(self, player_name):
        """Define um jogador como host"""
        self.host_name = player_name
        self.is_host = (player_name == self.player_name)
