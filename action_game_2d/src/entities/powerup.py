"""
Système de power-ups - Améliorations temporaires et permanentes
"""

import pygame
import math
import random
from config import *

class PowerUp:
    def __init__(self, x, y, powerup_type="health"):
        self.x = x
        self.y = y
        self.width = 24
        self.height = 24
        self.type = powerup_type
        
        # Animation
        self.float_offset = 0
        self.rotation = 0
        self.pulse_scale = 1.0
        
        # Durée de vie
        self.lifetime = 15.0  # Disparaît après 15 secondes
        
        # Rectangle de collision
        self.rect = pygame.Rect(x, y, self.width, self.height)
        
        # Propriétés selon le type
        self.color, self.effect = self._get_powerup_properties()
    
    def _get_powerup_properties(self):
        """Retourne les propriétés selon le type de power-up"""
        if self.type == "health":
            return GREEN, "Restaure 30 points de vie"
        elif self.type == "speed":
            return BLUE, "Augmente la vitesse pendant 10s"
        elif self.type == "damage":
            return RED, "Double les dégâts pendant 8s"
        elif self.type == "shield":
            return PURPLE, "Bouclier temporaire"
        elif self.type == "multi_shot":
            return ORANGE, "Tir multiple pendant 12s"
        else:
            return YELLOW, "Power-up mystérieux"
    
    def update(self, dt):
        """Met à jour le power-up"""
        # Animation flottante
        self.float_offset = math.sin(pygame.time.get_ticks() * 0.003) * 5
        self.rotation += dt * 2
        
        # Pulsation
        pulse_speed = 4
        self.pulse_scale = 1.0 + math.sin(pygame.time.get_ticks() * 0.01 * pulse_speed) * 0.2
        
        # Mettre à jour la position
        self.rect.y = int(self.y + self.float_offset)
        
        # Durée de vie
        self.lifetime -= dt
        
        return self.lifetime > 0
    
    def apply_effect(self, player):
        """Applique l'effet du power-up au joueur"""
        if self.type == "health":
            player.heal(30)
        elif self.type == "speed":
            player.speed_boost_time = 10.0
            player.speed_multiplier = 1.5
        elif self.type == "damage":
            player.damage_boost_time = 8.0
            player.damage_multiplier = 2.0
        elif self.type == "shield":
            player.shield_time = 5.0
        elif self.type == "multi_shot":
            player.multi_shot_time = 12.0
    
    def render(self, screen):
        """Affiche le power-up"""
        # Calculer la taille avec pulsation
        size = int(self.width * self.pulse_scale)
        
        # Position centrée
        render_x = self.rect.centerx - size // 2
        render_y = self.rect.centery - size // 2
        
        # Effet de lueur
        glow_size = size + 8
        glow_surf = pygame.Surface((glow_size, glow_size), pygame.SRCALPHA)
        glow_color = (*self.color[:3], 50)
        pygame.draw.circle(glow_surf, glow_color, (glow_size // 2, glow_size // 2), glow_size // 2)
        screen.blit(glow_surf, (render_x - 4, render_y - 4))
        
        # Power-up principal
        if self.type == "health":
            # Croix médicale
            pygame.draw.circle(screen, self.color, (render_x + size // 2, render_y + size // 2), size // 2)
            pygame.draw.rect(screen, WHITE, (render_x + size // 2 - 2, render_y + 4, 4, size - 8))
            pygame.draw.rect(screen, WHITE, (render_x + 4, render_y + size // 2 - 2, size - 8, 4))
        
        elif self.type == "speed":
            # Éclair
            pygame.draw.circle(screen, self.color, (render_x + size // 2, render_y + size // 2), size // 2)
            points = [
                (render_x + size // 2, render_y + 4),
                (render_x + size // 2 + 4, render_y + size // 2),
                (render_x + size // 2, render_y + size - 4),
                (render_x + size // 2 - 4, render_y + size // 2)
            ]
            pygame.draw.polygon(screen, WHITE, points)
        
        elif self.type == "damage":
            # Épée
            pygame.draw.circle(screen, self.color, (render_x + size // 2, render_y + size // 2), size // 2)
            pygame.draw.rect(screen, WHITE, (render_x + size // 2 - 1, render_y + 4, 2, size - 8))
            pygame.draw.rect(screen, WHITE, (render_x + size // 2 - 3, render_y + 6, 6, 3))
        
        elif self.type == "shield":
            # Bouclier
            pygame.draw.circle(screen, self.color, (render_x + size // 2, render_y + size // 2), size // 2)
            shield_rect = pygame.Rect(render_x + 4, render_y + 4, size - 8, size - 8)
            pygame.draw.ellipse(screen, WHITE, shield_rect, 2)
        
        elif self.type == "multi_shot":
            # Trois cercles
            pygame.draw.circle(screen, self.color, (render_x + size // 2, render_y + size // 2), size // 2)
            pygame.draw.circle(screen, WHITE, (render_x + size // 2 - 4, render_y + size // 2), 2)
            pygame.draw.circle(screen, WHITE, (render_x + size // 2, render_y + size // 2), 2)
            pygame.draw.circle(screen, WHITE, (render_x + size // 2 + 4, render_y + size // 2), 2)
        
        # Contour
        pygame.draw.circle(screen, WHITE, (render_x + size // 2, render_y + size // 2), size // 2, 2)

class PowerUpManager:
    def __init__(self):
        self.powerups = []
        self.spawn_timer = 0
        self.spawn_delay = 8.0  # Nouveau power-up toutes les 8 secondes
    
    def update(self, dt):
        """Met à jour tous les power-ups"""
        # Mettre à jour les power-ups existants
        self.powerups = [p for p in self.powerups if p.update(dt)]
        
        # Spawner de nouveaux power-ups
        self.spawn_timer += dt
        if self.spawn_timer > self.spawn_delay:
            self._spawn_random_powerup()
            self.spawn_timer = 0
    
    def _spawn_random_powerup(self):
        """Spawne un power-up aléatoire"""
        if len(self.powerups) < 3:  # Limite de 3 power-ups simultanés
            # Position aléatoire
            x = random.randint(50, SCREEN_WIDTH - 50)
            y = random.randint(100, SCREEN_HEIGHT - 200)
            
            # Type aléatoire
            powerup_type = random.choice(["health", "speed", "damage", "shield", "multi_shot"])
            
            powerup = PowerUp(x, y, powerup_type)
            self.powerups.append(powerup)
    
    def check_collision_with_player(self, player_rect):
        """Vérifie les collisions avec le joueur"""
        collected = []
        for powerup in self.powerups[:]:
            if powerup.rect.colliderect(player_rect):
                collected.append(powerup)
                self.powerups.remove(powerup)
        return collected
    
    def render(self, screen):
        """Affiche tous les power-ups"""
        for powerup in self.powerups:
            powerup.render(screen)