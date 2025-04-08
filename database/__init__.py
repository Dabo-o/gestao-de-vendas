from sqlalchemy import create_engine # Importa a função para a conexão com o banco de dados
from sqlalchemy.orm import sessionmaker, declarative_base # Importa ferramentas para criar sessões e a base de classes ORM

db = create_engine("sqlite:///meubanco.db") # Conecta com o banco SQLITE
Session = sessionmaker(bind=db)
session = Session() # Cria uma sessão ativa para manipular o banco
Base = declarative_base() # Cria a base para definição das classes que representam tabelas