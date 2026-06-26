CREATE TABLE usuarios (
id SERIAL PRIMARY KEY,
nome VARCHAR(150) NOT NULL,
email VARCHAR(255) NOT NULL UNIQUE,
senha VARCHAR(255) NOT NULL
);

CREATE TABLE clientes (
id SERIAL PRIMARY KEY,
nome VARCHAR(150) NOT NULL,
email VARCHAR(255),
telefone VARCHAR(30),
data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
usuario_id INTEGER NOT NULL,
ativo BOOLEAN DEFAULT TRUE,

CONSTRAINT fk_cliente_usuario
    FOREIGN KEY (usuario_id)
    REFERENCES usuarios(id)

);

CREATE TABLE produtos (
id SERIAL PRIMARY KEY,
nome VARCHAR(150) NOT NULL,
valor NUMERIC(10,2) NOT NULL,
estoque INTEGER NOT NULL DEFAULT 0,
usuario_id INTEGER NOT NULL,
ativo BOOLEAN DEFAULT TRUE,

CONSTRAINT fk_produto_usuario
    FOREIGN KEY (usuario_id)
    REFERENCES usuarios(id)

);

CREATE TABLE vendas (
id SERIAL PRIMARY KEY,
cliente_id INTEGER NOT NULL,
data_venda TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
usuario_id INTEGER NOT NULL,
total NUMERIC(10,2) NOT NULL DEFAULT 0,
fechada BOOLEAN DEFAULT FALSE,

CONSTRAINT fk_venda_cliente
    FOREIGN KEY (cliente_id)
    REFERENCES clientes(id),

CONSTRAINT fk_venda_usuario
    FOREIGN KEY (usuario_id)
    REFERENCES usuarios(id)

);

CREATE TABLE itens_venda (
id SERIAL PRIMARY KEY,
venda_id INTEGER NOT NULL,
produto_id INTEGER NOT NULL,
quantidade INTEGER NOT NULL,
valor_unitario NUMERIC(10,2) NOT NULL,

CONSTRAINT fk_item_venda
    FOREIGN KEY (venda_id)
    REFERENCES vendas(id),

CONSTRAINT fk_item_produto
    FOREIGN KEY (produto_id)
    REFERENCES produtos(id)

);

CREATE TABLE pagamentos (
id SERIAL PRIMARY KEY,
venda_id INTEGER NOT NULL,
valor_pago NUMERIC(10,2) NOT NULL,
data_pagamento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

CONSTRAINT fk_pagamento_venda
    FOREIGN KEY (venda_id)
    REFERENCES vendas(id)

);