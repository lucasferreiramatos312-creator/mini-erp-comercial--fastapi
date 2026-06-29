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

async function listarProdutosInativos() {

    try {

        const produtos = await api("/produtos/inativos");

        const lista = document.getElementById("listaProdutosInativos");

        lista.innerHTML = "";

        data.dados.forEach(produto => {

            lista.innerHTML += `
        <tr>
            <td>${produto.nome}</td>
            <td>R$ ${produto.valor}</td>
            <td>${produto.estoque}</td>
            
            <td>
                <button onclick="reativarProduto(${produto.id})">Reativar</button>
            </td>
        </tr>`;

        });

    } catch (error) {

        console.log(error)

        mostrarMensagem("Erro ao carregar produtos", "erro");
    }
}

async function reativarProduto(id) {

    try {

        await api(`/produtos/${id}/reativar`, {
            method: "PUT"
        });

        mostrarMensagem("Produto reativado com sucesso", "sucesso");

        listarProdutosInativos();

    } catch (error) {

        console.log(error)

        mostrarMensagem("Erro ao reativar produto", "erro");

    }
}

listarProdutosInativos();