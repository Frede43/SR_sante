# 🎮 Fonctionnalités Détaillées du Jeu d'Action 2D

## 🎯 Vue d'Ensemble du Gameplay

```
┌─────────────────────────────────────────────────────────────┐
│ Score: 1250        [████████████████████████] Vie: 85/100   │
│ Vague: 3           Power-ups Actifs:                        │
│ Ennemis: 15        • Vitesse: 7s                           │
│                    • Dégâts x2: 3s                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│     ┌─────┐                    💥                          │
│     │     │         👤 ➤ ∘∘∘ → 👹                         │
│     │     │        /│\                                     │
│ ┌───┴─────┴───┐    / \                                     │
│ │             │                                            │
│ │             │         ⭐                                 │
│ └─────────────┘    ┌─────┐                                │
│                    │     │         🔴                      │
│               ┌────┴─────┴────┐   Boss                     │
│               │               │  [████████] 250/300        │
│ ══════════════════════════════════════════════════════════ │
└─────────────────────────────────────────────────────────────┘
```

## ⚔️ Système de Combat Avancé

### Attaques du Joueur
- **Mêlée (X)** : Zone d'attaque étendue, 25 dégâts de base
- **Projectiles (Clic)** : Tir vers la souris, trajectoire calculée
- **Tir Multiple** : 3 projectiles en éventail avec power-up
- **Multiplicateur de dégâts** : Power-up double les dégâts

### Ennemis Intelligents
```
🔴 Ennemi Basique          🟣 Ennemi Rapide          🔥 Boss
- Vie: 50                  - Vie: 50                  - Vie: 300
- Vitesse: 2               - Vitesse: 4               - Patterns multiples
- Patrouille simple        - Détection étendue        - Phases adaptatives
- Attaque contact          - Mouvement agile          - Projectiles multiples
```

## 🏃 Système de Mouvement

### Contrôles Fluides
- **Course** : WASD/Flèches avec friction réaliste
- **Saut** : Simple et double saut avec gravité
- **Dash** : Déplacement rapide avec invulnérabilité
- **Physique** : Collision précise avec plateformes

### Animations Dynamiques
```
Idle:    👤     Course:  👤💨    Saut:    👤
        /│\             /│\              ╱│╲
        / \             / \             ╱ ╲

Attaque: 👤═══   Dash:   👤⚡⚡    Blessé:  💥👤
        /│\             /│\              /│\
        / \             / \              / \
```

## ⭐ Power-ups et Améliorations

### Types de Power-ups
```
💚 Santé        🔵 Vitesse       🔴 Dégâts
+30 HP          +50% vitesse     x2 dégâts
Instantané      10 secondes      8 secondes

🟣 Bouclier     🟠 Tir Multiple
Immunité        3 projectiles
5 secondes      12 secondes
```

### Effets Visuels
- **Auras colorées** autour du joueur
- **Particules** lors de la collecte
- **Barres de progression** pour la durée restante

## 🤖 Intelligence Artificielle

### États des Ennemis
```
📍 PATROUILLE → 👁️ DÉTECTION → 🏃 POURSUITE → ⚔️ ATTAQUE
     ↑                                              ↓
     ←──────────── 🔄 RETOUR ←──────────────────────┘
```

### Boss IA
1. **Phase 1** : Approche + Tirs simples
2. **Phase 2** : Tirs en éventail + Retraite tactique
3. **Adaptation** : Change de stratégie selon la vie restante

## 💥 Système de Particules

### Types d'Effets
- **Explosions** : Particules radiales avec gravité
- **Impacts** : Gerbes directionnelles
- **Traînées** : Particules flottantes sans gravité
- **Collecte** : Explosion colorée pour les power-ups

### Propriétés Physiques
- Gravité variable selon le type
- Fade-out progressif (alpha)
- Vitesses et directions aléatoires
- Durée de vie configurable

## 📊 Système de Progression

### Mécaniques de Score
```
Action                    Points
──────────────────────────────
Éliminer ennemi basique   +100
Éliminer ennemi rapide    +150
Éliminer boss             +1000
Collecter power-up        +50
Survie (par seconde)      +1
```

### Progression des Vagues
- **Vague 1-2** : Ennemis basiques uniquement
- **Vague 3+** : Mix d'ennemis + vitesse accrue
- **Toutes les 3 vagues** : Apparition d'un boss
- **Spawn adaptatif** : Délai réduit progressivement

## 🎨 Rendu et Graphismes

### Sprites Procéduraux
- **Joueur** : Personnage humanoid avec animations
- **Ennemis** : Créatures colorées selon le type
- **Boss** : Sprites plus grands avec détails
- **Power-ups** : Icônes symboliques animées

### Effets Visuels
- **Fond dégradé** : Ciel dynamique
- **Plateformes** : Textures avec ombres
- **Barres de vie** : Couleurs adaptatives
- **Clignotements** : Feedback de dégâts

## 🔧 Architecture Technique

### Systèmes Modulaires
```
Game (Boucle principale)
├── InputManager (Entrées)
├── SceneManager (États)
├── AudioManager (Sons)
├── ParticleSystem (Effets)
└── SaveSystem (Persistance)
```

### Scènes
- **MenuScene** : Navigation avec clavier
- **GameScene** : Gameplay principal
- **GameOverScene** : Statistiques et options

### Entités
- **Player** : Contrôlé par le joueur
- **Enemy** : IA autonome
- **Boss** : IA complexe
- **Projectile** : Physique balistique
- **PowerUp** : Collectibles animés

## 🎵 Système Audio

### Sons Synthétiques
- **Saut** : Ton ascendant (440 Hz)
- **Attaque** : Ton percutant (220 Hz)
- **Dégâts** : Ton grave (150 Hz)
- **Collecte** : Ton aigu (660 Hz)

### Gestion Robuste
- Détection automatique des capacités audio
- Fonctionnement silencieux si pas de carte son
- Volumes configurables par catégorie

## 💾 Sauvegarde et Persistance

### Données Sauvegardées
```json
{
  "high_scores": [
    {
      "score": 5420,
      "wave": 8,
      "enemies_killed": 45,
      "time_survived": 180
    }
  ],
  "total_enemies_killed": 234,
  "total_time_played": 1250,
  "games_played": 12
}
```

### Classements
- Top 10 des meilleurs scores
- Statistiques cumulatives
- Sauvegarde automatique à chaque partie

## 🎮 Conseils de Jeu

### Stratégies de Base
1. **Utilisez les plateformes** : Prenez de la hauteur pour éviter les ennemis
2. **Gérez les power-ups** : Collectez-les au bon moment
3. **Dash défensif** : Utilisez le dash pour échapper aux situations dangereuses
4. **Tir à distance** : Éliminez les ennemis avant qu'ils s'approchent

### Techniques Avancées
1. **Double saut + Dash** : Combo pour traverser de grandes distances
2. **Tir multiple + Dégâts** : Combo dévastateur contre les boss
3. **Bouclier + Approche** : Foncez sur les ennemis en sécurité
4. **Gestion des vagues** : Éliminez rapidement pour éviter l'accumulation

## 🔮 Extensions Possibles

Le jeu est conçu pour être facilement extensible :

### Nouvelles Entités
- Ennemis volants
- Boss avec phases multiples
- Alliés IA
- Objets destructibles

### Nouveaux Power-ups
- Saut triple
- Ralentissement du temps
- Régénération de vie
- Munitions infinies

### Nouveaux Niveaux
- Environnements thématiques
- Plateformes mobiles
- Pièges et obstacles
- Objectifs spéciaux

---

*Développé avec passion pour démontrer les capacités de Pygame et les techniques de développement de jeux 2D avancées.*