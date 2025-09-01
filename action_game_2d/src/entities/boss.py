"""
Classe de boss - Ennemis plus puissants avec patterns d'attaque complexes
"""

import pygame
import math
import random
from config import *
from entities.projectile import Projectile

class Boss:
    def __init__(self, x, y, boss_type="fire_demon"):
        self.x = x
        self.y = y
        self.width = 64
        self.height = 80
        self.velocity_x = 0
        self.velocity_y = 0
        
        # État du boss
        self.boss_type = boss_type
        self.health = 300
        self.max_health = 300
        self.facing_right = True
        self.on_ground = False
        
        # IA du boss
        self.ai_state = "approach"  # approach, attack_pattern_1, attack_pattern_2, retreat
        self.ai_timer = 0
        self.attack_timer = 0
        self.phase = 1
        
        # Patterns d'attaque
        self.attack_cooldown = 0
        self.special_attack_cooldown = 0
        self.projectiles = []
        
        # Animation
        self.animation_time = 0
        self.hurt_flash_time = 0
        
        # Rectangle de collision
        self.rect = pygame.Rect(x, y, self.width, self.height)
        
        # Créer les sprites
        self.sprites = self._create_boss_sprites()
    
    def _create_boss_sprites(self):
        """Crée les sprites du boss"""
        sprites = {}
        
        # Couleurs selon le type
        if self.boss_type == "fire_demon":
            body_color = (200, 50, 50)
            accent_color = ORANGE
            eye_color = YELLOW
        else:
            body_color = DARK_GRAY
            accent_color = PURPLE
            eye_color = RED
        
        # Sprite principal
        sprite = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        # Corps principal
        pygame.draw.ellipse(sprite, body_color, (8, 20, 48, 50))
        
        # Tête
        pygame.draw.circle(sprite, body_color, (32, 20), 20)
        
        # Yeux brillants
        pygame.draw.circle(sprite, eye_color, (25, 15), 4)
        pygame.draw.circle(sprite, eye_color, (39, 15), 4)
        pygame.draw.circle(sprite, WHITE, (25, 15), 2)
        pygame.draw.circle(sprite, WHITE, (39, 15), 2)
        
        # Cornes
        points_left = [(20, 8), (18, 2), (22, 6)]
        points_right = [(44, 8), (46, 2), (42, 6)]
        pygame.draw.polygon(sprite, accent_color, points_left)
        pygame.draw.polygon(sprite, accent_color, points_right)
        
        # Bras
        pygame.draw.ellipse(sprite, body_color, (0, 25, 16, 30))
        pygame.draw.ellipse(sprite, body_color, (48, 25, 16, 30))
        
        # Détails
        pygame.draw.circle(sprite, accent_color, (32, 35), 6)
        pygame.draw.circle(sprite, accent_color, (32, 50), 4)
        
        sprites['normal'] = sprite
        
        # Sprite d'attaque (yeux plus brillants)
        attack_sprite = sprite.copy()
        pygame.draw.circle(attack_sprite, WHITE, (25, 15), 6)
        pygame.draw.circle(attack_sprite, WHITE, (39, 15), 6)
        sprites['attack'] = attack_sprite
        
        return sprites
    
    def update(self, dt, player, platforms=None, projectile_manager=None):
        """Met à jour le boss"""
        # Timers
        self.attack_cooldown = max(0, self.attack_cooldown - dt)
        self.special_attack_cooldown = max(0, self.special_attack_cooldown - dt)
        self.hurt_flash_time = max(0, self.hurt_flash_time - dt)
        self.ai_timer += dt
        self.attack_timer += dt
        
        # Changer de phase selon la vie
        if self.health < self.max_health * 0.5 and self.phase == 1:
            self.phase = 2
            self.ai_state = "attack_pattern_2"
            self.ai_timer = 0
        
        # IA
        self._update_ai(player, dt, projectile_manager)
        
        # Physique
        self._update_physics(dt, platforms)
        
        # Animation
        self.animation_time += dt
    
    def _update_ai(self, player, dt, projectile_manager):
        """Met à jour l'IA du boss"""
        if not player:
            return
        
        distance_to_player = math.sqrt(
            (player.rect.centerx - self.rect.centerx) ** 2 + 
            (player.rect.centery - self.rect.centery) ** 2
        )
        
        # Orientation vers le joueur
        if player.rect.centerx > self.rect.centerx:
            self.facing_right = True
        else:
            self.facing_right = False
        
        # Machine à états
        if self.ai_state == "approach":
            self._approach_player(player, distance_to_player)
        elif self.ai_state == "attack_pattern_1":
            self._attack_pattern_1(player, projectile_manager)
        elif self.ai_state == "attack_pattern_2":
            self._attack_pattern_2(player, projectile_manager)
        elif self.ai_state == "retreat":
            self._retreat_from_player(player)
    
    def _approach_player(self, player, distance):
        """Se rapproche du joueur"""
        if distance > 150:
            if player.rect.centerx > self.rect.centerx:
                self.velocity_x = 3
            else:
                self.velocity_x = -3
        else:
            self.velocity_x = 0
            self.ai_state = "attack_pattern_1"
            self.ai_timer = 0
    
    def _attack_pattern_1(self, player, projectile_manager):
        """Pattern d'attaque 1: Tirs en ligne droite"""
        if self.attack_timer > 2.0 and self.attack_cooldown <= 0:
            if projectile_manager:
                # Tirer vers le joueur
                projectile_manager.add_projectile(
                    self.rect.centerx, self.rect.centery,
                    player.rect.centerx, player.rect.centery,
                    20, PROJECTILE_SPEED * 0.8, "bullet"
                )
            
            self.attack_cooldown = 1.0
            self.attack_timer = 0
        
        # Changer de pattern après un certain temps
        if self.ai_timer > 8.0:
            self.ai_state = "retreat"
            self.ai_timer = 0
    
    def _attack_pattern_2(self, player, projectile_manager):
        """Pattern d'attaque 2: Tirs en éventail (phase 2)"""
        if self.attack_timer > 1.5 and self.attack_cooldown <= 0:
            if projectile_manager:
                # Tirs en éventail
                center_angle = math.atan2(
                    player.rect.centery - self.rect.centery,
                    player.rect.centerx - self.rect.centerx
                )
                
                for i in range(5):
                    angle = center_angle + (i - 2) * 0.3
                    target_x = self.rect.centerx + math.cos(angle) * 200
                    target_y = self.rect.centery + math.sin(angle) * 200
                    
                    projectile_manager.add_projectile(
                        self.rect.centerx, self.rect.centery,
                        target_x, target_y,
                        15, PROJECTILE_SPEED * 1.2, "bullet"
                    )
            
            self.attack_cooldown = 2.0
            self.attack_timer = 0
        
        # Retourner à l'approche
        if self.ai_timer > 6.0:
            self.ai_state = "approach"
            self.ai_timer = 0
    
    def _retreat_from_player(self, player):
        """Recule du joueur"""
        if player.rect.centerx > self.rect.centerx:
            self.velocity_x = -2
        else:
            self.velocity_x = 2
        
        if self.ai_timer > 3.0:
            self.ai_state = "approach"
            self.ai_timer = 0
    
    def _update_physics(self, dt, platforms):
        """Met à jour la physique du boss"""
        # Gravité
        if not self.on_ground:
            self.velocity_y += GRAVITY * 0.5  # Gravité réduite pour le boss
        
        # Limiter la vitesse
        self.velocity_y = min(self.velocity_y, 10)
        
        # Mouvement
        old_x = self.x
        old_y = self.y
        
        self.x += self.velocity_x
        self.y += self.velocity_y
        
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        
        # Collision avec le sol
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.y = self.rect.y
            self.velocity_y = 0
            self.on_ground = True
        
        # Limites horizontales
        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - self.width))
        self.x = self.rect.x
    
    def take_damage(self, damage):
        """Le boss prend des dégâts"""
        self.health -= damage
        self.hurt_flash_time = 0.2
        
        # Effet de recul
        knockback = 20 if self.facing_right else -20
        self.velocity_x = -knockback
        
        return True
    
    def is_dead(self):
        """Vérifie si le boss est mort"""
        return self.health <= 0
    
    def get_attack_rect(self):
        """Retourne la zone d'attaque du boss"""
        if self.ai_state not in ["attack_pattern_1", "attack_pattern_2"]:
            return None
        
        attack_width = 60
        attack_height = 40
        
        if self.facing_right:
            attack_x = self.rect.right
        else:
            attack_x = self.rect.left - attack_width
        
        attack_y = self.rect.centery - attack_height // 2
        
        return pygame.Rect(attack_x, attack_y, attack_width, attack_height)
    
    def render(self, screen):
        """Affiche le boss"""
        # Flash quand blessé
        if self.hurt_flash_time > 0 and int(self.hurt_flash_time * 20) % 2:
            sprite = self.sprites['attack']
        else:
            sprite = self.sprites['normal']
        
        # Retourner le sprite si nécessaire
        if not self.facing_right:
            sprite = pygame.transform.flip(sprite, True, False)
        
        screen.blit(sprite, (self.rect.x, self.rect.y))
        
        # Barre de vie du boss (plus grande)
        self._render_boss_health_bar(screen)
        
        # Zone d'attaque en debug
        attack_rect = self.get_attack_rect()
        if attack_rect:
            pygame.draw.rect(screen, (255, 0, 0, 100), attack_rect, 2)
    
    def _render_boss_health_bar(self, screen):
        """Affiche la barre de vie du boss"""
        bar_width = 200
        bar_height = 12
        bar_x = SCREEN_WIDTH // 2 - bar_width // 2
        bar_y = 30
        
        # Fond
        pygame.draw.rect(screen, DARK_GRAY, (bar_x - 2, bar_y - 2, bar_width + 4, bar_height + 4))
        pygame.draw.rect(screen, RED, (bar_x, bar_y, bar_width, bar_height))
        
        # Vie actuelle
        health_ratio = self.health / self.max_health
        current_width = int(bar_width * health_ratio)
        
        # Couleur selon la phase
        if self.phase == 1:
            health_color = ORANGE
        else:
            health_color = RED
        
        pygame.draw.rect(screen, health_color, (bar_x, bar_y, current_width, bar_height))
        
        # Contour
        pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 2)
        
        # Texte
        font = pygame.font.Font(None, 24)
        text = font.render(f"BOSS - Phase {self.phase}", True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, bar_y - 15))
        screen.blit(text, text_rect)