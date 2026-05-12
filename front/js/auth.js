var AUTH_API = API_BASE + "/auth";

// --------------------
// TRADUÇÃO DE ERROS
// --------------------
function traduzirErro(msg) {
  if (!msg) return "Erro desconhecido";

  const lower = msg.toLowerCase();

  // erros reais de email inválido vindos do Pydantic
  if (
    lower === "value is not a valid email address" ||
    lower.includes("value is not a valid email address") ||
    lower.includes("an email address must have an @-sign")
  ) {
    return "Informe um endereço de email válido.";
  }

  return msg;
}

// --------------------
// FETCH USER (/me)
// --------------------
async function fetchUser() {
  const token = getToken();
  if (!token) return;

  try {
    const res = await fetch(`${AUTH_API}/me`, {
      method: "GET",
      headers: { "Authorization": "Bearer " + token }
    });

    const data = await res.json().catch(() => null);
    if (!res.ok || !data) return;

    const user = data?.data ?? data;
    localStorage.setItem("user", JSON.stringify(user));

  } catch (err) {
    console.log("Erro /me:", err);
  }
}

// --------------------
// LOGIN
// --------------------
async function login() {
  const email = document.getElementById("email").value.trim();
  const senha = document.getElementById("senha").value;
  const errorBox = document.getElementById("errorBox");
  errorBox.innerHTML = "";

  if (!email || !senha) {
    errorBox.innerHTML = `<div class="error-msg">Preencha email e senha</div>`;
    return;
  }

  let res, data;

  try {
    res = await fetch(`${AUTH_API}/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, senha })
    });
    data = await res.json().catch(() => null);
  } catch (err) {
    errorBox.innerHTML = `<div class="error-msg">Erro de conexão</div>`;
    return;
  }

  if (!res.ok) {
    errorBox.innerHTML = `<div class="error-msg">${traduzirErro(parseError(data))}</div>`;
    return;
  }

  const token = data?.data?.access_token;
  if (!token) {
    errorBox.innerHTML = `<div class="error-msg">Token não recebido</div>`;
    console.log("RESPOSTA BRUTA:", data);
    return;
  }

  localStorage.setItem("access_token", token);
  localStorage.setItem("refresh_token", data.data.refresh_token);

  await fetchUser();

  showMsg("Login realizado com sucesso");
  window.location.href = "/pages/dashboard.html";
}

// --------------------
// REGISTER
// --------------------
async function register() {
  const nome  = document.getElementById("nome").value.trim();
  const email = document.getElementById("email").value.trim();
  const senha = document.getElementById("senha").value;

  if (!nome || !email || !senha) {
    showMsg("Preencha todos os campos", "error");
    return;
  }

  try {
    const res = await fetch(`${AUTH_API}/criar_conta`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ nome, email, senha })
    });

    const data = await res.json().catch(() => null);

    if (!res.ok) {
      showMsg(traduzirErro(parseError(data)), "error");
      return;
    }

    showMsg("Conta criada com sucesso");
    document.getElementById("nome").value  = "";
    document.getElementById("email").value = "";
    document.getElementById("senha").value = "";

    setTimeout(() => { window.location.href = "login.html"; }, 1200);

  } catch (err) {
    showMsg("Erro de conexão", "error");
  }
}