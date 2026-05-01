const API = "http://localhost:8000/auth";


// LOGIN
async function login() {
  const res = await fetch(`${API}/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      email: document.getElementById("email").value,
      senha: document.getElementById("senha").value
    })
  });

  const data = await res.json();

  console.log(data);

  if (data.data?.access_token) {
    localStorage.setItem("token", data.data.access_token);
    alert("Login ok");
  }
}


// REGISTER
async function register() {
  const res = await fetch(`${API}/criar_conta`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      nome: document.getElementById("nome").value,
      email: document.getElementById("email").value,
      senha: document.getElementById("senha").value
    })
  });

  const data = await res.json();
  console.log(data);

  alert(data.msg);
}


// EXEMPLO DE USO DO TOKEN
function getProfile() {
  fetch(`${API}/profile`, {
    headers: {
      Authorization: `Bearer ${localStorage.getItem("token")}`
    }
  })
  .then(r => r.json())
  .then(console.log);
}