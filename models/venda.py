from sqlalchemy import Column, Integer, ForeignKey, Date
from database import Base
from datetime import date

class Venda(Base):
    __tablename__ = "TABvendas"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    cliente_id = Column("cliente_id", Integer, ForeignKey("TABclientes.id"))
    produto_id = Column("produto_id", Integer, ForeignKey("TABprodutos.id"))
    data_venda = Column("data_venda", Date, default=date.today)
    quantidade = Column("quantidade", Integer, nullable = False)