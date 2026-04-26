// Exemplo de uma requisição do front end para a rota de promover usuários
// node tests/nome_do_arquivo.js (use no terminal para rodar) 


fetch("http://127.0.0.1:8000/management/promover_usuario", {
  method: "PATCH",
  headers: {
    "Content-Type": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzc3MDc1MDQwfQ.aJjqdadRRzR-2YlqCkhd65oZQC3wPPCTkEMZQ5JuPoQ"
  },

  body: JSON.stringify({
    usuario_a_sofrer_alteracao: 4   // passando no body pois vem como resposta do AlterationUserSchema
  })

})
.then(res => res.json())
.then(data => console.log(data))
.catch(err => console.error(err));