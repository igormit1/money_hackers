CREATE DATABASE farmacia;
USE farmacia;

drop table pessoa;

CREATE TABLE if not exists Pessoa (
    ID_Pessoa INT AUTO_INCREMENT PRIMARY KEY,
    Nome VARCHAR(100) NOT NULL,
    usuario VARCHAR(100) NOT NULL unique,
    CPF VARCHAR(11) NOT NULL UNIQUE,
	Email VARCHAR(30) NOT NULL,
    Endereco VARCHAR(255) NOT NULL,
    Ocupacao VARCHAR(15) NOT NULL,
    Senha CHAR(64) NOT NULL
);

CREATE TABLE if not exists Medicamento (
    ID_Medicamento INT AUTO_INCREMENT PRIMARY KEY,
    Nome_Medicamento VARCHAR(100) NOT NULL,
    nome_generico VARCHAR(100) NULL,
    categoria VARCHAR(100) NULL,
    distribuidor  VARCHAR(100) NULL,
    Data_Validade DATE NOT NULL,
    Preço DECIMAL(10, 2) NOT NULL
);

CREATE TABLE if not exists Entrega (
    ID_Entrega INT AUTO_INCREMENT PRIMARY KEY,
    ID_balconista int not null,
    ID_cliente int not null,
    ID_Medicamento_ref INT not null,
    qtd_medicamento int not null,
    Data_Entrega DATE NOT NULL,
    FOREIGN KEY (ID_balconista) REFERENCES Pessoa(ID_Pessoa),
	FOREIGN KEY (ID_cliente) REFERENCES Pessoa(ID_Pessoa),
    FOREIGN KEY (ID_medicamento_ref) REFERENCES medicamento(ID_medicamento)
);
 
select * from pessoa;

INSERT INTO pessoa (Nome, CPF, email, Endereco, Ocupacao, Senha)
    VALUES ('bbbba', '222233', 'bbbbeeeeee@ee', 'bbbbendere', 'ocubbbpacao1', 'sbbbenha1');