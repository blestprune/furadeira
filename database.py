from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_declarative import Base, Frase
from replit_backup import backup
import os

# ----- Funções para o banco ------------------------------------------

db_string = os.getenv("DATABASE_URL")

engine = create_engine(db_string)

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)


def inserir_frase(url):
    session = DBSession()
    try:
        frase = Frase(url=url)
        session.add(frase)
        session.commit()
    except:
        session.rollback()
    finally:
        session.close()


def pegar_frases():
    session = DBSession()
    frases = []
    try:
        frases = session.query(Frase)
    except:
        return frases
    finally:
        session.close()
        return frases


def deletar_frase(index):
    session = DBSession()
    try:
        session.query(Frase).filter(Frase.id == index).delete()
        session.commit()
        return f"Ok! Apaguei a frase #{index}"
    except:
        return "Falhei"
    finally:
        session.close()


def importar_replit():
    for url in backup:
        inserir_frase(url)
