#!/usr/bin/env python3
"""
Jeu d'Action 2D Avancé
Un jeu de plateforme avec combat, ennemis intelligents et effets visuels
"""

import pygame
import sys
import os

# Ajouter le dossier src au path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.game import Game

def main():
    """Point d'entrée principal du jeu"""
    try:
        game = Game()
        game.run()
    except KeyboardInterrupt:
        print("\nJeu interrompu par l'utilisateur")
    except Exception as e:
        print(f"Erreur: {e}")
    finally:
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()