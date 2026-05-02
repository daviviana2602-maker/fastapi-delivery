const token = localStorage.getItem("access_token");

const path = window.location.pathname.toLowerCase();

const isPublic =
  path.includes("login.html") ||
  path.includes("register.html");

if (!token && !isPublic) {
  window.location.replace("/pages/login.html");
}