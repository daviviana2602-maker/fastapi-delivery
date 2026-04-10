// Exemplo de uma requisição do front end para a rota de criação de pedidos
// node tests/nome_do_arquivo.js (use no terminal para rodar) 


fetch("http://127.0.0.1:8000/order/pedido", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzc1ODQwNjc0fQ.vJLYG2APJ5P8mTFS8gqOiMISORECKRac90zacyPO7j4"
  }
  
})
.then(res => res.json())
.then(data => console.log(data))
.catch(err => console.error(err))