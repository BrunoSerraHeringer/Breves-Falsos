"""
Sistema de Configurações
Gerencia todas as configurações do jogo
"""

import pygame
from typing import Dict, Tuple


class SettingsSystem:
    """
    Sistema responsável por gerenciar configurações do jogo
    """
    
    def __init__(self):
        """Inicializa o sistema de configurações"""
        self.settings = {
            'screen_width': 1024,  # Médio por padrão
            'screen_height': 768,
            'fullscreen': False,  # Janela normal por padrão
            'volume': 1.0,
            'show_fps': False,
            'language': 'pt',
            'theme': 'dark'  # dark ou light
        }
        
        self.available_sizes = [
            {"name": "Pequeno", "size": (640, 480)},
            {"name": "Médio", "size": (1024, 768)},
            {"name": "Grande", "size": (1600, 900)},
            {"name": "Tela Cheia", "size": (0, 0)}
        ]
    
    def get_current_settings(self) -> Dict:
        """Retorna as configurações atuais"""
        return self.settings.copy()
    
    def apply_settings(self, new_settings: Dict) -> bool:
        """
        Aplica novas configurações
        
        Args:
            new_settings: Dicionário com novas configurações
            
        Returns:
            True se aplicado com sucesso, False caso contrário
        """
        try:
            # Validar configurações
            if not self._validate_settings(new_settings):
                return False
            
            # Aplicar configurações
            self.settings.update(new_settings)
            
            # Aplicar mudanças de tela
            if 'screen_width' in new_settings or 'screen_height' in new_settings:
                self._apply_screen_settings()
            
            return True
        except Exception as e:
            print(f"Erro ao aplicar configurações: {e}")
            return False
    
    def _validate_settings(self, settings: Dict) -> bool:
        """Valida as configurações antes de aplicar"""
        # Validar tamanho da tela (0 é válido para breakpoints)
        if 'screen_width' in settings:
            if settings['screen_width'] != 0 and not (400 <= settings['screen_width'] <= 3840):
                return False
        
        if 'screen_height' in settings:
            if settings['screen_height'] != 0 and not (300 <= settings['screen_height'] <= 2160):
                return False
        
        # Validar volume
        if 'volume' in settings:
            if not (0.0 <= settings['volume'] <= 1.0):
                return False
        
        # Validar tema
        if 'theme' in settings:
            if settings['theme'] not in ['dark', 'light']:
                return False
        
        return True
    
    def _apply_screen_settings(self):
        """Aplica configurações de tela"""
        try:
            if self.settings['fullscreen']:
                pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            else:
                pygame.display.set_mode(
                    (self.settings['screen_width'], self.settings['screen_height']),
                    pygame.RESIZABLE
                )
        except Exception as e:
            print(f"Erro ao aplicar configurações de tela: {e}")
    
    def get_screen_size(self) -> Tuple[int, int]:
        """Retorna o tamanho atual da tela"""
        return (self.settings['screen_width'], self.settings['screen_height'])
    
    def is_fullscreen(self) -> bool:
        """Verifica se está em tela cheia"""
        return self.settings['fullscreen']
    
    def toggle_fullscreen(self):
        """Alterna entre tela cheia e janela"""
        self.settings['fullscreen'] = not self.settings['fullscreen']
        self._apply_screen_settings()
    
    def set_screen_size(self, width: int, height: int):
        """Define o tamanho da tela"""
        self.settings['screen_width'] = width
        self.settings['screen_height'] = height
        self.settings['fullscreen'] = False
        self._apply_screen_settings()
    
    def get_available_sizes(self) -> list:
        """Retorna lista de tamanhos disponíveis"""
        return self.available_sizes
    
    def save_settings(self, filename: str = "settings.json"):
        """Salva configurações em arquivo"""
        try:
            import json
            with open(filename, 'w') as f:
                json.dump(self.settings, f, indent=2)
            return True
        except Exception as e:
            print(f"Erro ao salvar configurações: {e}")
            return False
    
    def load_settings(self, filename: str = "settings.json"):
        """Carrega configurações de arquivo"""
        try:
            import json
            with open(filename, 'r') as f:
                loaded_settings = json.load(f)
            
            # Validar e aplicar configurações carregadas
            if self._validate_settings(loaded_settings):
                self.settings.update(loaded_settings)
                self._apply_screen_settings()
                return True
            return False
        except FileNotFoundError:
            # Arquivo não existe, usar configurações padrão
            return True
        except Exception as e:
            print(f"Erro ao carregar configurações: {e}")
            return False
