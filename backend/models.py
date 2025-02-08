from sqlalchemy import Column, Integer, String, Float
from backend.database import Base

class Client(Base):
    """Table SQLAlchemy pour gérer les clients."""
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    montant_du = Column(Float, nullable=False)
    date_echeance = Column(String, nullable=False)
