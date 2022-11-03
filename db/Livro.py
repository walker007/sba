from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from db.Connection import Base
#import PySimpleGUI as sg

class Livro(Base):
    __tablename__ = "livros"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    codigo = Column(String(100), nullable=False)
    disponivel = Column(Boolean, nullable=True, default=True)
    endereco = Column(String(100), nullable=True)

    def __init__(self, nome, codigo, endereco,disponivel=True):
        self.nome = nome
        self.codigo = codigo
        self.disponivel = disponivel
        self.endereco = endereco

    def __repr__(self):
        return f"livro(nome={self.nome}, codigo={self.codigo}, endereco={self.endereco}, disponivel={self.disponivel})"
