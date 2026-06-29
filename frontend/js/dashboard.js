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

        document.getElementById("total_vendas").innerText = "R$ " + data.dados.total_vendas;

        document.getElementById("faturamento").innerText = "R$ " + data.dados.faturamento;

        document.getElementById("recebido").innerText = "R$ " + data.dados.recebido;

        document.getElementById("pendente").innerText = "R$ " + data.dados.pendente;

        document.getElementById("clientes").innerText = data.dados.total_clientes;

        document.getElementById("produtos").innerText = data.dados.total_produtos;

        document.getElementById("ticket").innerText = "R$ " + data.dados.ticket_medio;

    } catch (error) {
        mostrarMensagem("Erro inesperado", "erro");
    }
}

window.onload = carregarDashboard;