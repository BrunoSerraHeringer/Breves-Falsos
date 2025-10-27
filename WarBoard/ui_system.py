"""
Sistema de Interface do Usuário
Gerencia todas as telas e interações visuais
"""

import pygame
from game_states import GameState
from main_menu import MainMenu
from room_menu_screen import RoomMenuScreen
from create_room_screen import CreateRoomScreen
from join_room_screen import JoinRoomScreen
from player_name_screen import PlayerNameScreen
from settings_screen import SettingsScreen
from lobby_screen import LobbyScreen
from game_screen import GameScreen
from game_lobby_screen import GameLobbyScreen
from pause_screen import PauseScreen


class UISystem:
    """
    Sistema responsável por todas as interfaces do usuário
    """
    
    def __init__(self, screen, theme_system=None):
        """Inicializa o sistema de UI"""
        self.screen = screen
        self.theme_system = theme_system
        
        # Inicializar todas as telas
        self.screens = {
            'menu': MainMenu(screen),
            'room_menu': RoomMenuScreen(screen, theme_system),
            'create_room': CreateRoomScreen(screen, theme_system),
            'join_room': JoinRoomScreen(screen, theme_system),
            'player_name': PlayerNameScreen(screen, theme_system),
            'settings': SettingsScreen(screen, theme_system),
            'lobby': LobbyScreen(screen, theme_system),
            'game': GameScreen(screen, theme_system),
            'game_lobby': GameLobbyScreen(screen, theme_system),
            'pause': PauseScreen(screen, theme_system)
        }
        
        # Carregar configurações atuais na tela de configurações
        self._load_current_settings()
    
    def _load_current_settings(self):
        """Carrega as configurações atuais na tela de configurações"""
        try:
            # Importar aqui para evitar dependência circular
            from settings_system import SettingsSystem
            settings_system = SettingsSystem()
            current_settings = settings_system.get_current_settings()
            self.screens['settings'].load_current_settings(current_settings)
        except Exception as e:
            print(f"Erro ao carregar configurações atuais: {e}")
    
    # ============ EVENTOS ============
    
    def handle_menu_event(self, event):
        """Processa eventos do menu principal"""
        action = self.screens['menu'].handle_event(event)
        if action == 'jogo_classico':
            return {'type': 'change_state', 'new_state': GameState.ROOM_MENU}
        elif action == 'configuracoes':
            return {'type': 'change_state', 'new_state': GameState.SETTINGS}
        elif action == 'sair':
            return {'type': 'quit'}
        return None
    
    def handle_room_menu_event(self, event):
        """Processa eventos do menu de salas"""
        action = self.screens['room_menu'].handle_event(event)
        if action == 'create_room':
            return {'type': 'change_state', 'new_state': GameState.CREATE_ROOM}
        elif action == 'join_room':
            return {'type': 'change_state', 'new_state': GameState.JOIN_ROOM}
        elif action == 'back':
            return {'type': 'change_state', 'new_state': GameState.MENU}
        return None
    
    def handle_create_room_event(self, event):
        """Processa eventos da tela de criação de sala"""
        action = self.screens['create_room'].handle_event(event)
        if action == 'create_room':
            return {
                'type': 'create_room',
                'num_players': self.screens['create_room'].players
            }
        elif action == 'back':
            return {'type': 'change_state', 'new_state': GameState.ROOM_MENU}
        return None
    
    def handle_join_room_event(self, event):
        """Processa eventos da tela de entrada em sala"""
        action = self.screens['join_room'].handle_event(event)
        if action == 'join_room':
            return {
                'type': 'join_room',
                'room_code': self.screens['join_room'].get_room_code()
            }
        elif action == 'back':
            return {'type': 'change_state', 'new_state': GameState.ROOM_MENU}
        return None
    
    def handle_player_name_event(self, event):
        """Processa eventos da tela de nome do jogador"""
        action = self.screens['player_name'].handle_event(event)
        if action == 'confirm':
            return {
                'type': 'confirm_player_name',
                'username': self.screens['player_name'].player_name.strip() or 'Jogador'
            }
        elif action == 'back':
            return {'type': 'change_state', 'new_state': GameState.ROOM_MENU}
        return None
    
    def handle_lobby_event(self, event):
        """Processa eventos do lobby"""
        action = self.screens['lobby'].handle_event(event)
        if action == 'start_game':
            return {'type': 'start_game'}
        elif action == 'test_game_screen':
            return {'type': 'change_state', 'new_state': GameState.GAME_LOBBY}
        elif action == 'back':
            return {'type': 'change_state', 'new_state': GameState.ROOM_MENU}
        elif action == 'settings':
            return {'type': 'change_state', 'new_state': GameState.SETTINGS}
        return None
    
    def handle_game_event(self, event):
        """Processa eventos do jogo"""
        # Verificar ESC para configurações
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return {'type': 'change_state', 'new_state': GameState.SETTINGS}
        
        action = self.screens['game'].handle_event(event)
        if action == 'back_to_lobby':
            return {'type': 'change_state', 'new_state': GameState.LOBBY}
        elif action == 'quit_game':
            return {'type': 'quit'}
        return None
    
    def handle_settings_event(self, event):
        """Processa eventos das configurações"""
        action = self.screens['settings'].handle_event(event)
        
        if isinstance(action, dict) and action.get('action') == 'apply_settings':
            return {
                'type': 'apply_settings',
                'settings': action['settings']
            }
        elif action == 'back':
            # Voltar para tela anterior (será definida pelo GameManager)
            return {'type': 'back_from_settings'}
        return None
    
    def handle_game_lobby_event(self, event):
        """Processa eventos da tela de jogo"""
        action = self.screens['game_lobby'].handle_event(event)
        
        if action == 'back_to_lobby':
            return {'type': 'change_state', 'new_state': GameState.LOBBY}
        elif action == 'settings':
            return {'type': 'change_state', 'new_state': GameState.SETTINGS}
        elif action == 'pause':
            return {'type': 'pause_game'}
        
        return None
    
    def handle_pause_event(self, event):
        """Processa eventos da tela de pausa"""
        action = self.screens['pause'].handle_event(event)
        
        if action == 'resume':
            return {'type': 'resume_game'}
        elif action == 'settings':
            return {'type': 'change_state', 'new_state': GameState.SETTINGS}
        elif action == 'main_menu':
            return {'type': 'change_state', 'new_state': GameState.MENU}
        
        return None
    
    # ============ DESENHO ============
    
    def draw_menu(self):
        """Desenha o menu principal"""
        self.screens['menu'].draw()
    
    def draw_room_menu(self):
        """Desenha o menu de salas"""
        self.screens['room_menu'].draw()
    
    def draw_create_room(self):
        """Desenha a tela de criação de sala"""
        self.screens['create_room'].draw()
    
    def draw_join_room(self):
        """Desenha a tela de entrada em sala"""
        self.screens['join_room'].draw()
    
    def draw_player_name(self):
        """Desenha a tela de nome do jogador"""
        self.screens['player_name'].draw()
    
    def draw_lobby(self, player_data):
        """Desenha o lobby"""
        self.screens['lobby'].draw_with_data(player_data)
    
    def draw_game(self, game_state):
        """Desenha o jogo"""
        self.screens['game'].draw_with_state(game_state)
    
    def draw_settings(self, current_settings=None):
        """Desenha as configurações"""
        # Carregar configurações apenas se não foram carregadas ainda
        if not hasattr(self, '_settings_loaded') or not self._settings_loaded:
            # Usar configurações passadas ou carregar do sistema
            if current_settings is None:
                try:
                    from settings_system import SettingsSystem
                    settings_system = SettingsSystem()
                    current_settings = settings_system.get_current_settings()
                except Exception as e:
                    print(f"Erro ao carregar configurações atuais: {e}")
                    current_settings = {}
            
            # Aplicar configurações atuais na tela apenas uma vez
            self.screens['settings'].load_current_settings(current_settings)
            self._settings_loaded = True
        
        self.screens['settings'].draw()
    
    def reset_settings_loaded(self):
        """Reseta o flag de configurações carregadas"""
        self._settings_loaded = False
    
    def draw_game_lobby(self, game_data):
        """Desenha a tela de jogo com tabuleiro e chat"""
        self.screens['game_lobby'].set_game_data(game_data)
        self.screens['game_lobby'].draw()
    
    def draw_pause(self, previous_state):
        """Desenha a tela de pausa"""
        self.screens['pause'].set_previous_state(previous_state)
        self.screens['pause'].draw()
    
    # ============ ATUALIZAÇÕES ============
    
    def update_screen_size(self, width, height, chosen_width=None, chosen_height=None):
        """Atualiza o tamanho da tela para todas as telas"""
        # Usar resolução escolhida se disponível, senão usar resolução real
        effective_width = chosen_width if chosen_width else width
        effective_height = chosen_height if chosen_height else height
        
        print(f"Atualizando telas: real={width}x{height}, escolhida={effective_width}x{effective_height}")
        
        for screen in self.screens.values():
            if hasattr(screen, 'screen'):
                screen.screen = self.screen
            # Passar resolução escolhida para telas que suportam
            if hasattr(screen, 'set_chosen_resolution'):
                screen.set_chosen_resolution(effective_width, effective_height)
            if hasattr(screen, 'update_layout'):
                screen.update_layout()
