# Rotas para Pedidos

from sqlalchemy.orm import Session

from dependencies import get_db, usuario_logado

from models import OrderTable, UserTable

from schemas import OrderSchema

from fastapi import APIRouter, Depends, HTTPException


order_router = APIRouter(prefix = "/order", tags=["order"])   # define o caminho = domínio/order/(rota esolhinha)



@order_router.get("/")   # rota de entrada (inicial)
async def pedidos():
    return {"msg": "você entrou na tela de pedidos"}


@order_router.post("/criar_pedido")
async def criar_pedido(
                    OrderSchema: OrderSchema,
                    db: Session = Depends(get_db)
                    ):
    
    # checa se o id do usuário que fez o pedido existe
    id_found = db.query(UserTable).filter_by(
    id=OrderSchema.usuario_id
    ).first()
    
    if not id_found:
        raise HTTPException(status_code = 400, detail = "não existe um usuário com esse id")     # Retornando código do erro e mensagem
    

    novo_pedido = OrderTable(
        usuario_id = OrderSchema.usuario_id
    )
    
    db.add(novo_pedido)
    db.commit()
    db.refresh(novo_pedido)    # garante que campos gerados pelo banco (como id) estejam disponíveis (atualiza)

    return {"msg": "pedido criado com sucesso!", "id": novo_pedido.id}     # Retornando mensagem de sucesso