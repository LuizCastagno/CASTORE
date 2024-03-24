-- Database: produtos

-- DROP DATABASE IF EXISTS produtos;

CREATE TABLE produtos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    descricao TEXT,
    preco FLOAT NOT NULL,
    imagem VARCHAR(255)
);
