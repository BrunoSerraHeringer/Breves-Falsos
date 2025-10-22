"""
Estados e enums do jogo
"""

from enum import Enum


class GameState(Enum):
    """
    Estados possíveis do jogo
    """
    MENU = 1
    CLASSIC_SETUP = 5
    PLAYING = 2
    SETTINGS = 3
    QUIT = 4
    LOBBY = 6
