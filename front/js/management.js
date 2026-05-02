const API = "http://localhost:8000/management";
const ORDER_API = "http://localhost:8000/order";

// --------------------
// MSG UI
// --------------------
function showMsg(text, type = "success") {
  let el = document.getElementById("msg");

  el.innerHTML = text;
  el.style.marginBottom = "10px";
  el.style.padding = "10px";
  el.style.borderRadius = "10px";
  el.style.color = "#fff";
  el.style.background = type === "success" ? "#22c55e" : "#ef4444";
}

// --------------------
// AUTH
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

async function request(url, options) {
  const res = await fetch(url, options);

  if (res.status === 401) {
    showMsg("Sessão expirada", "error");

    localStorage.removeItem("access_token");

    setTimeout(() => {
      window.location.href = "/login.html";
    }, 800);

    return null;
  }

  return await res.json();
}

// --------------------
// USER ID
// --------------------
function getUserId() {
  const value = document.getElementById("userId").value;

  if (!value) {
    showMsg("Informe o ID do usuário", "error");
    return null;
  }

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

  if (data?.success) showMsg(data.msg || "Usuário promovido");
  else showMsg(data?.msg || "Erro ao promover", "error");
}

async function rebaixar() {
  const id = getUserId();
  if (!id) return;

  const data = await request(`${API}/rebaixar_usuario`, {
    method: "PATCH",
    headers: headers(),
    body: JSON.stringify({ usuario_a_sofrer_alteracao: id })
  });

  if (data?.success) showMsg(data.msg || "Usuário rebaixado");
  else showMsg(data?.msg || "Erro ao rebaixar", "error");
}

async function desativar() {
  const id = getUserId();
  if (!id) return;

  const data = await request(`${API}/desativar_usuario`, {
    method: "PATCH",
    headers: headers(),
    body: JSON.stringify({ usuario_a_sofrer_alteracao: id })
  });

  if (data?.success) showMsg(data.msg || "Usuário desativado");
  else showMsg(data?.msg || "Erro ao desativar", "error");
}

async function reativar() {
  const id = getUserId();
  if (!id) return;

  const data = await request(`${API}/reativar_usuario`, {
    method: "PATCH",
    headers: headers(),
    body: JSON.stringify({ usuario_a_sofrer_alteracao: id })
  });

  if (data?.success) showMsg(data.msg || "Usuário reativado");
  else showMsg(data?.msg || "Erro ao reativar", "error");
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

  if (!data?.success || !data.data?.length) {
    box.innerHTML = `<p style="color:#9ca3af">Nenhum pedido encontrado</p>`;
    return;
  }

  box.innerHTML = data.data.map(order => `
    <div class="order-card">
      <div>
        <strong>#${order.id}</strong><br>
        <span>User: ${order.usuario_id}</span>
      </div>

      <div>
        <span>Status: ${order.status}</span><br>
        <span>R$ ${order.preco}</span>
      </div>
    </div>
  `).join("");
}