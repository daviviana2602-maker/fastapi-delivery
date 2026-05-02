const API = "http://localhost:8000/management";
const ORDER_API = "http://localhost:8000/order";

// --------------------
// UTIL
// --------------------
function show(data) {
  document.getElementById("out").innerText =
    JSON.stringify(data, null, 2);
}

function getToken() {
  return localStorage.getItem("access_token");
}

function headers() {
  return {
    "Content-Type": "application/json",
    "Authorization": `Bearer ${getToken()}`
  };
}

async function request(url, options) {
  const res = await fetch(url, options);

  if (res.status === 401) {
    alert("Sessão expirada");
    localStorage.removeItem("access_token");
    window.location.href = "/login.html";
    return;
  }

  return await res.json();
}

// --------------------
// USER ID
// --------------------
function getUserId() {
  const value = document.getElementById("userId").value;

  if (!value) {
    alert("Informe o ID do usuário");
    return null;
  }

  return Number(value);
}

// --------------------
// USERS ACTIONS
// --------------------
async function promover() {
  const id = getUserId();
  if (!id) return;

  const data = await request(`${API}/promover_usuario`, {
    method: "PATCH",
    headers: headers(),
    body: JSON.stringify({ usuario_a_sofrer_alteracao: id })
  });

  show(data);
}

async function rebaixar() {
  const id = getUserId();
  if (!id) return;

  const data = await request(`${API}/rebaixar_usuario`, {
    method: "PATCH",
    headers: headers(),
    body: JSON.stringify({ usuario_a_sofrer_alteracao: id })
  });

  show(data);
}

async function desativar() {
  const id = getUserId();
  if (!id) return;

  const data = await request(`${API}/desativar_usuario`, {
    method: "PATCH",
    headers: headers(),
    body: JSON.stringify({ usuario_a_sofrer_alteracao: id })
  });

  show(data);
}

async function reativar() {
  const id = getUserId();
  if (!id) return;

  const data = await request(`${API}/reativar_usuario`, {
    method: "PATCH",
    headers: headers(),
    body: JSON.stringify({ usuario_a_sofrer_alteracao: id })
  });

  show(data);
}

// --------------------
// ORDERS (NOVO)
// --------------------
async function listarPedidos(status) {
  const data = await request(
    `${ORDER_API}/listar?status_type=${status}`,
    {
      method: "GET",
      headers: headers()
    }
  );

  show(data);
}