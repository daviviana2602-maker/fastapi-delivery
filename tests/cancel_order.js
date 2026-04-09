// Exemplo de uma requisição do front end para a rota de cancelamento de pedidos
// node tests/nome_do_arquivo.js (use no terminal para rodar) 


fetch("http://127.0.0.1:8000/order/pedido/cancelar", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzc1NzA1NDM1fQ.c_dsiS4LQTDMvVXOiyThZzRX-dW_jCRO14vLu17zyDA"
  },

  body: JSON.stringify({
    pedido_id: 1   // passando no body pois vem como resposta do CancelPedidoSchema
  })

})
.then(res => res.json())
.then(data => console.log(data))
.catch(err => console.error(err));