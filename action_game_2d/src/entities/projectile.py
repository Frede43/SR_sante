"""
Classe des projectiles - Balles, flèches, etc.
"""

import pygame
import math
from config import *

class Projectile:
    def __init__(self, x, y, target_x, target_y, damage=15, speed=PROJECTILE_SPEED, projectile_type="bullet"):
        self.x = x
        self.y = y
        self.damage = damage
        self.speed = speed
        self.type = projectile_type
        
        # Calculer la direction
        dx = target_x - x
        dy = target_y - y
        distance = math.sqrt(dx * dx + dy * dy)
        
        if distance > 0:
            self.velocity_x = (dx / distance) * speed
            self.velocity_y = (dy / distance) * speed
        else:
            self.velocity_x = speed
            self.velocity_y = 0
        
        # Propriétés visuelles
        self.width = 8 if projectile_type == "bullet" else 12
        self.height = 4 if projectile_type == "bullet" else 8
        self.color = YELLOW if projectile_type == "bullet" else ORANGE
        
        # Rectangle de collision
        self.rect = pygame.Rect(x, y, self.width, self.height)
        
        # Durée de vie
        self.lifetime = 3.0
        self.trail_timer = 0
    
    def update(self, dt, particle_system=None):
        """Met à jour le projectile"""
        # Mouvement
        self.x += self.velocity_x * dt * 60
        self.y += self.velocity_y * dt * 60
        
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        
        # Traînée de particules
        if particle_system:
            self.trail_timer += dt
            if self.trail_timer > 0.05:
                particle_system.add_trail(self.rect.centerx, self.rect.centery, self.color, 1)
                self.trail_timer = 0
        
        # Durée de vie
        self.lifetime -= dt
        
        return self.lifetime > 0 and self._is_on_screen()
    
    def _is_on_screen(self):
        """Vérifie si le projectile est encore à l'écran"""
        return (self.rect.right > 0 and self.rect.left < SCREEN_WIDTH and
                self.rect.bottom > 0 and self.rect.top < SCREEN_HEIGHT)
    
    def render(self, screen):
        """Affiche le projectile"""
        if self.type == "bullet":
            pygame.draw.ellipse(screen, self.color, self.rect)
            # Effet de lueur
            glow_rect = self.rect.inflate(4, 4)
            glow_color = (*self.color[:3], 100)
            glow_surf = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
            pygame.draw.ellipse(glow_surf, glow_color, glow_surf.get_rect())
            screen.blit(glow_surf, glow_rect)
        else:
            # Projectile en forme de flèche
            pygame.draw.rect(screen, self.color, self.rect)
            # Pointe
            if self.velocity_x > 0:
                points = [(self.rect.right, self.rect.centery),
                         (self.rect.right - 6, self.rect.top),
                         (self.rect.right - 6, self.rect.bottom)]
            else:
                points = [(self.rect.left, self.rect.centery),
                         (self.rect.left + 6, self.rect.top),
                         (self.rect.left + 6, self.rect.bottom)]
            pygame.draw.polygon(screen, self.color, points)

class ProjectileManager:
    def __init__(self):
        self.projectiles = []
    
    def add_projectile(self, x, y, target_x, target_y, damage=15, speed=PROJECTILE_SPEED, projectile_type="bullet"):
        """Ajoute un nouveau projectile"""
        projectile = Projectile(x, y, target_x, target_y, damage, speed, projectile_type)
        self.projectiles.append(projectile)
        return projectile
    
    def update(self, dt, particle_system=None):
        """Met à jour tous les projectiles"""
        self.projectiles = [p for p in self.projectiles if p.update(dt, particle_system)]
    
    def check_collision_with_rect(self, rect):
        """Vérifie les collisions avec un rectangle et retourne les projectiles qui touchent"""
        hit_projectiles = []
        for projectile in self.projectiles[:]:
            if projectile.rect.colliderect(rect):
                hit_projectiles.append(projectile)
                self.projectiles.remove(projectile)
        return hit_projectiles
    
    def render(self, screen):
        """Affiche tous les projectiles"""
        for projectile in self.projectiles:
            projectile.render(screen)