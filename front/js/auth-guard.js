console.log("GUARD RODANDO");

const token = localStorage.getItem("access_token");

console.log("TOKEN NO GUARD:", token);

if (!token) {
  console.log("SEM TOKEN -> REDIRECIONANDO");
  window.location.replace("/pages/login.html");
}