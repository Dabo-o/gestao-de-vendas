# Importação das Funções principais do Flask
from flask import Flask, render_template, request, redirect, url_for
# Importação de ferramentas para conectar e manipular o banco de dados
from database import session, db, Base 
# Importação dos modelos das tabelas do banco
from models.cliente import Cliente
from models.produto import Produto
from models.venda import Venda
# Importação da função para trabalhar com datas
from datetime import date

app = Flask(__name__) # Inicia o Flask
Base.metadata.create_all(bind=db) # Cria as tabelas no banco de dados

# Criação da rota da página principal
@app.route('/')
def index():
    return render_template("index.html")

# Criação da rota para ADICIONAR Clientes (Crud)
@app.route("/clientes/adicionar", methods=["POST"]) # Define a rota, e o método POST(Usado para enviar dados)
def adicionar_cliente(): # Cria a função de cadastrar clientes
    nome = request.form["nome"] # Variável que vai receber o valor inserido no formulário nome
    email = request.form["email"] # Variável que vai receber o valor inserido no formulário email
    telefone = request.form["telefone"] # Variável que vai receber o valor inserido no formulário telefone
    novo_cliente = Cliente(nome=nome,email=email,telefone=telefone) # Variável da classe Cliente que recebe esses valores
    session.add(novo_cliente) # Adiciona essa variável
    session.commit() # Confirma e salva as alterações no banco de dados
    return redirect(url_for("listar_clientes")) # Redireciona para a página de listagem de clientes
    
# Criação da rota para LISTAR Clientes (cRud)
@app.route("/clientes") # Define a rota (Método GET)
def listar_clientes(): # Função responsável por retornar a lista de clientes, com ou sem filtros

    filtro_nome = request.args.get("filtro_nome", "") # Variável utilizada para busca filtrada, que recebe o valor do filtro nome
    filtro_email = request.args.get("filtro_email", "") # Variável utilizada para busca filtrada, que recebe o valor do filtro email

    if filtro_nome: # Aplica filtro por nome, Se existir
        clientes = session.query(Cliente).filter(Cliente.nome.ilike(f"%{filtro_nome}%")).all() # Lista os clientes com o filtro_nome
    elif filtro_email: # Aplica filtro por email, Se existir
        clientes = session.query(Cliente).filter(Cliente.email.ilike(f"%{filtro_email}%")).all() # Lista os clientes com o filtro_email
    else: # Se não tiver filtros ele cai aqui
        clientes = session.query(Cliente).all() # Lista todos os clientes (sem filtro)


    return render_template("clientes.html", clientes=clientes) # Envia a lista para o template "clientes.html" pela variável 'clientes'

# Criação da rota para Excluir Clientes (cruD)
@app.route("/clientes/excluir/<int:cliente_id>") # Define a rota e um parametro que recebe o ID de um cliente
def excluir_cliente(cliente_id): 
    cliente = session.query(Cliente).filter_by(id=cliente_id).first() # Busca o cliente pelo ID
    if cliente: 
        session.delete(cliente) # Deleta esse cliente com id correspondente
        session.commit() # Confirma e salva as alterações no banco
        return redirect(url_for("listar_clientes")) # Redireciona para a página de listagem

# Criação da rota para Adicionar Produtos (Crud)
@app.route("/produtos/adicionar", methods =["POST"])
def adicionar_produto():
    nome = request.form["nome"]
    preco = request.form["preco"]
    estoque = request.form["estoque"]
    novo_produto = Produto(nome=nome,preco=float(preco),estoque=int(estoque))
    session.add(novo_produto)
    session.commit()
    return redirect(url_for("listar_produtos"))
    
# Criação da rota para Listar Produtos (cRud)
@app.route("/produtos", methods=["GET"])
def listar_produtos():
    filtro_nome = request.args.get("filtro_nome", "")

    if filtro_nome:
        produtos = session.query(Produto).filter(Produto.nome.ilike(f"%{filtro_nome}%")).all()
    else:
        produtos = session.query(Produto).all()

    return render_template("produtos.html", produtos=produtos)

# Criação da rota para Editar Produtos (crUd)
@app.route("/editar_produto/<int:id>", methods=["GET", "POST"]) # Define a rota com os métodos GET e POST
def editar_produto(id):
    produto = session.query(Produto).get(id) # Recebe um produto com o id correspondente (Utiliza o GET)

    if request.method == "POST": # Utiliza o POST para atualizar registros
        produto.nome = request.form["nome"] # Altera o campo nome
        produto.preco = float(request.form["preco"]) # Altera o campo preço
        produto.estoque = int(request.form["estoque"]) # Altera o campo estoque
        session.commit() # Salva as alterações no banco
        return redirect(url_for("listar_produtos")) # Redireciona para a listagem de alunos

    return render_template("editar_produto.html", produto=produto) # Exibe o formulário de edição com os dados atuais do produto

# Criação da rota para EXCLUIR Produtos (cruD)        
@app.route("/produtos/excluir/<int:produto_id>")
def excluir_produto(produto_id):
    produto = session.query(Produto).filter_by(id=produto_id).first()
    if produto:
        session.delete(produto)
        session.commit()
    return redirect(url_for("listar_produtos"))

# Criação da rota para ADICIONAR Vendas (Crud)
@app.route("/vendas/adicionar", methods=["POST"])
def adicionar_venda():
    cliente_id = request.form["cliente_id"]
    produto_id = request.form["produto_id"]
    quantidade = int(request.form["quantidade"])
    data_venda = date.today() # Cria uma variável pra receber a data atual

    # Busca o produto no banco
    produto = session.query(Produto).get(produto_id)

    if produto and produto.estoque >= quantidade: # Verifica se tem estoque disponível do produto
        # Cria a venda
        nova_venda = Venda(
            cliente_id=cliente_id, 
            produto_id=produto_id,
            quantidade=quantidade,
            data_venda=data_venda
        )

        # Atualiza o estoque
        produto.estoque -= quantidade

        session.add(nova_venda)
        session.commit()
        return redirect(url_for("listar_vendas"))
    else:
        return "Erro: Estoque insuficiente para realizar a venda.", 400

# Criação da rota para LISTAR Vendas (cRud)
@app.route("/vendas", methods =["GET"])
def listar_vendas():
    cliente_nome = request.args.get("cliente_nome", "").strip()
    produto_nome = request.args.get("produto_nome", "").strip()
    quantidade = request.args.get("quantidade", "").strip()
    data_venda = request.args.get("data_venda", "").strip()

    if data_venda:
        vendas = session.query(Venda).filter(Venda.data_venda == data_venda).all()
    else:
        vendas = session.query(Venda).all()

    resultado = []

# Percorre todas as vendas
    for venda in vendas:
        cliente = session.query(Cliente).filter_by(id=venda.cliente_id).first()
        produto = session.query(Produto).filter_by(id=venda.produto_id).first()
# Verifica se filtro condiz com algum registro
        if cliente_nome and (not cliente or cliente_nome.lower() not in cliente.nome.lower()):
            continue

        if produto_nome and (not produto or produto_nome.lower() not in produto.nome.lower()):
            continue

# Monta um dicionário com os dados formatados, e retorna uma mensagem de erro se necessário
        resultado.append({
            "id": venda.id,
            "cliente_nome": cliente.nome if cliente else "Cliente não encontrado",
            "produto_nome": produto.nome if produto else "Produto não encontrado",
            "cliente_id": cliente.id if cliente else "N/A",
            "produto_id": produto.id if produto else "N/A",
            "quantidade": venda.quantidade,
            "data_venda": venda.data_venda
    })


    return render_template("vendas.html", vendas=resultado) 

# Criação da rota para EXCLUIR Vendas (cruD)
@app.route("/vendas/excluir/<int:venda_id>")
def excluir_venda(venda_id):
    venda = session.query(Venda).filter_by(id=venda_id).first()
    produto = session.query(Produto).filter_by(id=venda.produto_id).first() # Acessa o ID do produto relacionado a venda
    if venda:
        produto.estoque += venda.quantidade # Adiciona a quantidade de volta ao estoque em caso de exclusão de venda
        session.delete(venda)
        session.commit()
    return redirect(url_for("listar_vendas"))

# Inicia o servidor flask
if __name__ == "__main__":
    app.run(debug=True)

