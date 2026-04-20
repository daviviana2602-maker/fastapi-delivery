// Exemplo de uma requisição do front end para a rota de excluir conta
// node tests/nome_do_arquivo.js (use no terminal para rodar) 


const url = "http://127.0.0.1:8000/profile/excluir_conta";

fetch(url, {
  method: "DELETE",
  headers: {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyIiwiZXhwIjoxNzc2NzEwMjIyfQ.CoHaSv6-uXJ_c95KSwKjC5KY-KZkEEX-TCd0jgEP3Ec"
  }
})
.then(response => {
  console.log(response.status);
  return response.json();
})
.then(data => console.dir(data, { depth: null })) 