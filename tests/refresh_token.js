// Exemplo de uma requisição do front end para a rota refresh (criar novo access_token com base no refresh_token)
// node tests/nome_do_arquivo.js (use no terminal para rodar)   


const url = "http://127.0.0.1:8000/auth/refresh";


// corpo da requisição conforme meu TokenSchema pede
// refresh_token não precisa do Bearer, pois não depende da função usuario_logado
const data = {
    refresh_token: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzc2NjQ4NzE3fQ.D0PUKj5E9hzOWKL4y0cETTUzzGBLH87YwqfmbD6VTEA"
};


// usando fetch com POST que é o metodo do endpoint em questão
fetch(url, {
    method: "POST",
    headers: {
        "Content-Type": "application/json"      // diz que o corpo é JSON
    },
    body: JSON.stringify(data)      // transforma o objeto JS em string JSON
})

.then(response => {
    console.log(response.status);     //  imprime o status HTTP (ex: 200)
    return response.json();         // pega o JSON da resposta
})

.then(json => {
    console.log(json);            // imprime o que a API respondeu
})

.catch(err => {         // forma do JavaScript capturar erros na requisição ou no processamento do .then().
    console.error("Erro na requisição:", err);    // caso algum erro na requisição (API offline, URL errada, JSON inválido), ele cai aqui
});