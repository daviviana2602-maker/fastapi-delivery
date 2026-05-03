# Relacionamento com DB

from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime 

from sqlalchemy.orm import declarative_base

from sqlalchemy.sql import func


Base = declarative_base()


#------------------- CLASSES -------------------


class UserTable(Base):   
    __tablename__ = "usuarios"   # criando tabela usuarios  
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    senha = Column(String, nullable=False)
    status = Column(String, nullable=False, default="ATIVO")
    admin = Column(Boolean, nullable=False, default=False)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())  # garante que o banco já coloque o horário correto quando criar algum registro
    
STATUS_USUARIO_VALIDOS = ("ATIVO", "DESATIVADO", "EXCLUIDO")


class OrderTable(Base):   
    __tablename__ = "pedidos"   # criando tabela pedidos
    id = Column(Integer, primary_key=True)
    status = Column(String, nullable=False, default="PENDENTE")     # PENDENTE, CANCELADO, CONCLUIDO
    usuario_id = Column(Integer, nullable=False)
    preco = Column(Float, nullable=False, default=0)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())   # garante que o banco já coloque o horário correto quando criar algum registro
    
STATUS_VALIDOS = ("PENDENTE", "CANCELADO", "CONCLUIDO")     # status válidos para pedidos
    
    
class CompletedOrderItem(Base):  # itens de pedidos já finalizados (concluídos)  
    __tablename__ = "itens_concluidos"   # criando tabela itens
    id = Column(Integer, primary_key=True)
    quantidade = Column(Integer, nullable=False)
    tipo = Column(String, nullable=False)
    tamanho = Column(String, nullable=False)
    preco_unit = Column(Float, nullable=False)
    preco_total = Column(Float, nullable=False)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"), nullable=False)

TAMANHOS_VALIDOS = ("GRANDE", "TRADICIONAL", "PEQUENO")     # status válidos para pedidos


class CardapioTable(Base):
    __tablename__ = "cardapio"
    id = Column(Integer, primary_key=True)  
    categoria = Column(String, nullable=False)  # tipo de comida: lanche, pizza, sobremesa etc
    nome = Column(String, unique=True, nullable=False)  # nome do item
    preco = Column(Float, nullable=False)         
    
    
class TempItemsTable(Base):
    __tablename__ = "temporarios"  
    id = Column(Integer, primary_key=True)
    quantidade = Column(Integer, nullable=False)
    nome = Column(String, nullable=False)
    tamanho = Column(String, nullable=False)
    preco_unit = Column(Float, nullable=False)
    preco_total = Column(Float, nullable=False)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"), nullable=False)     