// Exemplo de uma requisição do front end para a rota de desativar usuários
// node tests/nome_do_arquivo.js (use no terminal para rodar) 


const url = "http://127.0.0.1:8000/management/desativar_usuario?delete_user_id=3";  // passando na url pois não vem como resposta de schema

fetch(url, {
  method: "PATCH",
  headers: {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyIiwiZXhwIjoxNzc1NzA1NDk3fQ.dvvnvEVTa4tpkS6WQ-07bGmoytiKgDXB_n8izHa3NMo"
  }
})
.then(response => {
  console.log(response.status);
  return response.json();
})
.then(data => console.log(data))
.catch(err => console.error(err));