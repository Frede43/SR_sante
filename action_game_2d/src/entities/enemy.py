"""
Classe des ennemis - IA et comportements
"""

import pygame
import math
import random
from config import *

class Enemy:
    def __init__(self, x, y, enemy_type="basic"):
        self.x = x
        self.y = y
        self.width = 28
        self.height = 32
        self.velocity_x = 0
        self.velocity_y = 0
        
        # État de l'ennemi
        self.enemy_type = enemy_type
        self.health = ENEMY_HEALTH
        self.max_health = ENEMY_HEALTH
        self.facing_right = True
        self.on_ground = False
        
        # IA
        self.ai_state = "patrol"  # patrol, chase, attack, hurt
        self.ai_timer = 0
        self.patrol_start_x = x
        self.patrol_range = 100
        self.detection_range = 120
        self.attack_range = 40
        self.speed = 2
        
        # Combat
        self.attack_cooldown = 0
        self.damage = ENEMY_DAMAGE
        self.invulnerable_time = 0
        
        # Animation
        self.animation_time = 0
        self.hurt_flash_time = 0
        
        # Rectangle de collision
        self.rect = pygame.Rect(x, y, self.width, self.height)
        
        # Créer les sprites
        self.sprites = self._create_enemy_sprites()
    
    def _create_enemy_sprites(self):
        """Crée les sprites de l'ennemi"""
        sprites = {}
        
        # Couleur selon le type
        if self.enemy_type == "basic":
            body_color = RED
            eye_color = YELLOW
        elif self.enemy_type == "fast":
            body_color = PURPLE
            eye_color = WHITE
            self.speed = 4
            self.detection_range = 150
        else:
            body_color = DARK_GRAY
            eye_color = RED
        
        # Sprite de base
        sprite = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        # Corps
        pygame.draw.ellipse(sprite, body_color, (4, 8, 20, 20))
        # Yeux
        pygame.draw.circle(sprite, eye_color, (10, 14), 3)
        pygame.draw.circle(sprite, eye_color, (18, 14), 3)
        # Pupilles
        pygame.draw.circle(sprite, BLACK, (10, 14), 1)
        pygame.draw.circle(sprite, BLACK, (18, 14), 1)
        # Pieds
        pygame.draw.rect(sprite, body_color, (6, 28, 4, 4))
        pygame.draw.rect(sprite, body_color, (18, 28, 4, 4))
        
        sprites['normal'] = sprite
        
        # Sprite blessé (plus rouge)
        hurt_sprite = sprite.copy()
        hurt_overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        hurt_overlay.fill((255, 0, 0, 100))
        hurt_sprite.blit(hurt_overlay, (0, 0))
        sprites['hurt'] = hurt_sprite
        
        return sprites
    
    def update(self, dt, player, platforms=None):
        """Met à jour l'ennemi"""
        # Mettre à jour les timers
        self.attack_cooldown = max(0, self.attack_cooldown - dt)
        self.invulnerable_time = max(0, self.invulnerable_time - dt)
        self.hurt_flash_time = max(0, self.hurt_flash_time - dt)
        self.ai_timer += dt
        
        # IA
        self._update_ai(player, dt)
        
        # Physique
        self._update_physics(dt, platforms)
        
        # Animation
        self.animation_time += dt
    
    def _update_ai(self, player, dt):
        """Met à jour l'IA de l'ennemi"""
        if not player:
            return
        
        distance_to_player = math.sqrt(
            (player.rect.centerx - self.rect.centerx) ** 2 + 
            (player.rect.centery - self.rect.centery) ** 2
        )
        
        # Machine à états de l'IA
        if self.ai_state == "patrol":
            self._patrol()
            
            # Détecter le joueur
            if distance_to_player < self.detection_range:
                self.ai_state = "chase"
                
        elif self.ai_state == "chase":
            self._chase_player(player)
            
            # Attaquer si assez proche
            if distance_to_player < self.attack_range and self.attack_cooldown <= 0:
                self.ai_state = "attack"
                self.ai_timer = 0
            
            # Perdre le joueur si trop loin
            elif distance_to_player > self.detection_range * 1.5:
                self.ai_state = "patrol"
                
        elif self.ai_state == "attack":
            self._attack_player(player)
            
            # Retourner en chasse après l'attaque
            if self.ai_timer > 0.5:
                self.ai_state = "chase"
        
        elif self.ai_state == "hurt":
            # État temporaire après avoir pris des dégâts
            if self.ai_timer > 0.3:
                self.ai_state = "chase" if distance_to_player < self.detection_range else "patrol"
    
    def _patrol(self):
        """Comportement de patrouille"""
        # Mouvement de va-et-vient
        if self.facing_right:
            if self.x > self.patrol_start_x + self.patrol_range:
                self.facing_right = False
            else:
                self.velocity_x = self.speed * 0.5
        else:
            if self.x < self.patrol_start_x - self.patrol_range:
                self.facing_right = True
            else:
                self.velocity_x = -self.speed * 0.5
    
    def _chase_player(self, player):
        """Poursuit le joueur"""
        if player.rect.centerx > self.rect.centerx:
            self.velocity_x = self.speed
            self.facing_right = True
        else:
            self.velocity_x = -self.speed
            self.facing_right = False
    
    def _attack_player(self, player):
        """Attaque le joueur"""
        self.velocity_x = 0
        
        if self.ai_timer > 0.2:  # Délai avant l'attaque
            attack_rect = self.get_attack_rect()
            if attack_rect and attack_rect.colliderect(player.rect):
                if player.take_damage(self.damage):
                    # Repousser le joueur
                    knockback = 50 if self.facing_right else -50
                    player.velocity_x += knockback
            
            self.attack_cooldown = 1.0
    
    def _update_physics(self, dt, platforms):
        """Met à jour la physique de l'ennemi"""
        # Gravité
        if not self.on_ground:
            self.velocity_y += GRAVITY
        
        # Limiter la vitesse de chute
        self.velocity_y = min(self.velocity_y, 15)
        
        # Mettre à jour la position
        old_x = self.x
        old_y = self.y
        
        self.x += self.velocity_x
        self.y += self.velocity_y
        
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        
        # Collision avec les plateformes
        if platforms:
            self._handle_platform_collisions(platforms, old_x, old_y)
        
        # Sol
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.y = self.rect.y
            self.velocity_y = 0
            self.on_ground = True
        
        self.x = self.rect.x
        self.y = self.rect.y
    
    def _handle_platform_collisions(self, platforms, old_x, old_y):
        """Gère les collisions avec les plateformes"""
        self.on_ground = False
        
        for platform in platforms:
            if self.rect.colliderect(platform):
                # Collision verticale
                if old_y < platform.top and self.velocity_y > 0:
                    self.rect.bottom = platform.top
                    self.y = self.rect.y
                    self.velocity_y = 0
                    self.on_ground = True
    
    def get_attack_rect(self):
        """Retourne la zone d'attaque de l'ennemi"""
        if self.ai_state != "attack":
            return None
        
        attack_width = 30
        attack_height = 20
        
        if self.facing_right:
            attack_x = self.rect.right
        else:
            attack_x = self.rect.left - attack_width
        
        attack_y = self.rect.centery - attack_height // 2
        
        return pygame.Rect(attack_x, attack_y, attack_width, attack_height)
    
    def take_damage(self, damage):
        """L'ennemi prend des dégâts"""
        if self.invulnerable_time <= 0:
            self.health -= damage
            self.invulnerable_time = 0.5
            self.hurt_flash_time = 0.2
            self.ai_state = "hurt"
            self.ai_timer = 0
            
            # Effet de recul
            knockback = 30 if self.facing_right else -30
            self.velocity_x = -knockback
            
            return True
        return False
    
    def is_dead(self):
        """Vérifie si l'ennemi est mort"""
        return self.health <= 0
    
    def render(self, screen):
        """Affiche l'ennemi"""
        # Clignotement si blessé
        if self.hurt_flash_time > 0 and int(self.hurt_flash_time * 20) % 2:
            sprite = self.sprites['hurt']
        else:
            sprite = self.sprites['normal']
        
        # Retourner le sprite si nécessaire
        if not self.facing_right:
            sprite = pygame.transform.flip(sprite, True, False)
        
        screen.blit(sprite, (self.rect.x, self.rect.y))
        
        # Barre de vie
        if self.health < self.max_health:
            self._render_health_bar(screen)
        
        # Zone d'attaque en debug
        attack_rect = self.get_attack_rect()
        if attack_rect:
            pygame.draw.rect(screen, (255, 0, 0, 100), attack_rect, 2)
    
    def _render_health_bar(self, screen):
        """Affiche la barre de vie de l'ennemi"""
        bar_width = 30
        bar_height = 4
        bar_x = self.rect.centerx - bar_width // 2
        bar_y = self.rect.top - 8
        
        # Fond
        pygame.draw.rect(screen, RED, (bar_x, bar_y, bar_width, bar_height))
        
        # Vie actuelle
        health_ratio = self.health / self.max_health
        current_width = int(bar_width * health_ratio)
        pygame.draw.rect(screen, GREEN, (bar_x, bar_y, current_width, bar_height))