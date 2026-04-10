// Exemplo de uma requisição do front end para a rota de concluir pedido
// node tests/nome_do_arquivo.js (use no terminal para rodar) 


fetch("http://127.0.0.1:8000/order/pedido/concluir", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyIiwiZXhwIjoxNzc1ODQwNzEyfQ.wxNenBbiAtxToeEJb-LZKUrz1wIyujVMWQ7YrfJxSs8"
  },

  body: JSON.stringify({    // passando no body pois vem como resposta do ConcludeOrderSchema
    pedido_id: 1
  })

})
.then(res => res.json())
.then(data => console.log(data))
.catch(err => console.error(err));