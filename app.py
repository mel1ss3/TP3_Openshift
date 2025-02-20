from fastapi import FastAPI, Depends, Form
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Configurer la base de données
DATABASE_URL = "sqlite:///./mots.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Définition du modèle
class Mot(Base):
    __tablename__ = "mots"
    id = Column(Integer, primary_key=True, index=True)
    contenu = Column(String, index=True)

# Création de la table
Base.metadata.create_all(bind=engine)

# Initialiser FastAPI
app = FastAPI()

# Fonction pour obtenir la session de la base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Route pour ajouter un mot
@app.post("/add")
def add_mot(contenu: str = Form(...), db: Session = Depends(get_db)):
    mot = Mot(contenu=contenu)
    db.add(mot)
    db.commit()
    db.refresh(mot)
    return {"message": "Mot ajouté", "mot": mot.contenu}
