// Exemplo de uma requisição do front end para a rota de cancelamento de pedidos
// node tests/nome_do_arquivo.js (use no terminal para rodar) 


fetch("http://127.0.0.1:8000/order/pedido/cancelar", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzIiwiZXhwIjoxNzc2MjEzNTAzfQ.bVBstiLQF5cSWkthmL5cm2ZaR1pYrSGbJmiG9tZOSbg"
  },

  body: JSON.stringify({
    pedido_id: 1    // passando no body pois vem como resposta do CancelPedidoSchema
  })

})
.then(res => res.json())
.then(data => console.log(data))
.catch(err => console.error(err));