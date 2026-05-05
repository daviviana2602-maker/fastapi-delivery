const API_BASE =
  window.location.hostname === "localhost"
    ? "http://localhost:8000"
    : "https://fastapi-delivery-production.up.railway.app";

const API = `${API_BASE}/management`;
const ORDER_API = `${API_BASE}/order`;

// --------------------
// UI MSG
// --------------------
function showMsg(text, type = "success") {
  const el = document.getElementById("msg");

  el.innerHTML = text;
  el.style = `
    margin-bottom:10px;
    padding:10px;
    border-radius:10px;
    color:#fff;
    background:${type === "success" ? "#22c55e" : "#ef4444"};
  `;
}

// --------------------
// AUTH HEADER
// --------------------
function getToken() {
  return localStorage.getItem("access_token");
}

function headers() {
  return {
    "Content-Type": "application/json",
    "Authorization": `Bearer ${getToken()}`
  };
}

// --------------------
// REQUEST SAFE
// --------------------
async function request(url, options) {
  try {
    const res = await fetch(url, options);

    const text = await res.text();

    let data;
    try {
      data = JSON.parse(text);
    } catch {
      console.error("INVALID JSON:", text);
      showMsg("Erro inesperado do servidor", "error");
      return null;
    }

    if (!res.ok) {
      console.error("API ERROR:", res.status, data);
      showMsg(data?.detail || "Erro na requisição", "error");
      return null;
    }

    return data;

  } catch (err) {
    console.error("NETWORK ERROR:", err);
    showMsg("Erro de rede", "error");
    return null;
  }
}

// --------------------
// USER ID
// --------------------
function getUserId() {
  const value = document.getElementById("userId").value;
  if (!value) return showMsg("Informe o ID", "error"), null;
  return Number(value);
}

// --------------------
// AÇÕES ADMIN
// --------------------
async function promover() {
  const id = getUserId();
  if (!id) return;

  const data = await request(`${API}/promover_usuario`, {
    method: "PATCH",
    headers: headers(),
    body: JSON.stringify({ usuario_a_sofrer_alteracao: id })
  });

  if (data?.success) showMsg(data.msg);
}

async function rebaixar() {
  const id = getUserId();
  if (!id) return;

  const data = await request(`${API}/rebaixar_usuario`, {
    method: "PATCH",
    headers: headers(),
    body: JSON.stringify({ usuario_a_sofrer_alteracao: id })
  });

  if (data?.success) showMsg(data.msg);
}

async function desativar() {
  const id = getUserId();
  if (!id) return;

  const data = await request(`${API}/desativar_usuario`, {
    method: "PATCH",
    headers: headers(),
    body: JSON.stringify({ usuario_a_sofrer_alteracao: id })
  });

  if (data?.success) showMsg(data.msg);
}

async function reativar() {
  const id = getUserId();
  if (!id) return;

  const data = await request(`${API}/reativar_usuario`, {
    method: "PATCH",
    headers: headers(),
    body: JSON.stringify({ usuario_a_sofrer_alteracao: id })
  });

  if (data?.success) showMsg(data.msg);
}

// --------------------
// ORDERS
// --------------------
async function listarPedidos(status) {
  const data = await request(
    `${ORDER_API}/listar?status_type=${status}`,
    {
      method: "GET",
      headers: headers()
    }
  );

  const box = document.getElementById("ordersBox");

  if (!data?.data || !data.data.length) {
    box.innerHTML = `<p style="color:#9ca3af">Nenhum pedido</p>`;
    return;
  }

  box.innerHTML = data.data.map(o => `
    <div class="order-card">
      <strong>#${o.id}</strong> - User ${o.usuario_id} - ${o.status} - R$${o.preco}
    </div>
  `).join("");
}

// --------------------
// GLOBAL EXPORT (onclick)
window.promover = promover;
window.rebaixar = rebaixar;
window.desativar = desativar;
window.reativar = reativar;
window.listarPedidos = listarPedidos;