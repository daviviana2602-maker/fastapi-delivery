// ============================================================
// orders.js — pedidos, cardápio, carrinho
// Depende de: config.js (API_BASE, authHeaders, request, showMsg)
// ============================================================

var ORDERS_API = API_BASE + "/order";

var pedidoAtual = null;

// --------------------
// STATUS
// --------------------
function atualizarStatus() {
  var el = document.getElementById("statusPedido");
  if (!el) return;
  el.innerHTML = pedidoAtual
    ? `<strong>ID:</strong> ${pedidoAtual}`
    : "Nenhum pedido ativo";
}

// --------------------
// DEBUG
// --------------------
function showRaw(data) {
  var el = document.getElementById("out");
  if (el) el.innerText = JSON.stringify(data, null, 2);
}

// --------------------
// CRIAR PEDIDO
// --------------------
async function criarPedido() {
  const data = await request(`${ORDERS_API}/pedido`, {
    method: "POST",
    headers: authHeaders()
  });

  if (data) {
    pedidoAtual = data?.data?.id;
    atualizarStatus();
    showRaw(data);
  }
}

// --------------------
// ADICIONAR ITEM
// --------------------
async function adicionarItem(nome, qtyId, sizeId) {
  if (!pedidoAtual) return alert("Crie um pedido primeiro");

  const quantidade = Number(document.getElementById(qtyId).value);
  const tamanho    = document.getElementById(sizeId).value;

  if (!Number.isInteger(quantidade) || quantidade < 1) {
    return alert("Quantidade mínima é 1");
  }
  if (!tamanho) {
    return alert("Selecione um tamanho");
  }

  const data = await request(`${ORDERS_API}/pedido/adicionar_item`, {
    method: "POST",
    headers: authHeaders(),
    body: JSON.stringify({
      pedido_id: pedidoAtual,
      nome,
      quantidade,
      tamanho: tamanho.toUpperCase()
    })
  });

  if (data) {
    showRaw(data);
    listarCarrinho();
  }
}

// --------------------
// CARDÁPIO
// --------------------
async function carregarCardapio() {
  const data = await request(`${ORDERS_API}/cardapio`, {
    method: "GET",
    headers: authHeaders()
  });
  if (!data) return;

  const container = document.getElementById("cardapio");
  if (!container) return;

  container.innerHTML = data.data.map((item, index) => {
    const qtyId  = `qty_${index}`;
    const sizeId = `size_${index}`;
    return `
      <div class="cardapio-item">
        <div class="info">
          <strong>${item.nome}</strong>
          <span>${item.categoria}</span>
          <span>R$ ${item.preco}</span>
        </div>
        <div class="actions">
          <input id="${qtyId}" type="number" min="1" step="1" placeholder="Qtd">
          <select id="${sizeId}">
            <option value="">Tamanho</option>
            <option value="pequeno">Pequeno</option>
            <option value="tradicional">Tradicional</option>
            <option value="grande">Grande</option>
          </select>
          <button onclick="adicionarItem('${item.nome}', '${qtyId}', '${sizeId}')">
            Adicionar
          </button>
        </div>
      </div>
    `;
  }).join("");
}

// --------------------
// AJUSTAR ITEM
// --------------------
async function ajustarItem(itemId, ajuste) {
  const data = await request(`${ORDERS_API}/pedido/item`, {
    method: "PATCH",
    headers: authHeaders(),
    body: JSON.stringify({ item_id: itemId, ajuste })
  });

  if (data) {
    showRaw(data);
    listarCarrinho();
  }
}

// --------------------
// CARRINHO
// --------------------
async function listarCarrinho() {
  const container = document.getElementById("carrinho");
  if (!container) return;

  if (!pedidoAtual) {
    container.innerHTML = "<p>Crie um pedido primeiro</p>";
    return;
  }

  const data = await request(
    `${ORDERS_API}/pedido/item/listar_pedido_temp?pedido_id=${pedidoAtual}`,
    { method: "GET", headers: authHeaders() }
  );
  if (!data) return;

  const itens = data.data?.itens ?? [];

  if (itens.length === 0) {
    container.innerHTML = "<p>Carrinho vazio</p>";
    return;
  }

  container.innerHTML = itens.map(item => `
    <div class="carrinho-item">
      <strong>${item.nome}</strong>
      <span>Qtd: ${item.quantidade}</span>
      <span>Tamanho: ${item.tamanho}</span>
      <button onclick="ajustarItem(${item.id}, -1)">- remover</button>
      <button onclick="ajustarItem(${item.id}, +1)">+ adicionar</button>
    </div>
  `).join("");
}

// --------------------
// CONCLUIR
// --------------------
async function concluirPedido() {
  if (!pedidoAtual) return alert("Nenhum pedido ativo");

  const data = await request(`${ORDERS_API}/pedido/concluir`, {
    method: "PATCH",
    headers: authHeaders(),
    body: JSON.stringify({ pedido_id: pedidoAtual })
  });

  if (data) {
    showRaw(data);
    pedidoAtual = null;
    atualizarStatus();
    var carrinho = document.getElementById("carrinho");
    if (carrinho) carrinho.innerHTML = "";
  }
}

// --------------------
// CANCELAR
// --------------------
async function cancelarPedido() {
  if (!pedidoAtual) return alert("Nenhum pedido ativo");

  const data = await request(`${ORDERS_API}/pedido/cancelar`, {
    method: "PATCH",
    headers: authHeaders(),
    body: JSON.stringify({ pedido_id: pedidoAtual })
  });

  if (data) {
    showRaw(data);
    pedidoAtual = null;
    atualizarStatus();
    var carrinho = document.getElementById("carrinho");
    if (carrinho) carrinho.innerHTML = "";
  }
}

// --------------------
// INIT
// --------------------
carregarCardapio();
atualizarStatus();