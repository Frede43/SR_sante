"""
Gestionnaire de scènes - Gère les différents états du jeu
"""

import pygame
from scenes.game_scene import GameScene
from scenes.menu_scene import MenuScene
from scenes.game_over_scene import GameOverScene

class SceneManager:
    def __init__(self, game):
        self.game = game
        self.current_scene = None
        self.scenes = {
            'menu': MenuScene(self),
            'game': GameScene(self),
            'game_over': GameOverScene(self)
        }
        
        # Commencer par le menu
        self.change_scene('menu')
    
    def change_scene(self, scene_name):
        """Change la scène actuelle"""
        if scene_name in self.scenes:
            if self.current_scene:
                self.current_scene.exit()
            
            self.current_scene = self.scenes[scene_name]
            self.current_scene.enter()
    
    def handle_event(self, event):
        """Transmet les événements à la scène actuelle"""
        if self.current_scene:
            self.current_scene.handle_event(event)
    
    def update(self, dt):
        """Met à jour la scène actuelle"""
        if self.current_scene:
            self.current_scene.update(dt)
    
    def render(self, screen):
        """Affiche la scène actuelle"""
        if self.current_scene:
            self.current_scene.render(screen)