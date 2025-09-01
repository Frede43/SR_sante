"""
Système de particules - Gère les effets visuels
"""

import pygame
import random
import math
from config import *

class Particle:
    def __init__(self, x, y, velocity_x, velocity_y, color, size, lifetime):
        self.x = x
        self.y = y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.color = color
        self.size = size
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.gravity_affected = True
    
    def update(self, dt):
        """Met à jour la particule"""
        self.x += self.velocity_x * dt * 60
        self.y += self.velocity_y * dt * 60
        
        if self.gravity_affected:
            self.velocity_y += GRAVITY * dt * 60
        
        self.lifetime -= dt
        
        # Fade out
        alpha = max(0, self.lifetime / self.max_lifetime)
        self.current_color = (*self.color[:3], int(255 * alpha))
        
        return self.lifetime > 0
    
    def render(self, screen):
        """Affiche la particule"""
        if self.lifetime > 0:
            alpha = max(0, self.lifetime / self.max_lifetime)
            size = max(1, int(self.size * alpha))
            color = (*self.color[:3], int(255 * alpha))
            
            # Créer une surface avec alpha
            surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            pygame.draw.circle(surf, color, (size, size), size)
            screen.blit(surf, (int(self.x - size), int(self.y - size)))

class ParticleSystem:
    def __init__(self):
        self.particles = []
    
    def add_explosion(self, x, y, color=ORANGE, count=15):
        """Ajoute une explosion de particules"""
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(50, 150)
            velocity_x = math.cos(angle) * speed
            velocity_y = math.sin(angle) * speed
            
            particle = Particle(
                x, y,
                velocity_x, velocity_y,
                color,
                random.uniform(2, 6),
                random.uniform(0.5, 1.5)
            )
            self.particles.append(particle)
    
    def add_impact(self, x, y, direction_x=0, color=WHITE, count=8):
        """Ajoute des particules d'impact"""
        for _ in range(count):
            angle = random.uniform(-math.pi/3, math.pi/3) + (math.pi if direction_x < 0 else 0)
            speed = random.uniform(30, 80)
            velocity_x = math.cos(angle) * speed
            velocity_y = math.sin(angle) * speed
            
            particle = Particle(
                x, y,
                velocity_x, velocity_y,
                color,
                random.uniform(1, 3),
                random.uniform(0.3, 0.8)
            )
            self.particles.append(particle)
    
    def add_trail(self, x, y, color=YELLOW, count=3):
        """Ajoute des particules de traînée"""
        for _ in range(count):
            velocity_x = random.uniform(-20, 20)
            velocity_y = random.uniform(-10, 10)
            
            particle = Particle(
                x + random.uniform(-5, 5), 
                y + random.uniform(-5, 5),
                velocity_x, velocity_y,
                color,
                random.uniform(1, 2),
                random.uniform(0.2, 0.5)
            )
            particle.gravity_affected = False
            self.particles.append(particle)
    
    def update(self, dt):
        """Met à jour toutes les particules"""
        self.particles = [p for p in self.particles if p.update(dt)]
    
    def render(self, screen):
        """Affiche toutes les particules"""
        for particle in self.particles:
            particle.render(screen)