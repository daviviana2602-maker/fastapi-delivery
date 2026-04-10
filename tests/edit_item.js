// Exemplo de uma requisição do front end para a rota de editar itens temporários
// node tests/nome_do_arquivo.js (use no terminal para rodar) 


fetch("http://127.0.0.1:8000/order/pedido/item", {
  method: "PATCH",
  headers: {
    "Content-Type": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzc1ODQ4ODY5fQ.krOn4EO6qozWN0yTNFDPqnbxzrlrBED3KJlqLgeNtYM"
  },

  body: JSON.stringify({    // passando no body pois vem como resposta do AdjustItemSchema
    item_id: 2,       
    ajuste: 2        // quantidade de itens a serem removidos ou adicionados (positivo/negativo)
  })

})
.then(res => res.json())
.then(data => console.log(data))
.catch(err => console.error(err));