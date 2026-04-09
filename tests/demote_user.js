// Exemplo de uma requisição do front end para a rota de rebaixar usuários
// node tests/nome_do_arquivo.js (use no terminal para rodar) 


fetch("http://127.0.0.1:8000/management/rebaixar_usuario", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyIiwiZXhwIjoxNzc1NzA1NDk3fQ.dvvnvEVTa4tpkS6WQ-07bGmoytiKgDXB_n8izHa3NMo"
  },

  body: JSON.stringify({
    usuario_a_rebaixar_id: 2   // passando no body pois vem como resposta do DemoteUserSchema
  })

})
.then(res => res.json())
.then(data => console.log(data))
.catch(err => console.error(err));