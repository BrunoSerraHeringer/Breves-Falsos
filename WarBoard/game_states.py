"""
Estados e enums do jogo
"""

from enum import Enum


class GameState(Enum):
    """
    Estados possíveis do jogo
    """
    MENU = 1
    ROOM_MENU = 2
    CREATE_ROOM = 3
    JOIN_ROOM = 4
    PLAYER_NAME = 5
    CLASSIC_SETUP = 6
    PLAYING = 7
    SETTINGS = 8
    QUIT = 9
    LOBBY = 10
    GAME_LOBBY = 11
    PAUSED = 12
