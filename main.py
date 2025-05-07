from flask import Flask, request, render_template, jsonify
from dao import create, create2, create3, create4, pesquisa_cliente, pesquisa_medicamento, pesquisa_venda, pesquisa_venda2, recomenda, recomenda1, recomenda2
from dao import authenticate

app = Flask(__name__)

#--------------------------------------------------------------------------------------------------------------------
# principal

@app.route('/')
def index():
    return render_template('index.html')

#--------------------------------------------------------------------------------------------------------------------
#registro pessoa

@app.route('/register')
def register():
    return render_template('register.html')

#--------------------------------------------------------------------------------------------------------------------
#end registro pessoa

@app.route('/endcadastro')
def endcadastro():
    return render_template('endcadastro.html')

#--------------------------------------------------------------------------------------------------------------------
#registro cliente

@app.route('/adicionar_clientes')
def adicionar_clientes():
    return render_template('adicionar_clientes.html')

#--------------------------------------------------------------------------------------------------------------------
#registro medicamento

@app.route('/adicionar_medicamentos')
def adicionar_medicamentos():
    return render_template('adicionar_medicamentos.html')

#--------------------------------------------------------------------------------------------------------------------
#logado

@app.route('/logado')
def logado():
    return render_template('logado.html')

#--------------------------------------------------------------------------------------------------------------------
#registro venda

@app.route('/adicionar_venda')
def adicionar_venda():
    return render_template('adicionar_venda.html')

#--------------------------------------------------------------------------------------------------------------------
#sugestao cadastro cliente

@app.route("/suggest")
def suggest():
    query = request.args.get("query", "").lower()

    if not query:
        return jsonify({"erro": "A consulta não pode ser vazia."}), 400

    try:
        # Chama a função `recomenda` e processa os resultados
        medicamentos = recomenda()  # Recomenda retorna uma lista de medicamentos
        if not medicamentos:
            return jsonify({"suggestions": []})  # Retorna lista vazia caso não haja medicamentos

        # Filtra as sugestões
        suggestions = [med for med in medicamentos if query in med.lower()]

        return jsonify({"suggestions": suggestions})

    except Exception as e:
        print(f"Erro ao processar a solicitação: {e}")
        return jsonify({"erro": "Erro interno ao buscar medicamentos."}), 500


#--------------------------------------------------------------------------------------------------------------------
#sugestao1 cadastro - balconista

@app.route("/suggest1")
def suggest1():
    query = request.args.get("query", "").lower()

    if not query:
        return jsonify({"erro": "A consulta não pode ser vazia."}), 400

    try:
        nome_balconista = recomenda1()  # Recomenda retorna uma lista de medicamentos
        if not nome_balconista:
            return jsonify({"suggestions1": []})  # Retorna lista vazia caso não haja medicamentos

        # Filtra as sugestões
        suggestions1 = [name for name in nome_balconista if query in name.lower()]

        return jsonify({"suggestions1": suggestions1})

    except Exception as e:
        print(f"Erro ao processar a solicitação: {e}")
        return jsonify({"erro": "Erro interno ao buscar nome_balconista."}), 500
    
    #--------------------------------------------------------------------------------------------------------------------
#sugestao1 cadastro - cpf

@app.route("/suggest2")
def suggest2():
    query = request.args.get("query", "").lower()

    if not query:
        return jsonify({"erro": "A consulta não pode ser vazia."}), 400

    try:
        cpf = recomenda2()  # Recomenda retorna uma lista de medicamentos
        if not cpf:
            return jsonify({"suggestions2": []})  # Retorna lista vazia caso não haja medicamentos

        # Filtra as sugestões
        suggestions2 = [name for name in cpf if query in name.lower()]

        return jsonify({"suggestions2": suggestions2})

    except Exception as e:
        print(f"Erro ao processar a solicitação: {e}")
        return jsonify({"erro": "Erro interno ao buscar nome_balconista."}), 500
#--------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------

#login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['username']
        password = request.form['password']
        
        if authenticate(usuario, password):
            #return render_template('logado.html', usuario=usuario)
            return render_template('loginmoney.html')
        else:
            return render_template('login.html', error="Credenciais inválidas. Tente novamente.")
    
    return render_template('login.html')

#--------------------------------------------------------------------------------------------------------------------
#registro pessoa

@app.route('/submit', methods=['POST'])
def submit():
    nome = request.form['full-name']
    usuario = request.form['username']
    cpf = request.form['cpf']
    email = request.form['email']
    endereco = request.form['address']
    ocupacao = request.form['occupation']
    senha = request.form['password']

    try:
        create(nome, usuario, cpf, email, endereco, ocupacao, senha)
        mensagem = f"Cadastro realizado com sucesso! {nome}."
        return render_template('endcadastro.html', mensagem=mensagem)

    except Exception as e:
    # Verifique se o erro é uma duplicação de entrada
    
        if 'usuario' in str(e):
            mensagem = "O nome de usuário já está em uso. Escolha outro."
        elif 'CPF' in str(e):
            mensagem = "O CPF já está cadastrado no sistema."
        elif 'Email' in str(e):
            mensagem = "O e-mail já está registrado. Insira um e-mail diferente."
        else:
            mensagem = f"Ocorreu um erro inesperado: {str(e)}."
    
    # Verifique se o erro é relacionado ao número de caracteres excedente
    
        if 'usuario' in str(e):
            mensagem = "O nome de usuário já existe. Por favor, escolha outro!"
        elif 'CPF' in str(e):
            mensagem = "O CPF fornecido é inválido, já existe ou excedeu o limite de caracteres. Por favor, insira outro!"
        elif 'Email' in str(e):
            mensagem = "O e-mail fornecido excede o número máximo de caracteres permitido. Tente um e-mail mais curto."
        else:
            mensagem = f"Ocorreu um erro de tamanho de dados: {str(e)}."
    
    else:
        # Caso não seja erro de duplicidade ou de tamanho, exibe a mensagem genérica
        mensagem = f"Ocorreu um erro: {str(e)}."
    
    # Retorna a página com a mensagem de erro
    return render_template('endcadastro.html', mensagem=mensagem)

    
    
#--------------------------------------------------------------------------------------------------------------------
#registro cliente

@app.route('/submit2', methods=['POST'])
def submit2():
    nome = request.form['name']
    cpf_cnpj = request.form['cpf']
    email = request.form['email']
    endereco = request.form['address']

    try:
        create2(nome, cpf_cnpj, email, endereco)
        mensagem = f"Cadastro realizado com sucesso! {nome}."
        return render_template('endcliente.html', mensagem=mensagem)

    except Exception as e:
        mensagem = f"Ocorreu um erro: {str(e)}."
        return render_template('endcliente.html', mensagem=mensagem)
    
#--------------------------------------------------------------------------------------------------------------------
#registro medicamento

@app.route('/submit3', methods=['POST'])
def submit3():
    Nome_medicamento = request.form['Nome_medicamento']
    nome_generico = request.form['nome_generico']
    categoria = request.form['categoria']
    distribuidor = request.form['distribuidor']
    data_validade = request.form['data_validade']
    Preco = request.form['Preco']

    try:
        create3(Nome_medicamento , nome_generico, categoria, distribuidor, data_validade, Preco)
        mensagem = f"Cadastro realizado com sucesso! {Nome_medicamento}."
        return render_template('endcliente.html', mensagem=mensagem)
    
    except Exception as e:
        mensagem = f"Ocorreu um erro: {str(e)}."
        return render_template('endcliente.html', mensagem=mensagem)
    
#--------------------------------------------------------------------------------------------------------------------
#registro venda

@app.route('/submit4', methods=['POST'])
def submit4():
    balconista = request.form['balconista']
    cpf_cliente = request.form['cpf_cliente']
    data_venda = request.form['data_venda']
    medicamento = request.form['medicamento']
    qtd = request.form['qtd']
    lote = request.form['lote']

    try:
        create4(balconista, cpf_cliente, data_venda, medicamento, qtd, lote)
        mensagem = f"Cadastro realizado com sucesso! {data_venda}"
        return render_template('endcliente.html', mensagem=mensagem)

    except Exception as e:
        mensagem = f"Ocorreu um erro: {str(e)}."
        return render_template('endcliente.html', mensagem=mensagem)
    
#--------------------------------------------------------------------------------------------------------------------
#pesquisar cliente

@app.route('/pesquisar_cliente', methods=['POST'])
def pesquisar_cliente():
    data = request.get_json()  # Captura o JSON enviado
    letra = data['letra']  # Extrai o valor da letra
    resultados = pesquisa_cliente(letra)  # Chama a função de pesquisa no banco de dados
    
    resultados_formatados = [{'nome': cliente[0]} for cliente in resultados]

    return jsonify(resultados=resultados_formatados) 

#--------------------------------------------------------------------------------------------------------------------
#pesquisar medicamento

@app.route('/pesquisar_medicamento', methods=['POST'])
def pesquisar_medicamento():
    data = request.get_json()  # Captura o JSON enviado
    letra2 = data['letra2']  # Extrai o valor da letra
    resultados2 = pesquisa_medicamento(letra2)  # Chama a função de pesquisa no banco de dados
    
    resultados2_formatados = [{'nome_medicamento': medicamento[0]} for medicamento in resultados2]

    return jsonify(resultados2=resultados2_formatados) 



#--------------------------------------------------------------------------------------------------------------------
@app.route('/aplicacoes-financeiras')
def aplicacoes_financeiras():
    return render_template('aplicacoes-financeiras.html')

@app.route('/')
def home():  # Mudamos o nome de 'index' para 'home'
    return render_template('index.html')

#pesquisar venda

@app.route('/pesquisar_venda', methods=['POST'])
def pesquisar_venda():
    data = request.get_json()  # Captura o JSON enviado
    letra3 = data['letra3']  # Extrai o valor da letra
    resultados3 = pesquisa_venda(letra3)  # Chama a função de pesquisa no banco de dados

    resultados3_formatados = [
        {
            'Nome_Balconista': venda[0], 
            'Nome_Cliente': venda[1], 
            'Nome_Medicamento': venda[2], 
            'Data_Entrega': venda[3],       
            'qtd_medicamento': venda[4],  
            'lote': venda[5],   
        }
        for venda in resultados3
    ]

    return jsonify(resultados3=resultados3_formatados) 

#--------------------------------------------------------------------------------------------------------------------

#pesquisar venda medicamento

@app.route('/pesquisar_venda2', methods=['POST'])
def pesquisar_venda2():
    data = request.get_json()  # Captura o JSON enviado
    letra4 = data['letra4']  # Extrai o valor da letra
    resultados4 = pesquisa_venda2(letra4)  # Chama a função de pesquisa no banco de dados
    
    resultados4_formatados = [
        {
            'Nome_Balconista': venda[0], 
            'Nome_Cliente': venda[1], 
            'Nome_Medicamento': venda[2], 
            'Data_Entrega': venda[3],       
            'qtd_medicamento': venda[4],  
            'lote': venda[5],   
        }
        for venda in resultados4
    ]

    return jsonify(resultados4=resultados4_formatados) 

#--------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    app.run(debug=True)
