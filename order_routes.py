# Rotas para Pedidos

from sqlalchemy.orm import Session

from dependencies import get_db, usuario_logado, checar_admin

from helpers import checar_dono_ou_admin, resposta_sucesso

from models import OrderTable, UserTable, STATUS_VALIDOS, CardapioTable, CompletedOrderItem, TAMANHOS_VALIDOS, TempItemsTable

from fastapi import APIRouter, Depends, HTTPException

from schemas import AddItemSchema, FinishOrderSchema, AdjustItemSchema

from response_schemas import CommonResponse



order_router = APIRouter(prefix = "/order", tags=["order"])   # define o caminho = domínio/order/(rota esolhinha)



@order_router.post("/pedido", response_model=CommonResponse)
async def criar_pedido(
    db: Session = Depends(get_db),
    usuario_id: int = Depends(usuario_logado)
):
  
    # cria o pedido com base no usuário logado
    novo_pedido = OrderTable(
        usuario_id=usuario_id
    )   
    
    db.add(novo_pedido)
    db.commit()
    db.refresh(novo_pedido)

    return resposta_sucesso(            # success já vem como True pela função
        "Pedido criado com sucesso",   # msg
        {
            "id": novo_pedido.id,
            "status": novo_pedido.status,   # data 
            "preco": novo_pedido.preco
        }
    )
    
    
    
@order_router.get("/listar", response_model=CommonResponse)
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

    return resposta_sucesso(
    "Pedidos encontrados com sucesso",
    [
        {
            "id": pedido.id,
            "usuario_id": pedido.usuario_id,
            "status": pedido.status,
            "preco": pedido.preco
        }
        for pedido in pedidos   # pois pedidos é uma lista, devido ao .all() então é retornado um formato desse de data pra cada pedido
    ]
)



@order_router.post("/pedido/adicionar_item", response_model=CommonResponse)
async def adicionar_item_temp(
    add_item_schema: AddItemSchema,
    db: Session = Depends(get_db),
    usuario_id: int = Depends(usuario_logado)
):
    
    # pega o pedido
    pedido = db.query(OrderTable).filter_by(
        id=add_item_schema.pedido_id
        ).first()
    
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    
    if pedido.status != "PENDENTE":
        raise HTTPException(status_code=400, detail="Pedido não pode ser editado") # pedido já cancelado ou concluído


    # checa dono ou admin para conceder permissão
    checar_dono_ou_admin(
                    recurso_usuario_id=pedido.usuario_id,
                    usuario_id=usuario_id,
                    db=db
                    )


    # valida tamanho e item
    if add_item_schema.tamanho.upper() not in TAMANHOS_VALIDOS:
        raise HTTPException(status_code=400, detail="Tamanho inválido")
    
    # busca item no cardápio
    item_cardapio = db.query(CardapioTable).filter_by(
        nome=add_item_schema.nome.title()
        ).first()
    
    # caso item não exista no cardápio
    if not item_cardapio:
        raise HTTPException(status_code=404, detail="Item não encontrado no cardápio")

    preco_total=item_cardapio.preco * add_item_schema.quantidade

    # cria item temporário
    novo_item_temp = TempItemsTable(
        quantidade=add_item_schema.quantidade,
        nome=item_cardapio.nome,
        tamanho=add_item_schema.tamanho,
        preco_unit=item_cardapio.preco,
        preco_total=preco_total,
        pedido_id=pedido.id
    )
    
    db.add(novo_item_temp)
    db.commit()
    db.refresh(novo_item_temp)


    return resposta_sucesso(            # success já vem como True pela função
        f"{novo_item_temp.quantidade} {novo_item_temp.nome} adicionados temporariamente"   
    )
    
    
    
@order_router.patch("/pedido/concluir", response_model=CommonResponse)
async def concluir_pedido(
                        conclude_order: FinishOrderSchema,
                        db: Session = Depends(get_db),
                        usuario_id: int = Depends(usuario_logado)
                        ):
    
    
    pedido = db.query(OrderTable).filter_by(
        id=conclude_order.pedido_id
        ).first()
    
    if not pedido:
        raise HTTPException(404, "Pedido não encontrado")
    
    # checa dono ou admin
    checar_dono_ou_admin(
                        recurso_usuario_id=pedido.usuario_id,
                        usuario_id=usuario_id,
                        db=db
                        )

    if pedido.status != "PENDENTE":
        raise HTTPException(400, "Pedido não pode ser concluído")
    

    # # pega itens temporários do usuário em questão pelo pedido_id passado no schema
    temp_itens = db.query(TempItemsTable).filter_by(
        pedido_id=pedido.id
        ).all()
    
    if not temp_itens:
        raise HTTPException(status_code=400, detail="Pedido não possui itens")
    
    
    total = 0   # para total não ser None e quebrar quando for somar preço total
    
    # cria itens reais
    for t in temp_itens:
        item_real = CompletedOrderItem(
            quantidade=t.quantidade,
            tipo=t.nome,
            tamanho=t.tamanho,
            preco_unit=t.preco_unit,
            preco_total=t.quantidade * t.preco_unit,
            pedido_id=pedido.id
        )
        
        db.add(item_real)
        total = total + t.quantidade * t.preco_unit

    # atualiza preço total e muda status
    pedido.preco = total
    pedido.status = "CONCLUIDO"

    # limpa temporários
    db.query(TempItemsTable).filter_by(
        pedido_id=pedido.id
        ).delete()
    
    db.commit()


    return resposta_sucesso(            # success já vem como True pela função
        "Pedido concluído",   
        {
            "id": pedido.id,
            "preco": pedido.preco
        }
    )
    
    
    
@order_router.patch("/pedido/cancelar", response_model=CommonResponse)
async def cancelar_pedido(
                        cancel_order: FinishOrderSchema,
                        db: Session = Depends(get_db),
                        usuario_id: int = Depends(usuario_logado)
                        ):
    
    # pedido a ser cancelado
    pedido = db.query(OrderTable).filter_by(
        id=cancel_order.pedido_id
        ).first()
    
    if not pedido:
        raise HTTPException(404, "Pedido não encontrado")
    
    # checa dono ou admin
    checar_dono_ou_admin(
                        recurso_usuario_id=pedido.usuario_id,
                        usuario_id=usuario_id,
                        db=db
                        )

    if pedido.status != "PENDENTE":
        raise HTTPException(400, "Pedido não pode ser cancelado")
    
    pedido.status = "CANCELADO"

    # limpa itens temporários do pedido
    db.query(TempItemsTable).filter_by(
        pedido_id=pedido.id
        ).delete()
    
    db.commit()

    return resposta_sucesso(            # success já vem como True pela função
        "Pedido cancelado", 
        {
            "id": pedido.id
        }
    )



@order_router.patch("/pedido/item", response_model=CommonResponse)
async def ajustar_item_pedido(
    ajustar_item_schema: AdjustItemSchema,
    db: Session = Depends(get_db),
    usuario_id: int = Depends(usuario_logado)
):
    
    # procura o id na temporarios com base no id passado 
    item = db.query(TempItemsTable).filter_by(
        id=ajustar_item_schema.item_id  
        ).first()


    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado")  # verifica se existe o item


    # associa o pedido temporario com o pedido já existente na OrderTable
    pedido = db.query(OrderTable).filter_by(
        id=item.pedido_id
        ).first()


    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")    # se não houver o pedido na OrderTable

    if pedido.status != "PENDENTE":
        raise HTTPException(status_code=400, detail="Pedido não pode ser editado")  # se o pedido já tiver sido finalizado

    # permissão (dono ou admin)
    checar_dono_ou_admin(
        recurso_usuario_id=pedido.usuario_id,
        usuario_id=usuario_id,
        db=db
    )

    # ajuste de quantidade
    nova_quantidade = item.quantidade + ajustar_item_schema.ajuste

    if nova_quantidade <= 0:    # se a nova quantidade for 0 já é automaticamente deletado
        db.delete(item)
        db.commit()
        return resposta_sucesso(            # success já vem como True pela função
        "Item removido do pedido" 
        )


    item.quantidade = nova_quantidade
    item.preco_total = item.preco_unit * nova_quantidade

    db.commit()
    db.refresh(item)


    return resposta_sucesso(            # success já vem como True pela função
        "Item atualizado com sucesso", 
        {
        "item_id": item.id,
        "nome": item.nome,
        "quantidade": item.quantidade,
        "preco_total": item.preco_total
        }
    )
    
    
    
@order_router.get("/pedido/item/listar_pedido_temp", response_model=CommonResponse)
async def listar_pedido_temporario(
    pedido_id: int,
    db: Session = Depends(get_db),
    usuario_id: int = Depends(usuario_logado)
):

    # segurança extra
    pedido = db.query(OrderTable).filter_by(
        id=pedido_id
    ).first()


    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")    


    # checa dono ou admin
    checar_dono_ou_admin(
                        recurso_usuario_id=pedido.usuario_id,
                        usuario_id=usuario_id,
                        db=db
                        )
    
    
    # lista dos itens de determinado id presentes na tabela temporários que basicamente forma um pedido completo
    pedido_temp = db.query(TempItemsTable).filter_by(
        pedido_id=pedido_id
    ).all()


    if not pedido_temp:
        return resposta_sucesso(            # success já vem como True pela função
            "Carrinho vazio até o momento", 
            {
            "pedido_id": pedido_id,
            "status": pedido.status,
            "itens": [],    # retornando que o carrinho está vazio
            "total": 0
            }
        )
        

    total = sum(p.preco_total for p in pedido_temp)     # para cada item no pedido temporário some o item.preco_total na váriavel total para a resposta


    return resposta_sucesso(    # success já vem como True pela função
    "Itens temporários listados com sucesso", 
    {
        "pedido_id": pedido_id,
        "status": pedido.status,
        "itens": [      # colunas necessárias da TempItensTable
            {
                "id": item.id,
                "quantidade": item.quantidade,
                "nome": item.nome,
                "tamanho": item.tamanho,
                "preco_unit": item.preco_unit,
                "preco_total": item.preco_total
            }
            for item in pedido_temp    # pois pedido_temp é uma lista devido ao .all
        ],
        "total": total 
    }
)