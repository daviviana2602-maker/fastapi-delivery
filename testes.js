// Exemplo de uma requisição do front end para a API


const url = "http://127.0.0.1:8000/auth/refresh";   // entrando no /auth/refresh


// corpo da requisição conforme meu TokenSchema pede
const data = {
    refresh_token: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzc2MTAzNzcxfQ.R2LSsuFA05CatQZM-7TEqBoDKUZMj_A_PTFbVs6iBeA"
};


// usando fetch com POST que é o metodo do meu endpoint em questão
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