from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey    # import used types
from sqlalchemy.orm import declarative_base, sessionmaker

from dotenv import load_dotenv
import os
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")


engine = create_engine(DATABASE_URL)   # connect with the database
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


#------------------- CLASSES -------------------


class UserTable(Base):   # class is mandatory with database
    __tablename__ = "usuarios"   # criando tabela usuarios  
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    senha = Column(String, nullable=False)
    ativo = Column(Boolean, nullable=False, default = True)
    admin = Column(Boolean, nullable=False, default=False)
        
    
class OrderTable(Base):   # class is mandatory with database
    __tablename__ = "pedidos"   # criando tabela pedidos
    id = Column(Integer, primary_key=True)
    status = Column(String, nullable=False, default="PENDENTE")
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    preco = Column(Float, nullable=False, default=0)
    
    
class ItemTable(Base):   # class is mandatory with database
    __tablename__ = "itens"   # criando tabela itens
    id = Column(Integer, primary_key=True)
    quantidade = Column(Integer, nullable=False)
    tipo = Column(String, nullable=False)
    tamanho = Column(String, nullable=False)
    preco_unit = Column(Float, nullable=False)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"), nullable=False)