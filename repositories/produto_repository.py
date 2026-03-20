from database import conectar


def listar_produtos(id_usuario: int):

    conexao = conectar()
    cursor = conexao.cursor()

    query = """
        SELECT 
            p.Id,
            u.Nome,
            p.NomeProduto,
            p.Valor
        FROM Produtos p
        JOIN Usuarios u ON p.IdUsuario = u.Id
        WHERE p.IdUsuario = ?
    """

    cursor.execute(query, (id_usuario,))

    produtos = cursor.fetchall()

    conexao.close()

    return produtos


def buscar_produto(id):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT Produtos.Id, Usuarios.Nome,
        Produtos.NomeProduto, Produtos.Valor, IdUsuario
        FROM Produtos
        JOIN Usuarios ON Produtos.IdUsuario = Usuarios.Id
        WHERE Produtos.Id = ?
    """, (id,))

    produto = cursor.fetchone()

    conexao.close()

    return produto


def criar_produto(nome_produto, valor, id_usuario):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO Produtos (NomeProduto, Valor, IdUsuario)
        VALUES (?, ?, ?)
    """, (nome_produto, valor, id_usuario))

    conexao.commit()
    conexao.close()


def atualizar_produto(id, nome_produto, valor, id_usuario):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE Produtos
        SET NomeProduto = ?, Valor = ?, IdUsuario = ?
        WHERE Id = ?
    """, (nome_produto, valor, id_usuario, id))

    conexao.commit()
    conexao.close()


def deletar_produto(id):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "DELETE FROM Produtos WHERE Id = ?",
        (id,)
    )

    conexao.commit()
    conexao.close()