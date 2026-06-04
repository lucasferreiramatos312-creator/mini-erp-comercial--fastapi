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

let vendaAtual = null;
let itensVenda = [];

async function carregarClientes() {

    const data = await api("/clientes")

    const select = document.getElementById("clientes");

    data.forEach(c => {
        select.innerHTML += `<option value="${c.id}">${c.nome}</option>`;
    });
}

async function carregarProdutos() {

    const data = await api("/produtos/");

    const select = document.getElementById("produtos");

    data.forEach(p => {
        select.innerHTML += `<option value="${p.id}">${p.nome} - R$ ${p.valor}</option>`;
    });
}

function adcionarItem() {

    const selectProduto = document.getElementById("produtos");
    const produto_id = parseInt(selectProduto.value);
    const produto_nome = selectProduto.options[selectProduto.selectedIndex].text;
    const quantidade = parseInt(document.getElementById("quantidade").value);

    if (isNaN(quantidade) || quantidade <= 0) {
        mostrarMensagem("Quantidade inválida", "erro");
        return;
    }

    itensVenda.push({
        produto_id,
        produto_nome,
        quantidade
    });

    renderizarItens();

    document.getElementById("quantidade").value = "";
}

function renderizarItens() {
    const lista = document.getElementById("listaItens");
    lista.innerHTML = "";

    itensVenda.forEach((item, index) => {

        const li = document.createElement("li");

        li.innerHTML = `${item.produto_nome} - Quantidade: ${item.quantidade}
                <button onclick="removerItem(${index})">Remover</button>`;

        lista.appendChild(li);
    });
}

function removerItem(index) {
    itensVenda.splice(index, 1);
    renderizarItens();
}

async function finalizarVenda() {

    const cliente_id = document.getElementById("clientes").value;

    if (itensVenda.length === 0) {
        mostrarMensagem("Adicione pelo menos um item", "erro");
        return;
    }

    try {

        await api("/vendas/", {
            method: "POST",
            body: JSON.stringify({
                cliente_id: parseInt(cliente_id),
                itens: itensVenda.map(item => ({
                    produto_id: item.produto_id,
                    quantidade: item.quantidade
                }))
            })
        });

        mostrarMensagem("Venda criada com sucesso!", "sucesso")

        itensVenda = [];
        renderizarItens();
        listarVendas();

    } catch (error) {

        mostrarMensagem("Erro ao criar venda", "erro");
    }

}

async function listarVendas() {

    const data = await api("/vendas/")

    const tabela = document.getElementById("tabelaVendas");
    tabela.innerHTML = "";

    data.forEach(v => {
        const dataFormatada = new Date(v.data_venda).toLocaleString();

        tabela.innerHTML += `
                    <tr>
                        <td>${v.id}</td>
                        <td>${v.cliente_nome}</td>
                        <td>${v.total}</td>
                        <td>${dataFormatada}</td>
                        <td><span class="status ${v.status}">${v.status}</span></td>
                        <td><button onclick="verDetalhes(${v.id})">Detalhes</button>
                            <button class="btn-danger" onclick="excluirVenda(${v.id})">Excluir</button></td>
                    </tr>`;
    });
}

async function verDetalhes(id) {

    console.log("clicou detalhes", id);

    const data = await api(`/vendas/${id}`)

    vendaAtual = id;

    let html = `
                Cliente: ${data.venda.cliente_nome}<br>
                Total: R$ ${data.venda.total}<br>
                Pago: R$ ${data.total_pago}<br>
                Status: ${data.status}<br><br>
                <b>Itens:</b><br>
                `;

    data.itens.forEach(i => {
        html += `${i.produto_nome} - ${i.quantidade}x (R$ ${i.valor_unitario})
                
                <button onclick="editarItem(${i.produto_id}, ${i.quantidade})">Editar</button>
                <br>`;
    });

    document.getElementById("detalhes").innerHTML = html;
    document.getElementById("modal").style.display = "flex";
}

function fecharModal() {
    document.getElementById("modal").style.display = "none";
}

async function pagar() {

    const valor = document.getElementById("valorPagamento").value;

    try {

        await api(`/vendas/${vendaAtual}/pagamentos`, {
            method: "POST",
            body: JSON.stringify({ valor_pago: parseFloat(valor) })
        });

        mostrarMensagem("Pagamento registrado com sucesso!", "sucesso");

        fecharModal();
        listarVendas();

    } catch (error) {
        mostrarMensagem("Erro ao processar pagamento", "erro");
    }
}

async function fecharMes() {

    const confirmar = confirm("Deseja fechar o caixa do mês?");

    if (!confirmar) return;

    try {

        await api("/vendas/fechar-mes", {
            method: "POST"
        });

        mostrarMensagem("Mês fechado com sucesso!", "sucesso");

        listarVendas();

    } catch (error) {

        mostrarMensagem("Erro ao fechar o mês", "erro");
    }
}

async function editarItem(produto_id, quantidadeAtual) {

    const novaQuantidade = prompt("Digite a nova quantidade:", quantidadeAtual);

    if (novaQuantidade === null) {
        return;
    }

    const quantidade = parseInt(novaQuantidade);

    if (isNaN(quantidade) || quantidade <= 0) {
        mostrarMensagem("Quantidade inválida", "erro");
        return;
    }

    try {

        await api(`/vendas/${vendaAtual}
            /itens/${produto_id}?quantidade=
            ${quantidade}`, {
            method: "PUT",
        });

        mostrarMensagem("Item atualizado com sucesso!", "sucesso");

        verDetalhes(vendaAtual);

        listarVendas();

    } catch (error) {
        mostrarMensagem("Erro ao atualizar item", "erro");
    }

}

async function excluirVenda(id) {

    const confirmar = confirm("Tem certeza que deseja excluir esta venda?")
    if (!confirmar) {
        return;
    }

    try {

        await api(`/vendas/${id}`, {
            method: "DELETE",
        });

        mostrarMensagem("Venda excluída com sucesso!", "sucesso");

        listarVendas();

    } catch (error) {
        mostrarMensagem("Erro ao excluir venda", "erro");
    }
}

window.onload = () => {
    carregarClientes();
    carregarProdutos();
    listarVendas();
};