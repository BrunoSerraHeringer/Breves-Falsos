#!/usr/bin/env python3
"""
Script para executar o jogo THE RESISTANCE
"""

import sys
import os

# Adicionar o diretório WarBoard ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'WarBoard'))

# Executar o jogo
if __name__ == "__main__":
    try:
        import main
    except ImportError as e:
        print(f"Erro ao importar o jogo: {e}")
        print("Verifique se todos os arquivos estão no diretório WarBoard/")
        sys.exit(1)
    except Exception as e:
        print(f"Erro ao executar o jogo: {e}")
        sys.exit(1)

