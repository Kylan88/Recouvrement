from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL pour la base de données SQLite
DATABASE_URL = "sqlite:///backend/db.sqlite3"

SQLALCHEMY_DATABASE_URI = 'sqlite:///path_to_your_database.db'

# Initialisation du moteur SQLAlchemy
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Gestion des sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Classe de base pour les modèles SQLAlchemy
Base = declarative_base()
