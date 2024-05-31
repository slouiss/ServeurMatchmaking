from sqlalchemy import create_engine
from models import Base

# Chemin vers votre base de données
DATABASE_URL = 'sqlite:///matchmaking.db'

# Créer le moteur de base de données
engine = create_engine(DATABASE_URL)

# Créer les tables
Base.metadata.create_all(engine)
