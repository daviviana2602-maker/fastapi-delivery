var PROFILE_API = API_BASE + "/profile";

// --------------------
// EDITAR PERFIL
// --------------------
async function editarPerfil() {
  const body = {
    nome:        document.getElementById("nome").value || null,
    email:       document.getElementById("email").value || null,
    senha_atual: document.getElementById("senhaAtual").value || null,
    senha:       document.getElementById("novaSenha").value || null
  };

  const data = await request(`${PROFILE_API}/editar_perfil`, {
    method: "PATCH",
    headers: authHeaders(),
    body: JSON.stringify(body)
  });

  if (!data) return;

  if (data.success) {
    showMsg("Perfil atualizado com sucesso");
    document.getElementById("senhaAtual").value = "";
    document.getElementById("novaSenha").value  = "";
  } else {
    showMsg(data.detail || "Erro ao atualizar perfil", "error");
  }
}

// --------------------
// EXCLUIR CONTA
// --------------------
async function excluirConta() {
  if (!confirm("Tem certeza que quer excluir sua conta?")) return;

  const senha = document.getElementById("senhaExcluir").value.trim();
  if (!senha) {
    showMsg("Informe sua senha", "error");
    return;
  }

  const data = await request(
    `${PROFILE_API}/excluir_conta?senha_atual=${encodeURIComponent(senha)}`,
    { method: "DELETE", headers: authHeaders() }
  );

  if (!data) return;

  if (data.success) {
    showMsg(data.msg || "Conta excluída com sucesso");
    localStorage.removeItem("access_token");
    setTimeout(() => { window.location.href = "login.html"; }, 1200);
  } else {
    showMsg(data.msg || "Erro ao excluir conta", "error");
  }
}