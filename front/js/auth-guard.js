const token = localStorage.getItem("access_token");

if (!token) {
  window.location.replace("/pages/login.html");
}