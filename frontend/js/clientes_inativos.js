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

async function listaClientesInativos() {

    try {

        const clientes = await api("/clientes/inativos");

        const lista = document.getElementById("listaClientesInativos");

        lista.innerHTML = "";

        clientes.forEach(cliente => {

            lista.innerHTML += `
        <tr>
            <td>${cliente.nome}</td>
            <td>${cliente.email}</td>
            <td>${cliente.telefone}</td>
            
            <td>
                <button onclick="reativarCliente(${cliente.id})">Reativar</button>
            </td>
        </tr>`;

        });

    } catch (error) {

        console.log(error)

        mostrarMensagem("Erro ao carregar clientes", "erro");

    }
}

async function reativarCliente(id) {

    try {

        await api(`/clientes/${id}/reativar`, {
            method: "PUT"
        });

        mostrarMensagem("Cliente reativado com sucesso", "sucesso");

        listaClientesInativos();

    } catch (error) {

        console.log(error)

        mostrarMensagem("Erro ao reativar cliente", "erro")
    }
}

listaClientesInativos();