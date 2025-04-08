from sqlalchemy import Column, Integer, String # Importa as classes para definir colunas e tipos de dados
from database import Base # Importa a Base definida no arquivo do banco

# Cria a classe cliente que vai representar uma tabela no banco
class Cliente(Base):
    __tablename__ = "TABclientes"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String, nullable = False)
    email = Column("email", String, nullable = False)
    telefone = Column("telefone", Integer, nullable = False)
