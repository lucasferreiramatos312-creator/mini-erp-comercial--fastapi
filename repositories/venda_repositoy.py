from database import conectar

def criar_venda(cursor, cliente_id, usuario_id):

    cursor.execute("""
                   INSERT INTO vendas (cliente_id, data_venda, usuario_id)
                   OUTPUT INSERTED.id
                   VALUES (?, GETDATE(), ?)
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
                   WHERE v.id = ? AND v.usuario_id = ?
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
                   WHERE c.nome LIKE ? AND v.usuario_id = ? AND v.fechada = 0
                   ORDER BY v.data_venda DESC
                   """, (f"%{nome}%", usuario_id))
    
    resultado = cursor.fetchall()
    
    conexao.close()

    return resultado

def adicionar_item(cursor, venda_id, produto_id, quantidade):

    cursor.execute("""
                   SELECT valor, estoque
                   FROM produtos
                   WHERE id = ?
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
                   VALUES (?, ?, ?, ?)
                   """, (venda_id, produto_id, quantidade, valor))
    
    cursor.execute("""
                     UPDATE produtos
                        SET estoque = estoque - ?
                        WHERE id = ?
                     """, (quantidade, produto_id))

    return valor * quantidade

def atualizar_total_venda(cursor, venda_id):

    cursor.execute("""
                   SELECT SUM(quantidade * valor_unitario)
                   FROM itens_venda
                   WHERE venda_id = ?
                   """, (venda_id,))
    
    resultado = cursor.fetchone()

    total = resultado[0] if resultado and resultado[0] else 0

    cursor.execute("""
                   UPDATE vendas
                   SET total = ?
                   WHERE id = ?
                   """, (total, venda_id))

def listar_vendas_por_usuario(usuario_id,mes=None, ano=None):

    conexao = conectar()
    cursor = conexao.cursor()

    query = """
                SELECT v.id, c.id, c.nome, v.total, v.data_venda
                FROM vendas v
                JOIN clientes c ON v.cliente_id = c.id
                WHERE v.usuario_id = ? AND v.fechada = 0
            """
                  
    params = [usuario_id]

    if mes and ano:
        query += " AND MONTH(v.data_venda) = ? AND YEAR(v.data_venda) = ?"
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
                   WHERE v.usuario_id = ? AND v.fechada = 1
                   """

    params = [usuario_id]

    if mes and ano:
        query += " AND MONTH(v.data_venda) = ? AND YEAR(v.data_venda) = ?"
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
                   WHERE i.venda_id = ?
                  """, (venda_id,))
    
    itens = cursor.fetchall()
    conexao.close()

    return itens

def buscar_itens_para_estoque(cursor, venda_id):
    cursor.execute("""
                   SELECT produto_id, quantidade
                   FROM itens_venda
                   WHERE venda_id = ?
                   """, (venda_id))
    
    return cursor.fetchall()

def buscar_item_venda(cursor, venda_id, produto_id):
    cursor.execute("""
                   SELECT quantidade
                   FROM itens_venda
                   WHERE venda_id = ? AND produto_id = ?
                   """, (venda_id, produto_id))
    
    item = cursor.fetchone()

    return item

def atualizar_item_venda(cursor, venda_id, produto_id, quantidade):
    cursor.execute("""
                   UPDATE itens_venda
                   SET quantidade = ?
                   WHERE venda_id = ? AND produto_id = ?
                   """, (quantidade, venda_id, produto_id))

def deletar_itens_venda(cursor, venda_id):
    cursor.execute("""
                   DELETE FROM itens_venda
                   WHERE venda_id = ?
                   """, (venda_id))
    
def deletar_venda(cursor, venda_id, usuario_id):
    cursor.execute(""" DELETE FROM vendas
                   WHERE id = ? AND usuario_id = ?
                   """, (venda_id, usuario_id))
    
def devolver_estoque(cursor, produto_id, quatidade):
    cursor.execute("""
                   UPDATE produtos
                   SET estoque = estoque + ?
                   WHERE id = ?
                   """, (quatidade, produto_id))

def registrar_pagamento(cursor, venda_id, valor_pago):

    cursor.execute("""
                   INSERT INTO pagamentos (venda_id, valor_pago, data_pagamento)
                   VALUES (?, ?, GETDATE())
                   """, (venda_id, valor_pago))

def obter_total_pago(venda_id):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
                   SELECT SUM(valor_pago)
                   FROM pagamentos
                   WHERE venda_id = ?
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
                   WHERE id = ?
                   """, (venda_id,))
    
    resultado = cursor.fetchone()

    total = resultado[0] if resultado and resultado[0] else 0

    conexao.close()
    return total

def fechar_vendas_pagadas(cursor, usuario_id):

    cursor.execute("""
                   UPDATE vendas
                   SET fechada = 1
                   WHERE usuario_id = ? AND fechada = 0 AND id IN (

                       SELECT v.id
                       FROM vendas v
                       LEFT JOIN pagamentos p ON v.id = p.venda_id
                       WHERE v.usuario_id = ?
                       GROUP BY v.id, v.total
                       HAVING ISNULL(SUM(p.valor_pago), 0) >= v.total)
                   """, (usuario_id, usuario_id))