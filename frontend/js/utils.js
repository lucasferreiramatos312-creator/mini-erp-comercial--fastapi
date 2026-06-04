function mostrarMensagem(texto, tipo = "sucesso") {
    const mensagem = document.createElement("div");

    mensagem.innerText = texto;

    mensagem.style.position = "fixed";
    mensagem.style.top = "20px";
    mensagem.style.right = "20px";
    mensagem.style.padding = "15px 20px";
    mensagem.style.borderRadius = "8px";
    mensagem.style.color = "white";
    mensagem.style.fontWeight = "bold";
    mensagem.style.zIndex = "9999";

    if (tipo === "erro") {
        mensagem.style.backgroundColor = "#dc2626";
    } else {
        mensagem.style.backgroundColor = "#16a34a";
    }

    document.body.appendChild(mensagem);

    setTimeout(() => {
        mensagem.remove();
    }, 3000);

}