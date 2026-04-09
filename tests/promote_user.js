// Exemplo de uma requisição do front end para a rota de promover_usuários
// node tests/nome_do_arquivo.js (use no terminal para rodar) 


fetch("http://127.0.0.1:8000/management/promover_usuario", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzc1NzA1NDM1fQ.c_dsiS4LQTDMvVXOiyThZzRX-dW_jCRO14vLu17zyDA"
  },

  body: JSON.stringify({
    usuario_a_promover_id: 2    // passando no body pois vem como resposta do PromoteUserSchema
  })

})
.then(res => res.json())
.then(data => console.log(data))
.catch(err => console.error(err));