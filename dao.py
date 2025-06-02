import mysql.connector
from mysql.connector import Error
from flask import jsonify
import os

#cadastrar
def create(nome, usuario, cpf, email, endereco, ocupacao, senha):
    try:
        # Conexão ao banco de dados
        conexao = mysql.connector.connect(
            host='localhost',
            user='root',
            password='12345678',
            database='farmacia',
        )
        cursor = conexao.cursor()

        comando = '''
        INSERT INTO pessoa (Nome, usuario, CPF, Email, Endereco, Ocupacao, Senha)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        '''
        
        cursor.execute(comando, (nome, usuario, cpf, email, endereco, ocupacao, senha))
        conexao.commit()
    
    except Error as e:
        print(f'Erro ao conectar ao MySQL: {e}')
        raise  # Relevanta a exceção para ser tratada no submit()
    
    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()

#-----------------------------------------------------------------------------------------------------------

#login
def authenticate(usuario, password):
    try:
        # Conexão ao banco de dados
        conexao = mysql.connector.connect(
            host='localhost',
            user='root',
            password='12345678',
            database='farmacia',
        )
        cursor = conexao.cursor()
        
        # Verifique se o usuario e a senha correspondem
        comando = '''
        SELECT * FROM pessoa WHERE usuario = %s AND Senha = %s
        '''
        cursor.execute(comando, (usuario, password))
        result = cursor.fetchone()
        
        return result is not None  # Retorna True se encontrar um usuário

    except Error as e:
        print(f'Erro ao conectar ao MySQL: {e}')
        return False  # Retorna False em caso de erro

    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()

#-----------------------------------------------------------------------------------------------------------

#cliente
def create2(nome, cpf, email, endereco):
    try:
        # Conexão ao banco de dados
        conexao = mysql.connector.connect(
            host='localhost',
            user='root',
            password='12345678',
            database='farmacia',
        )
        cursor = conexao.cursor()

        comando = '''
        INSERT INTO cliente (Nome, CPF_cnpj, Email, Endereco)
        VALUES (%s, %s, %s, %s)
        '''
        
        cursor.execute(comando, (nome, cpf, email, endereco))
        conexao.commit()
    
    except Error as e:
        print(f'Erro ao conectar ao MySQL: {e}')
        raise  # Relevanta a exceção para ser tratada no submit()
    
    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()

#-----------------------------------------------------------------------------------------------------------

#medicamento
def create3(Nome_medicamento , nome_generico, categoria, distribuidor, data_validade, Preco):
    try:
        # Conexão ao banco de dados
        conexao = mysql.connector.connect(
            host='localhost',
            user='root',
            password='12345678',
            database='farmacia',
        )
        cursor = conexao.cursor()

        comando = '''
        INSERT INTO medicamento (Nome_medicamento, nome_generico, categoria, distribuidor, data_validade, Preco)
        VALUES (%s, %s, %s, %s, %s, %s)
        '''
        
        cursor.execute(comando, (Nome_medicamento, nome_generico, categoria, distribuidor, data_validade, Preco))
        conexao.commit()
    
    except Error as e:
        print(f'Erro ao conectar ao MySQL: {e}')
        raise  # Relevanta a exceção para ser tratada no submit()
    
    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()

#-----------------------------------------------------------------------------------------------------------

#venda
def create4(balconista, cpf_cliente, data_venda, medicamento, qtd, lote):
    try:
        # Conexão ao banco de dados
        conexao = mysql.connector.connect(
            host='localhost',
            user='root',
            password='12345678',
            database='farmacia',
        )
        cursor = conexao.cursor()

        # Formatar o objeto datetime para o formato MySQL
        #data_formatada = datetime.strptime(data_venda, "%d/%m/%Y")
        #data_mysql = data_formatada.strftime("%Y-%m-%d")

        # Consulta SQL com LIKE para encontrar o ID do medicamento
        comando1 = '''
        SELECT ID_Medicamento FROM medicamento WHERE Nome_Medicamento LIKE %s
        '''
        valor1 = f"%{medicamento}%"
        cursor.execute(comando1, (valor1,))
        resultado_medicamento = cursor.fetchone()

        if resultado_medicamento is None:
            raise ValueError("Medicamento não encontrado.")
        
        # Consulta SQL com LIKE para encontrar o ID do cliente
        comando2 = '''
        SELECT ID_cliente FROM cliente WHERE CPF_CNPJ LIKE %s
        '''
        valor2 = f"%{cpf_cliente}%"
        cursor.execute(comando2, (valor2,))
        resultado_cliente = cursor.fetchone()

        if resultado_cliente is None:
            raise ValueError("Cliente não encontrado.")
        
        # Consulta SQL com LIKE para encontrar o ID do balconista
        comando3 = '''
        SELECT ID_pessoa FROM Pessoa WHERE Nome LIKE %s AND Ocupacao = 'balconista'
        '''
        valor3 = f"%{balconista}%"
        cursor.execute(comando3, (valor3,))
        resultado_balconista = cursor.fetchone()

        if resultado_balconista is None:
            raise ValueError("Balconista não encontrado.")

        # Inserção de dados na tabela entrega
        comando_insert = '''
        INSERT INTO entrega (ID_balconista, ID_cliente, ID_Medicamento_ref, qtd_medicamento, Data_Entrega, lote)
        VALUES (%s, %s, %s, %s, %s, %s)
        '''
        
        cursor.execute(comando_insert, (resultado_balconista[0], resultado_cliente[0], resultado_medicamento[0], qtd, data_venda, lote))
        conexao.commit()

    except Error as e:
        print(f'Erro ao conectar ao MySQL: {e}')
        raise  # Relevanta a exceção para ser tratada no submit()
    
    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()

#-----------------------------------------------------------------------------------------------------------

def pesquisa_cliente(letra):
    try:
        # Conexão ao banco de dados
        conexao = mysql.connector.connect(
            host='localhost',
            user='root',
            password='12345678',
            database='farmacia',
        )
        cursor = conexao.cursor()

        # Comando SQL com LIKE
        comando = '''
        SELECT nome FROM cliente WHERE nome LIKE %s;
        '''
        
        # Variável de parâmetro para a query
        parametro = f'{letra}%'
        
        # Executa o comando com o parâmetro
        cursor.execute(comando, (parametro,))
        
        resultados = cursor.fetchall()
        
        return resultados 
    
    except Error as e:
        print(f'Erro ao conectar ao MySQL: {e}')
        raise  # Levanta a exceção para ser tratada em outro ponto
    
    finally:
        # Fecha o cursor e a conexão se estiverem abertos
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'conexao' in locals() and conexao:
            conexao.close()
def salvar_perfil_investidor(pontuacao, perfil, descricao):
    try:
        conexao = mysql.connector.connect(
            host='localhost',
            user='root',
            password='12345678',
            database='farmacia',
        )
        cursor = conexao.cursor()
        sql = "INSERT INTO perfil_investidor (pontuacao, perfil, descricao) VALUES (%s, %s, %s)"
        valores = (pontuacao, perfil, descricao)
        cursor.execute(sql, valores)
        conexao.commit()
        cursor.close()
        conexao.close()
        return True
    except Exception as e:
        print("Erro ao salvar perfil:", e)
        return False
#-----------------------------------------------------------------------------------------------------------

def pesquisa_medicamento(letra2):
    try:
        # Conexão ao banco de dados
        conexao = mysql.connector.connect(
            host='localhost',
            user='root',
            password='12345678',
            database='farmacia',
        )
        cursor = conexao.cursor()

        # Comando SQL com LIKE
        comando = '''
        SELECT nome_medicamento FROM medicamento WHERE nome_medicamento LIKE %s;
        '''
        
        # Variável de parâmetro para a query
        parametro = f'{letra2}%'
        
        # Executa o comando com o parâmetro
        cursor.execute(comando, (parametro,))
        
        resultados2 = cursor.fetchall()
        
        return resultados2  
    
    except Error as e:
        print(f'Erro ao conectar ao MySQL: {e}')
        raise  # Levanta a exceção para ser tratada em outro ponto
    
    finally:
        # Fecha o cursor e a conexão se estiverem abertos
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'conexao' in locals() and conexao:
            conexao.close()

#-----------------------------------------------------------------------------------------------------------

def pesquisa_venda(letra3):
    try:
        # Conexão ao banco de dados
        conexao = mysql.connector.connect(
            host='localhost',
            user='root',
            password='12345678',
            database='farmacia',
        )
        cursor = conexao.cursor()

        # Comando SQL com LIKE
        comando = '''
        SELECT 
    p.Nome AS Nome_Balconista,
    c.Nome AS Nome_Cliente,
    m.Nome_Medicamento AS Nome_Medicamento,
    Data_Entrega,
    e.qtd_medicamento,
    e.lote
FROM Entrega e JOIN  Pessoa p ON e.ID_balconista = p.ID_Pessoa
JOIN  Cliente c ON e.ID_cliente = c.ID_cliente
JOIN Medicamento m ON e.ID_Medicamento_ref = m.ID_Medicamento
WHERE c.Nome LIKE %s;
        '''
        
        # Variável de parâmetro para a query
        parametro = f'{letra3}%'
        
        # Executa o comando com o parâmetro
        cursor.execute(comando, (parametro,))
        
        resultados3 = cursor.fetchall()
        
        return resultados3  
    
    except Error as e:
        print(f'Erro ao conectar ao MySQL: {e}')
        raise  # Levanta a exceção para ser tratada em outro ponto
    
    finally:
        # Fecha o cursor e a conexão se estiverem abertos
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'conexao' in locals() and conexao:
            conexao.close()

#-----------------------------------------------------------------------------------------------------------

def pesquisa_venda2(letra4):
    try:
        # Conexão ao banco de dados
        conexao = mysql.connector.connect(
            host='localhost',
            user='root',
            password='12345678',
            database='farmacia',
        )
        cursor = conexao.cursor()

        # Comando SQL com LIKE
        comando = '''
        SELECT 
    p.Nome AS Nome_Balconista,
    c.Nome AS Nome_Cliente,
    m.Nome_Medicamento AS Nome_Medicamento,
    Data_Entrega,
    e.qtd_medicamento,
    e.lote
FROM Entrega e JOIN  Pessoa p ON e.ID_balconista = p.ID_Pessoa
JOIN  Cliente c ON e.ID_cliente = c.ID_cliente
JOIN Medicamento m ON e.ID_Medicamento_ref = m.ID_Medicamento
WHERE Nome_Medicamento LIKE %s;
        '''
        
        # Variável de parâmetro para a query
        parametro = f'{letra4}%'
        
        # Executa o comando com o parâmetro
        cursor.execute(comando, (parametro,))
        
        resultados4 = cursor.fetchall()
        
        return resultados4  
    
    except Error as e:
        print(f'Erro ao conectar ao MySQL: {e}')
        raise  # Levanta a exceção para ser tratada em outro ponto
    
    finally:
        # Fecha o cursor e a conexão se estiverem abertos
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'conexao' in locals() and conexao:
            conexao.close()

#----------------------------------------------------------------------------------------------------------
#recomendação venda medicamento

def recomenda():
    try:
        # Conexão ao banco de dados
        conexao = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', '123456'),
            database=os.getenv('DB_NAME', 'farmacia'),
        )
        cursor = conexao.cursor()

        # Comando SQL para consulta
        comando = '''
        SELECT nome_medicamento FROM medicamento;
        '''
        cursor.execute(comando)

        # Processa os resultados
        resultados = cursor.fetchall()
        nomes_medicamentos = [linha[0] for linha in resultados]  # Extrai apenas os nomes

        # Retorna os nomes dos medicamentos
        return nomes_medicamentos  # Retorna uma lista simples de strings

    except Error as e:
        # Log de erro e retorno de mensagem amigável
        print(f'Erro ao conectar ao MySQL: {e}')
        return []  # Retorna uma lista vazia em caso de erro, você pode melhorar isso com mais detalhes

    finally:
        # Fecha o cursor e a conexão
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()

#----------------------------------------------------------------------------------------------------------
#recomendação venda balconista

def recomenda1():
    try:
        # Conexão ao banco de dados
        conexao = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', '123456'),
            database=os.getenv('DB_NAME', 'farmacia'),
        )
        cursor = conexao.cursor()

        # Comando SQL para consulta
        comando = '''
        SELECT nome FROM pessoa;
        '''
        cursor.execute(comando)

        # Processa os resultados
        resultados = cursor.fetchall()
        nomes_balconista = [linha[0] for linha in resultados]  # Extrai apenas os nomes

        # Retorna os nomes dos medicamentos
        return nomes_balconista  # Retorna uma lista simples de strings

    except Error as e:
        # Log de erro e retorno de mensagem amigável
        print(f'Erro ao conectar ao MySQL: {e}')
        return []  # Retorna uma lista vazia em caso de erro, você pode melhorar isso com mais detalhes

    finally:
        # Fecha o cursor e a conexão
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()

#----------------------------------------------------------------------------------------------------------
#recomendação venda cpf

def recomenda2():
    try:
        # Conexão ao banco de dados
        conexao = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', '123456'),
            database=os.getenv('DB_NAME', 'farmacia'),
        )
        cursor = conexao.cursor()

        # Comando SQL para consulta
        comando = '''
        SELECT CPF_CNPJ FROM cliente;
        '''
        cursor.execute(comando)

        # Processa os resultados
        resultados = cursor.fetchall()
        cpf = [linha[0] for linha in resultados]  # Extrai apenas os nomes

        # Retorna os nomes dos medicamentos
        return cpf  # Retorna uma lista simples de strings

    except Error as e:
        # Log de erro e retorno de mensagem amigável
        print(f'Erro ao conectar ao MySQL: {e}')
        return []  # Retorna uma lista vazia em caso de erro, você pode melhorar isso com mais detalhes

    finally:
        # Fecha o cursor e a conexão
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()

        
