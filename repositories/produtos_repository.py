from database import conectar

def criar_produto(nome, valor, estoque, usuario_id):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO produtos (nome, valor, estoque, usuario_id)
        VALUES (%s, %s, %s, %s)
        RETURNING id
    """, (nome, valor, estoque, usuario_id))

    produto_id = cursor.fetchone()[0]

    conexao.commit()
    conexao.close()

    return produto_id

def listar_produtos(usuario_id):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, nome, valor, estoque, ativo
        FROM produtos
        WHERE usuario_id = %s AND ativo = TRUE
    """, (usuario_id,))

    produtos = cursor.fetchall()

    conexao.close()

    return produtos

def buscar_produto_por_id_geral(id, usuario_id):

    conexao = conectar()
    cursor = conexao.cursor()
    
    cursor.execute("""
                   SELECT id, nome, valor, estoque, ativo
                   FROM produtos
                   WHERE id = %s AND usuario_id = %s
                   """, (id, usuario_id))
    
    produto = cursor.fetchone()

    conexao.close()

    return produto

def buscar_produto_por_id(id, usuario_id):

    conexao = conectar()
    cursor = conexao.cursor()
    
    cursor.execute("""
                   SELECT id, nome, valor, estoque, ativo
                   FROM produtos
                   WHERE id = %s AND usuario_id = %s AND ativo = TRUE
                   """, (id, usuario_id))
    
    produto = cursor.fetchone()

    conexao.close()

    return produto

def buscar_produto_por_nome(nome, usuario_id):

        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("""
                       SELECT id, nome, valor, estoque, ativo
                       FROM produtos
                       WHERE usuario_id = %s AND nome ILIKE %s AND ativo = TRUE
                       """, (usuario_id, f'%{nome}%'))
        
        produtos = cursor.fetchall()
        conexao.close()

        return produtos


def atualizar_produto(id, nome, valor, estoque, usuario_id):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE produtos
        SET nome = %s, valor = %s, estoque = %s
        WHERE id = %s AND usuario_id = %s
    """, (nome, valor, estoque, id, usuario_id))

    conexao.commit()
    conexao.close()

def listar_produtos_inativos(usuario_id):
     
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, nome, valor, estoque, ativo
        FROM produtos
        WHERE usuario_id = %s AND ativo = FALSE
    """, (usuario_id,))

    produtos = cursor.fetchall()

    conexao.close()

    return produtos

def inativar_produto(id, usuario_id):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
                   UPDATE produtos
                   SET ativo = FALSE
                   WHERE id = %s AND usuario_id = %s
                   """,(id, usuario_id))

    conexao.commit()

    cursor.execute("""
                   SELECT id, nome, valor, estoque, ativo
                   FROM produtos 
                   WHERE id = %s AND usuario_id = %s
                   """, (id,usuario_id))
    
    produto = cursor.fetchone()

    conexao.close()

    return produto

def reativar_produto(id, usuario_id):
     
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
                   UPDATE produtos
                   SET ativo = TRUE
                   WHERE id = %s AND usuario_id = %s
                   """, (id, usuario_id))
    
    conexao.commit()

    cursor.execute("""
                   SELECT id, nome, valor, estoque, ativo
                   FROM produtos 
                   WHERE id = %s AND usuario_id = %s
                   """, (id,usuario_id))

    produto_reativado = cursor.fetchone()

    conexao.close()

    return produto_reativado