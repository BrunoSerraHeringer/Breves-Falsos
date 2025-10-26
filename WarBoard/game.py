"""
Classe principal do jogo War Board
"""

import pygame
import sys
import socket
import threading
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, WHITE, BLACK, LIGHT_GRAY, BOARD_IMAGE_PATH, BASE_ROOM_URL, SERVER_HOST, SERVER_PORT
from game_states import GameState
from main_menu import MainMenu

# Importar módulo The Resistance
try:
    from resistance_game import ResistanceGame, PlayerRole, MissionResult, Vote
    RESISTANCE_AVAILABLE = True
except ImportError:
    RESISTANCE_AVAILABLE = False
    print("Aviso: Módulo The Resistance não encontrado")


class Game:
    """
    Classe principal que gerencia o loop do jogo e estados
    """
    
    def __init__(self):
        """
        Inicializa o jogo
        """
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("War Board - Estratégia de Guerra")
        self.clock = pygame.time.Clock()
        self.state = GameState.MENU
        self.running = True
        self.is_fullscreen = False
        
        # Inicializar telas
        self.main_menu = MainMenu(self.screen)
        self.classic_setup = ClassicSetupScreen(self.screen)
        self.classic_playing = ClassicPlayingScreen(self.screen)
        self.lobby_screen = LobbyScreen(self.screen)
        self.classic_lobby = ClassicLobbyScreen(self.screen)
        self.classic_num_players = None
        
    def run(self):
        """
        Loop principal do jogo
        """
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
            
        try:
            # Garantir encerramento da conexão de jogo, se existir
            if hasattr(self, 'classic_playing'):
                self.classic_playing._disconnect()
        except Exception:
            pass
        pygame.quit()
        sys.exit()
        
    def handle_events(self):
        """
        Processa todos os eventos do jogo
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
                
            # Processar eventos baseado no estado atual
            if self.state == GameState.MENU:
                self._handle_menu_events(event)
            elif self.state == GameState.CLASSIC_SETUP:
                self._handle_classic_setup_events(event)
            elif self.state == GameState.PLAYING:
                self._handle_game_events(event)
            elif self.state == GameState.SETTINGS:
                self._handle_settings_events(event)
            elif self.state == GameState.LOBBY:
                if hasattr(self, 'classic_num_players') and self.classic_num_players:
                    self._handle_lobby_events(event)
                else:
                    action = self.lobby_screen.handle_event(event)
                    if action == 'start_game':
                        if getattr(self.lobby_screen, 'username', '').strip():
                            self.classic_playing.set_username(self.lobby_screen.username.strip())
                        self.state = GameState.PLAYING
    
    def _handle_menu_events(self, event):
        """
        Processa eventos específicos do menu
        
        Args:
            event: Evento do pygame
        """
        button_clicked = self.main_menu.handle_event(event)
        
        if button_clicked == 'jogo_classico':
            self.classic_setup.reset()
            self.state = GameState.CLASSIC_SETUP
        elif button_clicked == 'jogo_estendido':
            print("Iniciando Jogo Estendido...")  # Placeholder
            # self.state = GameState.PLAYING  # Implementar depois
        elif button_clicked == 'configuracoes':
            print("Abrindo configurações...")  # Placeholder
            # self.state = GameState.SETTINGS  # Implementar depois
        elif button_clicked == 'sair':
            self.running = False

    def _handle_classic_setup_events(self, event):
        """
        Processa eventos da tela de configuração do modo clássico
        """
        action = self.classic_setup.handle_event(event)
        if action and action.get('type') == 'start':
            self.classic_num_players = action['players']
            self.classic_lobby.reset(self.classic_num_players)
            self.state = GameState.LOBBY
        elif action and action.get('type') == 'back':
            self.state = GameState.MENU
    
    def _handle_lobby_events(self, event):
        """
        Processa eventos da tela de lobby do modo clássico
        """
        action = self.classic_lobby.handle_event(event)
        if action == 'start_game':
            self.classic_playing.start_new_game(self.classic_num_players)
            self.state = GameState.PLAYING
        elif action == 'back':
            self.state = GameState.CLASSIC_SETUP
    
    def _handle_game_events(self, event):
        """
        Processa eventos específicos do jogo
        
        Args:
            event: Evento do pygame
        """
        action = self.classic_playing.handle_event(event)
        if action == 'exit_game':
            self.classic_playing._disconnect()
            self.running = False
        elif action == 'invite_friends':
            # Placeholder: abriria UI de convite/amigos
            print("Convidar amigos - em breve")
        elif action == 'back_to_menu':
            self.classic_playing._disconnect()
            self.lobby_screen.reset()
            self.state = GameState.LOBBY
        elif action == 'toggle_fullscreen':
            self._toggle_fullscreen()
    
    def _handle_settings_events(self, event):
        """
        Processa eventos específicos das configurações
        
        Args:
            event: Evento do pygame
        """
        # Implementar lógica de eventos das configurações aqui
        pass
                    
    def update(self):
        """
        Atualiza a lógica do jogo baseada no estado atual
        """
        if self.state == GameState.PLAYING:
            # Implementar lógica de atualização do jogo aqui
            pass
        elif self.state == GameState.SETTINGS:
            # Implementar lógica de atualização das configurações aqui
            pass
        
    def draw(self):
        """
        Desenha o jogo baseado no estado atual
        """
        if self.state == GameState.MENU:
            self.main_menu.draw()
        elif self.state == GameState.CLASSIC_SETUP:
            self.classic_setup.draw()
        elif self.state == GameState.PLAYING:
            self.classic_playing.draw()
        elif self.state == GameState.SETTINGS:
            # Implementar desenho das configurações aqui
            pass
        elif self.state == GameState.LOBBY:
            # Verificar se é lobby do modo clássico ou lobby geral
            if hasattr(self, 'classic_num_players') and self.classic_num_players:
                self.classic_lobby.draw()
            else:
                self.lobby_screen.draw()
            
        pygame.display.flip()

    def _toggle_fullscreen(self):
        if not self.is_fullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.is_fullscreen = True
        else:
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.is_fullscreen = False
        # Propagar nova surface para telas
        self.main_menu.screen = self.screen
        self.classic_setup.screen = self.screen
        self.classic_playing.screen = self.screen
        self.lobby_screen.screen = self.screen

    def _handle_lobby_events(self, event):
        action = self.lobby_screen.handle_event(event)
        if action == 'start_game':
            # No futuro, sincronizar com servidor/peers. Por ora, inicia localmente.
            if getattr(self.lobby_screen, 'username', '').strip():
                self.classic_playing.set_username(self.lobby_screen.username.strip())
            self.state = GameState.PLAYING


class ClassicSetupScreen:
    """
    Tela de configuração do Modo Clássico
    - Seleção de número de jogadores (5 a 10)
    - Botões para Iniciar e Voltar
    """
    def __init__(self, screen):
        self.screen = screen
        self.font_title = pygame.font.Font(None, 64)
        self.font_text = pygame.font.Font(None, 40)
        self.font_small = pygame.font.Font(None, 32)
        self.players = 5
        self.plus_rect = pygame.Rect(760, 360, 60, 60)
        self.minus_rect = pygame.Rect(380, 360, 60, 60)
        self.start_rect = pygame.Rect(500, 500, 200, 60)
        self.back_rect = pygame.Rect(500, 580, 200, 50)

    def reset(self):
        self.players = 5

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.plus_rect.collidepoint(event.pos):
                if self.players < 10:
                    self.players += 1
            elif self.minus_rect.collidepoint(event.pos):
                if self.players > 5:
                    self.players -= 1
            elif self.start_rect.collidepoint(event.pos):
                return { 'type': 'start', 'players': self.players }
            elif self.back_rect.collidepoint(event.pos):
                return { 'type': 'back' }
        return None

    def draw(self):
        self.screen.fill(WHITE)
        title = self.font_title.render("Modo Clássico", True, BLACK)
        self.screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 120)))

        subtitle = self.font_text.render("Selecione o número de jogadores", True, BLACK)
        self.screen.blit(subtitle, subtitle.get_rect(center=(SCREEN_WIDTH // 2, 240)))

        # Controle de jogadores
        pygame.draw.rect(self.screen, LIGHT_GRAY, self.minus_rect, border_radius=8)
        pygame.draw.rect(self.screen, LIGHT_GRAY, self.plus_rect, border_radius=8)

        minus_txt = self.font_text.render("-", True, BLACK)
        plus_txt = self.font_text.render("+", True, BLACK)
        self.screen.blit(minus_txt, minus_txt.get_rect(center=self.minus_rect.center))
        self.screen.blit(plus_txt, plus_txt.get_rect(center=self.plus_rect.center))

        players_txt = self.font_title.render(str(self.players), True, BLACK)
        self.screen.blit(players_txt, players_txt.get_rect(center=(SCREEN_WIDTH // 2, 390)))

        # Botões
        pygame.draw.rect(self.screen, LIGHT_GRAY, self.start_rect, border_radius=10)
        start_txt = self.font_text.render("Iniciar", True, BLACK)
        self.screen.blit(start_txt, start_txt.get_rect(center=self.start_rect.center))

        pygame.draw.rect(self.screen, LIGHT_GRAY, self.back_rect, border_radius=10)
        back_txt = self.font_small.render("Voltar", True, BLACK)
        self.screen.blit(back_txt, back_txt.get_rect(center=self.back_rect.center))


class ClassicLobbyScreen:
    """
    Tela de lobby para o Modo Clássico (The Resistance)
    - Tabuleiro/imagem central
    - Chat para comunicação na lateral
    - Botão para iniciar jogo quando todos estiverem prontos
    """
    def __init__(self, screen):
        self.screen = screen
        self.font_title = pygame.font.Font(None, 48)
        self.font_text = pygame.font.Font(None, 40)
        self.font_small = pygame.font.Font(None, 32)
        self.font_chat_title = pygame.font.Font(None, 40)
        self.font_chat_text = pygame.font.Font(None, 28)
        self.num_players = 5
        self.connected_players = []
        self.chat_messages = []
        self.chat_input = ""
        self.chat_has_focus = False
        self.username = "Jogador"
        
        # Layout
        self.sidebar_width = 320
        self.padding = 20
        
        # Tabuleiro
        self.board_image = None
        self._load_board_image()
        
        # Botões
        self.start_rect = pygame.Rect(0, 0, 250, 60)
        self.back_rect = pygame.Rect(0, 0, 200, 50)
    
    def reset(self, num_players):
        """Reseta o lobby com número de jogadores"""
        self.num_players = num_players
        self.connected_players = [f"Jogador {i+1}" for i in range(num_players)]
        self.chat_messages = []
        self.chat_input = ""
        self.chat_has_focus = False
    
    def handle_event(self, event):
        """Processa eventos do lobby"""
        sw = self.screen.get_width()
        sh = self.screen.get_height()
        
        # Posicionar botões
        self.start_rect.center = (sw // 2, sh - 100)
        self.back_rect.center = (sw // 2, sh - 40)
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Botão iniciar (no centro do tabuleiro)
            layout = self._compute_layout()
            board_rect = layout['board_rect']
            center_x = board_rect.centerx
            center_y = board_rect.centery
            self.start_rect.center = (center_x, center_y)
            
            if self.start_rect.collidepoint(event.pos):
                if len(self.connected_players) >= self.num_players:
                    return 'start_game'
            
            # Chat input
            chat_input_rect = layout['chat_input_rect']
            self.chat_has_focus = chat_input_rect.collidepoint(event.pos)
        
        # Entrada de texto no chat
        if event.type == pygame.KEYDOWN and self.chat_has_focus:
            if event.key == pygame.K_RETURN:
                text = self.chat_input.strip()
                if text:
                    self._append_message(f"{self.username}: {text}")
                    self.chat_input = ""
            elif event.key == pygame.K_BACKSPACE:
                self.chat_input = self.chat_input[:-1]
            else:
                if event.unicode and len(self.chat_input) < 200 and ord(event.unicode) >= 32:
                    self.chat_input += event.unicode
        
        return None
    
    def draw(self):
        """Desenha a tela do lobby"""
        # Fundo verde de feltro (como antes)
        self.screen.fill((34, 139, 34))
        
        layout = self._compute_layout()
        board_rect = layout['board_rect']
        sidebar_rect = layout['sidebar_rect']
        
        # Tabuleiro (imagem ou placeholder)
        if self.board_image:
            scaled = pygame.transform.smoothscale(self.board_image, (board_rect.width, board_rect.height))
            self.screen.blit(scaled, board_rect.topleft)
            pygame.draw.rect(self.screen, BLACK, board_rect, 3)
        else:
            pygame.draw.rect(self.screen, (210, 180, 140), board_rect)
            pygame.draw.rect(self.screen, BLACK, board_rect, 3)
        
        # Cabeçalho
        header = self.font_title.render(
            f"Sala de Espera - Jogadores: {len(self.connected_players)}/{self.num_players}", 
            True, WHITE
        )
        self.screen.blit(header, (20, 20))
        
        # Botão Iniciar Jogo (centro do tabuleiro)
        self._draw_start_button(board_rect)
        
        # Chat à direita
        self._draw_chat_panel(sidebar_rect)
        
        # Lista de jogadores no tabuleiro
        self._draw_players_on_board(board_rect)
    
    def _compute_layout(self):
        """Calcula o layout da tela"""
        left = self.padding
        top = self.padding + 60  # espaço para o cabeçalho
        usable_w = SCREEN_WIDTH - self.padding * 3 - self.sidebar_width
        usable_h = SCREEN_HEIGHT - self.padding * 2
        board_rect = pygame.Rect(left, top, usable_w, usable_h - top + self.padding)
        sidebar_x = left + usable_w + self.padding
        sidebar_rect = pygame.Rect(sidebar_x, self.padding, self.sidebar_width, SCREEN_HEIGHT - self.padding * 2)
        # dentro do chat
        input_h = 40
        chat_input_rect = pygame.Rect(sidebar_rect.left + 12, sidebar_rect.bottom - input_h - 12, sidebar_rect.width - 24, input_h)
        messages_rect = pygame.Rect(sidebar_rect.left + 12, sidebar_rect.top + 60, sidebar_rect.width - 24, sidebar_rect.height - 60 - input_h - 24)
        return {
            'board_rect': board_rect,
            'sidebar_rect': sidebar_rect,
            'chat_input_rect': chat_input_rect,
            'messages_rect': messages_rect,
        }
    
    def _draw_start_button(self, board_rect):
        """Desenha o botão de iniciar jogo no centro do tabuleiro"""
        center_x = board_rect.centerx
        center_y = board_rect.centery
        
        self.start_rect.center = (center_x, center_y)
        
        if len(self.connected_players) >= self.num_players:
            pygame.draw.rect(self.screen, (0, 200, 0), self.start_rect, border_radius=15)
            pygame.draw.rect(self.screen, BLACK, self.start_rect, 3, border_radius=15)
            start_text = self.font_text.render("INICIAR JOGO", True, WHITE)
            self.screen.blit(start_text, start_text.get_rect(center=self.start_rect.center))
        else:
            pygame.draw.rect(self.screen, (100, 100, 100), self.start_rect, border_radius=15)
            pygame.draw.rect(self.screen, BLACK, self.start_rect, 3, border_radius=15)
            start_text = self.font_text.render(
                f"Esperando ({len(self.connected_players)}/{self.num_players})", 
                True, (200, 200, 200)
            )
            self.screen.blit(start_text, start_text.get_rect(center=self.start_rect.center))
    
    def _draw_players_on_board(self, board_rect):
        """Desenha lista de jogadores no tabuleiro"""
        y_pos = board_rect.top + 50
        players_title = self.font_small.render("Jogadores Conectados:", True, WHITE)
        self.screen.blit(players_title, (board_rect.left + 20, y_pos))
        y_pos += 35
        
        for i, player in enumerate(self.connected_players):
            color = (100, 255, 100) if i < len(self.connected_players) else (200, 200, 200)
            player_text = self.font_small.render(f"• {player}", True, color)
            self.screen.blit(player_text, (board_rect.left + 30, y_pos))
            y_pos += 30
    
    def _draw_chat_panel(self, sidebar_rect):
        """Desenha o painel de chat (igual ao que tinha antes)"""
        pygame.draw.rect(self.screen, (245, 245, 245), sidebar_rect, border_radius=10)
        pygame.draw.rect(self.screen, BLACK, sidebar_rect, 2, border_radius=10)
        title = self.font_chat_title.render("Chat", True, BLACK)
        self.screen.blit(title, title.get_rect(midtop=(sidebar_rect.centerx, sidebar_rect.top + 12)))

        layout = self._compute_layout()
        messages_rect = layout['messages_rect']
        chat_input_rect = layout['chat_input_rect']

        # Mensagens (mostra as últimas que cabem)
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
        pygame.draw.rect(self.screen, input_color, chat_input_rect, border_radius=8)
        pygame.draw.rect(self.screen, BLACK, chat_input_rect, 1, border_radius=8)
        txt = self.font_chat_text.render(self.chat_input or "Digite uma mensagem...", True, BLACK if self.chat_input else (120, 120, 120))
        self.screen.blit(txt, (chat_input_rect.left + 8, chat_input_rect.top + 9))
    
    def _load_board_image(self):
        """Carrega a imagem do tabuleiro"""
        try:
            self.board_image = pygame.image.load(BOARD_IMAGE_PATH).convert_alpha()
        except Exception:
            self.board_image = None
    
    def _get_chat_input_rect(self):
        """Retorna o retângulo do input do chat"""
        layout = self._compute_layout()
        return layout['chat_input_rect']
    
    def _append_message(self, msg):
        """Adiciona mensagem ao chat"""
        self.chat_messages.append(msg)
        if len(self.chat_messages) > 100:
            self.chat_messages = self.chat_messages[-100:]


class ClassicPlayingScreen:
    """
    Tela simples de jogo clássico com um tabuleiro genérico placeholder
    """
    def __init__(self, screen):
        self.screen = screen
        self.font_title = pygame.font.Font(None, 48)
        self.num_players = 0
        self.is_paused = False
        self.menu_items = [
            { 'key': 'exit_game', 'label': 'Sair do jogo' },
            { 'key': 'invite_friends', 'label': 'Convidar amigos' },
            { 'key': 'back_to_menu', 'label': 'Voltar ao menu principal' },
            { 'key': 'toggle_fullscreen', 'label': 'Alternar tela cheia' },
        ]
        self.menu_rects = []
        self.board_image = None
        self._load_board_image()
        # Layout e chat
        self.sidebar_width = 320
        self.padding = 20
        self.chat_messages = []
        self.chat_input = ""
        self.chat_has_focus = False
        self.font_chat_title = pygame.font.Font(None, 40)
        self.font_chat_text = pygame.font.Font(None, 28)
        # Rede (cliente TCP)
        self.sock = None
        self.recv_thread = None
        self.recv_running = False
        self.reconnector_thread = None
        self.reconnect_in_progress = False
        self.auto_reconnect = True
        self.username = "Jogador"

    def start_new_game(self, num_players):
        self.num_players = num_players
        self.is_paused = False
        self.menu_rects = []
        self.chat_messages = []
        self.chat_input = ""
        self.chat_has_focus = False
        
        # Inicializar jogo The Resistance
        if RESISTANCE_AVAILABLE:
            try:
                self.resistance_game = ResistanceGame(num_players)
                self.player_names = [f"Jogador {i+1}" for i in range(num_players)]
                # Usar o primeiro jogador como o usuário atual
                if self.username not in self.player_names:
                    self.player_names[0] = self.username
                self.resistance_game.alocar_papeis_jogadores(self.player_names)
                self.selected_team = []
                self._append_message(f"[Sistema] Jogo The Resistance iniciado com {num_players} jogadores!")
            except Exception as e:
                self._append_message(f"[Erro] Falha ao iniciar The Resistance: {e}")
                self.resistance_game = None
        else:
            self.resistance_game = None
            self.player_names = [f"Jogador {i+1}" for i in range(num_players)]
        
        self._connect()

    def set_username(self, name: str):
        n = (name or "").strip()
        self.username = n if n else "Jogador"

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.is_paused = not self.is_paused
            return None
        if self.is_paused and event.type == pygame.MOUSEBUTTONDOWN:
            for rect, item in self.menu_rects:
                if rect.collidepoint(event.pos):
                    return item['key']
        if self.is_paused:
            return None

        # Eventos do jogo The Resistance
        if hasattr(self, 'resistance_game') and self.resistance_game is not None:
            try:
                estado = self.resistance_game.obter_estado_jogo()
                
                if event.type == pygame.MOUSEBUTTONDOWN and not estado['game_over']:
                    layout = self._compute_layout()
                    main_rect = layout['board_rect']
                    
                    # Verificar se clicou nos botões de voto
                    if estado['current_mission_team']:
                        y_pos = main_rect.top + 350
                        approve_rect = pygame.Rect(main_rect.left + 20, y_pos, 150, 40)
                        reject_rect = pygame.Rect(main_rect.left + 180, y_pos, 150, 40)
                        
                        if approve_rect.collidepoint(event.pos):
                            self.resistance_game.votar_proposta_time(self.username, Vote.APPROVE)
                            resultado = self.resistance_game.gerenciar_ciclo_votacao_time()
                            self._append_message(f"[Sistema] {resultado['message']}")
                            
                        elif reject_rect.collidepoint(event.pos):
                            self.resistance_game.votar_proposta_time(self.username, Vote.REJECT)
                            resultado = self.resistance_game.gerenciar_ciclo_votacao_time()
                            self._append_message(f"[Sistema] {resultado['message']}")
                            
                            if resultado['status'] == 'time_rejeitado':
                                self.selected_team = []
                    
                    # Verificar se é o líder e pode propor time
                    if estado['current_leader'] == self.username and not estado['current_mission_team']:
                        y_pos = main_rect.top + 200
                        for i, player in enumerate(self.player_names):
                            player_rect = pygame.Rect(main_rect.left + 30, y_pos + i * 25, 200, 25)
                            if player_rect.collidepoint(event.pos):
                                if player in self.selected_team:
                                    self.selected_team.remove(player)
                                else:
                                    mission_config = estado['mission_config']
                                    if len(self.selected_team) < mission_config['mission_size']:
                                        self.selected_team.append(player)
                        
                        # Botão para confirmar time
                        confirm_y = y_pos + len(self.player_names) * 25 + 20
                        confirm_rect = pygame.Rect(main_rect.left + 20, confirm_y, 200, 40)
                        if confirm_rect.collidepoint(event.pos) and len(self.selected_team) == estado['mission_config']['mission_size']:
                            if self.resistance_game.selecionar_time_missao(self.username, self.selected_team):
                                self._append_message(f"[Sistema] Time proposto: {', '.join(self.selected_team)}")
                                self.selected_team = []
            except Exception:
                pass  # Se houver erro, continuar normalmente

        # Eventos do chat
        layout = self._compute_layout()
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.chat_has_focus = layout['chat_input_rect'].collidepoint(event.pos)
        elif event.type == pygame.KEYDOWN and self.chat_has_focus:
            if event.key == pygame.K_RETURN:
                text = self.chat_input.strip()
                if text:
                    self._append_message(f"Você: {text}")
                    # Prefixa com username para os demais clientes
                    self._send_message(f"{self.username}: {text}")
                    self.chat_input = ""
            elif event.key == pygame.K_BACKSPACE:
                self.chat_input = self.chat_input[:-1]
            else:
                if event.unicode and len(self.chat_input) < 200 and ord(event.unicode) >= 32:
                    self.chat_input += event.unicode
        return None

    def draw(self):
        # Fundo
        self.screen.fill((34, 139, 34))  # verde de feltro
        
        layout = self._compute_layout()
        board_rect = layout['board_rect']
        sidebar_rect = layout['sidebar_rect']

        # Tabuleiro (imagem ou placeholder)
        if self.board_image:
            scaled = pygame.transform.smoothscale(self.board_image, (board_rect.width, board_rect.height))
            self.screen.blit(scaled, board_rect.topleft)
            pygame.draw.rect(self.screen, BLACK, board_rect, 3)
        else:
            pygame.draw.rect(self.screen, (210, 180, 140), board_rect)
            pygame.draw.rect(self.screen, BLACK, board_rect, 3)

        # grade apenas se não houver imagem
        cols = 10
        rows = 6
        cell_w = board_rect.width // cols
        cell_h = board_rect.height // rows
        if not self.board_image:
            for c in range(1, cols):
                x = board_rect.left + c * cell_w
                pygame.draw.line(self.screen, BLACK, (x, board_rect.top), (x, board_rect.bottom), 1)
            for r in range(1, rows):
                y = board_rect.top + r * cell_h
                pygame.draw.line(self.screen, BLACK, (board_rect.left, y), (board_rect.right, y), 1)

        # Verificar se The Resistance está ativo
        if hasattr(self, 'resistance_game') and self.resistance_game is not None:
            # Desenhar interface do The Resistance
            self._draw_resistance_game(board_rect)
        else:
            # Cabeçalho padrão
            header = self.font_title.render(f"Jogo Clássico - Jogadores: {self.num_players}", True, WHITE)
            self.screen.blit(header, (20, 20))

        # Painel de chat à direita
        self._draw_chat_panel(sidebar_rect)

        if self.is_paused:
            self._draw_pause_menu()
    
    def _draw_resistance_game(self, main_rect):
        """Desenha a interface do jogo The Resistance"""
        font_title = pygame.font.Font(None, 56)
        font_large = pygame.font.Font(None, 42)
        font_medium = pygame.font.Font(None, 32)
        font_small = pygame.font.Font(None, 24)
        
        # Título
        title = font_title.render("THE RESISTANCE", True, WHITE)
        self.screen.blit(title, (main_rect.left + 20, main_rect.top + 20))
        
        # Estado do jogo
        try:
            estado = self.resistance_game.obter_estado_jogo()
        except Exception as e:
            error_text = font_medium.render(f"Erro: {str(e)}", True, (255, 0, 0))
            self.screen.blit(error_text, (main_rect.left + 20, main_rect.top + 100))
            return
        
        y_pos = main_rect.top + 90
        
        # Informações gerais
        mission_info = font_medium.render(f"Missão {estado['mission_number']}/5", True, WHITE)
        self.screen.blit(mission_info, (main_rect.left + 20, y_pos))
        
        y_pos += 35
        leader_info = font_medium.render(f"Líder: {estado['current_leader']}", True, (255, 215, 0))
        self.screen.blit(leader_info, (main_rect.left + 20, y_pos))
        
        y_pos += 35
        score_info = font_medium.render(f"Sucessos: {estado['success_count']} | Falhas: {estado['failure_count']}", True, WHITE)
        self.screen.blit(score_info, (main_rect.left + 20, y_pos))
        
        # Verificar se o jogo terminou
        if estado['game_over']:
            y_pos += 50
            winner_text = "RESISTÊNCIA VENCEU!" if estado['winner'] == "Resistência" else "ESPIÕES VENCERAM!"
            winner_color = (0, 255, 0) if estado['winner'] == "Resistência" else (255, 0, 0)
            winner_surface = font_large.render(winner_text, True, winner_color)
            self.screen.blit(winner_surface, (main_rect.left + 20, y_pos))
            return
        
        y_pos += 50
        
        # Lista de jogadores
        players_title = font_medium.render("Jogadores:", True, WHITE)
        self.screen.blit(players_title, (main_rect.left + 20, y_pos))
        y_pos += 35
        
        for i, player in enumerate(self.player_names):
            role = self.resistance_game.definir_papel_jogador(player)
            role_text = "Espião" if role == PlayerRole.SPY else "Resistência"
            role_color = (255, 100, 100) if role == PlayerRole.SPY else (100, 255, 100)
            
            # Marcar se está selecionado
            marker = "[X] " if hasattr(self, 'selected_team') and player in self.selected_team else "[ ] "
            if player == self.username:
                marker += "VOCÊ - "
            
            player_text = font_small.render(f"{marker}{player}: {role_text}", True, role_color)
            self.screen.blit(player_text, (main_rect.left + 30, y_pos))
            y_pos += 25
        
        y_pos += 20
        
        # Configuração da missão atual
        if estado['mission_config']:
            config = estado['mission_config']
            mission_size_text = font_medium.render(
                f"Time necessário: {config['mission_size']} jogadores", True, WHITE
            )
            self.screen.blit(mission_size_text, (main_rect.left + 20, y_pos))
            y_pos += 35
            
            fails_text = font_medium.render(
                f"Falhas para sabotar: {config['fails_needed']}", True, (255, 200, 0)
            )
            self.screen.blit(fails_text, (main_rect.left + 20, y_pos))
            y_pos += 50
        
        # Time proposto
        if estado['current_mission_team']:
            team_title = font_medium.render("Time Proposto:", True, WHITE)
            self.screen.blit(team_title, (main_rect.left + 20, y_pos))
            y_pos += 35
            
            for player in estado['current_mission_team']:
                team_text = font_small.render(f"• {player}", True, WHITE)
                self.screen.blit(team_text, (main_rect.left + 30, y_pos))
                y_pos += 25
            
            y_pos += 20
            
            # Botões de voto (se ainda não votou)
            if not estado['leader_votes'] or self.username not in estado['leader_votes']:
                approve_rect = pygame.Rect(main_rect.left + 20, y_pos, 150, 40)
                reject_rect = pygame.Rect(main_rect.left + 180, y_pos, 150, 40)
                
                pygame.draw.rect(self.screen, (0, 200, 0), approve_rect, border_radius=8)
                pygame.draw.rect(self.screen, (200, 0, 0), reject_rect, border_radius=8)
                
                approve_text = font_small.render("Aprovar", True, WHITE)
                reject_text = font_small.render("Rejeitar", True, WHITE)
                
                self.screen.blit(approve_text, (approve_rect.centerx - 40, approve_rect.centery - 10))
                self.screen.blit(reject_text, (reject_rect.centerx - 40, reject_rect.centery - 10))
        
        # Botão de confirmar time (se líder está selecionando)
        if estado['current_leader'] == self.username and not estado['current_mission_team']:
            y_pos_confirm = main_rect.top + 200 + len(self.player_names) * 25 + 20
            if hasattr(self, 'selected_team') and len(self.selected_team) == estado['mission_config']['mission_size']:
                confirm_rect = pygame.Rect(main_rect.left + 20, y_pos_confirm, 200, 40)
                pygame.draw.rect(self.screen, (0, 150, 255), confirm_rect, border_radius=8)
                confirm_text = font_small.render("Confirmar Time", True, WHITE)
                self.screen.blit(confirm_text, (confirm_rect.centerx - 60, confirm_rect.centery - 10))
        
        # Histórico de missões
        if estado['mission_results']:
            y_pos = main_rect.bottom - 100
            history_title = font_medium.render("Histórico:", True, WHITE)
            self.screen.blit(history_title, (main_rect.left + 20, y_pos))
            y_pos += 30
            
            for i, result in enumerate(estado['mission_results'], 1):
                result_color = (0, 255, 0) if result == "Sucesso" else (255, 0, 0)
                result_text = font_small.render(f"Missão {i}: {result}", True, result_color)
                self.screen.blit(result_text, (main_rect.left + 30, y_pos))
                y_pos += 20
    
    def _load_board_image(self):
        try:
            self.board_image = pygame.image.load(BOARD_IMAGE_PATH).convert_alpha()
        except Exception:
            self.board_image = None

    def _draw_pause_menu(self):
        # Dimensões atuais da tela (responsivo)
        sw = self.screen.get_width()
        sh = self.screen.get_height()

        overlay = pygame.Surface((sw, sh), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.screen.blit(overlay, (0, 0))

        # Painel central dimensionado proporcionalmente
        panel_w = max(420, min(640, int(sw * 0.5)))
        panel_h = max(320, min(520, int(sh * 0.5)))
        panel_x = (sw - panel_w) // 2
        panel_y = (sh - panel_h) // 2
        panel_rect = pygame.Rect(panel_x, panel_y, panel_w, panel_h)
        pygame.draw.rect(self.screen, (245, 245, 245), panel_rect, border_radius=12)
        pygame.draw.rect(self.screen, BLACK, panel_rect, 3, border_radius=12)

        # Título
        title_font = pygame.font.Font(None, 56)
        title = title_font.render("Pausa", True, BLACK)
        self.screen.blit(title, title.get_rect(center=(panel_rect.centerx, panel_rect.top + 50)))

        # Itens do menu centralizados no painel
        self.menu_rects = []
        item_font = pygame.font.Font(None, 40)
        btn_w = int(panel_w * 0.8)
        btn_h = 56
        start_y = panel_rect.top + 110
        spacing = 72
        for i, item in enumerate(self.menu_items):
            r = pygame.Rect(0, 0, btn_w, btn_h)
            r.centerx = panel_rect.centerx
            r.y = start_y + i * spacing
            pygame.draw.rect(self.screen, LIGHT_GRAY, r, border_radius=10)
            pygame.draw.rect(self.screen, BLACK, r, 2, border_radius=10)
            label = item_font.render(item['label'], True, BLACK)
            self.screen.blit(label, label.get_rect(center=r.center))
            self.menu_rects.append((r, item))

    def _compute_layout(self):
        left = self.padding
        top = self.padding + 60  # espaço para o cabeçalho
        usable_w = SCREEN_WIDTH - self.padding * 3 - self.sidebar_width
        usable_h = SCREEN_HEIGHT - self.padding * 2
        board_rect = pygame.Rect(left, top, usable_w, usable_h - top + self.padding)
        sidebar_x = left + usable_w + self.padding
        sidebar_rect = pygame.Rect(sidebar_x, self.padding, self.sidebar_width, SCREEN_HEIGHT - self.padding * 2)
        # dentro do chat
        input_h = 40
        chat_input_rect = pygame.Rect(sidebar_rect.left + 12, sidebar_rect.bottom - input_h - 12, sidebar_rect.width - 24, input_h)
        messages_rect = pygame.Rect(sidebar_rect.left + 12, sidebar_rect.top + 60, sidebar_rect.width - 24, sidebar_rect.height - 60 - input_h - 24)
        return {
            'board_rect': board_rect,
            'sidebar_rect': sidebar_rect,
            'chat_input_rect': chat_input_rect,
            'messages_rect': messages_rect,
        }

    def _draw_chat_panel(self, sidebar_rect):
        pygame.draw.rect(self.screen, (245, 245, 245), sidebar_rect, border_radius=10)
        pygame.draw.rect(self.screen, BLACK, sidebar_rect, 2, border_radius=10)
        title = self.font_chat_title.render("Chat", True, BLACK)
        self.screen.blit(title, title.get_rect(midtop=(sidebar_rect.centerx, sidebar_rect.top + 12)))

        layout = self._compute_layout()
        messages_rect = layout['messages_rect']
        chat_input_rect = layout['chat_input_rect']

        # Mensagens (mostra as últimas que cabem)
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
        pygame.draw.rect(self.screen, input_color, chat_input_rect, border_radius=8)
        pygame.draw.rect(self.screen, BLACK, chat_input_rect, 1, border_radius=8)
        txt = self.font_chat_text.render(self.chat_input or "Digite uma mensagem...", True, BLACK if self.chat_input else (120, 120, 120))
        self.screen.blit(txt, (chat_input_rect.left + 8, chat_input_rect.top + 9))

    def _append_message(self, msg):
        self.chat_messages.append(msg)
        if len(self.chat_messages) > 200:
            self.chat_messages = self.chat_messages[-200:]

    # ============== Rede: Cliente TCP ==================
    def _connect(self):
        if self.sock is not None:
            return
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2.0)
            s.connect((SERVER_HOST, SERVER_PORT))
            s.settimeout(None)
            self.sock = s
            self._append_message(f"[sistema] Conectado ao servidor {SERVER_HOST}:{SERVER_PORT}")
            self.recv_running = True
            self.recv_thread = threading.Thread(target=self._recv_loop, daemon=True)
            self.recv_thread.start()
            self.reconnect_in_progress = False
        except Exception as e:
            self.sock = None
            self._append_message(f"[sistema] Falha na conexão: {e}")
            self._schedule_reconnect()

    def _disconnect(self):
        try:
            self.auto_reconnect = False
            self.recv_running = False
            if self.sock is not None:
                try:
                    # Tenta avisar saída
                    self.sock.sendall(b"/quit\n")
                except Exception:
                    pass
                try:
                    self.sock.shutdown(socket.SHUT_RDWR)
                except Exception:
                    pass
                try:
                    self.sock.close()
                except Exception:
                    pass
        finally:
            self.sock = None

    def _recv_loop(self):
        while self.recv_running and self.sock is not None:
            try:
                data = self.sock.recv(4096)
                if not data:
                    break
                text = data.decode('utf-8', errors='ignore')
                for line in text.splitlines():
                    line = line.strip()
                    if line:
                        self._append_message(line)
            except OSError:
                break
            except Exception:
                # Ignora erros transitórios, mantém loop
                continue
        self._append_message("[sistema] Desconectado do servidor")
        self.sock = None
        if self.auto_reconnect:
            self._schedule_reconnect()

    def _send_message(self, text: str):
        if not self.sock:
            # tenta reconectar em background e informa falha
            self._schedule_reconnect()
            return
        try:
            payload = (text + "\n").encode('utf-8')
            self.sock.sendall(payload)
        except Exception:
            self._append_message("[sistema] Erro ao enviar mensagem")
            self.sock = None
            if self.auto_reconnect:
                self._schedule_reconnect()

    def _schedule_reconnect(self):
        if self.reconnect_in_progress or not self.auto_reconnect:
            return
        self.reconnect_in_progress = True

        def worker():
            delay = 1.0
            max_delay = 10.0
            self._append_message("[sistema] Tentando reconectar...")
            while self.reconnect_in_progress and self.sock is None and self.auto_reconnect:
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(2.0)
                    s.connect((SERVER_HOST, SERVER_PORT))
                    s.settimeout(None)
                    self.sock = s
                    self._append_message(f"[sistema] Reconectado em {SERVER_HOST}:{SERVER_PORT}")
                    self.recv_running = True
                    self.recv_thread = threading.Thread(target=self._recv_loop, daemon=True)
                    self.recv_thread.start()
                    self.reconnect_in_progress = False
                    return
                except Exception:
                    pass
                import time
                time.sleep(delay)
                delay = min(max_delay, delay * 1.5)

        t = threading.Thread(target=worker, daemon=True)
        t.start()


class LobbyScreen:
    """
    Tela de lobby: inserir nome de usuário, mostrar link da sala e iniciar jogo
    (Placeholder offline: link é gerado localmente; não há rede real.)
    """
    def __init__(self, screen):
        self.screen = screen
        self.font_title = pygame.font.Font(None, 64)
        self.font_label = pygame.font.Font(None, 36)
        self.font_text = pygame.font.Font(None, 32)
        self.font_button = pygame.font.Font(None, 40)
        self.username = ""
        self.room_id = self._generate_room_id()
        self.input_rect = pygame.Rect(0, 0, 500, 48)
        self.link_rect = pygame.Rect(0, 0, 700, 48)
        self.button_rect = pygame.Rect(0, 0, 240, 56)
        self.copy_rect = pygame.Rect(0, 0, 140, 40)
        self.has_focus = False

    def reset(self):
        self.username = ""
        self.room_id = self._generate_room_id()
        self.has_focus = False

    def _generate_room_id(self):
        import random, string
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))

    def handle_event(self, event):
        sw = self.screen.get_width()
        sh = self.screen.get_height()
        center_x = sw // 2
        top = 160
        self.input_rect.center = (center_x, top + 80)
        self.link_rect.center = (center_x, top + 180)
        self.button_rect.center = (center_x, top + 280)
        self.copy_rect.topleft = (self.link_rect.right + 10, self.link_rect.top + 4)

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.has_focus = self.input_rect.collidepoint(event.pos)
            if self.copy_rect.collidepoint(event.pos):
                # Apenas imprime; copiar para clipboard exigiria pyperclip
                print("Link copiado:", self._room_url())
        elif event.type == pygame.KEYDOWN and self.has_focus:
            if event.key == pygame.K_RETURN:
                if self.username.strip():
                    return 'start_game'
            elif event.key == pygame.K_BACKSPACE:
                self.username = self.username[:-1]
            else:
                if event.unicode and len(self.username) < 24 and ord(event.unicode) >= 32:
                    self.username += event.unicode
        return None

    def draw(self):
        sw = self.screen.get_width()
        sh = self.screen.get_height()
        self.screen.fill((20, 24, 28))

        title = self.font_title.render("Lobby", True, WHITE)
        self.screen.blit(title, title.get_rect(center=(sw // 2, 90)))

        # Username
        label = self.font_label.render("Nome de usuário", True, WHITE)
        self.screen.blit(label, label.get_rect(center=(sw // 2, 140)))

        self.input_rect.width = min(600, int(sw * 0.6))
        self.input_rect.centerx = sw // 2
        pygame.draw.rect(self.screen, WHITE if self.has_focus else (235, 235, 235), self.input_rect, border_radius=8)
        pygame.draw.rect(self.screen, BLACK, self.input_rect, 2, border_radius=8)
        txt = self.font_text.render(self.username or "Digite seu nome...", True, BLACK if self.username else (120, 120, 120))
        self.screen.blit(txt, txt.get_rect(midleft=(self.input_rect.left + 12, self.input_rect.centery)))

        # Link da sala
        link_label = self.font_label.render("Link da sala", True, WHITE)
        self.screen.blit(link_label, link_label.get_rect(center=(sw // 2, 220)))
        self.link_rect.width = min(800, int(sw * 0.7))
        self.link_rect.centerx = sw // 2
        pygame.draw.rect(self.screen, (245, 245, 245), self.link_rect, border_radius=8)
        pygame.draw.rect(self.screen, BLACK, self.link_rect, 2, border_radius=8)
        link_txt = self.font_text.render(self._room_url(), True, BLACK)
        self.screen.blit(link_txt, link_txt.get_rect(midleft=(self.link_rect.left + 12, self.link_rect.centery)))

        # Botão copiar (placeholder)
        self.copy_rect = pygame.Rect(self.link_rect.right + 10, self.link_rect.top + 4, 140, 40)
        pygame.draw.rect(self.screen, (230, 230, 230), self.copy_rect, border_radius=8)
        pygame.draw.rect(self.screen, BLACK, self.copy_rect, 2, border_radius=8)
        copy_txt = self.font_text.render("Copiar", True, BLACK)
        self.screen.blit(copy_txt, copy_txt.get_rect(center=self.copy_rect.center))

        # Botão iniciar
        self.button_rect.width = 260
        self.button_rect.centerx = sw // 2
        pygame.draw.rect(self.screen, (235, 235, 0), self.button_rect, border_radius=10)
        pygame.draw.rect(self.screen, BLACK, self.button_rect, 2, border_radius=10)
        btn_label = self.font_button.render("Iniciar jogo", True, BLACK)
        self.screen.blit(btn_label, btn_label.get_rect(center=self.button_rect.center))

    def _room_url(self):
        return f"{BASE_ROOM_URL}{self.room_id}"
