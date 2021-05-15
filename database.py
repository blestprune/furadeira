from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from sqlalchemy_declarative import Base, Frase
import os

# ----- Funções para o banco ------------------------------------------

db_string = os.getenv("DATABASE_URL").replace("postgres", "postgresql")

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


def todas_frases():
    session = DBSession()
    frases = []
    try:
        frases = session.query(Frase)
    except:
        return frases
    finally:
        session.close()
        return frases


def frase_aleatoria():
    session = DBSession()
    frase = ""
    try:
        frase = session.query(Frase).order_by(func.random()).first()
    except:
        return frase
    finally:
        session.close()
        return frase


def deletar_frase(index):
    session = DBSession()
    msg = ""
    try:
        session.query(Frase).filter(Frase.id == index).delete()
        session.commit()
        msg = f"Ok! Apaguei a frase #{index}"
    except:
        msg = "Falhei"
    finally:
        session.close()
        return msg
