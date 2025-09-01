"""
Scène de fin de partie
"""

import pygame
from config import *

class GameOverScene:
    def __init__(self, scene_manager):
        self.scene_manager = scene_manager
        self.font_large = None
        self.font_medium = None
        self.font_small = None
        self.selected_option = 0
        self.menu_options = ["Rejouer", "Menu Principal"]
        self.final_score = 0
        self.final_wave = 1
        self.enemies_killed = 0
        self.time_survived = 0
        
    def set_game_stats(self, score, wave, enemies_killed, time_survived):
        """Définit les statistiques finales"""
        self.final_score = score
        self.final_wave = wave
        self.enemies_killed = enemies_killed
        self.time_survived = time_survived
    
    def enter(self):
        """Appelé quand on entre dans cette scène"""
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 32)
        
        # Sauvegarder le score
        if hasattr(self.scene_manager.game, 'save_system'):
            rank = self.scene_manager.game.save_system.add_score(
                self.final_score, self.final_wave, self.enemies_killed, self.time_survived
            )
            self.score_rank = rank
    
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
        if self.selected_option == 0:  # Rejouer
            self.scene_manager.change_scene('game')
        elif self.selected_option == 1:  # Menu Principal
            self.scene_manager.change_scene('menu')
    
    def update(self, dt):
        """Met à jour la logique du game over"""
        pass
    
    def render(self, screen):
        """Affiche l'écran de game over"""
        # Fond sombre avec transparence
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        
        # Titre
        title_text = self.font_large.render("GAME OVER", True, RED)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
        screen.blit(title_text, title_rect)
        
        # Statistiques
        stats_y = 250
        stats = [
            f"Score Final: {self.final_score}",
            f"Vague Atteinte: {self.final_wave}",
            f"Ennemis Éliminés: {self.enemies_killed}",
            f"Temps Survécu: {int(self.time_survived)}s"
        ]
        
        for i, stat in enumerate(stats):
            stat_text = self.font_small.render(stat, True, WHITE)
            stat_rect = stat_text.get_rect(center=(SCREEN_WIDTH // 2, stats_y + i * 40))
            screen.blit(stat_text, stat_rect)
        
        # Options du menu
        options_y = 450
        for i, option in enumerate(self.menu_options):
            color = YELLOW if i == self.selected_option else WHITE
            option_text = self.font_medium.render(option, True, color)
            option_rect = option_text.get_rect(center=(SCREEN_WIDTH // 2, options_y + i * 60))
            screen.blit(option_text, option_rect)
            
            # Indicateur de sélection
            if i == self.selected_option:
                pygame.draw.rect(screen, YELLOW, option_rect.inflate(20, 10), 3)
        
        # Instructions
        instruction_text = self.font_small.render("↑↓ pour naviguer, ENTRÉE pour sélectionner", True, GRAY)
        instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        screen.blit(instruction_text, instruction_rect)