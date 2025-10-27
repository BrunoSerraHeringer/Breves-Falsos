"""
Sistema de Temas
Gerencia temas dark e light para o jogo
"""

from enum import Enum
from typing import Dict, Tuple


class Theme(Enum):
    """Temas disponíveis"""
    LIGHT = "light"
    DARK = "dark"


class ThemeSystem:
    """
    Sistema responsável por gerenciar temas do jogo
    """
    
    def __init__(self):
        """Inicializa o sistema de temas"""
        self.current_theme = Theme.DARK
        self.themes = self._create_themes()
    
    def _create_themes(self) -> Dict[Theme, Dict[str, Tuple[int, int, int]]]:
        """Cria as paletas de cores para cada tema"""
        return {
            Theme.LIGHT: {
                # Cores principais - apenas preto/branco
                'background': (255, 255, 255),      # Fundo branco
                'surface': (255, 255, 255),         # Superfícies brancas
                'primary': (0, 0, 0),               # Preto principal
                'secondary': (0, 0, 0),             # Preto secundário
                'accent': (0, 0, 0),                # Preto de destaque
                'error': (255, 0, 0),               # Vermelho de erro
                'warning': (255, 165, 0),           # Laranja de aviso
                'success': (0, 128, 0),             # Verde de sucesso
                
                # Cores de texto
                'text_primary': (0, 0, 0),          # Texto preto
                'text_secondary': (0, 0, 0),        # Texto preto
                'text_muted': (128, 128, 128),      # Cinza
                'text_inverse': (255, 255, 255),    # Texto branco
                
                # Cores específicas do jogo
                'board_background': (210, 180, 140), # Fundo do tabuleiro (mantém)
                'board_border': (0, 0, 0),           # Borda do tabuleiro
                'chat_background': (255, 255, 255),  # Fundo do chat branco
                'chat_border': (0, 0, 0),            # Borda do chat preta
                'input_background': (255, 255, 255), # Fundo de input branco
                'input_border': (0, 0, 0),           # Borda de input preta
                'input_focus': (0, 0, 255),          # Borda de foco azul
                
                # Cores de jogadores
                'player_connected': (0, 128, 0),     # Verde
                'player_disconnected': (128, 128, 128), # Cinza
                'player_highlight': (255, 165, 0),   # Laranja
                
                # Cores de resistência
                'resistance_primary': (220, 38, 127), # Rosa principal
                'resistance_secondary': (147, 51, 234), # Roxo secundário
                'spy_color': (255, 0, 0),           # Vermelho dos espiões
                'resistance_color': (0, 128, 0),    # Verde da resistência
            },
            
            Theme.DARK: {
                # Cores principais - apenas preto/branco
                'background': (0, 0, 0),             # Fundo preto
                'surface': (0, 0, 0),                # Superfícies pretas
                'primary': (255, 255, 255),          # Branco principal
                'secondary': (255, 255, 255),        # Branco secundário
                'accent': (255, 255, 255),           # Branco de destaque
                'error': (255, 0, 0),                # Vermelho de erro
                'warning': (255, 165, 0),            # Laranja de aviso
                'success': (0, 128, 0),              # Verde de sucesso
                
                # Cores de texto
                'text_primary': (255, 255, 255),     # Texto branco
                'text_secondary': (255, 255, 255),   # Texto branco
                'text_muted': (128, 128, 128),       # Cinza
                'text_inverse': (0, 0, 0),           # Texto preto
                
                # Cores específicas do jogo
                'board_background': (210, 180, 140), # Fundo do tabuleiro (mantém)
                'board_border': (0, 0, 0),           # Borda do tabuleiro
                'chat_background': (0, 0, 0),        # Fundo do chat preto
                'chat_border': (255, 255, 255),      # Borda do chat branca
                'input_background': (0, 0, 0),       # Fundo de input preto
                'input_border': (255, 255, 255),     # Borda de input branca
                'input_focus': (0, 0, 255),          # Borda de foco azul
                
                # Cores de jogadores
                'player_connected': (0, 128, 0),     # Verde
                'player_disconnected': (128, 128, 128), # Cinza
                'player_highlight': (255, 165, 0),   # Laranja
                
                # Cores de resistência
                'resistance_primary': (220, 38, 127), # Rosa principal
                'resistance_secondary': (147, 51, 234), # Roxo secundário
                'spy_color': (255, 0, 0),           # Vermelho dos espiões
                'resistance_color': (0, 128, 0),    # Verde da resistência
            }
        }
    
    def get_current_theme(self) -> Theme:
        """Retorna o tema atual"""
        return self.current_theme
    
    def set_theme(self, theme: Theme):
        """Define o tema atual"""
        self.current_theme = theme
    
    def get_color(self, color_name: str) -> Tuple[int, int, int]:
        """Retorna uma cor do tema atual"""
        theme_colors = self.themes[self.current_theme]
        return theme_colors.get(color_name, (255, 255, 255))  # Branco como fallback
    
    def get_all_colors(self) -> Dict[str, Tuple[int, int, int]]:
        """Retorna todas as cores do tema atual"""
        return self.themes[self.current_theme].copy()
    
    def toggle_theme(self):
        """Alterna entre tema dark e light"""
        if self.current_theme == Theme.DARK:
            self.current_theme = Theme.LIGHT
        else:
            self.current_theme = Theme.DARK
    
    def get_theme_name(self) -> str:
        """Retorna o nome do tema atual"""
        return "Claro" if self.current_theme == Theme.LIGHT else "Escuro"
    
    def get_available_themes(self) -> list:
        """Retorna lista de temas disponíveis"""
        return [
            {"name": "Escuro", "value": Theme.DARK},
            {"name": "Claro", "value": Theme.LIGHT}
        ]
