const API = "http://localhost:8000/order";

let pedidoAtual = null;

// --------------------
// UTIL: STATUS
// --------------------
function atualizarStatus() {
  const el = document.getElementById("statusPedido");

  el.innerHTML = pedidoAtual
    ? `<strong>ID:</strong> ${pedidoAtual}`
    : "Nenhum pedido ativo";
}

// --------------------
// UTIL: DEBUG RAW
// --------------------
function showRaw(data) {
  document.getElementById("out").innerText =
    JSON.stringify(data, null, 2);
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

  pedidoAtual = data.data.id;

  atualizarStatus();
  showRaw(data);
}

// --------------------
// ADICIONAR ITEM
// --------------------
async function adicionarItem(nome, qtyId, sizeId) {
  if (!pedidoAtual) {
    alert("Crie um pedido primeiro");
    return;
  }

  const quantidade = Number(document.getElementById(qtyId).value);
  let tamanho = document.getElementById(sizeId).value;

  if (!quantidade || !tamanho) {
    alert("Preencha quantidade e tamanho");
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
          <input id="${qtyId}" type="number" placeholder="Qtd">

          <div class="select-wrapper">
            <select id="${sizeId}">
              <option value="">Tamanho</option>
              <option value="pequeno">Pequeno</option>
              <option value="tradicional">Tradicional</option>
              <option value="grande">Grande</option>
            </select>
          </div>

          <button onclick="adicionarItem('${item.nome}', '${qtyId}', '${sizeId}')">
            Adicionar
          </button>
        </div>

      </div>
    `;
  }).join("");
}

// --------------------
// CARRINHO (BONITO AGORA)
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

  console.log("DEBUG CARRINHO:", data);

  // AQUI tá o fix real
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
}

// INIT
carregarCardapio();
atualizarStatus();