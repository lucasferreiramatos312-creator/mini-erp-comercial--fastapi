from database import conectar

def contar_vendas(usuario_id):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
                   SELECT SUM(total)
                   FROM vendas
                   WHERE usuario_id = %s AND fechada = FALSE
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
                   WHERE usuario_id = %s AND fechada = FALSE
                   """
    params = [usuario_id]

    if mes and ano:
        query += " AND EXTRACT(MONTH FROM data_venda) = %s AND EXTRACT(YEAR FROM data_venda) = %s"
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
                   WHERE v.usuario_id = %s AND v.fechada = FALSE
            """
    params = [usuario_id]

    if mes is not None and ano is not None:
        query += " AND EXTRACT(MONTH FROM v.data_venda) = %s AND EXTRACT(YEAR FROM v.data_venda) = %s"
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
                   WHERE usuario_id = %s AND ativo = TRUE
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
                   WHERE usuario_id = %s AND ativo = TRUE
                   """, (usuario_id,))
    
    resultado = cursor.fetchone()

    total = resultado[0] if resultado and resultado[0] else 0

    conexao.close()
    return total