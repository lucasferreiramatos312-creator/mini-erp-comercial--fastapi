from database import conectar

def criar_usuario(nome, email, senha_hash):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO Usuarios (Nome, Email, DataCadastro, Senha)
        VALUES (?, ?, GETDATE(), ?)
    """, (nome, email, senha_hash))

    conexao.commit()
    conexao.close()


def buscar_usuario_por_email(email):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT Id, Nome, Email, Senha
        FROM Usuarios
        WHERE Email = ?
    """, (email,))

    usuario = cursor.fetchone()

    conexao.close()

    return usuario