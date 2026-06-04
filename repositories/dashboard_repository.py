from database import conectar

def contar_vendas(usuario_id):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
                   SELECT SUM(total)
                   FROM vendas
                   WHERE usuario_id = ? AND fechada = 0
                   """, (usuario_id,))
    
    resultado = cursor.fetchone()

    total = resultado[0] if resultado and resultado[0] else 0

    conexao.close()
    return total

def obter_faturamento_total(usuario_id, mes=None, ano=None):

    conexao = conectar()
    cursor = conexao.cursor()

    query = """
                   SELECT SUM(total)
                   FROM vendas
                   WHERE usuario_id = ? AND fechada = 0
                   """
    params = [usuario_id]

    if mes and ano:
        query += " AND MONTH(data_venda) = ? AND YEAR(data_venda) = ?"
        params.extend([mes, ano])

    cursor.execute(query, params)

    resultado = cursor.fetchone()

    total = resultado[0] if resultado and resultado[0] else 0

    conexao.close()
    return total

def obter_total_recebido(usuario_id, mes=None, ano=None):

    conexao = conectar()
    cursor = conexao.cursor()

    query = """
                   SELECT SUM(p.valor_pago)
                   FROM pagamentos p
                   JOIN vendas v ON p.venda_id = v.id
                   WHERE v.usuario_id = ? AND v.fechada = 0
            """
    params = [usuario_id]

    if mes and ano:
        query += " AND MONTH(v.data_venda) = ? AND YEAR(v.data_venda) = ?"
        params.extend([mes, ano])

    cursor.execute(query, params)

    resultado = cursor.fetchone()

    total = resultado[0] if resultado and resultado[0] else 0

    conexao.close()
    return total

def contar_clientes(usuario_id):
    
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
                   SELECT COUNT(*)
                   FROM clientes
                   WHERE usuario_id = ? AND ativo = 1
                   """, (usuario_id,))
    
    resultado = cursor.fetchone()

    total = resultado[0] if resultado and resultado[0] else 0

    conexao.close()
    return total

def contar_produtos(usuario_id):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
                   SELECT COUNT(*)
                   FROM produtos
                   WHERE usuario_id = ? AND ativo = 1
                   """, (usuario_id,))
    
    resultado = cursor.fetchone()

    total = resultado[0] if resultado and resultado[0] else 0

    conexao.close()
    return total