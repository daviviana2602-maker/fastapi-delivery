// Exemplo de uma requisição do front end para a rota de mudar dados do perfil (nome, email e senha)
// node tests/nome_do_arquivo.js (use no terminal para rodar) 


fetch("http://127.0.0.1:8000/profile/editar_perfil", {
  method: "PATCH",
  headers: {
    "Content-Type": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzc2MTA4MTUwfQ.-pNjo4wzhwto9XxoEoddWxlmgOCyKRSKmxMGN-uLjKA"
  },

  body: JSON.stringify({    // passando no body pois vem como resposta do UpdateProfileSchema (nome, email, senha e senha_atual)
    "nome": "juliads",
    "email": "juliads@gmail.com",
    "senha": "juliads123",
    "senha_atual": "juliads123"
  })

})
.then(res => res.json())
.then(data => console.log(data))
.catch(err => console.error(err));