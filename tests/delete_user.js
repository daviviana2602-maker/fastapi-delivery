// Exemplo de uma requisição do front end para a rota de deletar usuários
// node tests/nome_do_arquivo.js (use no terminal para rodar) 


fetch("http://127.0.0.1:8000/management/deletar_usuario", {
  method: "DELETE",
  headers: {
    "Content-Type": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyIiwiZXhwIjoxNzc1NjcxNzA1fQ.huIWTOQ2UHwdiDitsSOE6lWQfhztK8stVEvzJHp3Zlo"
  },

  body: JSON.stringify({
    usuario_a_deletar_id: 1    // passando no body pois vem como resposta do CancelPedidoSchema
  })

})
.then(res => res.json())
.then(data => console.log(data))
.catch(err => console.error(err));