
const API_BASE =
  window.location.hostname === "localhost"
    ? "http://localhost:8000"
    : "https://fastapi-delivery-production.up.railway.app";

const API = `${API_BASE}/auth`;

// --------------------
// MSG GLOBAL
// --------------------
function showMsg(text, type = "success") {
  let el = document.getElementById("msg");

  if (!el) {
    el = document.createElement("div");
    el.id = "msg";
    document.querySelector(".card")?.prepend(el);
  }

  el.innerHTML = text;
  el.style.padding = "10px";
  el.style.borderRadius = "10px";
  el.style.marginBottom = "10px";
  el.style.color = "#fff";
  el.style.background = type === "success" ? "#22c55e" : "#ef4444";
}

// --------------------
// PARSE ERRO FASTAPI
// --------------------
function parseError(data) {
  if (!data) return "Erro desconhecido";

  if (typeof data === "string") return data;

  if (Array.isArray(data.detail)) {
    return data.detail.map(e => e.msg).join(", ");
  }

  if (data.detail) return data.detail;

  if (data.msg) return data.msg;

  return JSON.stringify(data);
}

// --------------------
// FETCH USER (/me)
// --------------------
async function fetchUser() {
  const token = localStorage.getItem("access_token");
  if (!token) return;

  try {
    const res = await fetch(`${API}/me`, {
      method: "GET",
      headers: {
        "Authorization": "Bearer " + token
      }
    });

    const data = await res.json().catch(() => null);

    if (!res.ok || !data) return;

    const user = data?.data ?? data;

    localStorage.setItem("user", JSON.stringify(user));

  } catch (err) {
    console.log("Erro /me:", err);
  }
}

// --------------------
// LOGIN
// --------------------
async function login() {

  const email = document.getElementById("email").value.trim();
  const senha = document.getElementById("senha").value;

  const errorBox = document.getElementById("errorBox");
  errorBox.innerHTML = "";

  if (!email || !senha) {
    errorBox.innerHTML = `<div class="error-msg">Preencha email e senha</div>`;
    return;
  }

  let res;
  let data;

  try {
    res = await fetch(`${API}/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ email, senha })
    });

    data = await res.json().catch(() => null);

  } catch (err) {
    errorBox.innerHTML = `<div class="error-msg">Erro de conexão</div>`;
    return;
  }

  if (!res.ok) {
    const msg = parseError(data);
    errorBox.innerHTML = `<div class="error-msg">${msg}</div>`;
    return;
  }

  const token = data?.data?.access_token;

  if (!token) {
    errorBox.innerHTML = `<div class="error-msg">Token não recebido</div>`;
    console.log("RESPOSTA BRUTA:", data);
    return;
  }

  localStorage.setItem("access_token", token);
  localStorage.setItem("refresh_token", data.data.refresh_token);

  await fetchUser();

  showMsg("Login realizado com sucesso");

  window.location.href = "/pages/dashboard.html";
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

  try {
    const res = await fetch(`${API}/criar_conta`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ nome, email, senha })
    });

    const data = await res.json().catch(() => null);

    if (!res.ok) {
      showMsg(parseError(data), "error");
      return;
    }

    showMsg("Conta criada com sucesso");

    document.getElementById("nome").value = "";
    document.getElementById("email").value = "";
    document.getElementById("senha").value = "";

    setTimeout(() => {
      window.location.href = "login.html";
    }, 1200);

  } catch (err) {
    showMsg("Erro de conexão", "error");
  }
}

// --------------------
// GET USER HELPER 
// --------------------
function getUser() {
  try {
    return JSON.parse(localStorage.getItem("user"));
  } catch {
    return null;
  }
}

// --------------------
// ADMIN CHECK PADRÃO
// --------------------
function isAdmin() {
  const user = getUser();
  return user?.admin === true;
}