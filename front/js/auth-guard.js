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
// bloqueio admin page (AQUI)
// --------------------
if (isAdminPage) {

  fetch("http://localhost:8000/auth/me", {
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