# Rotas para Pedidos

from sqlalchemy.orm import Session

from dependencies import get_db, usuario_logado

from models import OrderTable

from fastapi import APIRouter, Depends, HTTPException

from schemas import CancelPedidoSchema


order_router = APIRouter(prefix = "/order", tags=["order"])   # define o caminho = domínio/order/(rota esolhinha)



@order_router.get("/")   # rota de entrada (inicial)
async def pedidos():
    return {"msg": "você entrou na tela de pedidos"}



@order_router.post("/pedido")
async def criar_pedido(
    db: Session = Depends(get_db),
    usuario_id: int = Depends(usuario_logado)  # pegando id do usuário e validando se está autenticado
):
  
    # cria o pedido com base no usuário logado
    novo_pedido = OrderTable(
        usuario_id=usuario_id
    )
    
    
    db.add(novo_pedido)
    db.commit()
    db.refresh(novo_pedido)

    return {"msg": "pedido criado com sucesso!", "id": novo_pedido.id}



@order_router.post("/pedido/cancelar")
async def cancelar_pedido(
                        cancel_pedido_schema: CancelPedidoSchema, 
                        db: Session = Depends(get_db),
                        usuario_id: int = Depends(usuario_logado)  # pegando id do usuário e validando se está autenticado
                        ):
    
    pedido = db.query(OrderTable).filter_by(
        id=cancel_pedido_schema.pedido_id
    ).first()
    
    if not pedido:
         raise HTTPException(status_code=404, detail="pedido não encontrado")    # caso pedido não exista retorna erro
     
    pedido.status = "CANCELADO"    # caso exista muda o status no banco
    
    db.commit()
    db.refresh(pedido)  # atualiza pedido no banco
    
    return{"msg": "Pedido cancelado", "id": cancel_pedido_schema.pedido_id}