"""
War Board - Estratégia de Guerra
Ponto de entrada principal do jogo
"""

import pygame
from game import Game


def main():
    """
    Função principal que inicializa e executa o jogo
    """
    # Inicializar Pygame
    pygame.init()
    
    # Criar e executar o jogo
    game = Game()
    game.run()


if __name__ == "__main__":
    main()

