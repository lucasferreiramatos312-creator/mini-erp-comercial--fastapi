async function login() {

    const email = document.getElementById("email").value;
    const senha = document.getElementById("senha").value;

    if (!email || !senha) {
        mostrarMensagem("Preencha todos os campos", "erro");
        return;
    }

    try {
        const response = await fetch("https://mini-erp-comercial-fastapi.onrender.com/auth/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ email, senha })
        });

        const data = await response.json();

        if (!response.ok) {
            mostrarMensagem(data.detail || "Erro ao fazer login", "erro");
            return;
        }


        localStorage.setItem("token", data.dados.access_token);

        mostrarMensagem("Login bem-sucedido!", "sucesso");

        window.location.href = "home.html";

    } catch (error) {
        console.error(error);
        mostrarMensagem("Erro na conexão com o servidor", "erro");
    }

}