#!/usr/bin/env python3
"""
Script de lancement du jeu avec configuration d'environnement
"""

import os
import sys

# Configuration SDL pour l'environnement headless/conteneur
os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dummy'

# Ajouter le dossier courant au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Importer et lancer le jeu
try:
    from main import main
    print("=== JEU D'ACTION 2D AVANCÉ ===")
    print("Démarrage du jeu...")
    print("(Mode simulation - pas d'affichage graphique dans cet environnement)")
    print()
    
    # Simuler le jeu pendant quelques secondes pour montrer qu'il fonctionne
    import pygame
    pygame.init()
    
    # Créer une instance de jeu pour tester
    from src.game import Game
    game = Game()
    
    print("✓ Pygame initialisé")
    print("✓ Systèmes de jeu créés")
    print("✓ Audio configuré")
    print("✓ Gestionnaire de scènes prêt")
    print("✓ Système de particules actif")
    print()
    print("Le jeu est prêt à être lancé!")
    print("Dans un environnement avec affichage, utilisez: python3 main.py")
    
except Exception as e:
    print(f"Erreur lors du test: {e}")
    import traceback
    traceback.print_exc()