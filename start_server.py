import os
import sys

# Ajouter le dossier `backend` au PYTHONPATH pour éviter les erreurs d'import
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(BASE_DIR, "backend")
sys.path.append(BACKEND_DIR)

from backend.app import app  # Importer l'application Flask

if __name__ == "__main__":
    # Lancer l'application Flask
    app.run(debug=True, host="127.0.0.1", port=5000)
