const API = "http://localhost:8000/order";

let pedidoAtual = null;

// --------------------
// STATUS
// --------------------
function atualizarStatus() {
  const el = document.getElementById("statusPedido");

  el.innerHTML = pedidoAtual
    ? `<strong>ID:</strong> ${pedidoAtual}`
    : "Nenhum pedido ativo";
}

// --------------------
// DEBUG
// --------------------
function showRaw(data) {
  const el = document.getElementById("out");
  if (el) {
    el.innerText = JSON.stringify(data, null, 2);
  }
}

// --------------------
// CRIAR PEDIDO
// --------------------
async function criarPedido() {
  const res = await fetch(`${API}/pedido`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${localStorage.getItem("access_token")}`
    }
  });

  const data = await res.json();

  pedidoAtual = data?.data?.id;

  atualizarStatus();
  showRaw(data);
}

// --------------------
// ADICIONAR ITEM (COM TRAVA FORTE)
// --------------------
async function adicionarItem(nome, qtyId, sizeId) {
  if (!pedidoAtual) return alert("Crie um pedido primeiro");

  const quantidade = Number(document.getElementById(qtyId).value);
  const tamanho = document.getElementById(sizeId).value;

  // 🔒 TRAVA FRONTEND
  if (!Number.isInteger(quantidade) || quantidade < 1) {
    alert("Quantidade mínima é 1");
    return;
  }

  if (!tamanho) {
    alert("Selecione um tamanho");
    return;
  }

  const res = await fetch(`${API}/pedido/adicionar_item`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${localStorage.getItem("access_token")}`
    },
    body: JSON.stringify({
      pedido_id: pedidoAtual,
      nome,
      quantidade,
      tamanho: tamanho.toUpperCase()
    })
  });

  const data = await res.json();

  showRaw(data);
  listarCarrinho();
}

// --------------------
// CARDÁPIO
// --------------------
async function carregarCardapio() {
  const res = await fetch(`${API}/cardapio`);
  const data = await res.json();

  const container = document.getElementById("cardapio");

  container.innerHTML = data.data.map((item, index) => {
    const qtyId = `qty_${index}`;
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
// AJUSTAR ITEM (-1 / +1)
// --------------------
async function ajustarItem(itemId, ajuste) {
  const res = await fetch(`${API}/pedido/item`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${localStorage.getItem("access_token")}`
    },
    body: JSON.stringify({
      item_id: itemId,
      ajuste: ajuste
    })
  });

  const data = await res.json();

  showRaw(data);
  listarCarrinho();
}

// --------------------
// CARRINHO
// --------------------
async function listarCarrinho() {
  if (!pedidoAtual) {
    document.getElementById("carrinho").innerHTML =
      "<p>Crie um pedido primeiro</p>";
    return;
  }

  const res = await fetch(
    `${API}/pedido/item/listar_pedido_temp?pedido_id=${pedidoAtual}`,
    {
      headers: {
        "Authorization": `Bearer ${localStorage.getItem("access_token")}`
      }
    }
  );

  const data = await res.json();

  const itens = data.data?.itens ?? [];

  const container = document.getElementById("carrinho");

  if (itens.length === 0) {
    container.innerHTML = "<p>Carrinho vazio</p>";
    return;
  }

  container.innerHTML = itens.map(item => `
    <div class="carrinho-item">
      <strong>${item.nome}</strong>
      <span>Qtd: ${item.quantidade}</span>
      <span>Tamanho: ${item.tamanho}</span>

      <button onclick="ajustarItem(${item.id}, -1)">
        - remover
      </button>

      <button onclick="ajustarItem(${item.id}, +1)">
        + adicionar
      </button>
    </div>
  `).join("");
}

// --------------------
// FINALIZAR
// --------------------
async function concluirPedido() {
  if (!pedidoAtual) return alert("Nenhum pedido ativo");

  const res = await fetch(`${API}/pedido/concluir`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${localStorage.getItem("access_token")}`
    },
    body: JSON.stringify({ pedido_id: pedidoAtual })
  });

  const data = await res.json();

  showRaw(data);
  pedidoAtual = null;
  atualizarStatus();
  document.getElementById("carrinho").innerHTML = "";
}

// --------------------
// CANCELAR
// --------------------
async function cancelarPedido() {
  if (!pedidoAtual) return alert("Nenhum pedido ativo");

  const res = await fetch(`${API}/pedido/cancelar`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${localStorage.getItem("access_token")}`
    },
    body: JSON.stringify({ pedido_id: pedidoAtual })
  });

  const data = await res.json();

  showRaw(data);
  pedidoAtual = null;
  atualizarStatus();
  document.getElementById("carrinho").innerHTML = "";
}

// --------------------
// INIT
// --------------------
carregarCardapio();
atualizarStatus();