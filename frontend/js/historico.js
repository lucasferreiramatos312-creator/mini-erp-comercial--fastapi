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


async function buscarHistorico() {

    const token = localStorage.getItem("token");

    const mes = document.getElementById("mes").value;
    const ano = document.getElementById("ano").value;

    let endpoint = "/vendas/historico";

    if (mes && ano) {
        endpoint += `?mes=${mes}&ano=${ano}`;
    }

    const data = await api(endpoint);

    const tabela = document.getElementById("tabelaHistorico");
    tabela.innerHTML = "";

    data.dados.forEach(v => {
        const dataFormatada = new Date(v.data_venda).toLocaleString();

        tabela.innerHTML += `
                    <tr>
                        <td>${v.id}</td>
                        <td>${v.cliente_nome}</td>
                        <td>R$ ${v.total}</td>
                        <td>${dataFormatada}</td>
                        <td><span class="status ${v.status}">${v.status}</span></td>
                    </tr>
                `;
    });
}

window.onload = buscarHistorico;