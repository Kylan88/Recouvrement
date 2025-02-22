from flask import Flask, jsonify, request
from backend.database import engine, Base, SessionLocal
from flask_cors import CORS
from backend.models import Client
import os
import logging
from backend.rappel_recouvrement import rappel_recouvrement

# Initialisation de l'application Flask
app = Flask(__name__)
CORS(app)  # Permet les requêtes CORS

port = int(os.environ.get("PORT", 5000))  # Utilise le port de Railway ou 5000 par défaut
app.run(host="0.0.0.0", port=port)

@app.route("/")
def home():
    return "Bienvenue sur mon API ! Accédez aux données via /api/clients"

# S'assurer que le dossier "logs" existe
LOG_FOLDER = "backend/logs"
os.makedirs(LOG_FOLDER, exist_ok=True)

# Configuration de la journalisation
logging.basicConfig(
    filename=os.path.join(LOG_FOLDER, "rappels.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Synchroniser la base de données
with app.app_context():
    Base.metadata.create_all(bind=engine)

# Fonction utilitaire pour obtenir une session
def get_session():
    """Crée et retourne une session SQLAlchemy."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

# Routes
@app.route("/", methods=["GET"])
def home():
    """Route d'accueil."""
    return "Bienvenue dans l'application de recouvrement!"

@app.route("/api/clients", methods=["GET"])
def get_clients():
    """Récupérer tous les clients."""
    try:
        session = next(get_session())
        clients = session.query(Client).all()
        return jsonify([
            {
                "id": client.id,
                "nom": client.nom,
                "email": client.email,
                "montant_du": client.montant_du,
                "date_echeance": client.date_echeance
            }
            for client in clients
        ])
    except Exception as e:
        logging.error(f"Erreur lors de la récupération des clients : {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/clients", methods=["POST"])
def add_client():
    """Ajouter un nouveau client."""
    data = request.json
    if not data:
        return jsonify({"error": "Les données du client sont manquantes"}), 400
    
    # Validation des champs obligatoires
    required_fields = ["nom", "email", "montant_du", "date_echeance"]
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({"error": f"Champs manquants : {', '.join(missing_fields)}"}), 400

    try:
        session = next(get_session())
        client = Client(
            nom=data["nom"],
            email=data["email"],
            montant_du=data["montant_du"],
            date_echeance=data["date_echeance"]
        )
        session.add(client)
        session.commit()
        return jsonify({"message": "Client ajouté avec succès."}), 201
    except Exception as e:
        session.rollback()
        logging.error(f"Erreur lors de l'ajout du client : {e}")
        return jsonify({"error": str(e)}), 400
    finally:
        session.close()

@app.route('/api/rappels', methods=['POST'])
def send_reminders():
    try:
        # Appelez ici la fonction ou la logique pour envoyer les rappels
        # Exemple :
        rappel_recouvrement()
        return jsonify({"message": "Rappels envoyés avec succès."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
