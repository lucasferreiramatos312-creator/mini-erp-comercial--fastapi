from database import conectar
from exceptions.custom_exceptions import (VendaNaoEncontrada,
                                          ProdutoNaoEncontrado,
                                          QuantidadeInvalida,
                                          EstoqueInsuficiente,
                                          VendaPagaOuParcialmentePaga,
                                          PagamentoInvalido,
                                          PagamentoExcedeValorTotal)

from repositories.clientes_repository import (buscar_cliente_por_id)
from repositories.produtos_repository import (buscar_produto_por_id)

from exceptions.custom_exceptions import (ClienteNaoEncontrado)
from exceptions.custom_exceptions import (ProdutoNaoEncontrado)

from repositories.venda_repositoy import (criar_venda,
                                          listar_vendas_por_usuario,
                                          buscar_venda_por_id,
                                          buscar_venda_por_cliente,
                                          listar_venda_fechadas,
                                          listar_itens_venda,
                                          buscar_itens_para_estoque,
                                          deletar_itens_venda,
                                          deletar_venda,
                                          devolver_estoque,
                                          buscar_item_venda,
                                          atualizar_item_venda,
                                          registrar_pagamento,                                          
                                          adicionar_item,
                                          atualizar_total_venda,
                                          obter_total_pago,
                                          obter_total_venda,
                                          fechar_vendas_pagadas)

def formatar_venda(venda, itens=None, status=None, total_pago=None):

    return {
            "id": venda[0],
            "cliente_id": venda[1],
            "cliente_nome": venda[2],
            "total": venda[3],
            "data_venda": venda[4],
            "status": status,
            "total_pago": total_pago or 0,
            "itens": itens or []
    }

def formatar_itens(itens):

    return {
                "produto_id": itens[0],
                "produto_nome": itens[1],
                "quantidade": itens[2],
                "valor_unitario": itens[3]
            }

def criar_venda_com_itens(venda, usuario_id):

    conexao = conectar()
    cursor = conexao.cursor()

    try:

        cliente = buscar_cliente_por_id(venda.cliente_id, usuario_id)

        if not cliente:
            raise ClienteNaoEncontrado()

        venda_id = criar_venda(cursor, venda.cliente_id, usuario_id)
        
        produto = buscar_produto_por_id(venda.itens[0].produto_id, usuario_id)

        if not produto:
            raise ProdutoNaoEncontrado()

        for item in venda.itens:
            adicionar_item(cursor, venda_id, item.produto_id, item.quantidade)

        atualizar_total_venda(cursor, venda_id)

        conexao.commit()

        venda_criada = buscar_venda_por_id(venda_id, usuario_id)

        itens  = listar_itens_venda(venda_id)

        itens_formatados = [formatar_itens(i) for i in itens]

        status = calcular_status_venda(venda_id)

        return formatar_venda(venda_criada, itens=itens_formatados, status=status, total_pago=0)
    
    except Exception:
        conexao.rollback()
        raise
    
    finally:
        conexao.close()

def criar_venda_service(cliente_id, usuario_id):

    conexao = conectar()
    cursor = conexao.cursor()

    try:

        cliente = buscar_cliente_por_id(cliente_id, usuario_id)

        if not cliente:
            raise ClienteNaoEncontrado()

        venda_id = criar_venda(cursor,cliente_id, usuario_id)

        conexao.commit()

        venda_criada = buscar_venda_por_id(venda_id, usuario_id)

        status = calcular_status_venda(venda_id)

        return formatar_venda(venda_criada,itens=None, status=status, total_pago=0)
    
    except Exception:
        conexao.rollback()
        raise
    
    finally:
        conexao.close()

def adicionar_item_service(venda_id, produto_id, quantidade, usuario_id):

    conexao = conectar()
    cursor = conexao.cursor()

    try:

        produto = buscar_produto_por_id(produto_id, usuario_id)

        if not produto:
            raise ProdutoNaoEncontrado()

        venda = buscar_venda_por_id(venda_id, usuario_id)
        
        if not venda:
            raise VendaNaoEncontrada()
        
        if quantidade <= 0:
            raise QuantidadeInvalida()

        valor_total_item = adicionar_item(cursor, venda_id, produto_id, quantidade)
    
        atualizar_total_venda(cursor, venda_id)

        conexao.commit()
        
        return valor_total_item
    
    except Exception:
        conexao.rollback()
        raise 
    
    finally:
        conexao.close()

def buscar_venda_por_cliente_service(nome, usuario_id):

    vendas = buscar_venda_por_cliente(nome, usuario_id)

    if not vendas:
        raise VendaNaoEncontrada()
    
    return [formatar_venda(v) for v in vendas]

def listar_vendas_service(usuario_id, mes=None, ano=None):
    
    vendas = listar_vendas_por_usuario(usuario_id, mes, ano)

    return [formatar_venda(v) for v in vendas]

def buscar_venda_com_itens_service(venda_id, usuario_id):
    
    venda = buscar_venda_por_id(venda_id, usuario_id)

    if not venda:
        raise VendaNaoEncontrada()
    
    itens = listar_itens_venda(venda_id)
    
    itens_formatados = [formatar_itens(i) for i in itens]
    
    total_pago = obter_total_pago(venda_id)

    status = calcular_status_venda(venda_id)
    
    return formatar_venda(venda, itens=itens_formatados, status=status, total_pago=total_pago)

def atualizar_item_venda_service(venda_id, produto_id, quantidade, usuario_id):
    
    conexao = conectar()
    cursor = conexao.cursor()

    try: 
        venda = buscar_venda_por_id(venda_id, usuario_id)
        if not venda:
            raise VendaNaoEncontrada()
        
        item = buscar_item_venda(cursor, venda_id, produto_id)
        
        if not item:
            raise ProdutoNaoEncontrado()
        
        qtd_antiga = item[0]

        diferenca = quantidade - qtd_antiga

        if diferenca > 0:
            cursor.execute("SELECT estoque FROM produtos WHERE id = ?", (produto_id,))
            
            resultado = cursor.fetchone()

            if not resultado:
                raise ProdutoNaoEncontrado()
            
            estoque = resultado[0]
            
            if estoque < diferenca:
                raise EstoqueInsuficiente()
        
            cursor.execute("""
                            UPDATE produtos
                            SET estoque = estoque - ?
                            WHERE id = ?
                            """, (diferenca, produto_id))
        
        elif diferenca < 0:
            cursor.execute("""
                           UPDATE produtos
                           SET estoque = estoque + ?
                           WHERE id = ?
                           """, (abs(diferenca), produto_id))
        
        atualizar_item_venda(cursor, venda_id, produto_id, quantidade)

        atualizar_total_venda(cursor, venda_id)

        conexao.commit()

    except Exception:
        conexao.rollback()
        raise
    
    finally:
        conexao.close()

def excluir_venda_service(venda_id, usuario_id):

    conexao = conectar()
    cursor = conexao.cursor()

    try:
        venda = buscar_venda_por_id(venda_id, usuario_id)
        if not venda:
            raise VendaNaoEncontrada()

        status = calcular_status_venda(venda_id)

        if status in ["PAGO", "PARCIAL"]:
            raise VendaPagaOuParcialmentePaga()

        itens = buscar_itens_para_estoque(cursor, venda_id)

        for item in itens:
            produto_id, quantidade = item
            devolver_estoque(cursor, produto_id, quantidade)

        deletar_itens_venda(cursor, venda_id)

        deletar_venda(cursor, venda_id, usuario_id)

        conexao.commit()

    except Exception:
        conexao.rollback()
        raise 
    
    finally:
        conexao.close()

def registrar_pagamento_service(venda_id, valor_pago, usuario_id):

    conexao = conectar()
    cursor = conexao.cursor()

    try:
        venda = buscar_venda_por_id(venda_id, usuario_id)

        if not venda:
            raise VendaNaoEncontrada()

        if valor_pago <= 0:
            raise PagamentoInvalido()
        
        total_pago = obter_total_pago(venda_id)

        if valor_pago > total_pago + obter_total_venda(venda_id):
            raise PagamentoExcedeValorTotal()
        
        registrar_pagamento(cursor, venda_id, valor_pago)

        conexao.commit()
        
    except Exception:
        conexao.rollback()
        raise
    
    finally:
        conexao.close()

def fechar_vendas_pagadas_service(usuario_id):

    conexao = conectar()
    cursor = conexao.cursor()

    try:

        fechar_vendas_pagadas(cursor, usuario_id)

        conexao.commit()

    except Exception:
        conexao.rollback()
        raise
    
    finally:
        conexao.close()

def listar_vendas_fechadas_service(usuario_id, mes=None, ano=None):

    vendas = listar_venda_fechadas(usuario_id, mes, ano)

    status = "FECHADA"
    return [formatar_venda(v,status=status) for v in vendas]

def calcular_status_venda(venda_id):

    total = obter_total_venda(venda_id)
    total_pago = obter_total_pago(venda_id)

    if total_pago == 0:
        return "PENDENTE"
    elif total_pago < total:
        return "PARCIAL"
    else:
        return "PAGO"
    