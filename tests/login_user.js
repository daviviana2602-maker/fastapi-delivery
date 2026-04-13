// Exemplo de uma requisição do front end para a rota de logar usuário
// node tests/nome_do_arquivo.js (use no terminal para rodar) 


fetch("http://127.0.0.1:8000/auth/login", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },

  body: JSON.stringify({    // passando no body pois vem como resposta do CreateUserSchema
    "email": "julia@gmail.com",
    "senha": "julia123"
  })

})
.then(res => res.json())
.then(data => console.log(data))
.catch(err => console.error(err));