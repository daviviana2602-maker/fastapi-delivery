const token = localStorage.getItem("access_token");

const path = window.location.pathname.toLowerCase();

const isPublic =
  path.includes("login.html") ||
  path.includes("register.html");

const isAdminPage =
  path.includes("management.html");

// --------------------
// bloqueio login
// --------------------
if (!token && !isPublic) {
  window.location.replace("/pages/login.html");
}

// --------------------
// bloqueio admin page
// --------------------
if (isAdminPage) {

  const API_URL =
    window.location.hostname === "localhost"
      ? "http://localhost:8000"
      : "https://fastapi-delivery-production.up.railway.app";

  fetch(`${API_URL}/auth/me`, {
    headers: {
      "Authorization": "Bearer " + token
    }
  })
  .then(res => res.json())
  .then(user => {

    if (!user.admin) {
      alert("Acesso negado");
      window.location.replace("/pages/dashboard.html");
    }

  })
  .catch(() => {
    window.location.replace("/pages/login.html");
  });
}