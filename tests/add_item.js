// Exemplo de uma requisição do front end para a rota de adicionar itens no pedido temporário
// node tests/nome_do_arquivo.js (use no terminal para rodar) 


fetch("http://127.0.0.1:8000/order/pedido/adicionar_item", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzIiwiZXhwIjoxNzc2MTIxODUwfQ.mmOiF1F1G1ebWRWAcp_Ifl_XYO5-Y0MvelbxlOwzMjc"
  },

  body: JSON.stringify({    // passando no body pois vem como resposta do AddItemSchema
    quantidade: 2,
    nome: "estrogonofe",
    tamanho: "tradicional",
    pedido_id: 1
  })

})
.then(res => res.json())
.then(data => console.log(data))
.catch(err => console.error(err));