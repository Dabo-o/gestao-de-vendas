from sqlalchemy import Column, Integer, String, Float # Importa as classes para definir colunas e tipo de dados 
from database import Base # Importa a Base definida no arquivo do banco

class Produto(Base):
    __tablename__ = "TABprodutos"

    id = Column("id", Integer, primary_key = True, autoincrement=True) 
    nome = Column("nome", String, nullable = False)
    preco = Column("preco", Float, nullable = False)
    estoque = Column("estoque", Integer, nullable = False)
