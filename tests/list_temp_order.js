// Exemplo de uma requisição do front end para a rota de listar pedidos temporários (carrinho do usuário)
// node tests/nome_do_arquivo.js (use no terminal para rodar) 


const url = "http://127.0.0.1:8000/order/pedido/item/listar_pedido_temp?pedido_id=1";  // passando na url pois não vem como reposta de schema 

fetch(url, {
  method: "GET",
  headers: {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzc2MDQ1OTI2fQ.vA2I_6YL0WNPB_Ila5ZFB88BJqToJBMQHtyLCu7t3cs"
  }
})
.then(response => {
  console.log(response.status);
  return response.json();
})
.then(data => console.log(data))
.catch(err => console.error(err));