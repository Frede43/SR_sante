"""
Classe du joueur - Gère le personnage principal
"""

import pygame
import math
from config import *

class Player:
    def __init__(self, x, y, scene_manager=None):
        self.x = x
        self.y = y
        self.scene_manager = scene_manager
        self.width = 32
        self.height = 48
        self.velocity_x = 0
        self.velocity_y = 0
        
        # État du joueur
        self.health = PLAYER_HEALTH
        self.max_health = PLAYER_HEALTH
        self.facing_right = True
        self.on_ground = False
        self.can_double_jump = True
        self.has_double_jumped = False
        
        # Animation
        self.animation_state = "idle"
        self.animation_time = 0
        self.frame_duration = 0.1
        
        # Combat
        self.attack_cooldown = 0
        self.attack_duration = 0.3
        self.is_attacking = False
        self.invulnerable_time = 0
        
        # Dash
        self.dash_cooldown = 0
        self.dash_duration = 0.2
        self.is_dashing = False
        self.dash_speed = 300
        
        # Power-ups
        self.speed_boost_time = 0
        self.speed_multiplier = 1.0
        self.damage_boost_time = 0
        self.damage_multiplier = 1.0
        self.shield_time = 0
        self.multi_shot_time = 0
        
        # Rectangle de collision
        self.rect = pygame.Rect(x, y, self.width, self.height)
        
        # Créer les sprites du joueur
        self.sprites = self._create_player_sprites()
    
    def _create_player_sprites(self):
        """Crée les sprites du joueur de manière procédurale"""
        sprites = {}
        
        # Sprite idle
        idle_surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        # Corps
        pygame.draw.rect(idle_surf, BLUE, (8, 16, 16, 24))
        # Tête
        pygame.draw.circle(idle_surf, (255, 220, 177), (16, 12), 8)
        # Yeux
        pygame.draw.circle(idle_surf, BLACK, (13, 10), 2)
        pygame.draw.circle(idle_surf, BLACK, (19, 10), 2)
        # Bras
        pygame.draw.rect(idle_surf, (255, 220, 177), (4, 20, 6, 16))
        pygame.draw.rect(idle_surf, (255, 220, 177), (22, 20, 6, 16))
        # Jambes
        pygame.draw.rect(idle_surf, DARK_GRAY, (10, 40, 5, 8))
        pygame.draw.rect(idle_surf, DARK_GRAY, (17, 40, 5, 8))
        sprites['idle'] = idle_surf
        
        # Sprite de course (légèrement modifié)
        run_surf = idle_surf.copy()
        # Modifier légèrement la position des bras
        pygame.draw.rect(run_surf, (255, 220, 177), (2, 18, 6, 16))
        pygame.draw.rect(run_surf, (255, 220, 177), (24, 22, 6, 16))
        sprites['run'] = run_surf
        
        # Sprite de saut
        jump_surf = idle_surf.copy()
        # Bras levés
        pygame.draw.rect(jump_surf, (255, 220, 177), (4, 12, 6, 16))
        pygame.draw.rect(jump_surf, (255, 220, 177), (22, 12, 6, 16))
        # Jambes pliées
        pygame.draw.rect(jump_surf, DARK_GRAY, (10, 36, 5, 12))
        pygame.draw.rect(jump_surf, DARK_GRAY, (17, 36, 5, 12))
        sprites['jump'] = jump_surf
        
        # Sprite d'attaque
        attack_surf = idle_surf.copy()
        # Bras d'attaque étendu
        pygame.draw.rect(attack_surf, (255, 220, 177), (28, 18, 8, 6))
        # Épée
        pygame.draw.rect(attack_surf, GRAY, (32, 16, 12, 4))
        sprites['attack'] = attack_surf
        
        return sprites
    
    def handle_input(self, input_manager):
        """Gère les entrées du joueur"""
        if self.is_dashing:
            return
            
        # Mouvement horizontal
        if input_manager.is_key_pressed(pygame.K_LEFT) or input_manager.is_key_pressed(pygame.K_a):
            self.velocity_x = -PLAYER_SPEED * self.speed_multiplier
            self.facing_right = False
            if self.on_ground:
                self.animation_state = "run"
        elif input_manager.is_key_pressed(pygame.K_RIGHT) or input_manager.is_key_pressed(pygame.K_d):
            self.velocity_x = PLAYER_SPEED * self.speed_multiplier
            self.facing_right = True
            if self.on_ground:
                self.animation_state = "run"
        else:
            self.velocity_x *= FRICTION
            if self.on_ground and abs(self.velocity_x) < 0.5:
                self.velocity_x = 0
                self.animation_state = "idle"
        
        # Saut
        if (input_manager.is_key_just_pressed(pygame.K_SPACE) or 
            input_manager.is_key_just_pressed(pygame.K_UP) or
            input_manager.is_key_just_pressed(pygame.K_w)):
            self._jump()
        
        # Attaque
        if (input_manager.is_key_just_pressed(pygame.K_x) or 
            input_manager.is_mouse_just_pressed(1)) and self.attack_cooldown <= 0:
            self._attack()
        
        # Dash
        if (input_manager.is_key_just_pressed(pygame.K_c) or 
            input_manager.is_key_just_pressed(pygame.K_LSHIFT)) and self.dash_cooldown <= 0:
            self._dash()
    
    def _jump(self):
        """Gère le saut du joueur"""
        if self.on_ground:
            self.velocity_y = JUMP_STRENGTH
            self.on_ground = False
            self.has_double_jumped = False
            self.animation_state = "jump"
            # Son de saut
            if self.scene_manager.game.audio_manager:
                self.scene_manager.game.audio_manager.play_sound('jump')
        elif self.can_double_jump and not self.has_double_jumped:
            self.velocity_y = JUMP_STRENGTH * 0.8
            self.has_double_jumped = True
            # Effet de particules pour le double saut
            self.scene_manager.game.particle_system.add_trail(
                self.rect.centerx, self.rect.bottom, BLUE, 8
            )
    
    def _attack(self):
        """Gère l'attaque du joueur"""
        self.is_attacking = True
        self.attack_cooldown = 0.5
        self.animation_state = "attack"
        # Son d'attaque
        if self.scene_manager.game.audio_manager:
            self.scene_manager.game.audio_manager.play_sound('attack')
    
    def _dash(self):
        """Gère le dash du joueur"""
        self.is_dashing = True
        self.dash_cooldown = 1.0
        dash_direction = 1 if self.facing_right else -1
        self.velocity_x = self.dash_speed * dash_direction
        self.invulnerable_time = self.dash_duration
        
        # Effet de particules pour le dash
        self.scene_manager.game.particle_system.add_trail(
            self.rect.centerx, self.rect.centery, YELLOW, 12
        )
    
    def update(self, dt, platforms=None):
        """Met à jour le joueur"""
        # Mettre à jour les cooldowns
        self.attack_cooldown = max(0, self.attack_cooldown - dt)
        self.dash_cooldown = max(0, self.dash_cooldown - dt)
        self.invulnerable_time = max(0, self.invulnerable_time - dt)
        
        # Mettre à jour les power-ups
        self.speed_boost_time = max(0, self.speed_boost_time - dt)
        self.damage_boost_time = max(0, self.damage_boost_time - dt)
        self.shield_time = max(0, self.shield_time - dt)
        self.multi_shot_time = max(0, self.multi_shot_time - dt)
        
        # Réinitialiser les multiplicateurs
        if self.speed_boost_time <= 0:
            self.speed_multiplier = 1.0
        if self.damage_boost_time <= 0:
            self.damage_multiplier = 1.0
        
        # Gérer le dash
        if self.is_dashing:
            self.dash_duration -= dt
            if self.dash_duration <= 0:
                self.is_dashing = False
                self.dash_duration = 0.2
                self.velocity_x *= 0.3
        
        # Gérer l'attaque
        if self.is_attacking:
            self.attack_duration -= dt
            if self.attack_duration <= 0:
                self.is_attacking = False
                self.attack_duration = 0.3
                if self.on_ground:
                    self.animation_state = "idle"
        
        # Appliquer la gravité
        if not self.on_ground:
            self.velocity_y += GRAVITY
            if self.velocity_y > 0:
                self.animation_state = "jump"
        
        # Limiter la vitesse de chute
        self.velocity_y = min(self.velocity_y, 20)
        
        # Mettre à jour la position
        old_x = self.x
        old_y = self.y
        
        self.x += self.velocity_x
        self.y += self.velocity_y
        
        # Mettre à jour le rectangle de collision
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        
        # Collision avec les plateformes
        if platforms:
            self._handle_platform_collisions(platforms, old_x, old_y)
        
        # Limites de l'écran
        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - self.width))
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.y = self.rect.y
            self.velocity_y = 0
            self.on_ground = True
        
        # Mettre à jour les coordonnées
        self.x = self.rect.x
        self.y = self.rect.y
        
        # Animation
        self.animation_time += dt
    
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
                elif old_y > platform.bottom and self.velocity_y < 0:
                    self.rect.top = platform.bottom
                    self.y = self.rect.y
                    self.velocity_y = 0
                
                # Collision horizontale
                elif old_x < platform.left:
                    self.rect.right = platform.left
                    self.x = self.rect.x
                    self.velocity_x = 0
                elif old_x > platform.right:
                    self.rect.left = platform.right
                    self.x = self.rect.x
                    self.velocity_x = 0
    
    def get_attack_rect(self):
        """Retourne la zone d'attaque du joueur"""
        if not self.is_attacking:
            return None
        
        attack_width = 40
        attack_height = 20
        
        if self.facing_right:
            attack_x = self.rect.right
        else:
            attack_x = self.rect.left - attack_width
        
        attack_y = self.rect.centery - attack_height // 2
        
        return pygame.Rect(attack_x, attack_y, attack_width, attack_height)
    
    def take_damage(self, damage):
        """Le joueur prend des dégâts"""
        if self.invulnerable_time <= 0 and self.shield_time <= 0:
            self.health -= damage
            self.invulnerable_time = 1.0
            # Son de dégâts
            if self.scene_manager.game.audio_manager:
                self.scene_manager.game.audio_manager.play_sound('hurt')
            # Effet de particules
            self.scene_manager.game.particle_system.add_impact(
                self.rect.centerx, self.rect.centery, 0, RED, 10
            )
            return True
        return False
    
    def heal(self, amount):
        """Soigne le joueur"""
        self.health = min(self.max_health, self.health + amount)
    
    def render(self, screen):
        """Affiche le joueur"""
        # Clignotement si invulnérable
        if self.invulnerable_time > 0 and int(self.invulnerable_time * 10) % 2:
            return
        
        # Sélectionner le sprite approprié
        sprite = self.sprites.get(self.animation_state, self.sprites['idle'])
        
        # Retourner le sprite si nécessaire
        if not self.facing_right:
            sprite = pygame.transform.flip(sprite, True, False)
        
        screen.blit(sprite, (self.rect.x, self.rect.y))
        
        # Effets visuels des power-ups
        self._render_powerup_effects(screen)
        
        # Afficher la zone d'attaque en debug
        attack_rect = self.get_attack_rect()
        if attack_rect:
            pygame.draw.rect(screen, (255, 255, 0, 100), attack_rect, 2)
        
        # Barre de vie
        self._render_health_bar(screen)
    
    def _render_health_bar(self, screen):
        """Affiche la barre de vie du joueur"""
        bar_width = 100
        bar_height = 8
        bar_x = self.rect.centerx - bar_width // 2
        bar_y = self.rect.top - 15
        
        # Fond de la barre
        pygame.draw.rect(screen, RED, (bar_x, bar_y, bar_width, bar_height))
        
        # Barre de vie actuelle
        health_ratio = self.health / self.max_health
        current_width = int(bar_width * health_ratio)
        pygame.draw.rect(screen, GREEN, (bar_x, bar_y, current_width, bar_height))
        
        # Contour
        pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 1)
    
    def _render_powerup_effects(self, screen):
        """Affiche les effets visuels des power-ups actifs"""
        # Bouclier
        if self.shield_time > 0:
            shield_radius = 30
            shield_alpha = int(100 * (self.shield_time % 0.5) / 0.5)
            shield_surf = pygame.Surface((shield_radius * 2, shield_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(shield_surf, (*BLUE[:3], shield_alpha), (shield_radius, shield_radius), shield_radius, 3)
            screen.blit(shield_surf, (self.rect.centerx - shield_radius, self.rect.centery - shield_radius))
        
        # Vitesse augmentée
        if self.speed_boost_time > 0:
            # Traînée bleue
            trail_surf = pygame.Surface((self.width + 10, self.height + 10), pygame.SRCALPHA)
            pygame.draw.rect(trail_surf, (*BLUE[:3], 50), trail_surf.get_rect())
            screen.blit(trail_surf, (self.rect.x - 5, self.rect.y - 5))
        
        # Dégâts augmentés
        if self.damage_boost_time > 0:
            # Aura rouge
            aura_surf = pygame.Surface((self.width + 8, self.height + 8), pygame.SRCALPHA)
            pygame.draw.rect(aura_surf, (*RED[:3], 30), aura_surf.get_rect())
            screen.blit(aura_surf, (self.rect.x - 4, self.rect.y - 4))