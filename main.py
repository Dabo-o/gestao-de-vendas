from flask import Flask, render_template, request, redirect, url_for
from database import session, db, Base
from models.cliente import Cliente
from models.produto import Produto
from models.venda import Venda
from datetime import date

app = Flask(__name__)
Base.metadata.create_all(bind=db)

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/clientes/adicionar", methods=["POST"])
def adicionar_cliente():
    nome = request.form["nome"]
    email = request.form["email"]
    telefone = request.form["telefone"]
    novo_cliente = Cliente(nome=nome,email=email,telefone=telefone)
    session.add(novo_cliente)
    session.commit()
    return redirect(url_for("listar_clientes"))
    

@app.route("/clientes")
def listar_clientes():
    filtro_nome = request.args.get("filtro_nome", "")
    filtro_email = request.args.get("filtro_email", "")
    if filtro_nome:
        clientes = session.query(Cliente).filter(Cliente.nome.contains(filtro_nome)).all()
    elif filtro_email:
        clientes = session.query(Cliente).filter(Cliente.email.contains(filtro_email)).all()
    else:
        clientes = session.query(Cliente).all()


    return render_template("clientes.html", clientes=clientes)


@app.route("/clientes/excluir/<int:cliente_id>")
def excluir_cliente(cliente_id):
    cliente = session.query(Cliente).filter_by(id=cliente_id).first()
    if cliente:
        session.delete(cliente)
        session.commit()
        return redirect(url_for("listar_clientes"))

# CRUD para Produtos
@app.route("/produtos/adicionar", methods =["POST"])
def adicionar_produto():
    nome = request.form["nome"]
    preco = request.form["preco"]
    estoque = request.form["estoque"]
    novo_produto = Produto(nome=nome,preco=float(preco),estoque=int(estoque))
    session.add(novo_produto)
    session.commit()
    return redirect(url_for("listar_produtos"))
    
@app.route("/produtos", methods=["GET"])
def listar_produtos():
    filtro_nome = request.args.get("filtro_nome", "")

    if filtro_nome:
        produtos = session.query(Produto).filter(Produto.nome.ilike(f"%{filtro_nome}%")).all()
    else:
        produtos = session.query(Produto).all()

    return render_template("produtos.html", produtos=produtos)

@app.route("/editar_produto/<int:id>", methods=["GET", "POST"])
def editar_produto(id):
    produto = session.query(Produto).get(id)

    if request.method == "POST":
        produto.nome = request.form["nome"]
        produto.preco = float(request.form["preco"])
        produto.estoque = int(request.form["estoque"])
        session.commit()
        return redirect(url_for("listar_produtos"))

    return render_template("editar_produto.html", produto=produto)
        
@app.route("/produtos/excluir/<int:produto_id>")
def excluir_produto(produto_id):
    produto = session.query(Produto).filter_by(id=produto_id).first()
    if produto:
        session.delete(produto)
        session.commit()
    return redirect(url_for("listar_produtos"))

# CRUD para Vendas
@app.route("/vendas/adicionar", methods=["POST"])
def adicionar_venda():
    cliente_id = request.form["cliente_id"]
    produto_id = request.form["produto_id"]
    quantidade = int(request.form["quantidade"])
    data_venda = date.today()

    # Busca o produto no banco
    produto = session.query(Produto).get(produto_id)

    if produto and produto.estoque >= quantidade:
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

@app.route("/vendas", methods =["GET"])
def listar_vendas():
    cliente_nome = request.args.get("cliente_nome", "").strip()
    produto_nome = request.args.get("produto_nome", "").strip()
    quantidade = request.args.get("quantidade", "").strip()
    data_venda = request.args.get("data_venda", "").strip()

    vendas_query = session.query(Venda)   

    if data_venda:
        vendas_query = vendas_query.filter(Venda.data_venda == data_venda)

    vendas = vendas_query.all()
    resultado = []

    for venda in vendas:
        cliente = session.query(Cliente).filter_by(id=venda.cliente_id).first()
        produto = session.query(Produto).filter_by(id=venda.produto_id).first()

        if cliente_nome and (not cliente or cliente_nome.lower() not in cliente.nome.lower()):
            continue

        if produto_nome and (not produto or produto_nome.lower() not in produto.nome.lower()):
            continue

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

@app.route("/vendas/excluir/<int:venda_id>")
def excluir_venda(venda_id):
    venda = session.query(Venda).filter_by(id=venda_id).first()
    produto = session.query(Produto).filter_by(id=venda.produto_id).first()
    if venda:
        produto.estoque += venda.quantidade
        session.delete(venda)
        session.commit()
    return redirect(url_for("listar_vendas"))

if __name__ == "__main__":
    app.run(debug=True)

