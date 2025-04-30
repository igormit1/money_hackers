CREATE DATABASE farmacia;
USE farmacia;



CREATE TABLE if not exists Pessoa (
    ID_Pessoa INT AUTO_INCREMENT PRIMARY KEY,
    Nome VARCHAR(100) NOT NULL,
    usuario VARCHAR(100) NOT NULL unique,
    CPF VARCHAR(11) NOT NULL UNIQUE,
	Email VARCHAR(80) NOT NULL,
    Endereco VARCHAR(255) NOT NULL,
    Ocupacao VARCHAR(15) NOT NULL,
    Senha CHAR(64) NOT NULL
);




select * from pessoa;

INSERT INTO pessoa (Nome, CPF, email, Endereco, Ocupacao, Senha)
    VALUES ('bbbba', '222233', 'bbbbeeeeee@ee', 'bbbbendere', 'ocubbbpacao1', 'sbbbenha1');
