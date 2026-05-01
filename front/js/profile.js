const API = "http://localhost:8000/profile";

function show(data) {
  document.getElementById("out").innerText =
    JSON.stringify(data, null, 2);
}


// EDITAR PERFIL
async function editarPerfil() {

  const res = await fetch(`${API}/editar_perfil`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${localStorage.getItem("access_token")}`
    },
    body: JSON.stringify({
      nome: nome.value || null,
      email: email.value || null,
      senha_atual: senhaAtual.value || null,
      senha: novaSenha.value || null
    })
  });

  const data = await res.json();
  show(data);
}


// EXCLUIR CONTA
async function excluirConta() {

  const confirmar = confirm("Tem certeza que quer excluir sua conta?");
  if (!confirmar) return;

  const res = await fetch(`${API}/excluir_conta?senha_atual=${senhaExcluir.value}`, {
    method: "DELETE",
    headers: {
      "Authorization": `Bearer ${localStorage.getItem("access_token")}`
    }
  });

  const data = await res.json();
  show(data);

  if (data.success) {
    localStorage.removeItem("access_token");
    alert("Conta excluída. Redirecionando...");
    window.location.href = "login.html";
  }
}