// Exemplo de uma requisição do front end para a rota de excluir conta
// node tests/nome_do_arquivo.js (use no terminal para rodar) 


const url = "http://127.0.0.1:8000/profile/excluir_conta?senha_atual=julia123";

fetch(url, {
  method: "DELETE",
  headers: {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzIiwiZXhwIjoxNzc2NzE4Mjk2fQ.nXi-6vOE3wmWiyVjY-3o9xGilQzM_IgeMLUZPouQX3A"
  }
})
.then(response => {
  console.log(response.status);
  return response.json();
})
.then(data => console.dir(data, { depth: null })) 