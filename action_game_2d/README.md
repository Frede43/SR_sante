# 🎮 Jeu d'Action 2D Avancé

Un jeu de plateforme d'action 2D développé en Python avec Pygame, featuring un système de combat avancé, des ennemis intelligents, des power-ups, et des effets visuels impressionnants.

## 🚀 Fonctionnalités

### 🎯 Gameplay
- **Système de combat avancé** : Attaques au corps à corps et tir de projectiles
- **Mouvement fluide** : Course, saut, double saut, et dash
- **Ennemis intelligents** : IA avec différents comportements (patrouille, poursuite, attaque)
- **Boss épiques** : Ennemis puissants avec patterns d'attaque complexes
- **Système de vagues** : Difficulté progressive avec spawn d'ennemis

### ⚡ Power-ups
- **Vie** : Restaure 30 points de vie
- **Vitesse** : Augmente la vitesse de déplacement (10s)
- **Dégâts** : Double les dégâts d'attaque (8s)
- **Bouclier** : Protection temporaire contre les dégâts (5s)
- **Tir Multiple** : Tire 3 projectiles simultanément (12s)

### 🎨 Effets Visuels
- **Système de particules** : Explosions, impacts, traînées
- **Animations fluides** : Sprites animés pour tous les personnages
- **Effets de power-ups** : Auras visuelles pour les améliorations actives
- **Interface moderne** : HUD avec barres de vie, score, et indicateurs

### 🔊 Audio
- **Effets sonores** : Sons synthétiques pour toutes les actions
- **Gestion audio robuste** : Fonctionne même sans carte son

## 🎮 Contrôles

| Action | Touches |
|--------|---------|
| Déplacement | `WASD` ou `Flèches directionnelles` |
| Saut / Double saut | `Espace` ou `↑` |
| Attaque mêlée | `X` |
| Tir de projectile | `Clic gauche` |
| Dash | `C` ou `Shift` |
| Menu | `Échap` |
| Navigation menu | `↑↓` + `Entrée` |

## 🛠️ Installation et Lancement

### Prérequis
- Python 3.7+
- Pygame 2.0+
- NumPy

### Installation
```bash
# Cloner ou télécharger le projet
cd action_game_2d

# Installer les dépendances
pip3 install -r requirements.txt

# Lancer le jeu
python3 main.py
```

### Environnement sans affichage
Pour tester dans un environnement headless :
```bash
python3 run_game.py
```

## 📁 Structure du Projet

```
action_game_2d/
├── main.py                 # Point d'entrée principal
├── run_game.py            # Script de test pour environnement headless
├── requirements.txt       # Dépendances Python
├── README.md             # Cette documentation
├── src/
│   ├── config.py         # Configuration et constantes
│   ├── game.py           # Classe principale du jeu
│   ├── entities/         # Entités du jeu
│   │   ├── player.py     # Classe du joueur
│   │   ├── enemy.py      # Classe des ennemis
│   │   ├── boss.py       # Classe des boss
│   │   ├── projectile.py # Système de projectiles
│   │   └── powerup.py    # Système de power-ups
│   ├── scenes/           # Scènes du jeu
│   │   ├── menu_scene.py     # Menu principal
│   │   ├── game_scene.py     # Scène de jeu
│   │   └── game_over_scene.py # Écran de fin
│   ├── systems/          # Systèmes du jeu
│   │   ├── input_manager.py    # Gestion des entrées
│   │   ├── audio_manager.py    # Gestion audio
│   │   ├── particle_system.py  # Système de particules
│   │   └── scene_manager.py    # Gestion des scènes
│   └── utils/            # Utilitaires
│       └── save_system.py    # Système de sauvegarde
└── assets/               # Assets du jeu (images, sons)
    ├── images/
    └── sounds/
```

## 🎯 Système de Jeu

### Progression
- **Score** : Gagné en éliminant des ennemis et collectant des power-ups
- **Vagues** : Difficulté croissante toutes les 10 éliminations
- **Boss** : Apparaissent toutes les 3 vagues
- **Power-ups** : Apparaissent aléatoirement toutes les 8 secondes

### Combat
- **Attaque mêlée** : Zone d'attaque étendue devant le joueur
- **Projectiles** : Tir vers la position de la souris
- **Dégâts** : Système de multiplicateurs avec power-ups
- **Invulnérabilité** : Courte période après avoir pris des dégâts

### Physique
- **Gravité réaliste** : Chute naturelle avec limite de vitesse
- **Collision** : Détection précise avec plateformes et entités
- **Mouvement fluide** : Friction et accélération naturelles

## 🏆 Fonctionnalités Avancées

### Intelligence Artificielle
- **États multiples** : Patrouille, poursuite, attaque, retraite
- **Boss adaptatifs** : Changent de stratégie selon leur vie
- **Détection intelligente** : Portée de détection et d'attaque variables

### Effets Visuels
- **Particules dynamiques** : Explosions, impacts, traînées
- **Animations procédurales** : Sprites générés dynamiquement
- **Feedback visuel** : Clignotements, auras, effets de power-ups

### Persistance
- **Sauvegarde automatique** : Scores et statistiques
- **Classement** : Top 10 des meilleurs scores
- **Statistiques globales** : Temps joué, ennemis éliminés

## 🔧 Configuration

Modifiez `src/config.py` pour ajuster :
- Dimensions de l'écran
- Vitesses et forces physiques
- Couleurs et apparence
- Paramètres de difficulté
- Volumes audio

## 🎨 Personnalisation

Le jeu est conçu pour être facilement extensible :
- Ajoutez de nouveaux types d'ennemis dans `entities/enemy.py`
- Créez de nouveaux power-ups dans `entities/powerup.py`
- Modifiez les niveaux dans `scenes/game_scene.py`
- Ajoutez des effets de particules dans `systems/particle_system.py`

## 🐛 Dépannage

### Problèmes Audio
Si vous rencontrez des erreurs ALSA/audio :
- Le jeu désactivera automatiquement l'audio
- Utilisez `run_game.py` pour tester sans audio

### Performance
- Ajustez `FPS` dans `config.py` si le jeu est lent
- Réduisez le nombre de particules pour améliorer les performances

## 📝 Licence

Ce projet est un exemple éducatif. Libre d'utilisation et de modification.

---

**Amusez-vous bien ! 🎮**