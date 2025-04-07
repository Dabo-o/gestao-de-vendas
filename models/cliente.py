from sqlalchemy import Column, Integer, String
from database import Base

class Cliente(Base):
    __tablename__ = "TABclientes"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String, nullable = False)
    email = Column("email", String, nullable = False)
    telefone = Column("telefone", Integer, nullable = False)

    def init(self, nome, email, telefone):
        self.nome = nome
        self.email = email
        self.telefone = telefone