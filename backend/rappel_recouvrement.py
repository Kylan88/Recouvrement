import smtplib
from email.mime.text import MIMEText
import logging
import os
from backend.models import Client
from backend.database import SessionLocal

 # Assurez-vous que le dossier "logs" existe
LOG_FOLDER = "backend/logs"
os.makedirs(LOG_FOLDER, exist_ok=True)

# Configuration de la journalisation
logging.basicConfig(
    filename=os.path.join(LOG_FOLDER, "rappels.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
# Configuration SMTP
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "votre_email@gmail.com"
SMTP_PASSWORD = "votre_mot_de_passe"

# Configurer la journalisation
logging.basicConfig(
    filename="backend/logs/rappels.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def rappel_recouvrement():
    """Envoie des rappels de paiement aux clients."""
    session = SessionLocal()
    clients = session.query(Client).all()
    for client in clients:
        envoyer_email(client)

def envoyer_email(client):
    """Envoie un e-mail à un client."""
    try:
        msg = MIMEText(
            f"Bonjour {client.nom},\n\n"
            f"Veuillez régler {client.montant_du}€ avant le {client.date_echeance}.\n\nMerci.")
        msg["From"] = SMTP_USER
        msg["To"] = client.email
        msg["Subject"] = "Rappel de paiement"
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)
        logging.info(f"Email envoyé à {client.nom} ({client.email})")
    except Exception as e:
        logging.error(f"Erreur d'envoi pour {client.nom} ({client.email}) : {e}")
