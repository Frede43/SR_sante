#!/usr/bin/env python3
"""
Script d'installation automatique pour le jeu d'action 2D
"""

import os
import sys
import subprocess
import platform

def check_python_version():
    """Vérifie la version de Python"""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7+ requis. Version actuelle:", sys.version)
        return False
    print(f"✓ Python {sys.version.split()[0]} détecté")
    return True

def install_dependencies():
    """Installe les dépendances"""
    print("\n📦 Installation des dépendances...")
    
    try:
        # Essayer pip3 d'abord
        result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                              capture_output=True, text=True)
        
        if result.returncode != 0:
            # Essayer avec --break-system-packages si nécessaire
            print("Tentative avec --break-system-packages...")
            result = subprocess.run([sys.executable, "-m", "pip", "install", "--break-system-packages", 
                                   "-r", "requirements.txt"], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✓ Dépendances installées avec succès")
            return True
        else:
            print(f"❌ Erreur d'installation: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors de l'installation: {e}")
        return False

def test_game():
    """Teste que le jeu peut démarrer"""
    print("\n🧪 Test du jeu...")
    
    try:
        # Configuration pour test headless
        os.environ['SDL_VIDEODRIVER'] = 'dummy'
        os.environ['SDL_AUDIODRIVER'] = 'dummy'
        
        # Importer et tester
        sys.path.insert(0, 'src')
        import pygame
        pygame.init()
        
        from game import Game
        game = Game()
        
        print("✓ Jeu testé avec succès")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        return False

def create_launcher():
    """Crée un script de lancement"""
    print("\n🚀 Création du script de lancement...")
    
    launcher_content = """#!/usr/bin/env python3
import os
import sys

# Ajouter le dossier src au path
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(script_dir, 'src'))

# Lancer le jeu
from main import main

if __name__ == "__main__":
    main()
"""
    
    try:
        with open("launch_game.py", "w") as f:
            f.write(launcher_content)
        
        # Rendre exécutable sur Unix
        if platform.system() != "Windows":
            os.chmod("launch_game.py", 0o755)
        
        print("✓ Script de lancement créé: launch_game.py")
        return True
        
    except Exception as e:
        print(f"❌ Erreur création launcher: {e}")
        return False

def main():
    """Installation principale"""
    print("🎮 INSTALLATION - JEU D'ACTION 2D AVANCÉ")
    print("=" * 50)
    
    # Vérifications
    if not check_python_version():
        sys.exit(1)
    
    # Installation
    if not install_dependencies():
        print("\n⚠️  Installation des dépendances échouée.")
        print("Essayez manuellement: pip3 install pygame numpy")
        print("Ou utilisez: pip3 install --break-system-packages pygame numpy")
    
    # Test
    if not test_game():
        print("\n⚠️  Test du jeu échoué. Vérifiez les dépendances.")
    
    # Launcher
    create_launcher()
    
    print("\n" + "=" * 50)
    print("🎉 INSTALLATION TERMINÉE!")
    print("\n🚀 Pour jouer:")
    print("   python3 main.py")
    print("   ou")
    print("   python3 launch_game.py")
    print("\n📖 Consultez README.md pour plus d'informations")
    print("=" * 50)

if __name__ == "__main__":
    main()