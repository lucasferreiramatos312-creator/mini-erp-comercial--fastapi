const token = localStorage.getItem("token");

if (!token) {
    mostrarMensagem("Faça login para acessar", "erro");
    window.location.href = "login.html";
}

function ir(pagina) {
    window.location.href = pagina;
}

function logout() {
    localStorage.removeItem("token");
    window.location.href = "login.html";
}

async function carregarDashboard() {
    try {

        const data = await api("/dashboard");

        document.getElementById("total_vendas").innerText = "R$ " + data.total_vendas;

        document.getElementById("faturamento").innerText = "R$ " + data.faturamento;

        document.getElementById("recebido").innerText = "R$ " + data.recebido;

        document.getElementById("pendente").innerText = "R$ " + data.pendente;

        document.getElementById("clientes").innerText = data.total_clientes;

        document.getElementById("produtos").innerText = data.total_produtos;

        document.getElementById("ticket").innerText = "R$ " + data.ticket_medio;

    } catch (error) {
        mostrarMensagem("Erro inesperado", "erro");
    }
}

window.onload = carregarDashboard;