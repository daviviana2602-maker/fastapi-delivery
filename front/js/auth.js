const API = "http://localhost:8000/auth";

// --------------------
// MSG GLOBAL
// --------------------
function showMsg(text, type = "success") {
  let el = document.getElementById("msg");

  if (!el) {
    el = document.createElement("div");
    el.id = "msg";
    document.querySelector(".card").prepend(el);
  }

  el.innerHTML = text;
  el.style.padding = "10px";
  el.style.borderRadius = "10px";
  el.style.marginBottom = "10px";
  el.style.color = "#fff";
  el.style.background = type === "success" ? "#22c55e" : "#ef4444";
}

// --------------------
// BUSCAR USUÁRIO LOGADO (/me)
// --------------------
async function fetchUser() {
  const token = localStorage.getItem("access_token");

  if (!token) return;

  const res = await fetch(`${API}/me`, {
    method: "GET",
    headers: {
      "Authorization": "Bearer " + token
    }
  });

  const user = await res.json();

  localStorage.setItem("user", JSON.stringify(user));
}

// --------------------
// LOGIN
// --------------------
async function login() {

  const email = document.getElementById("email").value.trim();
  const senha = document.getElementById("senha").value;

  const res = await fetch(`${API}/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ email, senha })
  });

  const data = await res.json();

  if (data.success && data.data?.access_token) {

    localStorage.setItem("access_token", data.data.access_token);
    localStorage.setItem("refresh_token", data.data.refresh_token);

    // pega usuário logado (admin, etc)
    await fetchUser();

    alert("Login realizado com sucesso");

    window.location.replace("/pages/dashboard.html");

  } else {

    alert(data.msg || data.detail || "Login inválido");
  }
}


// --------------------
// REGISTER
// --------------------
async function register() {

  const nome = document.getElementById("nome").value.trim();
  const email = document.getElementById("email").value.trim();
  const senha = document.getElementById("senha").value;

  if (!nome || !email || !senha) {
    showMsg("Preencha todos os campos", "error");
    return;
  }

  const res = await fetch(`${API}/criar_conta`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ nome, email, senha })
  });

  const data = await res.json();

  if (data.success) {

    showMsg(data.msg || "Conta criada com sucesso");

    document.getElementById("nome").value = "";
    document.getElementById("email").value = "";
    document.getElementById("senha").value = "";

    setTimeout(() => {
      window.location.href = "login.html";
    }, 1200);

  } else {
    showMsg(data.msg || "Erro ao criar conta", "error");
  }
}