"""
Système de sauvegarde - Gère les scores et paramètres
"""

import json
import os

class SaveSystem:
    def __init__(self):
        self.save_file = "game_data.json"
        self.data = self._load_data()
    
    def _load_data(self):
        """Charge les données sauvegardées"""
        default_data = {
            "high_scores": [],
            "total_enemies_killed": 0,
            "total_time_played": 0,
            "games_played": 0,
            "settings": {
                "master_volume": 0.7,
                "sfx_volume": 0.8,
                "music_volume": 0.6
            }
        }
        
        try:
            if os.path.exists(self.save_file):
                with open(self.save_file, 'r') as f:
                    data = json.load(f)
                # Fusionner avec les données par défaut pour les nouvelles clés
                for key in default_data:
                    if key not in data:
                        data[key] = default_data[key]
                return data
        except:
            pass
        
        return default_data
    
    def save_data(self):
        """Sauvegarde les données"""
        try:
            with open(self.save_file, 'w') as f:
                json.dump(self.data, f, indent=2)
        except:
            pass
    
    def add_score(self, score, wave, enemies_killed, time_survived):
        """Ajoute un nouveau score"""
        score_entry = {
            "score": score,
            "wave": wave,
            "enemies_killed": enemies_killed,
            "time_survived": time_survived
        }
        
        self.data["high_scores"].append(score_entry)
        
        # Garder seulement les 10 meilleurs scores
        self.data["high_scores"].sort(key=lambda x: x["score"], reverse=True)
        self.data["high_scores"] = self.data["high_scores"][:10]
        
        # Mettre à jour les statistiques totales
        self.data["total_enemies_killed"] += enemies_killed
        self.data["total_time_played"] += time_survived
        self.data["games_played"] += 1
        
        self.save_data()
        
        return self._get_score_rank(score)
    
    def _get_score_rank(self, score):
        """Retourne le rang du score"""
        for i, entry in enumerate(self.data["high_scores"]):
            if entry["score"] == score:
                return i + 1
        return len(self.data["high_scores"])
    
    def get_high_scores(self):
        """Retourne la liste des meilleurs scores"""
        return self.data["high_scores"]
    
    def get_stats(self):
        """Retourne les statistiques générales"""
        return {
            "total_enemies_killed": self.data["total_enemies_killed"],
            "total_time_played": self.data["total_time_played"],
            "games_played": self.data["games_played"]
        }