"""
War Board - THE RESISTANCE
Ponto de entrada principal do jogo
"""

import pygame
import sys
from game_manager import GameManager


def main():
    """
    Função principal que inicializa e executa o jogo
    """
    try:
        # Criar e executar o jogo
        game = GameManager()
        game.run()
    except KeyboardInterrupt:
        print("\nJogo interrompido pelo usuário")
    except Exception as e:
        print(f"Erro inesperado: {e}")
        sys.exit(1)
    finally:
        pygame.quit()


if __name__ == "__main__":
    main()

