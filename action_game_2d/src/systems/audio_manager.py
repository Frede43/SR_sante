"""
Gestionnaire audio - Gère la musique et les effets sonores
"""

import pygame
import os
from config import *

class AudioManager:
    def __init__(self):
        self.sounds = {}
        self.music_playing = False
        self.enabled = True
        
        try:
            # Créer des sons synthétiques si pas de fichiers audio
            self.create_synthetic_sounds()
        except:
            print("Impossible de créer les sons - audio désactivé")
            self.enabled = False
    
    def create_synthetic_sounds(self):
        """Crée des sons synthétiques pour le jeu"""
        # Son de saut
        jump_sound = pygame.mixer.Sound(buffer=self._create_tone(440, 0.2))
        jump_sound.set_volume(SFX_VOLUME * 0.3)
        self.sounds['jump'] = jump_sound
        
        # Son d'attaque
        attack_sound = pygame.mixer.Sound(buffer=self._create_tone(220, 0.15))
        attack_sound.set_volume(SFX_VOLUME * 0.4)
        self.sounds['attack'] = attack_sound
        
        # Son de dégâts
        hurt_sound = pygame.mixer.Sound(buffer=self._create_tone(150, 0.3))
        hurt_sound.set_volume(SFX_VOLUME * 0.5)
        self.sounds['hurt'] = hurt_sound
        
        # Son de collecte
        pickup_sound = pygame.mixer.Sound(buffer=self._create_tone(660, 0.2))
        pickup_sound.set_volume(SFX_VOLUME * 0.3)
        self.sounds['pickup'] = pickup_sound
    
    def _create_tone(self, frequency, duration):
        """Crée un ton synthétique"""
        import numpy as np
        sample_rate = 22050
        frames = int(duration * sample_rate)
        arr = np.zeros((frames, 2))
        
        for i in range(frames):
            time = float(i) / sample_rate
            wave = np.sin(2 * np.pi * frequency * time)
            # Envelope pour éviter les clics
            envelope = min(1.0, 4.0 * time, 4.0 * (duration - time))
            arr[i] = [wave * envelope * 32767, wave * envelope * 32767]
        
        return arr.astype(np.int16)
    
    def play_sound(self, sound_name):
        """Joue un effet sonore"""
        if self.enabled and sound_name in self.sounds:
            try:
                self.sounds[sound_name].play()
            except:
                pass
    
    def play_music(self, music_file):
        """Joue une musique de fond"""
        try:
            pygame.mixer.music.load(music_file)
            pygame.mixer.music.set_volume(MUSIC_VOLUME)
            pygame.mixer.music.play(-1)  # Loop infini
            self.music_playing = True
        except:
            pass  # Ignore si le fichier n'existe pas
    
    def stop_music(self):
        """Arrête la musique"""
        pygame.mixer.music.stop()
        self.music_playing = False
    
    def set_master_volume(self, volume):
        """Définit le volume principal"""
        for sound in self.sounds.values():
            current_vol = sound.get_volume()
            sound.set_volume(current_vol * volume)