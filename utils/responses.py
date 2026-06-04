def sucesso(dados=None, mensagem=None):
    resposta =  {
        "sucesso": True
    }

    if dados is not None:
        resposta["dados"] = dados

    if mensagem:
        resposta["mensagem"] = mensagem

    return resposta

def erro(mensagem):
    return {
        "sucesso": False,
        "erro": mensagem
    }      