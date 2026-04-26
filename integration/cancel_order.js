// Exemplo de uma requisição do front end para a rota de cancelamento de pedidos
// node tests/nome_do_arquivo.js (use no terminal para rodar) 


fetch("http://127.0.0.1:8000/order/pedido/cancelar", {
  method: "PATCH",
  headers: {
    "Content-Type": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzc1ODQ0MDU1fQ.tXJ0hLujLrd87O1eypll9nb64lzLCZlZkvmsP3ioKGc"
  },

  body: JSON.stringify({
    pedido_id: 2   // passando no body pois vem como resposta do CancelOrderSchema
  })

})
.then(res => res.json())
.then(data => console.log(data))
.catch(err => console.error(err));