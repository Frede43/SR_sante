#!/usr/bin/env python3
import os
import sys

# Ajouter le dossier src au path
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(script_dir, 'src'))

# Lancer le jeu
from main import main

if __name__ == "__main__":
    main()
