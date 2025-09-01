Action 2D – Prototype

Lancer:
- Ouvrir `index.html` dans un navigateur moderne (ES Modules).

Contrôles:
- ZQSD/Flèches: déplacer
- Espace: sauter
- Maj: dash
- J: attaquer
- P: pause

Dossiers:
- `src/systems/Game.js`: boucle de jeu, rendu, resize
- `src/tools/Input.js`: clavier (down/pressed/released)
- `src/systems/camera/Camera.js`: caméra suiveuse
- `src/systems/world/Tilemap.js`: tuiles solides + collisions AABB
- `src/systems/scene/Scene.js`: scène, HUD, FX, pause
- `src/things/Player.js`: joueur (mouvements, saut, dash, attaque), HP
- `src/things/Enemy.js`: IA (patrouille, poursuite, attaque), HP
- `src/systems/fx/Particles.js`: particules légères

Pistes:
- Sprites animés, coyote-time, buffer d'input
- Armes, boss, drops, états
- Editeur de niveau, import JSON/CSV
- Son via Web Audio API
# SR_sante
Sante Reproductive
