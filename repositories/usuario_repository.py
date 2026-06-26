from database import conectar

def criar_usuario(nome, email, senha_hash):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO usuarios (nome, email, senha)
        VALUES (%s, %s, %s)
    """, (nome, email, senha_hash))

    conexao.commit()
    conexao.close()


def buscar_usuario_por_email(email):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, nome, email, senha
        FROM usuarios
        WHERE email = %s
    """, (email,))

    usuario = cursor.fetchone()

    conexao.close()

    return usuario