async function registrar() {

    const nome = document.getElementById("nome").value;

    const email = document.getElementById("email").value;

    const senha = document.getElementById("senha").value;

    if (!nome || !email || !senha) {

        mostrarMensagem("Preecha todos os campos", "erro");

        return;
    }

    try {

        const response = await fetch("http://127.0.0.1:8000/auth/registrar",
            {
                method: "POST",
                headers: {
                    "content-Type": "application/json"
                },
                body: JSON.stringify({
                    nome,
                    email,
                    senha
                })
            }
        );

        const data = await response.json()

        if (!response.ok) {

            mostrarMensagem(data.erro || data.detail || "Erro ao cadastrar", "erro");

            return;
        }

        mostrarMensagem("Usuário criado com sucesso", "sucesso");

        setTimeout(() => {

            window.location.href = "login.html";

        }, 1500);

    } catch (error) {

        console.error(error);

        mostrarMensagem("Erro ao conectar com servidor", "erro");

    }

}