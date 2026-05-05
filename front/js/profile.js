const API_BASE =
  window.location.hostname === "localhost"
    ? "http://localhost:8000"
    : "https://fastapi-delivery.up.railway.app";

const API = `${API_BASE}/profile`;

function showMsg(text, type = "success") {
  const el = document.getElementById("msg");

  el.innerHTML = `
    <div style="
      margin-top:10px;
      padding:10px;
      border-radius:10px;
      font-size:13px;
      color:white;
      background:${type === "success" ? "#22c55e" : "#ef4444"};
    ">
      ${text}
    </div>
  `;
}

// --------------------
// EDITAR PERFIL
// --------------------
async function editarPerfil() {

  const body = {
    nome: document.getElementById("nome").value || null,
    email: document.getElementById("email").value || null,
    senha_atual: document.getElementById("senhaAtual").value || null,
    senha: document.getElementById("novaSenha").value || null
  };

  const res = await fetch(`${API}/editar_perfil`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${localStorage.getItem("access_token")}`
    },
    body: JSON.stringify(body)
  });

  const data = await res.json();

  if (data.success) {
    showMsg("Perfil atualizado com sucesso");

    document.getElementById("senhaAtual").value = "";
    document.getElementById("novaSenha").value = "";
  } else {
    showMsg(data.detail || "Erro ao atualizar perfil", "error");
  }
}

// --------------------
// EXCLUIR CONTA
// --------------------
async function excluirConta() {

  const confirmar = confirm("Tem certeza que quer excluir sua conta?");
  if (!confirmar) return;

  const senha = document.getElementById("senhaExcluir").value.trim();

  if (!senha) {
    showMsg("Informe sua senha", "error");
    return;
  }

  const res = await fetch(
    `${API}/excluir_conta?senha_atual=${encodeURIComponent(senha)}`,
    {
      method: "DELETE",
      headers: {
        "Authorization": `Bearer ${localStorage.getItem("access_token")}`
      }
    }
  );

  const data = await res.json();

  if (data.success) {
    showMsg(data.msg || "Conta excluída com sucesso");

    localStorage.removeItem("access_token");

    setTimeout(() => {
      window.location.href = "login.html";
    }, 1200);

  } else {
    showMsg(data.msg || "Erro ao excluir conta", "error");
  }
}