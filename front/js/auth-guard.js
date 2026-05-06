// ============================================================
// auth-guard.js — proteção de rotas
// Depende de: config.js (API_BASE, getToken)
// ============================================================

var _token = localStorage.getItem("access_token");
var _path  = window.location.pathname.toLowerCase();

var _isPublic   = _path.includes("login.html") || _path.includes("register.html");
var _isAdminPage = _path.includes("management.html");

// --------------------
// Bloqueia páginas privadas
// --------------------
if (!_token && !_isPublic) {
  window.location.replace("/pages/login.html");
}

// --------------------
// Bloqueia página admin
// --------------------
if (_isAdminPage) {
  fetch(`${API_BASE}/auth/me`, {
    headers: { "Authorization": "Bearer " + _token }
  })
  .then(res => res.json())
  .then(data => {
    var user = data?.data ?? data;
    if (!user.admin) {
      alert("Acesso negado");
      window.location.replace("/pages/dashboard.html");
    }
  })
  .catch(() => {
    window.location.replace("/pages/login.html");
  });
}