"""
Scène du menu principal
"""

import pygame
from config import *

class MenuScene:
    def __init__(self, scene_manager):
        self.scene_manager = scene_manager
        self.font_large = None
        self.font_medium = None
        self.selected_option = 0
        self.menu_options = ["Jouer", "Quitter"]
        
    def enter(self):
        """Appelé quand on entre dans cette scène"""
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
    
    def exit(self):
        """Appelé quand on quitte cette scène"""
        pass
    
    def handle_event(self, event):
        """Gère les événements de la scène"""
        input_manager = self.scene_manager.game.input_manager
        
        if input_manager.is_key_just_pressed(pygame.K_UP):
            self.selected_option = (self.selected_option - 1) % len(self.menu_options)
        elif input_manager.is_key_just_pressed(pygame.K_DOWN):
            self.selected_option = (self.selected_option + 1) % len(self.menu_options)
        elif input_manager.is_key_just_pressed(pygame.K_RETURN) or input_manager.is_key_just_pressed(pygame.K_SPACE):
            self._select_option()
    
    def _select_option(self):
        """Exécute l'option sélectionnée"""
        if self.selected_option == 0:  # Jouer
            self.scene_manager.change_scene('game')
        elif self.selected_option == 1:  # Quitter
            self.scene_manager.game.running = False
    
    def update(self, dt):
        """Met à jour la logique du menu"""
        pass
    
    def render(self, screen):
        """Affiche le menu"""
        screen.fill(BLACK)
        
        # Titre
        title_text = self.font_large.render("JEU D'ACTION 2D", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
        screen.blit(title_text, title_rect)
        
        # Sous-titre
        subtitle_text = self.font_medium.render("Aventure Épique", True, GRAY)
        subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH // 2, 220))
        screen.blit(subtitle_text, subtitle_rect)
        
        # Options du menu
        start_y = 350
        for i, option in enumerate(self.menu_options):
            color = YELLOW if i == self.selected_option else WHITE
            option_text = self.font_medium.render(option, True, color)
            option_rect = option_text.get_rect(center=(SCREEN_WIDTH // 2, start_y + i * 80))
            screen.blit(option_text, option_rect)
            
            # Indicateur de sélection
            if i == self.selected_option:
                pygame.draw.rect(screen, YELLOW, option_rect.inflate(20, 10), 3)
        
        # Instructions
        instruction_font = pygame.font.Font(None, 32)
        instruction_text = instruction_font.render("Utilisez ↑↓ pour naviguer, ENTRÉE pour sélectionner", True, GRAY)
        instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        screen.blit(instruction_text, instruction_rect)