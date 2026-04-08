// Exemplo de uma requisição do front end para a rota de promover_usuários
// node tests/nome_do_arquivo.js (use no terminal para rodar) 


fetch("http://127.0.0.1:8000/management/promover_usuario", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyIiwiZXhwIjoxNzc1NjcwMTc1fQ.H-y34jDBPXdJ5PvVlFsF00IRWNIWx3UcefuXTu2Seak"
  },

  body: JSON.stringify({
    usuario_a_promover_id: 1    // passando no body pois vem como resposta do CancelPedidoSchema
  })

})
.then(res => res.json())
.then(data => console.log(data))
.catch(err => console.error(err));