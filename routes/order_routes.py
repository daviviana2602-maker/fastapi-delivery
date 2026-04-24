# Rotas para Pedidos

from services.order_services import(criar_pedido_services, listar_todos_pedidos_services, adicionar_item_temp_services, ajustar_item_pedido_services,
listar_pedido_temporario_services, cancelar_pedido_services, concluir_pedido_services)

from sqlalchemy.orm import Session

from dependencies import get_db, usuario_logado, checar_admin

from models import UserTable

from fastapi import APIRouter, Depends

from schemas import AddItemSchema, FinishOrderSchema, AdjustItemSchema

from response_schemas import CommonResponse


order_router = APIRouter(prefix = "/order", tags=["order"])   # define o caminho = domínio/order/(rota esolhinha)



@order_router.post("/pedido", response_model=CommonResponse)
def criar_pedido(
    db: Session = Depends(get_db),
    usuario_id: int = Depends(usuario_logado)
    ):
  
   return criar_pedido_services(db, usuario_id)
    
    
    
@order_router.get("/listar", response_model=CommonResponse)
def listar_todos_pedidos(
    status_type: str,
    db: Session = Depends(get_db),
    admin: UserTable = Depends(checar_admin)    # verifica se o usuario é um adm (função somente para adms)
    ):
    
    return listar_todos_pedidos_services(status_type, db, admin)



@order_router.post("/pedido/adicionar_item", response_model=CommonResponse)
def adicionar_item_temp(
    add_item_schema: AddItemSchema,
    db: Session = Depends(get_db),
    usuario_id: int = Depends(usuario_logado)
):
    
    return adicionar_item_temp_services(add_item_schema, db, usuario_id)
    
    
    
@order_router.patch("/pedido/concluir", response_model=CommonResponse)
def concluir_pedido(
        conclude_order: FinishOrderSchema,
        db: Session = Depends(get_db),
        usuario_id: int = Depends(usuario_logado)
        ):
    
    return concluir_pedido_services(conclude_order, db, usuario_id)
    
    
    
@order_router.patch("/pedido/cancelar", response_model=CommonResponse)
def cancelar_pedido(
        cancel_order: FinishOrderSchema,
        db: Session = Depends(get_db),
        usuario_id: int = Depends(usuario_logado)
        ):
    
    return cancelar_pedido_services(cancel_order, db, usuario_id)
   


@order_router.patch("/pedido/item", response_model=CommonResponse)
def ajustar_item_pedido(
    ajustar_item_schema: AdjustItemSchema,
    db: Session = Depends(get_db),
    usuario_id: int = Depends(usuario_logado)
    ):
    
    return ajustar_item_pedido_services(ajustar_item_schema, db, usuario_id)
    
    
    
@order_router.get("/pedido/item/listar_pedido_temp", response_model=CommonResponse)
async def listar_pedido_temporario(
    pedido_id: int,
    db: Session = Depends(get_db),
    usuario_id: int = Depends(usuario_logado)
):

    return listar_pedido_temporario_services(pedido_id, db, usuario_id)