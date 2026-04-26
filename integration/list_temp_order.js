// Exemplo de uma requisição do front end para a rota de listar pedidos temporários (carrinho do usuário)
// node tests/nome_do_arquivo.js (use no terminal para rodar) 


const url = "http://127.0.0.1:8000/order/pedido/item/listar_pedido_temp?pedido_id=1";  // passando na url pois não vem como reposta de schema 

fetch(url, {
  method: "GET",
  headers: {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzc2NjM4NjQxfQ.5TlJD6LhXb5qmUCBpgZNxdnJ_D4xyYVNN2wtUZKtTKA"
  }
})
.then(response => {
  console.log(response.status);
  return response.json();
})
.then(data => console.dir(data, { depth: null }))   // para ver a lista completa
.catch(err => console.error(err));