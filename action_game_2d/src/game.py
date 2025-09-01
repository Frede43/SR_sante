"""
Classe principale du jeu - Gère la boucle de jeu et les états
"""

import pygame
import sys
from config import *
from systems.input_manager import InputManager
from systems.scene_manager import SceneManager
from systems.audio_manager import AudioManager
from systems.particle_system import ParticleSystem
from utils.save_system import SaveSystem

class Game:
    def __init__(self):
        """Initialise le jeu"""
        pygame.init()
        
        # Initialiser l'audio de manière sécurisée
        try:
            pygame.mixer.init()
            self.audio_enabled = True
        except pygame.error:
            print("Audio désactivé - pas de carte son disponible")
            self.audio_enabled = False
        
        # Configuration de l'écran
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Jeu d'Action 2D Avancé")
        self.clock = pygame.time.Clock()
        
        # Systèmes du jeu
        self.input_manager = InputManager()
        self.audio_manager = AudioManager() if self.audio_enabled else None
        self.particle_system = ParticleSystem()
        self.save_system = SaveSystem()
        self.scene_manager = SceneManager(self)
        
        # État du jeu
        self.running = True
        self.dt = 0
        
    def handle_events(self):
        """Gère les événements pygame"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            else:
                self.input_manager.handle_event(event)
                self.scene_manager.handle_event(event)
    
    def update(self):
        """Met à jour la logique du jeu"""
        self.input_manager.update()
        self.scene_manager.update(self.dt)
        self.particle_system.update(self.dt)
    
    def render(self):
        """Affiche le jeu"""
        self.screen.fill(BACKGROUND_COLOR)
        self.scene_manager.render(self.screen)
        self.particle_system.render(self.screen)
        pygame.display.flip()
    
    def run(self):
        """Boucle principale du jeu"""
        while self.running:
            self.dt = self.clock.tick(FPS) / 1000.0  # Delta time en secondes
            
            self.handle_events()
            self.update()
            self.render()
        
        pygame.quit()
        sys.exit()