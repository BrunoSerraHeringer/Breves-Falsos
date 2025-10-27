"""
Gerenciador principal do jogo THE RESISTANCE
Coordena todas as partes do sistema
"""

import pygame
from game_states import GameState
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from ui_system import UISystem
from room_system import RoomSystem
from resistance_system import ResistanceSystem
from settings_system import SettingsSystem
from theme_system import ThemeSystem
from key_repeat_system import KeyRepeatSystem


class GameManager:
    """
    Gerenciador principal que coordena todas as partes do jogo
    """
    
    def __init__(self):
        """Inicializa o gerenciador do jogo"""
        # Inicializar Pygame
        pygame.init()
        
        # Configurações da tela
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("War Board - THE RESISTANCE")
        self.clock = pygame.time.Clock()
        self.running = True
        self.is_fullscreen = False
        
        # Estado atual do jogo
        self.state = GameState.MENU
        self.previous_state = None  # Para lembrar tela anterior
        
        # Inicializar sistemas
        self._initialize_systems()
        
    def _initialize_systems(self):
        """Inicializa todos os sistemas do jogo"""
        
        # Criar instâncias dos sistemas
        self.theme_system = ThemeSystem()
        self.ui_system = UISystem(self.screen, self.theme_system)
        self.room_system = RoomSystem()
        self.resistance_system = ResistanceSystem()
        self.settings_system = SettingsSystem()
        self.key_repeat_system = KeyRepeatSystem()
        
        # Dados compartilhados
        self.player_data = {
            'username': 'Jogador',
            'room_code': '',
            'num_players': 5
        }
    
    def run(self):
        """Loop principal do jogo"""
        while self.running:
            self._handle_events()
            self._update()
            self._draw()
            self.clock.tick(FPS)
        
        self._cleanup()
    
    def _handle_events(self):
        """Processa todos os eventos do jogo"""
        # Atualizar sistema de repetição de teclas
        self.key_repeat_system.update()
        
        # Processar eventos normais
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
            elif event.type == pygame.VIDEORESIZE and not self.is_fullscreen:
                # Redimensionamento em tempo real (apenas se não estiver em tela cheia)
                try:
                    new_width = max(800, event.w)
                    new_height = max(600, event.h)
                    self.screen = pygame.display.set_mode((new_width, new_height), pygame.RESIZABLE)
                    self.ui_system.update_screen_size(new_width, new_height)
                    print(f"Tela redimensionada para: {new_width}x{new_height}")
                except Exception as e:
                    print(f"Erro ao redimensionar: {e}")
            
            try:
                # Delegar eventos para o sistema apropriado
                action = self._route_event(event)
                if action:
                    self._handle_action(action)
            except Exception as e:
                print(f"Erro ao processar evento: {e}")
                # Continuar funcionando mesmo com erro
        
        # Processar eventos de repetição de teclas
        for repeat_event in self.key_repeat_system.get_repeat_events():
            try:
                action = self._route_event(repeat_event)
                if action:
                    self._handle_action(action)
            except Exception as e:
                print(f"Erro ao processar evento de repetição: {e}")
                # Continuar funcionando mesmo com erro
    
    def _route_event(self, event):
        """Roteia eventos para o sistema apropriado"""
        try:
            # Tecla F11 para alternar fullscreen
            if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                self._toggle_fullscreen()
                return None
            if self.state == GameState.MENU:
                return self.ui_system.handle_menu_event(event)
            elif self.state == GameState.ROOM_MENU:
                return self.ui_system.handle_room_menu_event(event)
            elif self.state == GameState.CREATE_ROOM:
                return self.ui_system.handle_create_room_event(event)
            elif self.state == GameState.JOIN_ROOM:
                return self.ui_system.handle_join_room_event(event)
            elif self.state == GameState.PLAYER_NAME:
                return self.ui_system.handle_player_name_event(event)
            elif self.state == GameState.LOBBY:
                return self.ui_system.handle_lobby_event(event)
            elif self.state == GameState.PLAYING:
                return self.ui_system.handle_game_event(event)
            elif self.state == GameState.GAME_LOBBY:
                return self.ui_system.handle_game_lobby_event(event)
            elif self.state == GameState.SETTINGS:
                return self.ui_system.handle_settings_event(event)
        except Exception as e:
            print(f"Erro ao rotear evento: {e}")
            print(f"Estado atual: {self.state}")
        
        return None
    
    def _handle_action(self, action):
        """Processa ações retornadas pelos sistemas"""
        action_type = action.get('type')
        
        if action_type == 'change_state':
            new_state = action['new_state']
            # Se indo para configurações, lembrar tela atual
            if new_state == GameState.SETTINGS and self.state != GameState.SETTINGS:
                self.previous_state = self.state
            # Se saindo das configurações, voltar para tela anterior
            elif self.state == GameState.SETTINGS and new_state != GameState.SETTINGS:
                self.previous_state = None
            self.state = new_state
        elif action_type == 'update_player_data':
            self.player_data.update(action['data'])
        elif action_type == 'confirm_player_name':
            try:
                username = action.get('username', 'Jogador')
                if not username or not username.strip():
                    username = 'Jogador'
                self.player_data['username'] = username.strip()
                # Ir para o lobby
                self.state = GameState.LOBBY
            except Exception as e:
                print(f"Erro ao confirmar nome: {e}")
                # Usar nome padrão e continuar
                self.player_data['username'] = 'Jogador'
                self.state = GameState.LOBBY
        elif action_type == 'create_room':
            self.room_system.create_room(action['num_players'])
            self.player_data['room_code'] = self.room_system.get_room_code()
            self.player_data['num_players'] = action['num_players']
            self.player_data['is_host'] = True  # Quem cria a sala é o host
            # Ir para tela de nome do jogador
            self.state = GameState.PLAYER_NAME
        elif action_type == 'join_room':
            # Tentar entrar na sala
            success = self.room_system.join_room(action['room_code'], 'Jogador')
            if success:
                self.player_data['room_code'] = action['room_code']
                self.player_data['is_host'] = False  # Quem entra não é host
                # Obter dados da sala
                room_data = self.room_system.get_room_data()
                if room_data:
                    self.player_data['num_players'] = room_data['num_players']
                # Ir para tela de nome do jogador
                self.state = GameState.PLAYER_NAME
            else:
                # TODO: Mostrar erro de sala não encontrada
                print(f"Sala {action['room_code']} não encontrada ou cheia")
                return
        elif action_type == 'start_game':
            self.resistance_system.start_game(self.player_data['num_players'])
            # Ir para tela de jogo
            self.state = GameState.GAME_LOBBY
        elif action_type == 'apply_settings':
            print(f"Aplicando configurações: {action['settings']}")
            if self.settings_system.apply_settings(action['settings']):
                print("Configurações aplicadas com sucesso")
                # Aplicar mudanças de tela no Pygame
                self._apply_screen_settings()
                # Aplicar tema
                self._apply_theme()
                # Resetar flag para próxima vez
                self.ui_system.reset_settings_loaded()
                # Voltar para tela anterior
                if self.previous_state:
                    self.state = self.previous_state
                    self.previous_state = None
                else:
                    self.state = GameState.MENU
            else:
                print("Erro ao aplicar configurações")
        elif action_type == 'back_from_settings':
            # Voltar para tela anterior
            self.ui_system.reset_settings_loaded()  # Resetar flag para próxima vez
            if self.previous_state:
                self.state = self.previous_state
                self.previous_state = None
            else:
                self.state = GameState.MENU
        elif action_type == 'quit':
            self.running = False
    
    def _update(self):
        """Atualiza lógica do jogo"""
        # Atualizar sistemas baseado no estado
        if self.state == GameState.PLAYING:
            self.resistance_system.update()
    
    def _draw(self):
        """Desenha o jogo"""
        try:
            # Limpar tela
            self.screen.fill((0, 0, 0))
            
            # Desenhar baseado no estado
            if self.state == GameState.MENU:
                self.ui_system.draw_menu()
            elif self.state == GameState.ROOM_MENU:
                self.ui_system.draw_room_menu()
            elif self.state == GameState.CREATE_ROOM:
                self.ui_system.draw_create_room()
            elif self.state == GameState.JOIN_ROOM:
                self.ui_system.draw_join_room()
            elif self.state == GameState.PLAYER_NAME:
                self.ui_system.draw_player_name()
            elif self.state == GameState.LOBBY:
                self.ui_system.draw_lobby(self.player_data)
            elif self.state == GameState.PLAYING:
                self.ui_system.draw_game(self.resistance_system.get_game_state())
            elif self.state == GameState.GAME_LOBBY:
                self.ui_system.draw_game_lobby(self.player_data)
            elif self.state == GameState.SETTINGS:
                current_settings = self.settings_system.get_current_settings()
                self.ui_system.draw_settings(current_settings)
            
            pygame.display.flip()
        except Exception as e:
            print(f"Erro ao desenhar: {e}")
            print(f"Estado atual: {self.state}")
            # Desenhar tela de erro
            self.screen.fill((255, 0, 0))
            error_font = pygame.font.Font(None, 36)
            error_text = error_font.render(f"Erro: {str(e)}", True, (255, 255, 255))
            self.screen.blit(error_text, (50, 50))
            pygame.display.flip()
    
    def _apply_screen_settings(self):
        """Aplica configurações de tela"""
        settings = self.settings_system.get_current_settings()
        
        try:
            # Determinar se é tela cheia real ou resolução específica
            if settings.get('screen_width', 0) == 0:
                # Tela cheia real - usar toda a tela disponível
                self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                self.is_fullscreen = True
                actual_width = self.screen.get_width()
                actual_height = self.screen.get_height()
            else:
                # Resolução específica - usar dimensões definidas em janela normal
                width = settings['screen_width']
                height = settings['screen_height']
                self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
                self.is_fullscreen = False
                actual_width = width
                actual_height = height
            
            # Atualizar todas as telas com nova surface e resolução escolhida
            chosen_width = settings.get('screen_width', actual_width)
            chosen_height = settings.get('screen_height', actual_height)
            self.ui_system.update_screen_size(actual_width, actual_height, chosen_width, chosen_height)
            
            print(f"Tela configurada: {actual_width}x{actual_height} (Fullscreen: {settings['fullscreen']})")
            
        except pygame.error as e:
            print(f"Erro ao configurar tela: {e}")
    
    def _toggle_fullscreen(self):
        """Alterna entre fullscreen e janela"""
        try:
            settings = self.settings_system.get_current_settings()
            
            if self.is_fullscreen:
                # Sair do fullscreen - usar resolução específica em janela
                if settings.get('screen_width', 0) == 0:
                    # Se era tela cheia real, usar médio como padrão
                    width, height = 1024, 768
                else:
                    width, height = settings['screen_width'], settings['screen_height']
                
                self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
                self.is_fullscreen = False
                print(f"Saiu do fullscreen: {width}x{height}")
            else:
                # Entrar no fullscreen
                if settings.get('screen_width', 0) == 0:
                    # Tela cheia real
                    self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                else:
                    # Fullscreen com resolução específica
                    width, height = settings['screen_width'], settings['screen_height']
                    self.screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
                
                self.is_fullscreen = True
                print(f"Entrou no fullscreen: {self.screen.get_width()}x{self.screen.get_height()}")
            
            # Atualizar todas as telas
            actual_width = self.screen.get_width()
            actual_height = self.screen.get_height()
            self.ui_system.update_screen_size(actual_width, actual_height, settings.get('screen_width', actual_width), settings.get('screen_height', actual_height))
            
        except pygame.error as e:
            print(f"Erro ao alternar fullscreen: {e}")
            # Fallback para tela padrão
            self.screen = pygame.display.set_mode((1024, 768), pygame.RESIZABLE)
            self.is_fullscreen = False
            self.ui_system.update_screen_size(1024, 768)
    
    def _apply_theme(self):
        """Aplica o tema atual"""
        settings = self.settings_system.get_current_settings()
        theme_name = settings.get('theme', 'dark')
        
        # Atualizar tema no sistema de temas
        from theme_system import Theme
        if theme_name == 'light':
            self.theme_system.set_theme(Theme.LIGHT)
        else:
            self.theme_system.set_theme(Theme.DARK)
        
        # Recriar sistema de UI com novo tema
        self.ui_system = UISystem(self.screen, self.theme_system)
    
    def _cleanup(self):
        """Limpa recursos ao sair"""
        pygame.quit()


def main():
    """Função principal"""
    game = GameManager()
    game.run()


if __name__ == "__main__":
    main()
