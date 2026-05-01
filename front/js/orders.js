const API = "http://localhost:8000/order";

let pedidoAtual = null;

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
  show(data);
}

// --------------------
// ADICIONAR ITEM (manual)
// --------------------
async function adicionarItem(nome) {
  if (!pedidoAtual) {
    alert("Crie um pedido primeiro");
    return;
  }

  const quantidade = Number(document.getElementById("quantidade").value);
  const tamanho = document.getElementById("tamanho").value;

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
      nome: nome,
      quantidade: quantidade,
      tamanho: tamanho
    })
  });

  const data = await res.json();

  console.log(data); // IMPORTANTE PRA DEBUG
  show(data);
}


// --------------------
// ADICIONAR PELO CARDÁPIO
// --------------------
function addDoCardapio(nome) {
  document.getElementById("nome").value = nome;
}

// --------------------
// LISTAR CARRINHO
// --------------------
async function listarCarrinho() {
  const res = await fetch(`${API}/pedido/item/listar_pedido_temp?pedido_id=${pedidoAtual}`, {
    method: "GET",
    headers: {
      "Authorization": `Bearer ${localStorage.getItem("access_token")}`
    }
  });

  const data = await res.json();

  show(data);
}

// --------------------
// CARREGAR CARDÁPIO
// --------------------
async function carregarCardapio() {
  const res = await fetch(`${API}/cardapio`);
  const data = await res.json();

  const container = document.getElementById("cardapio");

  container.innerHTML = data.data.map(item => `
    <div style="margin-bottom: 8px;">
      <strong>${item.nome}</strong> - ${item.categoria} - R$ ${item.preco}
      <button onclick="adicionarItem('${item.nome}')">Adicionar</button>
    </div>
  `).join("");
}


// --------------------
// STATUS NA TELA
// --------------------
function atualizarStatus() {
  const el = document.getElementById("statusPedido");

  el.innerHTML = `
    <p><strong>Pedido atual:</strong> ${pedidoAtual ?? "nenhum"}</p>
  `;
}

// --------------------
// DEBUG OUTPUT
// --------------------
function show(data) {
  document.getElementById("out").innerText =
    JSON.stringify(data, null, 2);
}

// --------------------
// INIT
// --------------------
carregarCardapio();



// --------------------
// CONCLUIR PEDIDO
// --------------------
async function concluirPedido() {
  if (!pedidoAtual) {
    alert("Nenhum pedido ativo");
    return;
  }

  const res = await fetch(`${API}/pedido/concluir`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${localStorage.getItem("access_token")}`
    },
    body: JSON.stringify({
      pedido_id: pedidoAtual
    })
  });

  const data = await res.json();

  show(data);
  pedidoAtual = null; // limpa pedido atual
  atualizarStatus();
}



// --------------------
// CANCELAR PEDIDO
// --------------------
async function cancelarPedido() {
  if (!pedidoAtual) {
    alert("Nenhum pedido ativo");
    return;
  }

  const res = await fetch(`${API}/pedido/cancelar`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${localStorage.getItem("access_token")}`
    },
    body: JSON.stringify({
      pedido_id: pedidoAtual
    })
  });

  const data = await res.json();

  show(data);
  pedidoAtual = null;
  atualizarStatus();
}