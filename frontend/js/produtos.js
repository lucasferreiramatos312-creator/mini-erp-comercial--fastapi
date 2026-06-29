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

function renderizarProdutos(data) {
    const lista = document.getElementById("listaProdutos");
    lista.innerHTML = "";

    data.dados.forEach(p => {
        const tr = document.createElement("tr");

        tr.innerHTML = `
            <td>${p.nome}</td>
            <td>R$ ${p.valor.toFixed(2)}</td>
            <td>${p.estoque}</td>
            <td>
                <button onclick="editarProduto(
                ${p.id},
                '${p.nome}',
                ${p.valor},
                ${p.estoque})">Editar</button>
                <button  class="btn-danger" 
                onclick="inativarProduto(${p.id})">Inativar</button>
                `;

        lista.appendChild(tr);
    });
}

function editarProduto(id, nome, valor, estoque) {

    document.getElementById("nomeProduto").value = nome;
    document.getElementById("preco").value = valor;
    document.getElementById("estoque").value = estoque

    window.produtoEditando = id;

    document.getElementById("btnSalvar").innerText = "Atualizar";
}

function cancelarEdicao() {
    window.produtoEditando = null;

    document.getElementById("nomeProduto").value = "";
    document.getElementById("preco").value = "";
    document.getElementById("estoque").value = "";
    document.getElementById("btnSalvar").innerText = "Salvar";

}

async function criarProduto() {
    const nome = document.getElementById("nomeProduto").value.trim();
    const preco = parseFloat(document.getElementById("preco").value);
    const estoque = parseInt(document.getElementById("estoque").value);

    if (!nome || isNaN(preco) || isNaN(estoque)) {
        mostrarMensagem("Preencha todos os campos corretamente", "erro");
        return;
    }


    let endpoint = "/produtos/";
    let method = "POST";

    if (window.produtoEditando) {
        endpoint += window.produtoEditando;
        method = "PUT";
    }

    try {

        await api(endpoint, {
            method: method,
            body: JSON.stringify({
                nome: nome,
                valor: preco,
                estoque: estoque
            })
        });

        mostrarMensagem(window.produtoEditando ? "Produto atualizado!" : "Produto criado!", "sucesso");

        window.produtoEditando = null;

        document.getElementById("nomeProduto").value = "";
        document.getElementById("preco").value = "";
        document.getElementById("estoque").value = "";
        document.getElementById("btnSalvar").innerText = "Salvar";

        listarProdutos();

    } catch (error) {
        mostrarMensagem("Erro ao salvar produto", "erro");
        console.error(error);

        listarProdutos();
    }
}

async function listarProdutos() {

    const data = await api("/produtos");
    renderizarProdutos(data);
}

async function buscarProduto() {
    const nome = document.getElementById("buscarProduto").value.trim();

    const data = await api(`/produtos?nome=${nome}`);
    renderizarProdutos(data);
}

async function inativarProduto(id) {
    const confirmar = confirm("tem certeza que deseja inativar ? Você poderá reativar novamente ");
    if (!confirmar) return;

    try {
        await api(`/produtos/${id}/inativar`, {
            method: "PUT"
        });

        mostrarMensagem("Produto inativado com sucesso!", "sucesso");

        listarProdutos();

    } catch (error) {
        mostrarMensagem("Erro ao inativar produto", "erro");
        console.error(error);
    }

}