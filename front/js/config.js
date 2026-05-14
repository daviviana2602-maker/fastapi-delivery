var API_BASE =
  window.location.hostname === "localhost"
    ? "http://localhost:8000"
    : "https://fastapi-delivery-wwlo-production.up.railway.app";

// --------------------
// MSG GLOBAL
// --------------------
function showMsg(text, type = "success") {
  let el = document.getElementById("msg");

  if (!el) {
    el = document.createElement("div");
    el.id = "msg";
    document.querySelector(".card")?.prepend(el);
  }

  el.innerHTML = `
    <div style="
      margin-top:10px;
      padding:10px;
      border-radius:10px;
      font-size:13px;
      color:white;
      background:${type === "success" ? "#22c55e" : "#ef4444"};
    ">${text}</div>
  `;
}

// --------------------
// PARSE ERRO FASTAPI
// --------------------
function parseError(data) {
  if (!data) return "Erro desconhecido";
  if (typeof data === "string") return data;
  if (Array.isArray(data.detail)) return data.detail.map(e => e.msg).join(", ");
  if (data.detail) return data.detail;
  if (data.msg) return data.msg;
  return JSON.stringify(data);
}

// --------------------
// AUTH HELPERS
// --------------------
function getToken() {
  return localStorage.getItem("access_token");
}

function authHeaders() {
  return {
    "Content-Type": "application/json",
    "Authorization": `Bearer ${getToken()}`
  };
}

function getUser() {
  try {
    return JSON.parse(localStorage.getItem("user"));
  } catch {
    return null;
  }
}

function isAdmin() {
  return getUser()?.admin === true;
}

// --------------------
// REQUEST SAFE
// --------------------
async function request(url, options) {
  try {
    const res = await fetch(url, options);
    const text = await res.text();

    let data;
    try {
      data = JSON.parse(text);
    } catch {
      console.error("INVALID JSON:", text);
      showMsg("Erro inesperado do servidor", "error");
      return null;
    }

    if (!res.ok) {
      console.error("API ERROR:", res.status, data);
      showMsg(parseError(data), "error");
      return null;
    }

    return data;

  } catch (err) {
    console.error("NETWORK ERROR:", err);
    showMsg("Erro de rede", "error");
    return null;
  }
}