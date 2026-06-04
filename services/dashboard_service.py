from repositories.dashboard_repository import(contar_vendas,
                                              obter_faturamento_total,
                                              obter_total_recebido,
                                              contar_clientes,
                                              contar_produtos
                                              )

def resumo_dashboard(usuario_id, mes=None, ano=None):
    
    total_vendas = contar_vendas(usuario_id) or 0
    faturamento = obter_faturamento_total(usuario_id, mes, ano) or 0
    recebido = obter_total_recebido(usuario_id, mes, ano) or 0
    clientes = contar_clientes(usuario_id) or 0
    produtos = contar_produtos(usuario_id) or 0

    pendente = faturamento - recebido
    saldo = faturamento - pendente

    ticket_medio = faturamento / total_vendas if total_vendas > 0 else 0

    return {
        'total_vendas': total_vendas,
        'faturamento': faturamento,
        'recebido': recebido,
        'pendente': pendente,
        "saldo": saldo,
        'total_clientes': clientes,
        "total_produtos": produtos,
        'ticket_medio': round(ticket_medio, 2)
        }