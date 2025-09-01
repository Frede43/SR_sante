"""
Gestionnaire d'entrées - Gère clavier et souris
"""

import pygame

class InputManager:
    def __init__(self):
        self.keys_pressed = {}
        self.keys_just_pressed = {}
        self.keys_just_released = {}
        self.mouse_pos = (0, 0)
        self.mouse_pressed = {}
        self.mouse_just_pressed = {}
        
    def handle_event(self, event):
        """Gère les événements d'entrée"""
        if event.type == pygame.KEYDOWN:
            self.keys_just_pressed[event.key] = True
            self.keys_pressed[event.key] = True
            
        elif event.type == pygame.KEYUP:
            self.keys_just_released[event.key] = True
            self.keys_pressed[event.key] = False
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.mouse_just_pressed[event.button] = True
            self.mouse_pressed[event.button] = True
            
        elif event.type == pygame.MOUSEBUTTONUP:
            self.mouse_pressed[event.button] = False
    
    def update(self):
        """Met à jour l'état des entrées"""
        # Reset des états "just pressed/released"
        self.keys_just_pressed.clear()
        self.keys_just_released.clear()
        self.mouse_just_pressed.clear()
        
        # Mise à jour position souris
        self.mouse_pos = pygame.mouse.get_pos()
    
    def is_key_pressed(self, key):
        """Vérifie si une touche est maintenue"""
        return self.keys_pressed.get(key, False)
    
    def is_key_just_pressed(self, key):
        """Vérifie si une touche vient d'être pressée"""
        return self.keys_just_pressed.get(key, False)
    
    def is_key_just_released(self, key):
        """Vérifie si une touche vient d'être relâchée"""
        return self.keys_just_released.get(key, False)
    
    def is_mouse_pressed(self, button):
        """Vérifie si un bouton de souris est maintenu"""
        return self.mouse_pressed.get(button, False)
    
    def is_mouse_just_pressed(self, button):
        """Vérifie si un bouton de souris vient d'être pressé"""
        return self.mouse_just_pressed.get(button, False)
    
    def get_mouse_pos(self):
        """Retourne la position de la souris"""
        return self.mouse_pos