// Exemplo de uma requisição do front end para a rota de promover usuários
// node tests/nome_do_arquivo.js (use no terminal para rodar) 


fetch("http://127.0.0.1:8000/management/promover_usuario", {
  method: "PATCH",
  headers: {
    "Content-Type": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzc2MDQ2NzY5fQ.YLKgLHxnmMm0D7slrCZFVj3har4T8s9G9u-yOtSKk5s"
  },

  body: JSON.stringify({
    usuario_a_sofrer_alteracao: 2   // passando no body pois vem como resposta do AlterationUserSchema
  })

})
.then(res => res.json())
.then(data => console.log(data))
.catch(err => console.error(err));