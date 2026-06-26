from database import conectar

def criar_cliente(nome, email, telefone, usuario_id):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO clientes (nome, email, telefone, usuario_id)        
        VALUES (%s, %s, %s, %s)
        RETURNING id
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
        WHERE usuario_id = %s AND ativo = TRUE
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
                   WHERE id = %s AND usuario_id = %s
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
                   WHERE id = %s AND usuario_id = %s AND ativo = TRUE
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
                   WHERE usuario_id = %s AND nome ILIKE %s AND ativo = TRUE
                   """, (usuario_id, f'%{nome}%')) 

    clientes = cursor.fetchall()
    conexao.close()

    return clientes

def atualizar_cliente(id, nome, email, telefone, usuario_id):
    
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
                  UPDATE clientes
                  SET nome = %s, email = %s, telefone = %s
                  WHERE id = %s AND usuario_id = %s
                   """, (nome, email, telefone, id, usuario_id))
    
    conexao.commit()
    conexao.close()

def listar_clientes_inativos(usuario_id):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, nome, email, telefone, ativo
        FROM clientes
        WHERE ativo = FALSE AND usuario_id = %s 
        """,(usuario_id,))
    
    clientes = cursor.fetchall()

    conexao.close()

    return clientes

def inativar_cliente(id, usuario_id):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
                   UPDATE clientes
                   SET ativo = FALSE
                   WHERE id = %s AND usuario_id = %s
                   """, (id, usuario_id))
    
    conexao.commit()
    
    cursor.execute("""
                   SELECT id, nome, email, telefone, ativo
                   FROM clientes
                   WHERE id = %s AND usuario_id = %s
                   """, (id, usuario_id))
    

    cliente = cursor.fetchone()

    conexao.close()

    return cliente

def reativar_cliente(id, usuario_id):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
                   UPDATE clientes
                   SET ativo = TRUE
                   WHERE id = %s AND usuario_id = %s
                   """, (id, usuario_id))
    
    conexao.commit()

    cursor.execute("""
                   SELECT id, nome, email, telefone, ativo
                   FROM clientes
                   WHERE id = %s AND usuario_id = %s
                   """, (id, usuario_id))

    cliente = cursor.fetchone()

    conexao.close()

    return cliente