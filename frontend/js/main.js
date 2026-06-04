const token = localStorage.getItem("token");

if (!token) {
    mostrarMensagem("Faça login", "erro");
    window.location.href = "login.html";
}

function ir(pagina) {
    window.location.href = pagina;
}

function logout() {
    localStorage.removeItem("token");
    window.location.href = "login.html";
}