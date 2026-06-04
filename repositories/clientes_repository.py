from database import conectar

def criar_cliente(nome, email, telefone, usuario_id):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO clientes (nome, email, telefone, usuario_id)
        OUTPUT INSERTED.id
        VALUES (?, ?, ?, ?)
    """, (nome, email, telefone, usuario_id))

    cliente_id = cursor.fetchone()[0]

    conexao.commit()
    conexao.close()

    return cliente_id

def listar_clientes(usuario_id):
    
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, nome, email, telefone, ativo
        FROM clientes
        WHERE usuario_id = ? AND ativo = 1
    """, (usuario_id,))

    clientes = cursor.fetchall()
    
    conexao.close()

    return clientes


def buscar_cliente_por_id_geral(id, usuario_id):

    conexao = conectar()
    cursor = conexao.cursor()
    
    cursor.execute("""
                   SELECT id, nome, email, telefone, ativo
                   FROM clientes
                   WHERE id = ? AND usuario_id = ?
                   """, (id, usuario_id))
    
    cliente =  cursor.fetchone()

    conexao.close()

    return cliente

def buscar_cliente_por_id(cliente_id, usuario_id):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
                   SELECT id, nome, email, telefone, ativo
                   FROM clientes
                   WHERE id = ? AND usuario_id = ? AND ativo = 1
                   """, (cliente_id, usuario_id))
    
    cliente = cursor.fetchone()

    conexao.close()

    return cliente

def buscar_cliente_por_nome(nome, usuario_id):
    
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
                   SELECT id, nome, email, telefone, ativo
                   FROM clientes
                   WHERE usuario_id = ? AND nome LIKE ? AND ativo = 1
                   """, (usuario_id, f'%{nome}%')) 

    clientes = cursor.fetchall()
    conexao.close()

    return clientes

def atualizar_cliente(id, nome, email, telefone, usuario_id):
    
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
                  UPDATE clientes
                  SET nome = ?, email = ?, telefone = ?
                  WHERE id = ? AND usuario_id = ?
                   """, (nome, email, telefone, id, usuario_id))
    
    conexao.commit()
    conexao.close()

def listar_clientes_inativos(usuario_id):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, nome, email, telefone, ativo
        FROM clientes
        WHERE ativo = 0 AND usuario_id = ? 
        """,(usuario_id,))
    
    clientes = cursor.fetchall()

    conexao.close()

    return clientes

def inativar_cliente(id, usuario_id):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
                   UPDATE clientes
                   SET ativo = 0
                   WHERE id = ? AND usuario_id = ?
                   """, (id, usuario_id))
    
    conexao.commit()
    
    cursor.execute("""
                   SELECT id, nome, email, telefone, ativo
                   FROM clientes
                   WHERE id = ? AND usuario_id = ?
                   """, (id, usuario_id))
    

    cliente = cursor.fetchone()

    conexao.close()

    return cliente

def reativar_cliente(id, usuario_id):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
                   UPDATE clientes
                   SET ativo = 1 
                   WHERE id = ? AND usuario_id = ?
                   """, (id, usuario_id))
    
    conexao.commit()

    cursor.execute("""
                   SELECT id, nome, email, telefone, ativo
                   FROM clientes
                   WHERE id = ? AND usuario_id = ?
                   """, (id, usuario_id))

    cliente = cursor.fetchone()

    conexao.close()

    return cliente