from sqlalchemy import Column, Integer, String, Float
from database import Base

class Produto(Base):
    __tablename__ = "TABprodutos"

    id = Column("id", Integer, primary_key = True, autoincrement=True)
    nome = Column("nome", String, nullable = False)
    preco = Column("preco", Float, nullable = False)
    estoque = Column("estoque", Integer, nullable = False)

    def init(self, nome, preco, estoque):
        self.nome = nome
        self.preco = preco
        self.estoque = estoque