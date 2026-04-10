// Exemplo de uma requisição do front end para a rota de editar itens temporários
// node tests/nome_do_arquivo.js (use no terminal para rodar) 


fetch("http://127.0.0.1:8000/order/pedido/item", {
  method: "PATCH",
  headers: {
    "Content-Type": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyIiwiZXhwIjoxNzc1ODQ0NzE5fQ.GQlH9aaMsaCQvnzsPbQNvDxMSB_-a1ph2IS9vCUXHIU"
  },

  body: JSON.stringify({    // passando no body pois vem como resposta do AdjustItemSchema
    item_id: 2,       
    ajuste: 20        // quantidade de itens a serem removidos ou adicionados (positivo/negativo)
  })

})
.then(res => res.json())
.then(data => console.log(data))
.catch(err => console.error(err));