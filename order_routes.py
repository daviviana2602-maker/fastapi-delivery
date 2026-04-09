# Rotas para Pedidos

from sqlalchemy.orm import Session

from dependencies import get_db, usuario_logado, checar_admin

from permissions import checar_dono_ou_admin

from models import OrderTable, UserTable, STATUS_VALIDOS, ItemCardapioTable, ItemsTable, TAMANHOS_VALIDOS

from fastapi import APIRouter, Depends, HTTPException

from schemas import CancelPedidoSchema, AddItemSchema


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
    
    # Pega o pedido no banco
    pedido = db.query(OrderTable).filter_by(
        id=cancel_pedido_schema.pedido_id
        ).first()
    
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    if pedido.status in ("CANCELADO", "CONCLUIDO"):     
        raise HTTPException(status_code=400, detail="esse pedido não pode ser cancelado")   # verifica se o pedido já foi cancelado ou concluído


    # Verifica se o usuário logado é dono do pedido ou admin
    checar_dono_ou_admin(
                        recurso_usuario_id=pedido.usuario_id,   # Pega o id de quem criou esse pedido
                        usuario_id=usuario_id,
                        db=db
                        )


    # Se passou na checagem, pode cancelar
    pedido.status = "CANCELADO"
    db.commit()
    db.refresh(pedido)

    return {
        "msg": f"Pedido de id {pedido.id} foi cancelado",
        "pedido": pedido
    }
    
    
    
@order_router.get("/listar")
async def listar_todos_pedidos(
    status_type: str,
    db: Session = Depends(get_db),
    admin: UserTable = Depends(checar_admin)    # verifica se o usuario é um adm (função somente para adms)
):
    
    status_type = status_type.upper()   # transformando em maiúsculas pra bater com os nomes de status da tabela pedidos
    
    
    if status_type not in STATUS_VALIDOS:
        raise HTTPException(status_code=400, detail="status inválido")   # verifica se o status existe no sistema
    
    pedidos = db.query(OrderTable).filter_by(
        status=status_type
        ).all()
    
    if not pedidos:
        raise HTTPException(status_code=404, detail="nenhum pedido encontrado")   # verifica se existem pedidos de determinado status no sistema

    return pedidos



@order_router.post("/pedido/adicionar_item")
async def adicionar_item(
    add_item_schema: AddItemSchema,
    db: Session = Depends(get_db),
    usuario_id: int = Depends(usuario_logado)
):
    
    if add_item_schema.tamanho.upper() not in TAMANHOS_VALIDOS:
        raise HTTPException(status_code=400, detail="Tamanho inválido")  # verifica se o tamanho está nas opções válidas

    add_item_schema.nome = add_item_schema.nome.title()  # usando title pra bater com o nome dos alimentos no cardápio
    
    # verifica se o pedido existe
    pedido = db.query(OrderTable).filter_by(
        id=add_item_schema.pedido_id
        ).first()
    
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    if pedido.status in ("CANCELADO", "CONCLUIDO"):
        raise HTTPException(status_code=400, detail="Esse pedido não pode ser editado")
    
    
    # Verifica se o usuário logado é dono do pedido ou admin
    checar_dono_ou_admin(
                        recurso_usuario_id=pedido.usuario_id,   # Pega o id de quem criou esse pedido
                        usuario_id=usuario_id,
                        db=db
                        )


    # busca o item no cardápio
    item_cardapio = db.query(ItemCardapioTable).filter_by(
        nome=add_item_schema.nome
        ).first()
    
    if not item_cardapio:
        raise HTTPException(status_code=404, detail="Item não encontrado no cardápio")    # validando se existe o item no cardápio

    # calcula preço dos itens com base na quantidade
    preco_total_item = item_cardapio.preco * add_item_schema.quantidade

    # cria o item do pedido
    novo_item = ItemsTable(
        quantidade=add_item_schema.quantidade,
        tipo=item_cardapio.nome,
        tamanho=add_item_schema.tamanho,
        preco_unit=item_cardapio.preco,
        preco_total=preco_total_item,
        pedido_id=add_item_schema.pedido_id
    )

    db.add(novo_item)

    # atualiza o preço total do pedido
    pedido.preco = (pedido.preco or 0) + preco_total_item   # se pedido.preco for none ele vira 0 pra poder ser somado

    db.commit()
    db.refresh(novo_item)
    db.refresh(pedido)

    return {
        "msg": f"{novo_item.quantidade} e {novo_item.tipo} adicionados ao pedido {pedido.id}",
        "pedido_id": pedido.id,
        "preco_pedido": pedido.preco
    }