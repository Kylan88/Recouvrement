from backend.app import app  # Remplacez "backend" par le bon chemin si nécessaire
from waitress import serve

if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=5000)
