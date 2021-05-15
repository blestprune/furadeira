from sqlalchemy import Column, String, Integer
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import os

# ----- Cria tabela -----------------------------------------------------------

db_string = os.getenv("DATABASE_URL")

Base = declarative_base()


class Frase(Base):
    __tablename__ = 'frases'
    id = Column(Integer, primary_key=True)
    url = Column(String(200))


engine = create_engine(db_string)


def criar_tabela():
    Base.metadata.create_all(engine)
