from database import conectar

def criar_produto(nome, valor, estoque, usuario_id):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO produtos (nome, valor, estoque, usuario_id)
        OUTPUT INSERTED.id
        VALUES (?, ?, ?, ?)
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
        WHERE usuario_id = ? AND ativo = 1
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
                   WHERE id = ? AND usuario_id = ?
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
                   WHERE id = ? AND usuario_id = ? AND ativo = 1
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
                       WHERE usuario_id = ? AND nome LIKE ? AND ativo = 1
                       """, (usuario_id, f'%{nome}%'))
        
        produtos = cursor.fetchall()
        conexao.close()

        return produtos


def atualizar_produto(id, nome, valor, estoque, usuario_id):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE produtos
        SET nome = ?, valor = ?, estoque = ?
        WHERE id = ? AND usuario_id = ?
    """, (nome, valor, estoque, id, usuario_id))

    conexao.commit()
    conexao.close()

def produto_tem_vendas(produto_id):
     
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
                   SELECT COUNT(*)
                   FROM itens_venda
                   WHERE produto_id = ?
                   """, (produto_id,))
    
    total = cursor.fetchone()[0]

    conexao.close()

    return total > 0

def listar_produtos_inativos(usuario_id):
     
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, nome, valor, estoque, ativo
        FROM produtos
        WHERE usuario_id = ? AND ativo = 0
    """, (usuario_id,))

    produtos = cursor.fetchall()

    conexao.close()

    return produtos

def inativar_produto(id, usuario_id):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
                   UPDATE produtos
                   SET ativo = 0
                   WHERE id = ? AND usuario_id = ?
                   """,(id, usuario_id))

    conexao.commit()

    cursor.execute("""
                   SELECT id, nome, valor, estoque, ativo
                   FROM produtos 
                   WHERE id = ? AND usuario_id = ?
                   """, (id,usuario_id))
    
    produto = cursor.fetchone()

    conexao.close()

    return produto

def reativar_produto(id, usuario_id):
     
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
                   UPDATE produtos
                   SET ativo = 1
                   WHERE id = ? AND usuario_id = ?
                   """, (id, usuario_id))
    
    conexao.commit()

    cursor.execute("""
                   SELECT id, nome, valor, estoque, ativo
                   FROM produtos 
                   WHERE id = ? AND usuario_id = ?
                   """, (id,usuario_id))

    produto_reativado = cursor.fetchone()

    conexao.close()

    return produto_reativado