var MGMT_API       = API_BASE + "/management";
var MGMT_ORDER_API = API_BASE + "/order";

// --------------------
// MSG DO ADMIN
// Usa #msgAdmin se existir (dashboard), senão cai no #msg global
// --------------------
function showMsgAdmin(text, type) {
  type = type || "success";
  var target = document.getElementById("msgAdmin") || document.getElementById("msg");
  if (!target) return;
  target.innerHTML = '<div style="margin-top:10px;padding:10px;border-radius:10px;font-size:13px;color:white;background:' + (type === "success" ? "#22c55e" : "#ef4444") + '">' + text + '</div>';
}

// --------------------
// USER ID
// --------------------
function getUserId() {
  const value = document.getElementById("userId").value;
  if (!value) {
    showMsgAdmin("Informe o ID", "error");
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
  const data = await request(`${MGMT_API}/promover_usuario`, {
    method: "PATCH",
    headers: authHeaders(),
    body: JSON.stringify({ usuario_a_sofrer_alteracao: id })
  });
  if (data?.success) showMsgAdmin(data.msg);
}

async function rebaixar() {
  const id = getUserId();
  if (!id) return;
  const data = await request(`${MGMT_API}/rebaixar_usuario`, {
    method: "PATCH",
    headers: authHeaders(),
    body: JSON.stringify({ usuario_a_sofrer_alteracao: id })
  });
  if (data?.success) showMsgAdmin(data.msg);
}

async function desativar() {
  const id = getUserId();
  if (!id) return;
  const data = await request(`${MGMT_API}/desativar_usuario`, {
    method: "PATCH",
    headers: authHeaders(),
    body: JSON.stringify({ usuario_a_sofrer_alteracao: id })
  });
  if (data?.success) showMsgAdmin(data.msg);
}

async function reativar() {
  const id = getUserId();
  if (!id) return;
  const data = await request(`${MGMT_API}/reativar_usuario`, {
    method: "PATCH",
    headers: authHeaders(),
    body: JSON.stringify({ usuario_a_sofrer_alteracao: id })
  });
  if (data?.success) showMsgAdmin(data.msg);
}

// --------------------
// LISTAR PEDIDOS
// --------------------
async function listarPedidos(status) {
  const data = await request(
    `${MGMT_ORDER_API}/listar?status_type=${status}`,
    { method: "GET", headers: authHeaders() }
  );

  const box = document.getElementById("ordersBox");
  if (!box) return;

  if (!data?.data?.length) {
    box.innerHTML = '<p style="color:#9ca3af">Nenhum pedido</p>';
    return;
  }

  box.innerHTML = data.data.map(function(o) {
    return '<div class="order-card"><strong>#' + o.id + '</strong> — User ' + o.usuario_id + ' — ' + o.status + ' — R$' + o.preco + '</div>';
  }).join("");
}