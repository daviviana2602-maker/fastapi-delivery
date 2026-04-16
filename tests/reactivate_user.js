// Exemplo de uma requisição do front end para a rota de reativar usuários
// node tests/nome_do_arquivo.js (use no terminal para rodar) 


fetch("http://127.0.0.1:8000/management/reativar_usuario", {
  method: "PATCH",
  headers: {
    "Content-Type": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzc2MTIyMTgxfQ.BROUQud4EkEvHFgUFS1vGIxwwhWkzoieF1WsMUWPIKQ"
  },

  body: JSON.stringify({
    usuario_a_sofrer_alteracao: 2    // passando no body pois vem como resposta do AlterationUserSchema
  })

})
.then(res => res.json())
.then(data => console.log(data))
.catch(err => console.error(err));