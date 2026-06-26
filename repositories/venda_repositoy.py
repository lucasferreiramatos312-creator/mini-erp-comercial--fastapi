from database import conectar

def criar_venda(cursor, cliente_id, usuario_id):

    cursor.execute("""
                   INSERT INTO vendas (cliente_id, data_venda, usuario_id)
                   VALUES (%s, CURRENT_TIMESTAMP, %s)
                   RETURNING id
                  """, (cliente_id, usuario_id))

    venda_id = cursor.fetchone()[0]

    if not venda_id:
        raise Exception("Erro ao criar venda")
    
    return venda_id

def buscar_venda_por_id(vendas_id, usuario_id):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
                   SELECT v.id, c.id, c.nome, v.total, v.data_venda
                   FROM vendas v
                   JOIN clientes c ON v.cliente_id = c.id
                   WHERE v.id = %s AND v.usuario_id = %s
                  """, (vendas_id, usuario_id))
    
    venda = cursor.fetchone()
    
    conexao.close()

    return venda

def buscar_venda_por_cliente(nome, usuario_id):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
                   SELECT v.id, c.id, c.nome, v.total, v.data_venda
                   FROM vendas v
                   JOIN clientes c ON v.cliente_id = c.id
                   WHERE c.nome ILIKE %s AND v.usuario_id = %s AND v.fechada = FALSE
                   ORDER BY v.data_venda DESC
                   """, (f"%{nome}%", usuario_id))
    
    resultado = cursor.fetchall()
    
    conexao.close()

    return resultado

def adicionar_item(cursor, venda_id, produto_id, quantidade):

    cursor.execute("""
                   SELECT valor, estoque
                   FROM produtos
                   WHERE id = %s
                   """, (produto_id,))
    produto = cursor.fetchone()

    if not produto:
        raise Exception("Produto não encontrado")

    valor, estoque = produto

    if estoque < quantidade:
        raise Exception("Estoque insuficiente")
    
    cursor.execute("""
                   INSERT INTO itens_venda (venda_id, produto_id,
                   quantidade, valor_unitario)
                   VALUES (%s, %s, %s, %s)
                   """, (venda_id, produto_id, quantidade, valor))
    
    cursor.execute("""
                     UPDATE produtos
                        SET estoque = estoque - %s
                        WHERE id = %s
                     """, (quantidade, produto_id))

    return valor * quantidade

def atualizar_total_venda(cursor, venda_id):

    cursor.execute("""
                   SELECT SUM(quantidade * valor_unitario)
                   FROM itens_venda
                   WHERE venda_id = %s
                   """, (venda_id,))
    
    resultado = cursor.fetchone()

    total = resultado[0] if resultado and resultado[0] else 0

    cursor.execute("""
                   UPDATE vendas
                   SET total = %s
                   WHERE id = %s
                   """, (total, venda_id))

def listar_vendas_por_usuario(usuario_id,mes=None, ano=None):

    conexao = conectar()
    cursor = conexao.cursor()

    query = """
                SELECT v.id, c.id, c.nome, v.total, v.data_venda
                FROM vendas v
                JOIN clientes c ON v.cliente_id = c.id
                WHERE v.usuario_id = %s AND v.fechada = FALSE
            """
                  
    params = [usuario_id]

    if mes and ano:
        query += " AND EXTRACT(MONTH FROM v.data_venda) = %s AND EXTRACT(YEAR FROM v.data_venda) = %s"
        params.extend([mes, ano])
    
    cursor.execute(query, params)
    
    vendas = cursor.fetchall()
    conexao.close()

    return vendas

def listar_venda_fechadas(usuario_id, mes=None, ano=None):
    
    conexao = conectar()
    cursor = conexao.cursor()

    query = """ 
                   SELECT v.id, c.id, c.nome, v.total, v.data_venda
                   FROM vendas v
                   JOIN clientes c ON v.cliente_id = c.id
                   WHERE v.usuario_id = %s AND v.fechada = TRUE
                   """

    params = [usuario_id]

    if mes and ano:
        query += " AND EXTRACT(MONTH FROM v.data_venda) = %s AND EXTRACT(YEAR FROM v.data_venda) = %s"
        params.extend([mes, ano])

    query += " ORDER BY v.data_venda DESC"

    cursor.execute(query, params)

    vendas = cursor.fetchall()

    conexao.close()

    return vendas

def listar_itens_venda(venda_id):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
                   SELECT p.id, p.nome, i.quantidade, i.valor_unitario
                   FROM itens_venda i
                   JOIN produtos p ON i.produto_id = p.id
                   WHERE i.venda_id = %s
                  """, (venda_id,))
    
    itens = cursor.fetchall()
    conexao.close()

    return itens

def buscar_itens_para_estoque(cursor, venda_id):
    cursor.execute("""
                   SELECT produto_id, quantidade
                   FROM itens_venda
                   WHERE venda_id = %s
                   """, (venda_id,))
    
    return cursor.fetchall()

def buscar_item_venda(cursor, venda_id, produto_id):
    cursor.execute("""
                   SELECT quantidade
                   FROM itens_venda
                   WHERE venda_id = %s AND produto_id = %s
                   """, (venda_id, produto_id))
    
    item = cursor.fetchone()

    return item

def atualizar_item_venda(cursor, venda_id, produto_id, quantidade):
    cursor.execute("""
                   UPDATE itens_venda
                   SET quantidade = %s
                   WHERE venda_id = %s AND produto_id = %s
                   """, (quantidade, venda_id, produto_id))

def deletar_itens_venda(cursor, venda_id):
    cursor.execute("""
                   DELETE FROM itens_venda
                   WHERE venda_id = %s
                   """, (venda_id,))
    
def deletar_venda(cursor, venda_id, usuario_id):
    cursor.execute(""" DELETE FROM vendas
                   WHERE id = %s AND usuario_id = %s
                   """, (venda_id, usuario_id))
    
def devolver_estoque(cursor, produto_id, quatidade):
    cursor.execute("""
                   UPDATE produtos
                   SET estoque = estoque + %s
                   WHERE id = %s
                   """, (quatidade, produto_id))

def registrar_pagamento(cursor, venda_id, valor_pago):

    cursor.execute("""
                   INSERT INTO pagamentos (venda_id, valor_pago, data_pagamento)
                   VALUES (%s, %s, CURRENT_TIMESTAMP)
                   """, (venda_id, valor_pago))

def obter_total_pago(venda_id):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
                   SELECT SUM(valor_pago)
                   FROM pagamentos
                   WHERE venda_id = %s
                   """, (venda_id,))
    
    resultado = cursor.fetchone()

    total_pago = resultado[0] if resultado and resultado[0] else 0
    
    conexao.close()
    return total_pago

def obter_total_venda(venda_id):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
                   SELECT total
                   FROM vendas
                   WHERE id = %s
                   """, (venda_id,))
    
    resultado = cursor.fetchone()

    total = resultado[0] if resultado and resultado[0] else 0

    conexao.close()
    return total

def fechar_vendas_pagadas(cursor, usuario_id):

    cursor.execute("""
                   UPDATE vendas
                   SET fechada = TRUE
                   WHERE usuario_id = %s AND fechada = FALSE AND id IN (

                       SELECT v.id
                       FROM vendas v
                       LEFT JOIN pagamentos p ON v.id = p.venda_id
                       WHERE v.usuario_id = %s
                       GROUP BY v.id, v.total
                       HAVING COALESCE(SUM(p.valor_pago), 0) >= v.total)
                   """, (usuario_id, usuario_id))