# Relacionamento com DB

from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey, DateTime    # import used types
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql import func

from config import DATABASE_URL

engine = create_engine(DATABASE_URL)   # connect with the database
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


#------------------- CLASSES -------------------


class UserTable(Base):   
    __tablename__ = "usuarios"   # criando tabela usuarios  
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    senha = Column(String, nullable=False)
    ativo = Column(Boolean, nullable=False, default = True)
    admin = Column(Boolean, nullable=False, default=False)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())  # garante que o banco já coloque o horário correto quando criar algum registro
    

class OrderTable(Base):   
    __tablename__ = "pedidos"   # criando tabela pedidos
    id = Column(Integer, primary_key=True)
    status = Column(String, nullable=False, default="PENDENTE")     # PENDENTE, CANCELADO, CONCLUIDO
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    preco = Column(Float, nullable=False, default=0)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())   # garante que o banco já coloque o horário correto quando criar algum registro
    
STATUS_VALIDOS = ("PENDENTE", "CANCELADO", "CONCLUIDO")     # status válidos para pedidos
    
    
class ItemsTable(Base):   
    __tablename__ = "itens"   # criando tabela itens
    id = Column(Integer, primary_key=True)
    quantidade = Column(Integer, nullable=False)
    tipo = Column(String, nullable=False)
    tamanho = Column(String, nullable=False)
    preco_unit = Column(Float, nullable=False)
    preco_total = Column(Float, nullable=False)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"), nullable=False)

TAMANHOS_VALIDOS = ("GRANDE", "TRADICIONAL", "PEQUENO")     # status válidos para pedidos


class ItemCardapioTable(Base):
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