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

function editarCliente(id, nome, email, telefone) {
    document.getElementById("nome").value = nome;
    document.getElementById("email").value = email;
    document.getElementById("telefone").value = telefone;

    window.clienteEditando = id;

    document.getElementById("bntSalvar").innerText = "Atualizar";
}

function cancelarEdicao() {
    window.clienteEditando = null;

    document.getElementById("nome").value = "";
    document.getElementById("email").value = "";
    document.getElementById("telefone").value = "";
    document.getElementById("bntSalvar").innerText = "Salvar";
}

async function criarCliente() {
    const nome = document.getElementById("nome").value.trim();
    const email = document.getElementById("email").value.trim();
    const telefone = document.getElementById("telefone").value.trim();


    if (!nome || !email || !telefone) {
        mostrarMensagem("Preencha todos os campos", "erro");
        return;
    }

    let endpoint = "/clientes/";
    let method = "POST";

    if (window.clienteEditando) {
        endpoint += window.clienteEditando;
        method = "PUT";
    }

    try {

        await api(endpoint, {
            method: method,
            body: JSON.stringify({
                nome,
                email,
                telefone
            })
        });

        mostrarMensagem(window.clienteEditando ?
            "Cliente atualizado com sucesso!" : "Cliente criado com sucesso!", "sucesso");

        window.clienteEditando = null;

        document.getElementById("nome").value = "";
        document.getElementById("email").value = "";
        document.getElementById("telefone").value = "";
        document.getElementById("bntSalvar").innerText = "Salvar";

        buscar();

    } catch (error) {
        mostrarMensagem("Erro ao salvar cliente", "erro");
        console.error(error);
    }
}

async function buscar() {
    const nome = document.getElementById("busca").value.trim();
    const lista = document.getElementById("listar");

    lista.innerHTML = "";

    if (!nome) {
        lista.innerHTML = "<li>Digite um nome para buscar</li>";
        return;
    }

    const data = await api(`/clientes?nome=${nome}`);

    if (!data || data.length === 0) {
        lista.innerHTML = "<li>Nenhum cliente encontrado</li>";
        return;
    }

    data.forEach(c => {
        const tr = document.createElement("tr");
        tr.innerHTML = `<td>${c.nome}</td>
                        <td>${c.email}</td>
                        <td>${c.telefone}</td>
                <td>
                    <button onclick="editarCliente(
                        ${c.id},
                        '${c.nome}',
                        '${c.email}',
                        '${c.telefone}')">Editar</button>
                        
                    <button onclick="inativarCliente(
                        ${c.id})" class="btn-danger">Inativar</button>
                </td>`;

        lista.appendChild(tr);
    });
}

async function inativarCliente(id) {
    const confirmar = confirm("tem certeza que deseja inativar ? Você poderá reativar novamente ");
    if (!confirmar) return;

    try {
        await api(`/clientes/${id}/inativar`, {
            method: "put"
        });

        mostrarMensagem("Cliente inativado com sucesso!", "sucesso");

        buscar();

    } catch (error) {
        mostrarMensagem("Erro ao inativar cliente", "erro");
        console.error(error);
    }
}