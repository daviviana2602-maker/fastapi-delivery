// Exemplo de uma requisição do front end para a rota de listar pedidos
// node tests/nome_do_arquivo.js (use no terminal para rodar) 


const url = "http://127.0.0.1:8000/order/listar?status_type=concluido";  // passando na url pois não vem como reposta de schema 

fetch(url, {
  method: "GET",
  headers: {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzc2MTA4MTUwfQ.-pNjo4wzhwto9XxoEoddWxlmgOCyKRSKmxMGN-uLjKA"
  }
})
.then(response => {
  console.log(response.status);
  return response.json();
})
.then(data => console.log(data))
.catch(err => console.error(err));