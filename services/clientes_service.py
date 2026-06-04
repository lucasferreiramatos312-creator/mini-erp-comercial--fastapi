from exceptions.custom_exceptions import ClienteNaoEncontrado
from repositories.clientes_repository import(criar_cliente,
                                            listar_clientes,
                                            buscar_cliente_por_id_geral,
                                            buscar_cliente_por_id,
                                            buscar_cliente_por_nome,
                                            atualizar_cliente,
                                            listar_clientes_inativos,
                                            inativar_cliente,
                                            reativar_cliente)

def formatar_cliente(cliente):

    return {
        "id": cliente[0],
        "nome": cliente[1],
        "email": cliente[2],
        "telefone": cliente[3],
        "ativo": cliente[4]
    }

def criar_cliente_service(nome, email, telefone, usuario_id):
   
   cliente_id = criar_cliente(nome, email, telefone, usuario_id)

   novo_cliente = buscar_cliente_por_id_geral(cliente_id, usuario_id)

   return formatar_cliente(novo_cliente)

def listar_clientes_service(usuario_id):
    
    clientes = listar_clientes(usuario_id)

    return [formatar_cliente(c) for c in clientes]

def buscar_cliente_por_nome_service(nome, usuario_id):
    
    clientes =  buscar_cliente_por_nome(nome, usuario_id)

    if not clientes:
        raise ClienteNaoEncontrado()
    
    return [formatar_cliente(c) for c in clientes]

def buscar_cliente_por_id_geral_service(id, usuario_id):

    cliente = buscar_cliente_por_id_geral(id, usuario_id)

    if not cliente:
        raise ClienteNaoEncontrado()
    
    return formatar_cliente(cliente)

def atualizar_cliente_service(id, nome, email, telefone, usuario_id):
    
    cliente_existente = buscar_cliente_por_id(id, usuario_id)

    if not cliente_existente:
        raise ClienteNaoEncontrado()
    
    atualizar_cliente(id, nome, email, telefone, usuario_id)

    cliente_atualizado = buscar_cliente_por_id(id, usuario_id)

    return formatar_cliente(cliente_atualizado)

def listar_clientes_inativos_service(usuario_id):

    clientes = listar_clientes_inativos(usuario_id)

    return [formatar_cliente(c) for c in clientes]

def inativar_cliente_service(id, usuario_id):

    cliente = buscar_cliente_por_id(id, usuario_id)

    if not cliente:
        raise ClienteNaoEncontrado()
    
    cliente_inativado = inativar_cliente(id, usuario_id)

    return formatar_cliente(cliente_inativado)

def reativar_cliente_service(id, usuario_id):

    cliente = buscar_cliente_por_id_geral(id, usuario_id)

    if not cliente:
        raise ClienteNaoEncontrado()
    
    cliente_reativado = reativar_cliente(id, usuario_id)

    return formatar_cliente(cliente_reativado)