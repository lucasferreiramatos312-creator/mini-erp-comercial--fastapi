class ERPException(Exception):
    def __init__(self, mensagem: str,
                status_code: int = 400):
        self.mensagem = mensagem
        self.status_code = status_code

class NaoEncontradoException(ERPException):
    def __init__(self, mensagem="Registro não encontrado"):
        super().__init__(mensagem, 404)

class ValidacaoException(ERPException):
    def __init__(self, mensagem="Erro de validação"):
        super().__init__(mensagem, 400)

class AutenticacaoException(ERPException):
    def __init__(self, mensagem="Não autorizado"):
        super().__init__(mensagem, 401)

class EntidadeNaoProcessavel(ERPException):
    def __init__(self, mensagem="Entidade não processável"):
        super().__init__(mensagem, 422)

class ClienteNaoEncontrado(NaoEncontradoException):
    def __init__(self):
        super().__init__("Cliente não encontrado")

class ClienteComVendas(ValidacaoException):
    def __init__(self):
        super().__init__("Clinte possui vendas e não pode ser excluído")

class ProdutoNaoEncontrado(NaoEncontradoException):
    def __init__(self):
        super().__init__("Produto não encontrado")

class ProdutoEmVenda(ValidacaoException):
    def __init__(self):
        super().__init__("Produto possui vendas vinculadas")

class EstoqueInsuficiente(EntidadeNaoProcessavel):
    def __init__(self):
        super().__init__("Estoque insuficiente")

class VendaNaoEncontrada(NaoEncontradoException):
    def __init__(self):
        super().__init__("Venda não encontrada")

class QuantidadeInvalida(ValidacaoException):
    def __init__(self):
        super().__init__("Quantidade inválida")

class VendaPagaOuParcialmentePaga(EntidadeNaoProcessavel):
    def __init__(self):
        super().__init__("Venda já está paga ou parcialmente paga")

class PagamentoInvalido(ValidacaoException):
    def __init__(self):
        super().__init__("Valor de pagamento inválido")

class PagamentoExcedeValorTotal(ValidacaoException):
    def __init__(self):
        super().__init__("Valor de pagamento excede o valor total da venda")