"""
Scène de jeu principale - Gère le gameplay
"""

import pygame
import random
import math
from config import *
from entities.player import Player
from entities.enemy import Enemy
from entities.boss import Boss
from entities.projectile import ProjectileManager
from entities.powerup import PowerUpManager

class GameScene:
    def __init__(self, scene_manager):
        self.scene_manager = scene_manager
        self.player = None
        self.enemies = []
        self.boss = None
        self.platforms = []
        self.projectile_manager = ProjectileManager()
        self.powerup_manager = PowerUpManager()
        
        # État du jeu
        self.score = 0
        self.wave = 1
        self.enemies_killed = 0
        self.game_time = 0
        
        # Spawn des ennemis
        self.enemy_spawn_timer = 0
        self.enemy_spawn_delay = 3.0
        
        # UI
        self.font = None
        self.ui_font = None
        
        # Caméra
        self.camera_x = 0
        self.camera_y = 0
    
    def enter(self):
        """Appelé quand on entre dans cette scène"""
        # Initialiser les polices
        self.font = pygame.font.Font(None, 36)
        self.ui_font = pygame.font.Font(None, 24)
        
        # Créer le joueur
        self.player = Player(100, SCREEN_HEIGHT - 100, self.scene_manager)
        
        # Créer les plateformes du niveau
        self._create_level()
        
        # Spawner quelques ennemis initiaux
        self._spawn_initial_enemies()
        
        # Réinitialiser les statistiques si on recommence
        self._reset_game()
    
    def exit(self):
        """Appelé quand on quitte cette scène"""
        pass
    
    def _create_level(self):
        """Crée le niveau avec des plateformes"""
        self.platforms = []
        
        # Plateformes principales
        platforms_data = [
            (200, SCREEN_HEIGHT - 150, 200, 20),
            (500, SCREEN_HEIGHT - 200, 150, 20),
            (800, SCREEN_HEIGHT - 250, 180, 20),
            (300, SCREEN_HEIGHT - 300, 120, 20),
            (700, SCREEN_HEIGHT - 350, 200, 20),
            (100, SCREEN_HEIGHT - 400, 100, 20),
            (950, SCREEN_HEIGHT - 180, 150, 20),
            (600, SCREEN_HEIGHT - 450, 140, 20),
        ]
        
        for x, y, w, h in platforms_data:
            self.platforms.append(pygame.Rect(x, y, w, h))
    
    def _spawn_initial_enemies(self):
        """Spawne les ennemis initiaux"""
        spawn_positions = [
            (300, SCREEN_HEIGHT - 200),
            (600, SCREEN_HEIGHT - 300),
            (900, SCREEN_HEIGHT - 150),
            (400, SCREEN_HEIGHT - 350),
        ]
        
        for x, y in spawn_positions:
            enemy_type = random.choice(["basic", "fast"])
            enemy = Enemy(x, y, enemy_type)
            self.enemies.append(enemy)
    
    def _spawn_enemy(self):
        """Spawne un nouvel ennemi"""
        # Choisir une position de spawn aléatoire
        spawn_x = random.choice([50, SCREEN_WIDTH - 100])
        spawn_y = SCREEN_HEIGHT - 100
        
        # Type d'ennemi basé sur la vague
        if self.wave > 3:
            enemy_type = random.choice(["basic", "fast", "basic"])
        else:
            enemy_type = "basic"
        
        enemy = Enemy(spawn_x, spawn_y, enemy_type)
        self.enemies.append(enemy)
    
    def _spawn_boss(self):
        """Spawne un boss"""
        boss_x = SCREEN_WIDTH // 2
        boss_y = SCREEN_HEIGHT - 200
        self.boss = Boss(boss_x, boss_y, "fire_demon")
    
    def handle_event(self, event):
        """Gère les événements de la scène"""
        input_manager = self.scene_manager.game.input_manager
        
        # Retour au menu
        if input_manager.is_key_just_pressed(pygame.K_ESCAPE):
            self.scene_manager.change_scene('menu')
        
        # Tir de projectile
        if input_manager.is_mouse_just_pressed(1):  # Clic gauche
            mouse_x, mouse_y = input_manager.get_mouse_pos()
            self._player_shoot(mouse_x, mouse_y)
    
    def _player_shoot(self, target_x, target_y):
        """Le joueur tire un projectile"""
        if self.player.attack_cooldown <= 0:
            # Position de départ du projectile
            start_x = self.player.rect.centerx
            start_y = self.player.rect.centery
            
            # Dégâts avec multiplicateur
            damage = int(PLAYER_DAMAGE * self.player.damage_multiplier)
            
            if self.player.multi_shot_time > 0:
                # Tir multiple
                angles = [-0.3, 0, 0.3]  # 3 directions
                for angle in angles:
                    # Calculer la direction avec l'angle
                    dx = target_x - start_x
                    dy = target_y - start_y
                    import math
                    base_angle = math.atan2(dy, dx)
                    new_angle = base_angle + angle
                    
                    # Position cible ajustée
                    distance = 200
                    adj_target_x = start_x + math.cos(new_angle) * distance
                    adj_target_y = start_y + math.sin(new_angle) * distance
                    
                    self.projectile_manager.add_projectile(
                        start_x, start_y, adj_target_x, adj_target_y,
                        damage, PROJECTILE_SPEED * 1.5, "bullet"
                    )
            else:
                # Tir simple
                self.projectile_manager.add_projectile(
                    start_x, start_y, target_x, target_y, 
                    damage, PROJECTILE_SPEED * 1.5, "bullet"
                )
            
            self.player.attack_cooldown = 0.3
            if self.scene_manager.game.audio_manager:
                self.scene_manager.game.audio_manager.play_sound('attack')
    
    def update(self, dt):
        """Met à jour la scène de jeu"""
        self.game_time += dt
        
        # Mettre à jour le joueur
        if self.player:
            self.player.handle_input(self.scene_manager.game.input_manager)
            self.player.update(dt, self.platforms)
        
        # Mettre à jour les ennemis
        for enemy in self.enemies[:]:
            enemy.update(dt, self.player, self.platforms)
            
            # Supprimer les ennemis morts
            if enemy.is_dead():
                self.enemies.remove(enemy)
                self.enemies_killed += 1
                self.score += 100
                
                # Effet d'explosion
                self.scene_manager.game.particle_system.add_explosion(
                    enemy.rect.centerx, enemy.rect.centery, RED, 20
                )
                
                # Son de victoire (utiliser le son de pickup)
                if self.scene_manager.game.audio_manager:
                    self.scene_manager.game.audio_manager.play_sound('pickup')
        
        # Mettre à jour le boss
        if self.boss:
            self.boss.update(dt, self.player, self.platforms, self.projectile_manager)
            
            # Boss mort
            if self.boss.is_dead():
                self.score += 1000
                # Grande explosion
                self.scene_manager.game.particle_system.add_explosion(
                    self.boss.rect.centerx, self.boss.rect.centery, ORANGE, 40
                )
                self.boss = None
        
        # Mettre à jour les projectiles
        self.projectile_manager.update(dt, self.scene_manager.game.particle_system)
        
        # Mettre à jour les power-ups
        self.powerup_manager.update(dt)
        
        # Vérifier les collisions power-ups-joueur
        if self.player:
            collected_powerups = self.powerup_manager.check_collision_with_player(self.player.rect)
            for powerup in collected_powerups:
                powerup.apply_effect(self.player)
                self.score += 50
                
                # Effet de collecte
                self.scene_manager.game.particle_system.add_explosion(
                    powerup.rect.centerx, powerup.rect.centery, powerup.color, 8
                )
                
                if self.scene_manager.game.audio_manager:
                    self.scene_manager.game.audio_manager.play_sound('pickup')
        
        # Vérifier les collisions projectiles-ennemis
        for enemy in self.enemies:
            hit_projectiles = self.projectile_manager.check_collision_with_rect(enemy.rect)
            for projectile in hit_projectiles:
                if enemy.take_damage(projectile.damage):
                    # Effet d'impact
                    self.scene_manager.game.particle_system.add_impact(
                        projectile.rect.centerx, projectile.rect.centery, 
                        projectile.velocity_x, WHITE, 5
                    )
        
        # Vérifier les collisions projectiles-boss
        if self.boss:
            hit_projectiles = self.projectile_manager.check_collision_with_rect(self.boss.rect)
            for projectile in hit_projectiles:
                if self.boss.take_damage(projectile.damage):
                    # Effet d'impact plus important
                    self.scene_manager.game.particle_system.add_impact(
                        projectile.rect.centerx, projectile.rect.centery, 
                        projectile.velocity_x, ORANGE, 8
                    )
        
        # Spawn d'ennemis
        self.enemy_spawn_timer += dt
        if self.enemy_spawn_timer > self.enemy_spawn_delay:
            if len(self.enemies) < 6:  # Limite d'ennemis
                self._spawn_enemy()
            self.enemy_spawn_timer = 0
            
            # Augmenter la difficulté et spawner des boss
            if self.enemies_killed > 0 and self.enemies_killed % 10 == 0:
                self.wave += 1
                self.enemy_spawn_delay = max(1.0, self.enemy_spawn_delay - 0.2)
                
                # Spawner un boss toutes les 3 vagues
                if self.wave % 3 == 0 and not self.boss:
                    self._spawn_boss()
        
        # Vérifier si le joueur est mort
        if self.player and self.player.health <= 0:
            self._game_over()
    
    def _game_over(self):
        """Gère la fin de partie"""
        # Passer les statistiques à l'écran de game over
        game_over_scene = self.scene_manager.scenes['game_over']
        game_over_scene.set_game_stats(self.score, self.wave, self.enemies_killed, self.game_time)
        self.scene_manager.change_scene('game_over')
        
        # Réinitialiser la scène pour la prochaine partie
        self._reset_game()
    
    def render(self, screen):
        """Affiche la scène de jeu"""
        # Fond dégradé
        for y in range(SCREEN_HEIGHT):
            color_ratio = y / SCREEN_HEIGHT
            r = int(135 * (1 - color_ratio * 0.3))
            g = int(206 * (1 - color_ratio * 0.2))
            b = int(235 * (1 - color_ratio * 0.1))
            pygame.draw.line(screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        
        # Plateformes
        for platform in self.platforms:
            pygame.draw.rect(screen, PLATFORM_COLOR, platform)
            # Ombre
            shadow_rect = platform.copy()
            shadow_rect.y += 3
            pygame.draw.rect(screen, (100, 50, 25), shadow_rect)
            # Contour
            pygame.draw.rect(screen, (200, 150, 100), platform, 2)
        
        # Sol
        ground_rect = pygame.Rect(0, SCREEN_HEIGHT - 20, SCREEN_WIDTH, 20)
        pygame.draw.rect(screen, PLATFORM_COLOR, ground_rect)
        
        # Entités
        if self.player:
            self.player.render(screen)
        
        for enemy in self.enemies:
            enemy.render(screen)
        
        # Boss
        if self.boss:
            self.boss.render(screen)
        
        self.projectile_manager.render(screen)
        self.powerup_manager.render(screen)
        
        # UI
        self._render_ui(screen)
    
    def _render_ui(self, screen):
        """Affiche l'interface utilisateur"""
        # Score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        
        # Vague
        wave_text = self.font.render(f"Vague: {self.wave}", True, WHITE)
        screen.blit(wave_text, (10, 50))
        
        # Ennemis tués
        kills_text = self.ui_font.render(f"Ennemis: {self.enemies_killed}", True, WHITE)
        screen.blit(kills_text, (10, 90))
        
        # Temps de jeu
        time_text = self.ui_font.render(f"Temps: {int(self.game_time)}s", True, WHITE)
        screen.blit(time_text, (10, 110))
        
        # Vie du joueur (grande barre)
        if self.player:
            bar_width = 200
            bar_height = 20
            bar_x = SCREEN_WIDTH - bar_width - 10
            bar_y = 10
            
            # Fond
            pygame.draw.rect(screen, DARK_GRAY, (bar_x - 2, bar_y - 2, bar_width + 4, bar_height + 4))
            pygame.draw.rect(screen, RED, (bar_x, bar_y, bar_width, bar_height))
            
            # Vie actuelle
            health_ratio = self.player.health / self.player.max_health
            current_width = int(bar_width * health_ratio)
            
            # Couleur selon la vie
            if health_ratio > 0.6:
                health_color = GREEN
            elif health_ratio > 0.3:
                health_color = YELLOW
            else:
                health_color = RED
            
            pygame.draw.rect(screen, health_color, (bar_x, bar_y, current_width, bar_height))
            
            # Texte de vie
            health_text = self.ui_font.render(f"Vie: {int(self.player.health)}/{self.player.max_health}", True, WHITE)
            screen.blit(health_text, (bar_x, bar_y + 25))
            
            # Affichage des power-ups actifs
            self._render_active_powerups(screen)
        
        # Instructions de contrôle
        instructions = [
            "WASD/Flèches: Bouger",
            "Espace: Saut/Double saut", 
            "X: Attaque mêlée",
            "Clic gauche: Tirer",
            "C/Shift: Dash",
            "Échap: Menu"
        ]
        
        for i, instruction in enumerate(instructions):
            text = pygame.font.Font(None, 20).render(instruction, True, GRAY)
            screen.blit(text, (10, SCREEN_HEIGHT - 140 + i * 20))
    
    def _render_active_powerups(self, screen):
        """Affiche les power-ups actifs du joueur"""
        if not self.player:
            return
            
        powerup_y = 60
        powerup_x = SCREEN_WIDTH - 220
        
        active_powerups = []
        
        if self.player.speed_boost_time > 0:
            active_powerups.append(("Vitesse", self.player.speed_boost_time, BLUE))
        if self.player.damage_boost_time > 0:
            active_powerups.append(("Dégâts x2", self.player.damage_boost_time, RED))
        if self.player.shield_time > 0:
            active_powerups.append(("Bouclier", self.player.shield_time, PURPLE))
        if self.player.multi_shot_time > 0:
            active_powerups.append(("Tir Multiple", self.player.multi_shot_time, ORANGE))
        
        for i, (name, time_left, color) in enumerate(active_powerups):
            y_pos = powerup_y + i * 25
            
            # Barre de temps restant
            bar_width = 80
            bar_height = 8
            time_ratio = min(1.0, time_left / 10.0)  # Normaliser sur 10 secondes max
            current_width = int(bar_width * time_ratio)
            
            pygame.draw.rect(screen, DARK_GRAY, (powerup_x, y_pos, bar_width, bar_height))
            pygame.draw.rect(screen, color, (powerup_x, y_pos, current_width, bar_height))
            
            # Texte
            text = self.ui_font.render(f"{name}: {int(time_left)}s", True, WHITE)
            screen.blit(text, (powerup_x + bar_width + 10, y_pos - 5))
    
    def _reset_game(self):
        """Réinitialise la partie"""
        self.score = 0
        self.wave = 1
        self.enemies_killed = 0
        self.game_time = 0
        self.enemy_spawn_timer = 0
        self.enemy_spawn_delay = 3.0
        self.enemies.clear()
        self.boss = None
        self.projectile_manager = ProjectileManager()
        self.powerup_manager = PowerUpManager()
        
        # Recréer le joueur
        if self.player:
            self.player = Player(100, SCREEN_HEIGHT - 100, self.scene_manager)