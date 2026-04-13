// Exemplo de uma requisição do front end para a rota de geração de novo acces token com uso do refresh token
// node tests/nome_do_arquivo.js (use no terminal para rodar) 


fetch("http://127.0.0.1:8000/auth/refresh", {
  method: "POST",
  headers: {
    "Content-Type": "application/json"
  },

  body: JSON.stringify({    // passando no body pois vem como resposta do TokenSchema
    refresh_token: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzc2NzEyNTM3fQ.Weldqg1WPgKaHuNa-SXst34Z7lPmm4s1xXinWNM4FZE"   
  })

})
.then(res => res.json())
.then(data => console.log(data))
.catch(err => console.error(err));