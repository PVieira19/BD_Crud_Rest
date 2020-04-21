from flask import Flask, render_template, request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from datetime import timedelta
from pprint import pprint
from sqlalchemy.sql import text as SQLQuery
import os
from datetime import date


app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost/ultima'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db=SQLAlchemy(app)


class Alergias(db.Model):
    __tablename__ = 'alergias'
    codigoalerg=db.Column(db.Integer, primary_key=True)
    designacao=db.Column(db.String(30),  nullable=False)

    def __init__(self, designacao):
        self.designacao=designacao


class Clientes(db.Model):
    __tablename__ = 'clientes'
    codigocli=db.Column(db.Integer, primary_key=True)
    nome=db.Column(db.String(20), nullable=False)
    NIF=db.Column(db.Integer, nullable=False)

    def __init__(self, nome, NIF):
        self.nome=nome
        self.NIF=NIF


class Locais(db.Model):
    __tablename__ = 'locais'
    codigoloc=db.Column(db.Integer, primary_key=True)
    designacao=db.Column(db.String(30), nullable=False)

    def __init__(self, designacao):
        self.designacao=designacao


class Restaurantes(db.Model):
    __tablename__ = 'restaurantes'
    codigorest=db.Column(db.Integer, primary_key=True)
    codigoloc=db.Column(db.Integer, db.ForeignKey('locais.codigoloc'), nullable=False)
    contacto=db.Column(db.String(30), nullable=False)
    contacto=db.Column(db.String(50), nullable=False)

    def __init__(self, codigoloc,designacao,contacto):
        self.codigoloc=codigoloc
        self.designacao=designacao
        self.contacto=contacto

class Funcionarios(db.Model):
    __tablename__ = 'funcionarios'
    codigofunc=db.Column(db.Integer, primary_key=True)
    nome=db.Column(db.String(20), nullable=False)
    contacto=db.Column(db.String(50), nullable=False)
    salario=db.Column(db.Integer, nullable=False)

    def __init__(self, nome,contacto,salario):
        self.nome=nome
        self.contacto=contacto
        self.salario=salario


class LocaisCons(db.Model):
    __tablename__ = 'locaiscons'
    codigolocaiscons=db.Column(db.Integer, primary_key=True)
    codigofunc=db.Column(db.Integer, db.ForeignKey('funcionarios.codigofunc') ,nullable=False)
    codigorest=db.Column(db.Integer, db.ForeignKey('restaurantes.codigorest') ,nullable=False)
    designacao=db.Column(db.String(30), nullable=False)

    def __init__(self, codigofunc,codigorest,designacao):
        self.codigofunc=codigofunc
        self.codigorest=codigorest
        self.designacao=designacao


class LocaisConsClientes(db.Model):
    __tablename__ = 'locaisconsclientes'
    codigolocaiscons=db.Column(db.Integer, db.ForeignKey('locaiscons.codigolocaiscons') ,primary_key=True)
    codigocli=db.Column(db.Integer, db.ForeignKey('clientes.codigocli') ,primary_key=True)

    def __init__(self, codigolocaiscons,codigocli):
        self.codigolocaiscons=codigolocaiscons
        self.codigocli=codigocli


class Consumo(db.Model):
    __tablename__ = 'consumo'
    codigoconsumo=db.Column(db.Integer, primary_key=True)
    codigofunc=db.Column(db.Integer, db.ForeignKey('funcionarios.codigofunc') , nullable=False)
    codigolocaiscons=db.Column(db.Integer, db.ForeignKey('locaiscons.codigolocaiscons'), nullable=False)
    data=db.Column(db.Date, nullable=False)

    def __init__(self, codigofunc,codigolocaiscons,data):
        self.codigofunc=codigofunc
        self.codigolocaiscons=codigolocaiscons
        self.data=data


class TiposEmentas(db.Model):
    __tablename__ = 'tiposementas'
    codigotipoement=db.Column(db.Integer, primary_key=True)
    designacao=db.Column(db.String(30), nullable=False)

    def __init__(self, designacao):
        self.designacao=designacao


class TiposRef(db.Model):
    __tablename__ = 'tiposref'
    codigotiporef=db.Column(db.Integer, primary_key=True)
    designacao=db.Column(db.String(30), nullable=False)

    def __init__(self, designacao):
        self.designacao=designacao


class Ementas(db.Model):
    __tablename__ = 'ementas'
    codigoementa=db.Column(db.Integer, primary_key=True)
    codigotiporef=db.Column(db.Integer, db.ForeignKey('tiposref.codigotiporef') , nullable=False)
    codigotipoement=db.Column(db.Integer, db.ForeignKey('tiposementas.codigotipoement') , nullable=False)
    data=db.Column(db.Date, nullable=False)

    def __init__(self, codigotiporef, codigotipoement, data):
        self.codigotiporef=codigotiporef
        self.codigotipoement=codigotipoement
        self.data=data


class TiposItem(db.Model):
    __tablename__ = 'tipositem'
    codigotipoitem=db.Column(db.Integer, primary_key=True)
    designacao=db.Column(db.String(30), nullable=False)

    def __init__(self, designacao):
        self.designacao=designacao


class Items(db.Model):
    __tablename__ = 'items'
    codigoitems=db.Column(db.Integer, primary_key=True)
    codigotipoitem=db.Column(db.Integer, db.ForeignKey('tipositem.codigotipoitem') ,nullable=False)
    designacao=db.Column(db.String(30), nullable=False)
    custo=db.Column(db.Float, nullable=False)

    def __init__(self, codigotipoitem, designacao, custo):
        self.codigotipoitem=codigotipoitem
        self.designacao=designacao
        self.custo=custo

class RestaurantesEmentas(db.Model):
    __tablename__ = 'restaurantesementas'
    codigorest=db.Column(db.Integer, db.ForeignKey('restaurantes.codigorest') ,primary_key=True)
    codigoementa=db.Column(db.Integer, db.ForeignKey('ementas.codigoementa') ,primary_key=True)

    def __init__(self, codigorest,codigoementa):
        self.codigorest=codigorest
        self.codigoementa=codigoementa


class EmentasItems(db.Model):
    __tablename__ = 'ementasitems'
    codigoementa=db.Column(db.Integer, db.ForeignKey('ementas.codigoementa') ,primary_key=True)
    codigoitems=db.Column(db.Integer, db.ForeignKey('items.codigoitems') ,primary_key=True)

    def __init__(self, codigoementa,codigoitems):
        self.codigoementa=codigoementa
        self.codigoitems=codigoitems

class ItemsAlergias(db.Model):
    __tablename__ = 'itemsalergias'
    codigoitems=db.Column(db.Integer, db.ForeignKey('items.codigoitems') ,primary_key=True)
    codigoalerg=db.Column(db.Integer, db.ForeignKey('alergias.codigoalerg') ,primary_key=True)

    def __init__(self, codigoitems,codigoalerg):
        self.codigoitems=codigoitems
        self.codigoalerg=codigoalerg

class ConsumoItems(db.Model):
    __tablename__ = 'consimoitems'
    codigoconsumo=db.Column(db.Integer, db.ForeignKey('consumo.codigoconsumo') ,primary_key=True)
    codigoitems=db.Column(db.Integer, db.ForeignKey('items.codigoitems') ,primary_key=True)
    estado=db.Column(db.Integer, nullable=False)
    quantidade=db.Column(db.Integer, nullable=False)

    def __init__(self, codigoconsumo,codigoitems,estado,quantidade):
        self.codigoconsumo=codigoconsumo
        self.codigoitems=codigoitems
        self.estado=estado
        self.quantidade=quantidade

class ClientesLocaisCons(db.Model):
    __tablename__ = 'clienteslocaiscons'
    codigocli=db.Column(db.Integer, db.ForeignKey('clientes.codigocli') ,primary_key=True)
    codigolocaiscons=db.Column(db.Integer, db.ForeignKey('locaiscons.codigolocaiscons') ,primary_key=True)

    def __init__(self, codigocli,codigolocaiscons):
        self.codigocli=codigocli
        self.codigolocaiscons=codigolocaiscons

RestauranteFinal = 15

@app.route('/')
def index():
    dadosRestaurantes=db.engine.execute("Select * from view_restaurantes")
    return render_template('index.html',dadosRestaurantes=dadosRestaurantes)

@app.route('/novo', methods=['POST'])
def novo():
    global RestauranteFinal
    RestauranteFinal = request.form['Escolha_Local']
    return render_template('novo.html')

@app.route('/novo1',)
def novo1():
    return render_template('novo.html')

@app.route('/ementa')
def ementa():
    return render_template('ementa.html')

@app.route('/mesa')
def mesa():
    return render_template('mesa.html')

@app.route('/funcionarios')
def funcionarios():
    return render_template('funcionarios.html')

@app.route('/alergias')
def alergias():
    dados=db.engine.execute("SELECT * FROM view_alergias order by designacao")
    return render_template('alergias.html',dados=dados)

@app.route('/updatealergias',methods=['POST','GET'])
def updatealergias():

    id_data=request.form['id']
    teste=request.form['designacao2']
    db.session.execute("CALL proc_ja_da(" + str(id_data) + ",'" + str(teste) + "')")
    db.session.commit()
    dados=db.engine.execute("SELECT * FROM view_alergias order by designacao")
    return render_template('alergias.html',dados=dados)


@app.route('/adicionaralergias', methods=['POST','GET'])
def adicionaralergias():

    nome=request.form['designacao1']

    db.session.execute("CALL proc_adicionar_alerg('" + str(nome) + "')")
    db.session.commit()
    dados=db.engine.execute("SELECT * FROM view_alergias order by designacao")
    return render_template('alergias.html',dados=dados)

@app.route('/eliminaralergias/<string:id_data>', methods=['GET'])
def eliminaralergias(id_data):
    db.session.execute("CALL proc_apaga_alergias (" + str(id_data) + ")")
    db.session.commit()
    dados=db.engine.execute("SELECT * FROM view_alergias order by designacao")
    return render_template('alergias.html',dados=dados)

@app.route('/estatisticas')
def estatisticas():
    return render_template('estatisticas.html')


@app.route('/mesa1')
def mesa1():
    dadosEntradas=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa=db.engine.execute("SELECT * FROM view_sobremesas")

    dadosEntradas2=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne2=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes2=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas2=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa2=db.engine.execute("SELECT * FROM view_sobremesas")

    valor1=int(RestauranteFinal)

    minha = db.engine.execute("Select codigolocaiscons from view_mesa_restaurante where codigorest=%s",valor1)
    
    amounts = minha
    for teste, id_mesa in enumerate(amounts):
        if teste==0:
            dadostabela = db.engine.execute("Select * from view_consumo, view_consumo_items, view_items where view_consumo.codigoconsumo=view_consumo_items.codigoconsumo and view_items.codigoitems=view_consumo_items.codigoitems and view_consumo.codigolocaiscons= %s ORDER BY designacao;", id_mesa)

    return render_template('mesa1.html',dadostabela=dadostabela,dadosEntradas=dadosEntradas,dadosCarne=dadosCarne,dadosBebidas=dadosBebidas,dadosPeixes=dadosPeixes,dadosSobremesa=dadosSobremesa,dadosEntradas2=dadosEntradas2,dadosCarne2=dadosCarne2,dadosBebidas2=dadosBebidas2,dadosPeixes2=dadosPeixes2,dadosSobremesa2=dadosSobremesa2)

@app.route('/mesa2')
def mesa2():


    dadosEntradas=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa=db.engine.execute("SELECT * FROM view_sobremesas")

    dadosEntradas2=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne2=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes2=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas2=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa2=db.engine.execute("SELECT * FROM view_sobremesas")

    valor1=int(RestauranteFinal)

    minha = db.engine.execute("Select codigolocaiscons from view_mesa_restaurante where codigorest=%s",valor1)
    
    amounts = minha
    for teste, id_mesa in enumerate(amounts):
        if teste==1:
            dadostabela = db.engine.execute("Select * from view_consumo, view_consumo_items, view_items where view_consumo.codigoconsumo=view_consumo_items.codigoconsumo and view_items.codigoitems=view_consumo_items.codigoitems and view_consumo.codigolocaiscons= %s ORDER BY designacao", id_mesa)

    return render_template('mesa2.html',dadostabela=dadostabela,dadosEntradas=dadosEntradas,dadosCarne=dadosCarne,dadosBebidas=dadosBebidas,dadosPeixes=dadosPeixes,dadosSobremesa=dadosSobremesa,dadosEntradas2=dadosEntradas2,dadosCarne2=dadosCarne2,dadosBebidas2=dadosBebidas2,dadosPeixes2=dadosPeixes2,dadosSobremesa2=dadosSobremesa2)

@app.route('/mesa3')
def mesa3():

    dadosEntradas=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa=db.engine.execute("SELECT * FROM view_sobremesas")

    dadosEntradas2=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne2=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes2=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas2=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa2=db.engine.execute("SELECT * FROM view_sobremesas")

    valor1=int(RestauranteFinal)

    minha = db.engine.execute("Select codigolocaiscons from view_mesa_restaurante where codigorest=%s ",valor1)
    
    amounts = minha
    for teste, id_mesa in enumerate(amounts):
        if teste==2:
            dadostabela = db.engine.execute("Select * from view_consumo, view_consumo_items, view_items where view_consumo.codigoconsumo=view_consumo_items.codigoconsumo and view_items.codigoitems=view_consumo_items.codigoitems and view_consumo.codigolocaiscons= %s ORDER BY designacao", id_mesa)

    return render_template('mesa3.html',dadostabela=dadostabela,dadosEntradas=dadosEntradas,dadosCarne=dadosCarne,dadosBebidas=dadosBebidas,dadosPeixes=dadosPeixes,dadosSobremesa=dadosSobremesa,dadosEntradas2=dadosEntradas2,dadosCarne2=dadosCarne2,dadosBebidas2=dadosBebidas2,dadosPeixes2=dadosPeixes2,dadosSobremesa2=dadosSobremesa2)

@app.route('/mesa4')
def mesa4():

    dadosEntradas=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa=db.engine.execute("SELECT * FROM view_sobremesas")

    dadosEntradas2=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne2=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes2=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas2=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa2=db.engine.execute("SELECT * FROM view_sobremesas")

    valor1=int(RestauranteFinal)

    minha = db.engine.execute("Select codigolocaiscons from view_mesa_restaurante where codigorest=%s ",valor1)
    
    amounts = minha
    for teste, id_mesa in enumerate(amounts):
        if teste==3:
            dadostabela = db.engine.execute("Select * from view_consumo, view_consumo_items, view_items where view_consumo.codigoconsumo=view_consumo_items.codigoconsumo and view_items.codigoitems=view_consumo_items.codigoitems and view_consumo.codigolocaiscons= %s ORDER BY designacao", id_mesa)

    return render_template('mesa4.html',dadostabela=dadostabela,dadosEntradas=dadosEntradas,dadosCarne=dadosCarne,dadosBebidas=dadosBebidas,dadosPeixes=dadosPeixes,dadosSobremesa=dadosSobremesa,dadosEntradas2=dadosEntradas2,dadosCarne2=dadosCarne2,dadosBebidas2=dadosBebidas2,dadosPeixes2=dadosPeixes2,dadosSobremesa2=dadosSobremesa2)

@app.route('/mesa5')
def mesa5():

    dadosEntradas=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa=db.engine.execute("SELECT * FROM view_sobremesas")

    dadosEntradas2=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne2=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes2=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas2=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa2=db.engine.execute("SELECT * FROM view_sobremesas")

    valor1=int(RestauranteFinal)

    minha = db.engine.execute("Select codigolocaiscons from view_mesa_restaurante where codigorest=%s ",valor1)
    
    amounts = minha
    for teste, id_mesa in enumerate(amounts):
        if teste==4:
            dadostabela = db.engine.execute("Select * from view_consumo, view_consumo_items, view_items where view_consumo.codigoconsumo=view_consumo_items.codigoconsumo and view_items.codigoitems=view_consumo_items.codigoitems and view_consumo.codigolocaiscons= %s ORDER BY designacao", id_mesa)

    return render_template('mesa5.html',dadostabela=dadostabela,dadosEntradas=dadosEntradas,dadosCarne=dadosCarne,dadosBebidas=dadosBebidas,dadosPeixes=dadosPeixes,dadosSobremesa=dadosSobremesa,dadosEntradas2=dadosEntradas2,dadosCarne2=dadosCarne2,dadosBebidas2=dadosBebidas2,dadosPeixes2=dadosPeixes2,dadosSobremesa2=dadosSobremesa2)

@app.route('/mesa6')
def mesa6():

    dadosEntradas=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa=db.engine.execute("SELECT * FROM view_sobremesas")

    dadosEntradas2=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne2=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes2=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas2=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa2=db.engine.execute("SELECT * FROM view_sobremesas")

    valor1=int(RestauranteFinal)

    minha = db.engine.execute("Select codigolocaiscons from view_mesa_restaurante where codigorest=%s ",valor1)
    
    amounts = minha
    for teste, id_mesa in enumerate(amounts):
        if teste==5:
            dadostabela = db.engine.execute("Select * from view_consumo, view_consumo_items, view_items where view_consumo.codigoconsumo=view_consumo_items.codigoconsumo and view_items.codigoitems=view_consumo_items.codigoitems and view_consumo.codigolocaiscons= %s ORDER BY designacao", id_mesa)

    return render_template('mesa6.html',dadostabela=dadostabela,dadosEntradas=dadosEntradas,dadosCarne=dadosCarne,dadosBebidas=dadosBebidas,dadosPeixes=dadosPeixes,dadosSobremesa=dadosSobremesa,dadosEntradas2=dadosEntradas2,dadosCarne2=dadosCarne2,dadosBebidas2=dadosBebidas2,dadosPeixes2=dadosPeixes2,dadosSobremesa2=dadosSobremesa2)

@app.route('/mesa7')
def mesa7():

    dadosEntradas=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa=db.engine.execute("SELECT * FROM view_sobremesas")

    dadosEntradas2=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne2=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes2=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas2=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa2=db.engine.execute("SELECT * FROM view_sobremesas")

    valor1=int(RestauranteFinal)

    minha = db.engine.execute("Select codigolocaiscons from view_mesa_restaurante where codigorest=%s ",valor1)
    
    amounts = minha
    for teste, id_mesa in enumerate(amounts):
        if teste==6:
            dadostabela = db.engine.execute("Select * from view_consumo, view_consumo_items, view_items where view_consumo.codigoconsumo=view_consumo_items.codigoconsumo and view_items.codigoitems=view_consumo_items.codigoitems and view_consumo.codigolocaiscons= %s ORDER BY designacao", id_mesa)

    return render_template('mesa7.html',dadostabela=dadostabela,dadosEntradas=dadosEntradas,dadosCarne=dadosCarne,dadosBebidas=dadosBebidas,dadosPeixes=dadosPeixes,dadosSobremesa=dadosSobremesa,dadosEntradas2=dadosEntradas2,dadosCarne2=dadosCarne2,dadosBebidas2=dadosBebidas2,dadosPeixes2=dadosPeixes2,dadosSobremesa2=dadosSobremesa2)


@app.route('/itens')
def itens():
    return render_template('itens.html',)

@app.route('/itens_entradas')
def itens_entradas():
    alergias=db.engine.execute("SELECT * FROM alergias")
    dados=db.engine.execute("Select * from view_entradas")
    return render_template('itens_entradas.html',dados=dados,alergias=alergias)

@app.route('/itens_pratos_carne')
def itens_pratos_carne():
    alergias=db.engine.execute("SELECT * FROM alergias")
    dados=db.engine.execute("Select * from view_carne")
    return render_template('itens_pratos_carne.html',dados=dados,alergias=alergias)

@app.route('/itens_pratos_peixe')
def itens_pratos_peixe():
    alergias=db.engine.execute("SELECT * FROM alergias")
    dados=db.engine.execute("Select * from view_peixe")
    return render_template('itens_pratos_peixe.html',dados=dados,alergias=alergias)

@app.route('/itens_bebidas')
def itens_bebidas():
    alergias=db.engine.execute("SELECT * FROM alergias")
    dados=db.engine.execute("Select * from view_bebidas")
    return render_template('itens_bebidas.html',dados=dados,alergias=alergias)

@app.route('/itens_sobremesas')
def itens_sobremesas():
    alergias=db.engine.execute("SELECT * FROM alergias")
    dados=db.engine.execute("Select * from view_sobremesas")
    return render_template('itens_sobremesas.html',dados=dados,alergias=alergias)

@app.route('/adicionarementa')
def adicionarementa():
    dados=db.engine.execute("Select * from view_items")
    tipos = db.session.execute("Select * from view_tipos_ementas")
    return render_template('adicionarementa.html', dados=dados, tipos=tipos)

@app.route('/adicionarmesa')
def adicionarmesa():
    dados=db.engine.execute("SELECT * FROM view_tipos_ementas")
    dadosEntradas=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa=db.engine.execute("SELECT * FROM view_sobremesas")

    return render_template('adicionarmesa.html', dados=dados,dadosCarne=dadosCarne,dadosEntradas=dadosEntradas,dadosPeixes=dadosPeixes,dadosBebidas=dadosBebidas,dadosSobremesa=dadosSobremesa)

@app.route('/editartipoementa')
def editartipoementa():
    dados = db.session.execute("SELECT * FROM view_tipos_ementas")
    return render_template('editartipoementa.html', dados=dados)
                           
@app.route('/novoprato/<string:id_data>')
def novoprato(id_data):
    dadosEntradas=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa=db.engine.execute("SELECT * FROM view_sobremesas")
    tipo = id_data
    return render_template('novoprato.html',tipo=tipo, dadosCarne=dadosCarne,dadosEntradas=dadosEntradas,dadosPeixes=dadosPeixes,dadosBebidas=dadosBebidas,dadosSobremesa=dadosSobremesa)


@app.route('/adicionarprato/<string:id_data>', methods=['POST', 'GET'])
def adicionarprato(id_data):

    amounts = request.form.getlist('Escolha_Data')
    
    
    for teste, data_selecionada in enumerate(amounts):
        
        if data_selecionada == 'Segunda-Feira':
            data_ementa = 1
        
        if data_selecionada == 'Terça-Feira':
            data_ementa = 2
            
        if data_selecionada == 'Quarta-Feira':
            data_ementa = 3
            
        if data_selecionada == 'Quinta-Feira':
            data_ementa = 4
            
        if data_selecionada == 'Sexta-Feira':
            data_ementa = 5
            
        if data_selecionada == 'Sabado':
            data_ementa = 6
        
        if data_selecionada == 'Domingo':
            data_ementa = 7

        tipo = 1
        teste = request.form['Escolha_Tipo']
        if teste == 'Almoço':
            tipo = 1
        else: 
            tipo = 2
            """
        dados=Ementas(tipo,1,data_ementa) 
        db.session.add(dados)
        db.session.flush()
    """
        dados123=db.session.execute("CALL proc_add_ementa2(" + str(tipo) + "," + str(id_data) + ","  + str(data_ementa) + ")")
        db.session.commit()
        
        
        
        receber_ementa = db.engine.execute("Select codigoementa from view_ultima_ementa")
        amounts = receber_ementa
        for teste, id_mesa in enumerate(amounts):
            dados1234=db.session.execute("CALL proc_add_ementa_local(" + str(RestauranteFinal) + "," + str(id_mesa[0]) + ")")
            db.session.commit()
            amounts1 = request.form.getlist('Escolha_Entradas')
            for teste, idx in enumerate(amounts1): 
                sql = "select codigoitems from view_entradas where designacao= '" + idx + "' ;"
                amounts2=db.session.execute(sql)
                for teste, idx in enumerate(amounts2): 
                    db.session.execute('CALL proc_add_ementa_item(' + str(id_mesa[0]) + ',' + str(idx[0]) + ')')
                    db.session.commit()
        
            amounts3 = request.form.getlist('Escolha_Carne')
            for teste1, idx1 in enumerate(amounts3): 
                sql = "select codigoitems from view_carne where designacao= '" + idx1 + "' ;"
                amounts4=db.session.execute(sql)
                for teste1, idx1 in enumerate(amounts4): 
                    db.session.execute('CALL proc_add_ementa_item(' + str(id_mesa[0]) + ',' + str(idx1[0]) + ')')
                    db.session.commit()
                    
            amounts5 = request.form.getlist('Escolha_Peixe')
            for teste, idx2 in enumerate(amounts5): 
                sql = "select codigoitems from view_peixe where designacao= '" + idx2 + "' ;"
                amounts6=db.session.execute(sql)
                for teste, idx2 in enumerate(amounts6): 
                    db.session.execute('CALL proc_add_ementa_item(' + str(id_mesa[0]) + ',' + str(idx2[0]) + ')')
                    db.session.commit()

            amounts7 = request.form.getlist('Escolha_Bebida')
            for teste, idx3 in enumerate(amounts7): 
                sql = "select codigoitems from view_bebidas where designacao= '" + idx3 + "' ;"
                amounts8=db.session.execute(sql)
                for teste, idx3 in enumerate(amounts8): 
                    db.session.execute('CALL proc_add_ementa_item(' + str(id_mesa[0]) + ',' + str(idx3[0]) + ')')
                    db.session.commit()
                    
            amounts9 = request.form.getlist('Escolha_Sobremesa')
            for teste, idx4 in enumerate(amounts9): 
                sql = "select codigoitems from view_sobremesas where designacao= '" + idx4 + "' ;"
                amounts10=db.session.execute(sql)
                for teste, idx4 in enumerate(amounts10): 
                    db.session.execute('CALL proc_add_ementa_item(' + str(id_mesa[0]) + ',' + str(idx4[0]) + ')')
                    db.session.commit()
        
        """ dadoscarne=EmentasItems(dados.codigoementa,request.form['Escolha_Carne'])
        dadospeixe=EmentasItems(dados.codigoementa,request.form['Escolha_Peixe'])
        dadosbebidas=EmentasItems(dados.codigoementa,request.form['Escolha_Bebida'])
        dadossobremesas=EmentasItems(dados.codigoementa,request.form['Escolha_Sobremesa']) 

        db.session.add(dadosentradas)
        db.session.add(dadoscarne)
        db.session.add(dadospeixe)
        db.session.add(dadosbebidas)
        db.session.add(dadossobremesas) """


    return render_template('adicionarementa.html')


@app.route('/eliminaritemsobremesa/<string:id_data>', methods=['GET'])
def eliminaritemsobremesa(id_data):
    alergias=db.engine.execute("SELECT * FROM alergias")
    db.session.execute("CALL proc_apaga_item (" + str(id_data) + ")")
    db.session.commit()
    dados=db.engine.execute("SELECT * FROM view_sobremesas")
    return render_template('itens_sobremesas.html',dados=dados,alergias=alergias)

@app.route('/eliminartipoementa/<string:id_data>', methods=['GET'])
def eliminartipoementa(id_data):
    db.session.execute("CALL proc_elimina_tipo_ementa (" + str(id_data) + ")")
    db.session.commit()
    dados = db.session.execute("SELECT * FROM view_tipos_ementas")
    return render_template('editartipoementa.html',dados=dados) 


@app.route('/eliminaritementradas/<string:id_data>', methods=['GET'])
def eliminaritementradas(id_data):
    alergias=db.engine.execute("SELECT * FROM alergias")
    db.session.execute("CALL proc_apaga_item (" + str(id_data) + ")")
    db.session.commit()
    dados=db.engine.execute("SELECT * FROM view_entradas")
    return render_template('itens_entradas.html',dados=dados,alergias=alergias)

@app.route('/eliminaritemcarne/<string:id_data>', methods=['GET'])
def eliminaritemcarne(id_data):
    alergias=db.engine.execute("SELECT * FROM alergias")
    db.session.execute("CALL proc_apaga_item (" + str(id_data) + ")")
    db.session.commit()
    dados=db.engine.execute("SELECT * FROM view_carne")
    return render_template('itens_pratos_carne.html',dados=dados,alergias=alergias)

@app.route('/eliminaritempeixe/<string:id_data>', methods=['GET'])
def eliminaritempeixe(id_data):
    alergias=db.engine.execute("SELECT * FROM alergias")
    db.session.execute("CALL proc_apaga_item (" + str(id_data) + ")")
    db.session.commit()
    dados=db.engine.execute("SELECT * FROM view_peixe")
    return render_template('itens_pratos_peixe.html',dados=dados,alergias=alergias)

@app.route('/eliminaritembebidas/<string:id_data>', methods=['GET'])
def eliminaritembebidas(id_data):
    alergias=db.engine.execute("SELECT * FROM alergias")
    db.session.execute("CALL proc_apaga_item (" + str(id_data) + ")")
    db.session.commit()
    dados=db.engine.execute("SELECT * FROM view_bebidas")
    return render_template('itens_bebidas.html',dados=dados,alergias=alergias)

@app.route('/historicoementas')
def historicoementas():
    data= datetime.now()
    date_time = data.strftime("%Y/%m/%d")
    print(type(date_time))
    valor1=int(RestauranteFinal)
    dados=db.session.query(Ementas.data,Ementas.codigoementa,Ementas.codigotiporef,Ementas.codigotipoement,Ementas.codigotiporef,RestaurantesEmentas.codigoementa,RestaurantesEmentas.codigorest,TiposEmentas.codigotipoement,TiposEmentas.designacao).filter(TiposEmentas.codigotipoement==Ementas.codigotipoement).filter(RestaurantesEmentas.codigoementa==Ementas.codigoementa).filter(RestaurantesEmentas.codigorest==valor1).filter(Ementas.data<=datetime.now()).order_by(Ementas.data,Ementas.codigotiporef,Ementas.codigotipoement).all()
    print(date_time)

    dadosEntradas=db.session.query(Ementas,EmentasItems,Items).filter(Ementas.codigoementa==EmentasItems.codigoementa).filter(EmentasItems.codigoitems==Items.codigoitems).filter(Items.codigotipoitem==1).all()
    dadosCarne=db.session.query(Ementas,EmentasItems,Items).filter(Ementas.codigoementa==EmentasItems.codigoementa).filter(EmentasItems.codigoitems==Items.codigoitems).filter(Items.codigotipoitem==2).all()
    dadosPeixes=db.session.query(Ementas,EmentasItems,Items).filter(Ementas.codigoementa==EmentasItems.codigoementa).filter(EmentasItems.codigoitems==Items.codigoitems).filter(Items.codigotipoitem==3).all()
    dadosBebidas=db.session.query(Ementas,EmentasItems,Items).filter(Ementas.codigoementa==EmentasItems.codigoementa).filter(EmentasItems.codigoitems==Items.codigoitems).filter(Items.codigotipoitem==4).all()
    dadosSobremesa=db.session.query(Ementas,EmentasItems,Items).filter(Ementas.codigoementa==EmentasItems.codigoementa).filter(EmentasItems.codigoitems==Items.codigoitems).filter(Items.codigotipoitem==5).all()
                            
   
    return render_template('historicoementas.html',dados=dados,dadosEntradas=dadosEntradas,dadosCarne=dadosCarne,dadosPeixes=dadosPeixes,dadosBebidas=dadosBebidas,dadosSobremesa=dadosSobremesa)

@app.route('/updateentradas',methods=['POST','GET'])
def updateentradas():
    alergias=db.engine.execute("SELECT * FROM alergias")
    id2=request.form['id']
    designacao=request.form['designacao']
    preco=request.form['custo']
    db.session.execute("call proc_update_item ( '" + str(designacao) + "'," + str(preco) + "," + str(id2) +")")
    db.session.commit()
    
    dados=db.engine.execute("SELECT * FROM view_entradas")
    return render_template('itens_entradas.html',dados=dados,alergias=alergias)

@app.route('/updatecarne',methods=['POST','GET'])
def updatecarne():
    alergias=db.engine.execute("SELECT * FROM alergias")
    id2=request.form['id']
    designacao=request.form['designacao']
    preco=request.form['custo']
    db.session.execute("call proc_update_item ( '" + str(designacao) + "'," + str(preco) + "," + str(id2) +")")
    db.session.commit()
    dados=db.engine.execute("SELECT * FROM view_carne")
    return render_template('itens_pratos_carne.html',dados=dados,alergias=alergias)

@app.route('/updatepeixe',methods=['POST','GET'])
def updatepeixe():
    alergias=db.engine.execute("SELECT * FROM alergias")

    id2=request.form['id']
    designacao=request.form['designacao']
    preco=request.form['custo']
    db.session.execute("call proc_update_item ( '" + str(designacao) + "'," + str(preco) + "," + str(id2) +")")
    db.session.commit()
    dados=db.engine.execute("SELECT * FROM view_peixe")
    return render_template('itens_pratos_peixe.html',dados=dados,alergias=alergias)

@app.route('/updatebebidas',methods=['POST','GET'])
def updatebebidas():
    alergias=db.engine.execute("SELECT * FROM alergias")
    id2=request.form['id']
    designacao=request.form['designacao']
    preco=request.form['custo']
    db.session.execute("call proc_update_item ( '" + str(designacao) + "'," + str(preco) + "," + str(id2) +")")
    db.session.commit()
    dados=db.engine.execute("SELECT * FROM view_bebidas")
    return render_template('itens_bebidas.html',dados=dados,alergias=alergias)

@app.route('/updatesobremesas',methods=['POST','GET'])
def updatesobremesas():
    alergias=db.engine.execute("SELECT * FROM alergias")
    id2=request.form['id']
    designacao=request.form['designacao']
    preco=request.form['custo']
    db.session.execute("call proc_update_item ( '" + str(designacao) + "'," + str(preco) + "," + str(id2) +")")
    db.session.commit()
    dados=db.engine.execute("SELECT * FROM view_sobremesas")
    return render_template('itens_sobremesas.html',dados=dados,alergias=alergias)

@app.route('/updatetipoementa',methods=['POST','GET'])
def updatetipoementa():
    desi=request.form['designacao']
    numero=request.form['id']
    db.session.execute("call proc_update_tipo (" + str(numero) + ",'" + str(desi) + "')")
    db.session.commit()
    dados=db.engine.execute("SELECT * FROM view_tipos_ementas")
    return render_template('editartipoementa.html',dados=dados)


@app.route('/criartipoementa',methods=['POST','GET'])
def criartipoementa():
    nome=request.form['item']
    db.session.execute("call proc_novo_tipo ('" + str(nome) + "')")
    db.session.commit()
    dados=db.engine.execute("SELECT * FROM view_tipos_ementas")
    return render_template('editartipoementa.html',dados=dados)

@app.route('/adicionarentrada', methods = ['POST'])
def adicionarentrada():
    alergias=db.engine.execute("SELECT * FROM alergias")
    alergias1=request.form['Escolha_Alergia']
    designacao = request.form['item']
    custo = request.form['preco1']
    db.session.execute("call proc_add_item ('" + str(designacao) + "'," + str(1) + "," + str(custo) + "," + str(alergias1) + ")")
    db.session.commit()
    dados=db.engine.execute("SELECT * FROM view_entradas")
    return render_template('itens_entradas.html',dados=dados,alergias=alergias)

@app.route('/adicionarcarne', methods = ['POST'])
def adicionarcarne():
    alergias=db.engine.execute("SELECT * FROM alergias")
    alergias1=request.form['Escolha_Alergia']
    designacao = request.form['item']
    custo = request.form['preco1']
    db.session.execute("call proc_add_item ('" + str(designacao) + "'," + str(2) + "," + str(custo) + "," + str(alergias1) + ")")
    db.session.commit()
    dados=db.engine.execute("SELECT * FROM view_carne")
    return render_template('itens_pratos_carne.html',dados=dados,alergias=alergias)

@app.route('/adicionarpeixe', methods = ['POST'])
def adicionarpeixe():
    alergias=db.engine.execute("SELECT * FROM alergias")
    alergias1=request.form['Escolha_Alergia']
    designacao = request.form['item']
    custo = request.form['preco1']
    db.session.execute("call proc_add_item ('" + str(designacao) + "'," + str(3) + "," + str(custo) + "," + str(alergias1) + ")")
    db.session.commit()
    dados=db.engine.execute("SELECT * FROM view_peixe")
    return render_template('itens_pratos_peixe.html',dados=dados,alergias=alergias)

@app.route('/adicionarbebidas', methods = ['POST'])
def adicionarbebidas():
    alergias=db.engine.execute("SELECT * FROM alergias")
    alergias1=request.form['Escolha_Alergia']
    designacao = request.form['item']
    custo = request.form['preco1']
    db.session.execute("call proc_add_item ('" + str(designacao) + "'," + str(4) + "," + str(custo) + "," + str(alergias1) + ")")
    db.session.commit()
    dados=db.engine.execute("SELECT * FROM view_bebidas")
    return render_template('itens_bebidas.html',dados=dados,alergias=alergias)

@app.route('/adicionarsobremesas', methods = ['POST'])
def adicionarsobremesas():
    alergias=db.engine.execute("SELECT * FROM alergias")
    alergias1=request.form['Escolha_Alergia']
    designacao = request.form['item']
    custo = request.form['preco1']
    db.session.execute("call proc_add_item ('" + str(designacao) + "'," + str(5) + "," + str(custo) + "," + str(alergias1) + ")")
    db.session.commit()
    dados=db.engine.execute("SELECT * FROM view_sobremesas")
    return render_template('itens_sobremesas.html',dados=dados,alergias=alergias)




























































































@app.route('/adicionarmesa1/<string:id_data>', methods=['POST','GET'])
def adicionarmesa1(id_data):
    db.session.execute("call proc_adiciona_consumo (" + str(id_data) + "," + str(RestauranteFinal) + ")")
    db.session.commit()
    dadosEntradas=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa=db.engine.execute("SELECT * FROM view_sobremesas")

    dadosEntradas2=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne2=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes2=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas2=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa2=db.engine.execute("SELECT * FROM view_sobremesas")

    consumo=db.engine.execute("Select * from view_ultimo_consumo")
    amounts = consumo
    for teste, id_mesa in enumerate(amounts):
        amounts1 = request.form.getlist('Escolha_Entradas1')
        for teste, idx in enumerate(amounts1): 
            sql = "select codigoitems from view_entradas where designacao= '" + idx + "' ;"
            amounts2=db.session.execute(sql)
            for teste, idx1 in enumerate(amounts2): 
                db.session.execute('CALL proc_adiciona_consumo_item(' + str(id_mesa[0]) + ',' + str(idx1[0]) + ')')
                db.session.commit()
    consumo=db.engine.execute("Select * from view_ultimo_consumo")
    amounts = consumo
    for teste, id_mesa in enumerate(amounts):
        amounts1 = request.form.getlist('Escolha_Carne1')
        for teste, idx in enumerate(amounts1): 
            sql = "select codigoitems from view_carne where designacao= '" + idx + "' ;"
            amounts2=db.session.execute(sql)
            for teste, idx1 in enumerate(amounts2): 
                db.session.execute('CALL proc_adiciona_consumo_item(' + str(id_mesa[0]) + ',' + str(idx1[0]) + ')')
                db.session.commit()

    consumo=db.engine.execute("Select * from view_ultimo_consumo")
    amounts = consumo
    for teste, id_mesa in enumerate(amounts):
        amounts1 = request.form.getlist('Escolha_Peixe1')
        for teste, idx in enumerate(amounts1): 
            sql = "select codigoitems from view_peixe where designacao= '" + idx + "' ;"
            amounts2=db.session.execute(sql)
            for teste, idx1 in enumerate(amounts2): 
                db.session.execute('CALL proc_adiciona_consumo_item(' + str(id_mesa[0]) + ',' + str(idx1[0]) + ')')
                db.session.commit()

    consumo=db.engine.execute("Select * from view_ultimo_consumo")
    amounts = consumo
    for teste, id_mesa in enumerate(amounts):
        amounts1 = request.form.getlist('Escolha_Bebida1')
        for teste, idx in enumerate(amounts1): 
            sql = "select codigoitems from view_bebidas where designacao= '" + idx + "' ;"
            amounts2=db.session.execute(sql)
            for teste, idx1 in enumerate(amounts2): 
                db.session.execute('CALL proc_adiciona_consumo_item(' + str(id_mesa[0]) + ',' + str(idx1[0]) + ')')
                db.session.commit()


    consumo=db.engine.execute("Select * from view_ultimo_consumo")
    amounts = consumo
    for teste, id_mesa in enumerate(amounts):
        amounts1 = request.form.getlist('Escolha_Sobremesa1')
        for teste, idx in enumerate(amounts1): 
            sql = "select codigoitems from view_sobremesas where designacao= '" + idx + "' ;"
            amounts2=db.session.execute(sql)
            for teste, idx1 in enumerate(amounts2): 
                db.session.execute('CALL proc_adiciona_consumo_item(' + str(id_mesa[0]) + ',' + str(idx1[0]) + ')')
                db.session.commit()


    valor1=int(RestauranteFinal)

    minha = db.engine.execute("Select codigolocaiscons from view_mesa_restaurante where codigorest=%s limit 1",valor1)

    amounts = minha
    for teste, id_mesa in enumerate(amounts):
        print(id_mesa)
    
    dadostabela = db.engine.execute("Select * from view_consumo, view_consumo_items, view_items where view_consumo.codigoconsumo=view_consumo_items.codigoconsumo and view_items.codigoitems=view_consumo_items.codigoitems and view_consumo.codigolocaiscons= %s ORDER BY designacao", id_mesa)
    return render_template('mesa1.html',dadostabela=dadostabela,dadosEntradas=dadosEntradas,dadosCarne=dadosCarne,dadosBebidas=dadosBebidas,dadosPeixes=dadosPeixes,dadosSobremesa=dadosSobremesa,dadosEntradas2=dadosEntradas2,dadosCarne2=dadosCarne2,dadosBebidas2=dadosBebidas2,dadosPeixes2=dadosPeixes2,dadosSobremesa2=dadosSobremesa2)



@app.route('/contadicionarmesa1', methods=['POST'])
def contadicionarmesa1():
    dadosEntradas=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa=db.engine.execute("SELECT * FROM view_sobremesas")

    dadosEntradas2=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne2=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes2=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas2=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa2=db.engine.execute("SELECT * FROM view_sobremesas")

    consumo=db.engine.execute("Select * from view_ultimo_consumo")
    amounts = consumo
    for teste, id_mesa in enumerate(amounts):
        amounts1 = request.form.getlist('Escolha_Entradas')
        for teste, idx in enumerate(amounts1): 
            sql = "select codigoitems from view_entradas where designacao= '" + idx + "' ;"
            amounts2=db.session.execute(sql)
            for teste, idx1 in enumerate(amounts2): 
                db.session.execute('CALL proc_adiciona_consumo_item(' + str(id_mesa[0]) + ',' + str(idx1[0]) + ')')
                db.session.commit()
    consumo=db.engine.execute("Select * from view_ultimo_consumo")
    amounts = consumo
    for teste, id_mesa in enumerate(amounts):
        amounts1 = request.form.getlist('Escolha_Carne')
        for teste, idx in enumerate(amounts1): 
            sql = "select codigoitems from view_carne where designacao= '" + idx + "' ;"
            amounts2=db.session.execute(sql)
            for teste, idx1 in enumerate(amounts2): 
                db.session.execute('CALL proc_adiciona_consumo_item(' + str(id_mesa[0]) + ',' + str(idx1[0]) + ')')
                db.session.commit()

    consumo=db.engine.execute("Select * from view_ultimo_consumo")
    amounts = consumo
    for teste, id_mesa in enumerate(amounts):
        amounts1 = request.form.getlist('Escolha_Peixe')
        for teste, idx in enumerate(amounts1): 
            sql = "select codigoitems from view_peixe where designacao= '" + idx + "' ;"
            amounts2=db.session.execute(sql)
            for teste, idx1 in enumerate(amounts2): 
                db.session.execute('CALL proc_adiciona_consumo_item(' + str(id_mesa[0]) + ',' + str(idx1[0]) + ')')
                db.session.commit()

    consumo=db.engine.execute("Select * from view_ultimo_consumo")
    amounts = consumo
    for teste, id_mesa in enumerate(amounts):
        amounts1 = request.form.getlist('Escolha_Bebida')
        for teste, idx in enumerate(amounts1): 
            sql = "select codigoitems from view_bebidas where designacao= '" + idx + "' ;"
            amounts2=db.session.execute(sql)
            for teste, idx1 in enumerate(amounts2): 
                db.session.execute('CALL proc_adiciona_consumo_item(' + str(id_mesa[0]) + ',' + str(idx1[0]) + ')')
                db.session.commit()

    consumo=db.engine.execute("Select * from view_ultimo_consumo")
    amounts = consumo
    for teste, id_mesa in enumerate(amounts):
        amounts1 = request.form.getlist('Escolha_Sobremesa')
        for teste, idx in enumerate(amounts1): 
            sql = "select codigoitems from view_sobremesas where designacao= '" + idx + "' ;"
            amounts2=db.session.execute(sql)
            for teste, idx1 in enumerate(amounts2): 
                db.session.execute('CALL proc_adiciona_consumo_item(' + str(id_mesa[0]) + ',' + str(idx1[0]) + ')')
                db.session.commit()


    valor1=int(RestauranteFinal)

    minha = db.engine.execute("Select codigolocaiscons from view_mesa_restaurante where codigorest=%s limit 1",valor1)

    amounts = minha
    for teste, id_mesa in enumerate(amounts):
        print(id_mesa)
    
    dadostabela = db.engine.execute("Select * from view_consumo, view_consumo_items, view_items where view_consumo.codigoconsumo=view_consumo_items.codigoconsumo and view_items.codigoitems=view_consumo_items.codigoitems and view_consumo.codigolocaiscons= %s ORDER BY designacao", id_mesa)
    return render_template('mesa1.html',dadostabela=dadostabela,dadosEntradas=dadosEntradas,dadosCarne=dadosCarne,dadosBebidas=dadosBebidas,dadosPeixes=dadosPeixes,dadosSobremesa=dadosSobremesa,dadosEntradas2=dadosEntradas2,dadosCarne2=dadosCarne2,dadosBebidas2=dadosBebidas2,dadosPeixes2=dadosPeixes2,dadosSobremesa2=dadosSobremesa2)






@app.route('/eliminaritemmesa1/<string:id_data>/<string:id_consumo>', methods=['POST','GET'])
def eliminaritemmesa1(id_data,id_consumo):

    valor1=int(RestauranteFinal)

    minha = db.engine.execute("Select codigolocaiscons from view_mesa_restaurante where codigorest=%s limit 1",valor1)

    amounts = minha
    for teste, id_mesa in enumerate(amounts):
        print(id_mesa)



    dadosEntradas=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa=db.engine.execute("SELECT * FROM view_sobremesas")

    dadosEntradas2=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne2=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes2=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas2=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa2=db.engine.execute("SELECT * FROM view_sobremesas")

    db.session.execute('CALL proc_delete_consumo(' + str(id_data) + ',' + str(id_consumo) +')')
    db.session.commit()

    dadostabela = db.engine.execute("Select * from view_consumo, view_consumo_items, view_items where view_consumo.codigoconsumo=view_consumo_items.codigoconsumo and view_items.codigoitems=view_consumo_items.codigoitems and view_consumo.codigolocaiscons= %s ORDER BY designacao", id_mesa)
    return render_template('mesa1.html',dadostabela=dadostabela,dadosEntradas=dadosEntradas,dadosCarne=dadosCarne,dadosBebidas=dadosBebidas,dadosPeixes=dadosPeixes,dadosSobremesa=dadosSobremesa,dadosEntradas2=dadosEntradas2,dadosCarne2=dadosCarne2,dadosBebidas2=dadosBebidas2,dadosPeixes2=dadosPeixes2,dadosSobremesa2=dadosSobremesa2)

    amounts = minha
    for teste, id_mesa in enumerate(amounts):
        if teste==6:
            db.session.execute("CALL proc_terminar_mesa(" + str(id_data) + ",'"+ str(nome) + "',"+ str(NIF) + ","+ str(id_mesa[0]) +")")
            db.session.commit()
            dadostabela = db.engine.execute("Select * from view_consumo, view_consumo_items, view_items where view_consumo.codigoconsumo=view_consumo_items.codigoconsumo and view_items.codigoitems=view_consumo_items.codigoitems and view_consumo.codigolocaiscons= %s ORDER BY designacao", id_mesa)
    return render_template('mesa7.html',dadostabela=dadostabela,dadosEntradas=dadosEntradas,dadosCarne=dadosCarne,dadosBebidas=dadosBebidas,dadosPeixes=dadosPeixes,dadosSobremesa=dadosSobremesa,dadosEntradas2=dadosEntradas2,dadosCarne2=dadosCarne2,dadosBebidas2=dadosBebidas2,dadosPeixes2=dadosPeixes2,dadosSobremesa2=dadosSobremesa2)

@app.route('/terminarmesa1/<string:id_data>', methods=['POST','GET'])
def terminarmesa1(id_data):

    dadosEntradas=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa=db.engine.execute("SELECT * FROM view_sobremesas")

    dadosEntradas2=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne2=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes2=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas2=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa2=db.engine.execute("SELECT * FROM view_sobremesas")

    nome=request.form['Escolha_Nome']
    NIF=request.form['Escolha_NIF']

    valor1=int(RestauranteFinal)

    minha = db.engine.execute("Select codigolocaiscons from view_mesa_restaurante where codigorest=%s limit 1",valor1)

    amounts = minha
    for teste, id_mesa in enumerate(amounts):
        print(id_mesa)
        db.session.execute("CALL proc_terminar_mesa(" + str(id_data) + ",'"+ str(nome) + "',"+ str(NIF) + ","+ str(id_mesa[0]) +")")
        db.session.commit()
        dadostabela = db.engine.execute("Select * from view_consumo, view_consumo_items, view_items where view_consumo.codigoconsumo=view_consumo_items.codigoconsumo and view_items.codigoitems=view_consumo_items.codigoitems and view_consumo.codigolocaiscons= %s ORDER BY designacao", id_mesa)
        return render_template('mesa1.html',dadostabela=dadostabela,dadosEntradas=dadosEntradas,dadosCarne=dadosCarne,dadosBebidas=dadosBebidas,dadosPeixes=dadosPeixes,dadosSobremesa=dadosSobremesa,dadosEntradas2=dadosEntradas2,dadosCarne2=dadosCarne2,dadosBebidas2=dadosBebidas2,dadosPeixes2=dadosPeixes2,dadosSobremesa2=dadosSobremesa2)

@app.route('/maismesa1/<int:id_data>/<string:quantidade>/<string:consumo>', methods=['POST','GET'])
def maismesa1(id_data,quantidade,consumo):

    dadosEntradas=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa=db.engine.execute("SELECT * FROM view_sobremesas")
    dadosEntradas2=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne2=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes2=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas2=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa2=db.engine.execute("SELECT * FROM view_sobremesas")    

    db.session.execute('CALL proc_mais_mesa1(' + str(id_data) + ','+ str(quantidade) + ','+ str(consumo)+')')
    db.session.commit()
    
    valor1=int(RestauranteFinal)

    minha = db.engine.execute("Select codigolocaiscons from view_mesa_restaurante where codigorest=%s limit 1",valor1)

    amounts = minha
    for teste, id_mesa in enumerate(amounts):
        print(id_mesa)
    
    dadostabela = db.engine.execute("Select * from view_consumo, view_consumo_items, view_items where view_consumo.codigoconsumo=view_consumo_items.codigoconsumo and view_items.codigoitems=view_consumo_items.codigoitems and view_consumo.codigolocaiscons= %s ORDER BY designacao", id_mesa)
    return render_template('mesa1.html',dadostabela=dadostabela,dadosEntradas=dadosEntradas,dadosCarne=dadosCarne,dadosBebidas=dadosBebidas,dadosPeixes=dadosPeixes,dadosSobremesa=dadosSobremesa,dadosEntradas2=dadosEntradas2,dadosCarne2=dadosCarne2,dadosBebidas2=dadosBebidas2,dadosPeixes2=dadosPeixes2,dadosSobremesa2=dadosSobremesa2)

@app.route('/menosmesa1/<string:id_data>/<int:quantidade>/<string:consumo>', methods=['POST','GET'])
def menosmesa1(id_data,quantidade,consumo):

    dadosEntradas=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa=db.engine.execute("SELECT * FROM view_sobremesas")
    dadosEntradas2=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne2=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes2=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas2=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa2=db.engine.execute("SELECT * FROM view_sobremesas")    

    db.session.execute('CALL proc_menos_mesa1(' + str(id_data) + ','+ str(quantidade) + ','+ str(consumo)+')')
    db.session.commit()
    
    valor1=int(RestauranteFinal)

    minha = db.engine.execute("Select codigolocaiscons from view_mesa_restaurante where codigorest=%s limit 1",valor1)

    amounts = minha
    for teste, id_mesa in enumerate(amounts):
        print(id_mesa)
    
    dadostabela = db.engine.execute("Select * from view_consumo, view_consumo_items, view_items where view_consumo.codigoconsumo=view_consumo_items.codigoconsumo and view_items.codigoitems=view_consumo_items.codigoitems and view_consumo.codigolocaiscons= %s ORDER BY designacao", id_mesa)
    return render_template('mesa1.html',dadostabela=dadostabela,dadosEntradas=dadosEntradas,dadosCarne=dadosCarne,dadosBebidas=dadosBebidas,dadosPeixes=dadosPeixes,dadosSobremesa=dadosSobremesa,dadosEntradas2=dadosEntradas2,dadosCarne2=dadosCarne2,dadosBebidas2=dadosBebidas2,dadosPeixes2=dadosPeixes2,dadosSobremesa2=dadosSobremesa2)


@app.route('/adicionarmesa2/<string:id_data>', methods=['POST','GET'])
def adicionarmesa2(id_data):
    db.session.execute("call proc_adiciona_consumo (" + str(id_data) + "," + str(RestauranteFinal) + ")")
    db.session.commit()
    dadosEntradas=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa=db.engine.execute("SELECT * FROM view_sobremesas")

    dadosEntradas2=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne2=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes2=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas2=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa2=db.engine.execute("SELECT * FROM view_sobremesas")

    consumo=db.engine.execute("Select * from view_ultimo_consumo")
    amounts = consumo
    for teste, id_mesa in enumerate(amounts):
        amounts1 = request.form.getlist('Escolha_Entradas1')
        for teste, idx in enumerate(amounts1): 
            sql = "select codigoitems from view_entradas where designacao= '" + idx + "' ;"
            amounts2=db.session.execute(sql)
            for teste, idx1 in enumerate(amounts2): 
                db.session.execute('CALL proc_adiciona_consumo_item(' + str(id_mesa[0]) + ',' + str(idx1[0]) + ')')
                db.session.commit()
    consumo=db.engine.execute("Select * from view_ultimo_consumo")
    amounts = consumo
    for teste, id_mesa in enumerate(amounts):
        amounts1 = request.form.getlist('Escolha_Carne1')
        for teste, idx in enumerate(amounts1): 
            sql = "select codigoitems from view_carne where designacao= '" + idx + "' ;"
            amounts2=db.session.execute(sql)
            for teste, idx1 in enumerate(amounts2): 
                db.session.execute('CALL proc_adiciona_consumo_item(' + str(id_mesa[0]) + ',' + str(idx1[0]) + ')')
                db.session.commit()

    consumo=db.engine.execute("Select * from view_ultimo_consumo")
    amounts = consumo
    for teste, id_mesa in enumerate(amounts):
        amounts1 = request.form.getlist('Escolha_Peixe1')
        for teste, idx in enumerate(amounts1): 
            sql = "select codigoitems from view_peixe where designacao= '" + idx + "' ;"
            amounts2=db.session.execute(sql)
            for teste, idx1 in enumerate(amounts2): 
                db.session.execute('CALL proc_adiciona_consumo_item(' + str(id_mesa[0]) + ',' + str(idx1[0]) + ')')
                db.session.commit()

    consumo=db.engine.execute("Select * from view_ultimo_consumo")
    amounts = consumo
    for teste, id_mesa in enumerate(amounts):
        amounts1 = request.form.getlist('Escolha_Bebida1')
        for teste, idx in enumerate(amounts1): 
            sql = "select codigoitems from view_bebidas where designacao= '" + idx + "' ;"
            amounts2=db.session.execute(sql)
            for teste, idx1 in enumerate(amounts2): 
                db.session.execute('CALL proc_adiciona_consumo_item(' + str(id_mesa[0]) + ',' + str(idx1[0]) + ')')
                db.session.commit()


    consumo=db.engine.execute("Select * from view_ultimo_consumo")
    amounts = consumo
    for teste, id_mesa in enumerate(amounts):
        amounts1 = request.form.getlist('Escolha_Sobremesa1')
        for teste, idx in enumerate(amounts1): 
            sql = "select codigoitems from view_sobremesas where designacao= '" + idx + "' ;"
            amounts2=db.session.execute(sql)
            for teste, idx1 in enumerate(amounts2): 
                db.session.execute('CALL proc_adiciona_consumo_item(' + str(id_mesa[0]) + ',' + str(idx1[0]) + ')')
                db.session.commit()


    valor1=int(RestauranteFinal)

    minha = db.engine.execute("Select codigolocaiscons from view_mesa_restaurante where codigorest=%s ",valor1)

    amounts = minha
    for teste, id_mesa in enumerate(amounts):
        if teste==1:
            dadostabela = db.engine.execute("Select * from view_consumo, view_consumo_items, view_items where view_consumo.codigoconsumo=view_consumo_items.codigoconsumo and view_items.codigoitems=view_consumo_items.codigoitems and view_consumo.codigolocaiscons= %s ORDER BY designacao", id_mesa)
    return render_template('mesa2.html',dadostabela=dadostabela,dadosEntradas=dadosEntradas,dadosCarne=dadosCarne,dadosBebidas=dadosBebidas,dadosPeixes=dadosPeixes,dadosSobremesa=dadosSobremesa,dadosEntradas2=dadosEntradas2,dadosCarne2=dadosCarne2,dadosBebidas2=dadosBebidas2,dadosPeixes2=dadosPeixes2,dadosSobremesa2=dadosSobremesa2)




@app.route('/contadicionarmesa2', methods=['POST'])
def contadicionarmesa2():
    dadosEntradas=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa=db.engine.execute("SELECT * FROM view_sobremesas")

    dadosEntradas2=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne2=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes2=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas2=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa2=db.engine.execute("SELECT * FROM view_sobremesas")

    consumo=db.engine.execute("Select * from view_ultimo_consumo")
    amounts = consumo
    for teste, id_mesa in enumerate(amounts):
        amounts1 = request.form.getlist('Escolha_Entradas')
        for teste, idx in enumerate(amounts1): 
            sql = "select codigoitems from view_entradas where designacao= '" + idx + "' ;"
            amounts2=db.session.execute(sql)
            for teste, idx1 in enumerate(amounts2): 
                db.session.execute('CALL proc_adiciona_consumo_item(' + str(id_mesa[0]) + ',' + str(idx1[0]) + ')')
                db.session.commit()
    consumo=db.engine.execute("Select * from view_ultimo_consumo")
    amounts = consumo
    for teste, id_mesa in enumerate(amounts):
        amounts1 = request.form.getlist('Escolha_Carne')
        for teste, idx in enumerate(amounts1): 
            sql = "select codigoitems from view_carne where designacao= '" + idx + "' ;"
            amounts2=db.session.execute(sql)
            for teste, idx1 in enumerate(amounts2): 
                db.session.execute('CALL proc_adiciona_consumo_item(' + str(id_mesa[0]) + ',' + str(idx1[0]) + ')')
                db.session.commit()

    consumo=db.engine.execute("Select * from view_ultimo_consumo")
    amounts = consumo
    for teste, id_mesa in enumerate(amounts):
        amounts1 = request.form.getlist('Escolha_Peixe')
        for teste, idx in enumerate(amounts1): 
            sql = "select codigoitems from view_peixe where designacao= '" + idx + "' ;"
            amounts2=db.session.execute(sql)
            for teste, idx1 in enumerate(amounts2): 
                db.session.execute('CALL proc_adiciona_consumo_item(' + str(id_mesa[0]) + ',' + str(idx1[0]) + ')')
                db.session.commit()

    consumo=db.engine.execute("Select * from view_ultimo_consumo")
    amounts = consumo
    for teste, id_mesa in enumerate(amounts):
        amounts1 = request.form.getlist('Escolha_Bebida')
        for teste, idx in enumerate(amounts1): 
            sql = "select codigoitems from view_bebidas where designacao= '" + idx + "' ;"
            amounts2=db.session.execute(sql)
            for teste, idx1 in enumerate(amounts2): 
                db.session.execute('CALL proc_adiciona_consumo_item(' + str(id_mesa[0]) + ',' + str(idx1[0]) + ')')
                db.session.commit()

    consumo=db.engine.execute("Select * from view_ultimo_consumo")
    amounts = consumo
    for teste, id_mesa in enumerate(amounts):
        amounts1 = request.form.getlist('Escolha_Sobremesa')
        for teste, idx in enumerate(amounts1): 
            sql = "select codigoitems from view_sobremesas where designacao= '" + idx + "' ;"
            amounts2=db.session.execute(sql)
            for teste, idx1 in enumerate(amounts2): 
                db.session.execute('CALL proc_adiciona_consumo_item(' + str(id_mesa[0]) + ',' + str(idx1[0]) + ')')
                db.session.commit()


    valor1=int(RestauranteFinal)

    minha = db.engine.execute("Select codigolocaiscons from view_mesa_restaurante where codigorest=%s ",valor1)

    amounts = minha
    for teste, id_mesa in enumerate(amounts):
        if teste==1:
            dadostabela = db.engine.execute("Select * from view_consumo, view_consumo_items, view_items where view_consumo.codigoconsumo=view_consumo_items.codigoconsumo and view_items.codigoitems=view_consumo_items.codigoitems and view_consumo.codigolocaiscons= %s ORDER BY designacao", id_mesa)
    return render_template('mesa2.html',dadostabela=dadostabela,dadosEntradas=dadosEntradas,dadosCarne=dadosCarne,dadosBebidas=dadosBebidas,dadosPeixes=dadosPeixes,dadosSobremesa=dadosSobremesa,dadosEntradas2=dadosEntradas2,dadosCarne2=dadosCarne2,dadosBebidas2=dadosBebidas2,dadosPeixes2=dadosPeixes2,dadosSobremesa2=dadosSobremesa2)







@app.route('/eliminaritemmesa2/<string:id_data>/<string:id_consumo>', methods=['POST','GET'])
def eliminaritemmesa2(id_data,id_consumo):

    dadosEntradas=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa=db.engine.execute("SELECT * FROM view_sobremesas")

    dadosEntradas2=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne2=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes2=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas2=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa2=db.engine.execute("SELECT * FROM view_sobremesas")


    db.session.execute('CALL proc_delete_consumo(' + str(id_data) + ',' + str(id_consumo) +')')
    db.session.commit()

    valor1=int(RestauranteFinal)

    minha = db.engine.execute("Select codigolocaiscons from view_mesa_restaurante where codigorest=%s ",valor1)

    amounts = minha
    for teste, id_mesa in enumerate(amounts):
        print(id_mesa)
        if teste==1:
            dadostabela = db.engine.execute("Select * from view_consumo, view_consumo_items, view_items where view_consumo.codigoconsumo=view_consumo_items.codigoconsumo and view_items.codigoitems=view_consumo_items.codigoitems and view_consumo.codigolocaiscons= %s ORDER BY designacao", id_mesa)


    
    return render_template('mesa2.html',dadostabela=dadostabela,dadosEntradas=dadosEntradas,dadosCarne=dadosCarne,dadosBebidas=dadosBebidas,dadosPeixes=dadosPeixes,dadosSobremesa=dadosSobremesa,dadosEntradas2=dadosEntradas2,dadosCarne2=dadosCarne2,dadosBebidas2=dadosBebidas2,dadosPeixes2=dadosPeixes2,dadosSobremesa2=dadosSobremesa2)


@app.route('/terminarmesa2/<string:id_data>', methods=['POST','GET'])
def terminarmesa2(id_data):


    dadosEntradas=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa=db.engine.execute("SELECT * FROM view_sobremesas")

    dadosEntradas2=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne2=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes2=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas2=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa2=db.engine.execute("SELECT * FROM view_sobremesas")


    nome=request.form['Escolha_Nome']
    NIF=request.form['Escolha_NIF']

    valor1=int(RestauranteFinal)

    minha = db.engine.execute("Select codigolocaiscons from view_mesa_restaurante where codigorest=%s",valor1)

    amounts = minha
    for teste, id_mesa in enumerate(amounts):
        if teste==1:
            db.session.execute("CALL proc_terminar_mesa(" + str(id_data) + ",'"+ str(nome) + "',"+ str(NIF) + ","+ str(id_mesa[0]) +")")
            db.session.commit()
            dadostabela = db.engine.execute("Select * from view_consumo, view_consumo_items, view_items where view_consumo.codigoconsumo=view_consumo_items.codigoconsumo and view_items.codigoitems=view_consumo_items.codigoitems and view_consumo.codigolocaiscons= %s ORDER BY designacao", id_mesa)
            return render_template('mesa2.html',dadostabela=dadostabela,dadosEntradas=dadosEntradas,dadosCarne=dadosCarne,dadosBebidas=dadosBebidas,dadosPeixes=dadosPeixes,dadosSobremesa=dadosSobremesa,dadosEntradas2=dadosEntradas2,dadosCarne2=dadosCarne2,dadosBebidas2=dadosBebidas2,dadosPeixes2=dadosPeixes2,dadosSobremesa2=dadosSobremesa2)

@app.route('/maismesa2/<int:id_data>/<string:quantidade>/<string:consumo>', methods=['POST','GET'])
def maismesa2(id_data,quantidade,consumo):

    dadosEntradas=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa=db.engine.execute("SELECT * FROM view_sobremesas")
    dadosEntradas2=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne2=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes2=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas2=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa2=db.engine.execute("SELECT * FROM view_sobremesas")    

    db.session.execute('CALL proc_mais_mesa1(' + str(id_data) + ','+ str(quantidade) + ','+ str(consumo)+')')
    db.session.commit()
    
    valor1=int(RestauranteFinal)

    minha = db.engine.execute("Select codigolocaiscons from view_mesa_restaurante where codigorest=%s ",valor1)

    amounts = minha
    for teste, id_mesa in enumerate(amounts):
        if teste==1:
            dadostabela = db.engine.execute("Select * from view_consumo, view_consumo_items, view_items where view_consumo.codigoconsumo=view_consumo_items.codigoconsumo and view_items.codigoitems=view_consumo_items.codigoitems and view_consumo.codigolocaiscons= %s ORDER BY designacao", id_mesa)
    return render_template('mesa2.html',dadostabela=dadostabela,dadosEntradas=dadosEntradas,dadosCarne=dadosCarne,dadosBebidas=dadosBebidas,dadosPeixes=dadosPeixes,dadosSobremesa=dadosSobremesa,dadosEntradas2=dadosEntradas2,dadosCarne2=dadosCarne2,dadosBebidas2=dadosBebidas2,dadosPeixes2=dadosPeixes2,dadosSobremesa2=dadosSobremesa2)

@app.route('/menosmesa2/<string:id_data>/<int:quantidade>/<string:consumo>', methods=['POST','GET'])
def menosmesa2(id_data,quantidade,consumo):

    dadosEntradas=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa=db.engine.execute("SELECT * FROM view_sobremesas")
    dadosEntradas2=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne2=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes2=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas2=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa2=db.engine.execute("SELECT * FROM view_sobremesas")    

    db.session.execute('CALL proc_menos_mesa1(' + str(id_data) + ','+ str(quantidade) + ','+ str(consumo)+')')
    db.session.commit()
    
    valor1=int(RestauranteFinal)

    minha = db.engine.execute("Select codigolocaiscons from view_mesa_restaurante where codigorest=%s ",valor1)

    amounts = minha
    for teste, id_mesa in enumerate(amounts):
        if teste==1:
            dadostabela = db.engine.execute("Select * from view_consumo, view_consumo_items, view_items where view_consumo.codigoconsumo=view_consumo_items.codigoconsumo and view_items.codigoitems=view_consumo_items.codigoitems and view_consumo.codigolocaiscons= %s ORDER BY designacao", id_mesa)
    return render_template('mesa2.html',dadostabela=dadostabela,dadosEntradas=dadosEntradas,dadosCarne=dadosCarne,dadosBebidas=dadosBebidas,dadosPeixes=dadosPeixes,dadosSobremesa=dadosSobremesa,dadosEntradas2=dadosEntradas2,dadosCarne2=dadosCarne2,dadosBebidas2=dadosBebidas2,dadosPeixes2=dadosPeixes2,dadosSobremesa2=dadosSobremesa2)

@app.route('/adicionarmesa3/<string:id_data>', methods=['POST','GET'])
def adicionarmesa3(id_data):
    db.session.execute("call proc_adiciona_consumo (" + str(id_data) + "," + str(RestauranteFinal) + ")")
    db.session.commit()
    dadosEntradas=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa=db.engine.execute("SELECT * FROM view_sobremesas")

    dadosEntradas2=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne2=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes2=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas2=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa2=db.engine.execute("SELECT * FROM view_sobremesas")

    consumo=db.engine.execute("Select * from view_ultimo_consumo")
    amounts = consumo
    for teste, id_mesa in enumerate(amounts):
        amounts1 = request.form.getlist('Escolha_Entradas1')
        for teste, idx in enumerate(amounts1): 
            sql = "select codigoitems from view_entradas where designacao= '" + idx + "' ;"
            amounts2=db.session.execute(sql)
            for teste, idx1 in enumerate(amounts2): 
                db.session.execute('CALL proc_adiciona_consumo_item(' + str(id_mesa[0]) + ',' + str(idx1[0]) + ')')
                db.session.commit()
    consumo=db.engine.execute("Select * from view_ultimo_consumo")
    amounts = consumo
    for teste, id_mesa in enumerate(amounts):
        amounts1 = request.form.getlist('Escolha_Carne1')
        for teste, idx in enumerate(amounts1): 
            sql = "select codigoitems from view_carne where designacao= '" + idx + "' ;"
            amounts2=db.session.execute(sql)
            for teste, idx1 in enumerate(amounts2): 
                db.session.execute('CALL proc_adiciona_consumo_item(' + str(id_mesa[0]) + ',' + str(idx1[0]) + ')')
                db.session.commit()

    consumo=db.engine.execute("Select * from view_ultimo_consumo")
    amounts = consumo
    for teste, id_mesa in enumerate(amounts):
        amounts1 = request.form.getlist('Escolha_Peixe1')
        for teste, idx in enumerate(amounts1): 
            sql = "select codigoitems from view_peixe where designacao= '" + idx + "' ;"
            amounts2=db.session.execute(sql)
            for teste, idx1 in enumerate(amounts2): 
                db.session.execute('CALL proc_adiciona_consumo_item(' + str(id_mesa[0]) + ',' + str(idx1[0]) + ')')
                db.session.commit()

    consumo=db.engine.execute("Select * from view_ultimo_consumo")
    amounts = consumo
    for teste, id_mesa in enumerate(amounts):
        amounts1 = request.form.getlist('Escolha_Bebida1')
        for teste, idx in enumerate(amounts1): 
            sql = "select codigoitems from view_bebidas where designacao= '" + idx + "' ;"
            amounts2=db.session.execute(sql)
            for teste, idx1 in enumerate(amounts2): 
                db.session.execute('CALL proc_adiciona_consumo_item(' + str(id_mesa[0]) + ',' + str(idx1[0]) + ')')
                db.session.commit()


    consumo=db.engine.execute("Select * from view_ultimo_consumo")
    amounts = consumo
    for teste, id_mesa in enumerate(amounts):
        amounts1 = request.form.getlist('Escolha_Sobremesa1')
        for teste, idx in enumerate(amounts1): 
            sql = "select codigoitems from view_sobremesas where designacao= '" + idx + "' ;"
            amounts2=db.session.execute(sql)
            for teste, idx1 in enumerate(amounts2): 
                db.session.execute('CALL proc_adiciona_consumo_item(' + str(id_mesa[0]) + ',' + str(idx1[0]) + ')')
                db.session.commit()


    valor1=int(RestauranteFinal)

    minha = db.engine.execute("Select codigolocaiscons from view_mesa_restaurante where codigorest=%s ",valor1)

    amounts = minha
    for teste, id_mesa in enumerate(amounts):
        if teste==2:
            dadostabela = db.engine.execute("Select * from view_consumo, view_consumo_items, view_items where view_consumo.codigoconsumo=view_consumo_items.codigoconsumo and view_items.codigoitems=view_consumo_items.codigoitems and view_consumo.codigolocaiscons= %s ORDER BY designacao", id_mesa)

    return render_template('mesa3.html',dadostabela=dadostabela,dadosEntradas=dadosEntradas,dadosCarne=dadosCarne,dadosBebidas=dadosBebidas,dadosPeixes=dadosPeixes,dadosSobremesa=dadosSobremesa,dadosEntradas2=dadosEntradas2,dadosCarne2=dadosCarne2,dadosBebidas2=dadosBebidas2,dadosPeixes2=dadosPeixes2,dadosSobremesa2=dadosSobremesa2)




@app.route('/contadicionarmesa3', methods=['POST'])
def contadicionarmesa3():
    dadosEntradas=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa=db.engine.execute("SELECT * FROM view_sobremesas")

    dadosEntradas2=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne2=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes2=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas2=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa2=db.engine.execute("SELECT * FROM view_sobremesas")

    consumo=db.engine.execute("Select * from view_ultimo_consumo")
    amounts = consumo
    for teste, id_mesa in enumerate(amounts):
        amounts1 = request.form.getlist('Escolha_Entradas')
        for teste, idx in enumerate(amounts1): 
            sql = "select codigoitems from view_entradas where designacao= '" + idx + "' ;"
            amounts2=db.session.execute(sql)
            for teste, idx1 in enumerate(amounts2): 
                db.session.execute('CALL proc_adiciona_consumo_item(' + str(id_mesa[0]) + ',' + str(idx1[0]) + ')')
                db.session.commit()
    consumo=db.engine.execute("Select * from view_ultimo_consumo")
    amounts = consumo
    for teste, id_mesa in enumerate(amounts):
        amounts1 = request.form.getlist('Escolha_Carne')
        for teste, idx in enumerate(amounts1): 
            sql = "select codigoitems from view_carne where designacao= '" + idx + "' ;"
            amounts2=db.session.execute(sql)
            for teste, idx1 in enumerate(amounts2): 
                db.session.execute('CALL proc_adiciona_consumo_item(' + str(id_mesa[0]) + ',' + str(idx1[0]) + ')')
                db.session.commit()

    consumo=db.engine.execute("Select * from view_ultimo_consumo")
    amounts = consumo
    for teste, id_mesa in enumerate(amounts):
        amounts1 = request.form.getlist('Escolha_Peixe')
        for teste, idx in enumerate(amounts1): 
            sql = "select codigoitems from view_peixe where designacao= '" + idx + "' ;"
            amounts2=db.session.execute(sql)
            for teste, idx1 in enumerate(amounts2): 
                db.session.execute('CALL proc_adiciona_consumo_item(' + str(id_mesa[0]) + ',' + str(idx1[0]) + ')')
                db.session.commit()

    consumo=db.engine.execute("Select * from view_ultimo_consumo")
    amounts = consumo
    for teste, id_mesa in enumerate(amounts):
        amounts1 = request.form.getlist('Escolha_Bebida')
        for teste, idx in enumerate(amounts1): 
            sql = "select codigoitems from view_bebidas where designacao= '" + idx + "' ;"
            amounts2=db.session.execute(sql)
            for teste, idx1 in enumerate(amounts2): 
                db.session.execute('CALL proc_adiciona_consumo_item(' + str(id_mesa[0]) + ',' + str(idx1[0]) + ')')
                db.session.commit()

    consumo=db.engine.execute("Select * from view_ultimo_consumo")
    amounts = consumo
    for teste, id_mesa in enumerate(amounts):
        amounts1 = request.form.getlist('Escolha_Sobremesa')
        for teste, idx in enumerate(amounts1): 
            sql = "select codigoitems from view_sobremesas where designacao= '" + idx + "' ;"
            amounts2=db.session.execute(sql)
            for teste, idx1 in enumerate(amounts2): 
                db.session.execute('CALL proc_adiciona_consumo_item(' + str(id_mesa[0]) + ',' + str(idx1[0]) + ')')
                db.session.commit()


    valor1=int(RestauranteFinal)

    minha = db.engine.execute("Select codigolocaiscons from view_mesa_restaurante where codigorest=%s ",valor1)

    amounts = minha
    for teste, id_mesa in enumerate(amounts):
        if teste==2:
            dadostabela = db.engine.execute("Select * from view_consumo, view_consumo_items, view_items where view_consumo.codigoconsumo=view_consumo_items.codigoconsumo and view_items.codigoitems=view_consumo_items.codigoitems and view_consumo.codigolocaiscons= %s ORDER BY designacao", id_mesa)
    return render_template('mesa3.html',dadostabela=dadostabela,dadosEntradas=dadosEntradas,dadosCarne=dadosCarne,dadosBebidas=dadosBebidas,dadosPeixes=dadosPeixes,dadosSobremesa=dadosSobremesa,dadosEntradas2=dadosEntradas2,dadosCarne2=dadosCarne2,dadosBebidas2=dadosBebidas2,dadosPeixes2=dadosPeixes2,dadosSobremesa2=dadosSobremesa2)







@app.route('/eliminaritemmesa3/<string:id_data>/<string:id_consumo>', methods=['POST','GET'])
def eliminaritemmesa3(id_data,id_consumo):

    dadosEntradas=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa=db.engine.execute("SELECT * FROM view_sobremesas")

    dadosEntradas2=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne2=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes2=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas2=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa2=db.engine.execute("SELECT * FROM view_sobremesas")

    db.session.execute('CALL proc_delete_consumo(' + str(id_data) + ',' + str(id_consumo) +')')
    db.session.commit()

    valor1=int(RestauranteFinal)

    minha = db.engine.execute("Select codigolocaiscons from view_mesa_restaurante where codigorest=%s ",valor1)

    amounts = minha
    for teste, id_mesa in enumerate(amounts):
        print(id_mesa)
        if teste==2:
            dadostabela = db.engine.execute("Select * from view_consumo, view_consumo_items, view_items where view_consumo.codigoconsumo=view_consumo_items.codigoconsumo and view_items.codigoitems=view_consumo_items.codigoitems and view_consumo.codigolocaiscons= %s ORDER BY designacao", id_mesa)
    return render_template('mesa3.html',dadostabela=dadostabela,dadosEntradas=dadosEntradas,dadosCarne=dadosCarne,dadosBebidas=dadosBebidas,dadosPeixes=dadosPeixes,dadosSobremesa=dadosSobremesa,dadosEntradas2=dadosEntradas2,dadosCarne2=dadosCarne2,dadosBebidas2=dadosBebidas2,dadosPeixes2=dadosPeixes2,dadosSobremesa2=dadosSobremesa2)

@app.route('/terminarmesa3/<string:id_data>', methods=['POST','GET'])
def terminarmesa3(id_data):


    dadosEntradas=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa=db.engine.execute("SELECT * FROM view_sobremesas")

    dadosEntradas2=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne2=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes2=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas2=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa2=db.engine.execute("SELECT * FROM view_sobremesas")


    nome=request.form['Escolha_Nome']
    NIF=request.form['Escolha_NIF']

    valor1=int(RestauranteFinal)

    minha = db.engine.execute("Select codigolocaiscons from view_mesa_restaurante where codigorest=%s",valor1)

    amounts = minha
    for teste, id_mesa in enumerate(amounts):
        if teste==2:
            db.session.execute("CALL proc_terminar_mesa(" + str(id_data) + ",'"+ str(nome) + "',"+ str(NIF) + ","+ str(id_mesa[0]) +")")
            db.session.commit()
            dadostabela = db.engine.execute("Select * from view_consumo, view_consumo_items, view_items where view_consumo.codigoconsumo=view_consumo_items.codigoconsumo and view_items.codigoitems=view_consumo_items.codigoitems and view_consumo.codigolocaiscons= %s ORDER BY designacao", id_mesa)
            return render_template('mesa3.html',dadostabela=dadostabela,dadosEntradas=dadosEntradas,dadosCarne=dadosCarne,dadosBebidas=dadosBebidas,dadosPeixes=dadosPeixes,dadosSobremesa=dadosSobremesa,dadosEntradas2=dadosEntradas2,dadosCarne2=dadosCarne2,dadosBebidas2=dadosBebidas2,dadosPeixes2=dadosPeixes2,dadosSobremesa2=dadosSobremesa2)

@app.route('/maismesa3/<int:id_data>/<string:quantidade>/<string:consumo>', methods=['POST','GET'])
def maismesa3(id_data,quantidade,consumo):

    dadosEntradas=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa=db.engine.execute("SELECT * FROM view_sobremesas")
    dadosEntradas2=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne2=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes2=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas2=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa2=db.engine.execute("SELECT * FROM view_sobremesas")    

    db.session.execute('CALL proc_mais_mesa1(' + str(id_data) + ','+ str(quantidade) + ','+ str(consumo)+')')
    db.session.commit()
    
    valor1=int(RestauranteFinal)

    minha = db.engine.execute("Select codigolocaiscons from view_mesa_restaurante where codigorest=%s ",valor1)

    amounts = minha
    for teste, id_mesa in enumerate(amounts):
        print(id_mesa)
    
        if teste==2:
            dadostabela = db.engine.execute("Select * from view_consumo, view_consumo_items, view_items where view_consumo.codigoconsumo=view_consumo_items.codigoconsumo and view_items.codigoitems=view_consumo_items.codigoitems and view_consumo.codigolocaiscons= %s ORDER BY designacao", id_mesa)
    return render_template('mesa3.html',dadostabela=dadostabela,dadosEntradas=dadosEntradas,dadosCarne=dadosCarne,dadosBebidas=dadosBebidas,dadosPeixes=dadosPeixes,dadosSobremesa=dadosSobremesa,dadosEntradas2=dadosEntradas2,dadosCarne2=dadosCarne2,dadosBebidas2=dadosBebidas2,dadosPeixes2=dadosPeixes2,dadosSobremesa2=dadosSobremesa2)

@app.route('/menosmesa3/<string:id_data>/<int:quantidade>/<string:consumo>', methods=['POST','GET'])
def menosmesa3(id_data,quantidade,consumo):

    dadosEntradas=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa=db.engine.execute("SELECT * FROM view_sobremesas")
    dadosEntradas2=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne2=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes2=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas2=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa2=db.engine.execute("SELECT * FROM view_sobremesas")    

    db.session.execute('CALL proc_menos_mesa1(' + str(id_data) + ','+ str(quantidade) + ','+ str(consumo)+')')
    db.session.commit()
    
    valor1=int(RestauranteFinal)

    minha = db.engine.execute("Select codigolocaiscons from view_mesa_restaurante where codigorest=%s ",valor1)

    amounts = minha
    for teste, id_mesa in enumerate(amounts):
        if teste==2:
            dadostabela = db.engine.execute("Select * from view_consumo, view_consumo_items, view_items where view_consumo.codigoconsumo=view_consumo_items.codigoconsumo and view_items.codigoitems=view_consumo_items.codigoitems and view_consumo.codigolocaiscons= %s ORDER BY designacao", id_mesa)
    return render_template('mesa3.html',dadostabela=dadostabela,dadosEntradas=dadosEntradas,dadosCarne=dadosCarne,dadosBebidas=dadosBebidas,dadosPeixes=dadosPeixes,dadosSobremesa=dadosSobremesa,dadosEntradas2=dadosEntradas2,dadosCarne2=dadosCarne2,dadosBebidas2=dadosBebidas2,dadosPeixes2=dadosPeixes2,dadosSobremesa2=dadosSobremesa2)

@app.route('/adicionarmesa4/<string:id_data>', methods=['POST','GET'])
def adicionarmesa4(id_data):
    db.session.execute("call proc_adiciona_consumo (" + str(id_data) + "," + str(RestauranteFinal) + ")")
    db.session.commit()
    dadosEntradas=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa=db.engine.execute("SELECT * FROM view_sobremesas")

    dadosEntradas2=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne2=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes2=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas2=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa2=db.engine.execute("SELECT * FROM view_sobremesas")

    consumo=db.engine.execute("Select * from view_ultimo_consumo")
    amounts = consumo
    for teste, id_mesa in enumerate(amounts):
        amounts1 = request.form.getlist('Escolha_Entradas1')
        for teste, idx in enumerate(amounts1): 
            sql = "select codigoitems from view_entradas where designacao= '" + idx + "' ;"
            amounts2=db.session.execute(sql)
            for teste, idx1 in enumerate(amounts2): 
                db.session.execute('CALL proc_adiciona_consumo_item(' + str(id_mesa[0]) + ',' + str(idx1[0]) + ')')
                db.session.commit()
    consumo=db.engine.execute("Select * from view_ultimo_consumo")
    amounts = consumo
    for teste, id_mesa in enumerate(amounts):
        amounts1 = request.form.getlist('Escolha_Carne1')
        for teste, idx in enumerate(amounts1): 
            sql = "select codigoitems from view_carne where designacao= '" + idx + "' ;"
            amounts2=db.session.execute(sql)
            for teste, idx1 in enumerate(amounts2): 
                db.session.execute('CALL proc_adiciona_consumo_item(' + str(id_mesa[0]) + ',' + str(idx1[0]) + ')')
                db.session.commit()

    consumo=db.engine.execute("Select * from view_ultimo_consumo")
    amounts = consumo
    for teste, id_mesa in enumerate(amounts):
        amounts1 = request.form.getlist('Escolha_Peixe1')
        for teste, idx in enumerate(amounts1): 
            sql = "select codigoitems from view_peixe where designacao= '" + idx + "' ;"
            amounts2=db.session.execute(sql)
            for teste, idx1 in enumerate(amounts2): 
                db.session.execute('CALL proc_adiciona_consumo_item(' + str(id_mesa[0]) + ',' + str(idx1[0]) + ')')
                db.session.commit()

    consumo=db.engine.execute("Select * from view_ultimo_consumo")
    amounts = consumo
    for teste, id_mesa in enumerate(amounts):
        amounts1 = request.form.getlist('Escolha_Bebida1')
        for teste, idx in enumerate(amounts1): 
            sql = "select codigoitems from view_bebidas where designacao= '" + idx + "' ;"
            amounts2=db.session.execute(sql)
            for teste, idx1 in enumerate(amounts2): 
                db.session.execute('CALL proc_adiciona_consumo_item(' + str(id_mesa[0]) + ',' + str(idx1[0]) + ')')
                db.session.commit()


    consumo=db.engine.execute("Select * from view_ultimo_consumo")
    amounts = consumo
    for teste, id_mesa in enumerate(amounts):
        amounts1 = request.form.getlist('Escolha_Sobremesa1')
        for teste, idx in enumerate(amounts1): 
            sql = "select codigoitems from view_sobremesas where designacao= '" + idx + "' ;"
            amounts2=db.session.execute(sql)
            for teste, idx1 in enumerate(amounts2): 
                db.session.execute('CALL proc_adiciona_consumo_item(' + str(id_mesa[0]) + ',' + str(idx1[0]) + ')')
                db.session.commit()


    valor1=int(RestauranteFinal)

    minha = db.engine.execute("Select codigolocaiscons from view_mesa_restaurante where codigorest=%s ",valor1)

    amounts = minha
    for teste, id_mesa in enumerate(amounts):
        if teste==3:
            dadostabela = db.engine.execute("Select * from view_consumo, view_consumo_items, view_items where view_consumo.codigoconsumo=view_consumo_items.codigoconsumo and view_items.codigoitems=view_consumo_items.codigoitems and view_consumo.codigolocaiscons= %s ORDER BY designacao", id_mesa)
    return render_template('mesa4.html',dadostabela=dadostabela,dadosEntradas=dadosEntradas,dadosCarne=dadosCarne,dadosBebidas=dadosBebidas,dadosPeixes=dadosPeixes,dadosSobremesa=dadosSobremesa,dadosEntradas2=dadosEntradas2,dadosCarne2=dadosCarne2,dadosBebidas2=dadosBebidas2,dadosPeixes2=dadosPeixes2,dadosSobremesa2=dadosSobremesa2)




@app.route('/contadicionarmesa4', methods=['POST'])
def contadicionarmesa4():
    dadosEntradas=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa=db.engine.execute("SELECT * FROM view_sobremesas")

    dadosEntradas2=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne2=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes2=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas2=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa2=db.engine.execute("SELECT * FROM view_sobremesas")

    consumo=db.engine.execute("Select * from view_ultimo_consumo")
    amounts = consumo
    for teste, id_mesa in enumerate(amounts):
        amounts1 = request.form.getlist('Escolha_Entradas')
        for teste, idx in enumerate(amounts1): 
            sql = "select codigoitems from view_entradas where designacao= '" + idx + "' ;"
            amounts2=db.session.execute(sql)
            for teste, idx1 in enumerate(amounts2): 
                db.session.execute('CALL proc_adiciona_consumo_item(' + str(id_mesa[0]) + ',' + str(idx1[0]) + ')')
                db.session.commit()
    consumo=db.engine.execute("Select * from view_ultimo_consumo")
    amounts = consumo
    for teste, id_mesa in enumerate(amounts):
        amounts1 = request.form.getlist('Escolha_Carne')
        for teste, idx in enumerate(amounts1): 
            sql = "select codigoitems from view_carne where designacao= '" + idx + "' ;"
            amounts2=db.session.execute(sql)
            for teste, idx1 in enumerate(amounts2): 
                db.session.execute('CALL proc_adiciona_consumo_item(' + str(id_mesa[0]) + ',' + str(idx1[0]) + ')')
                db.session.commit()

    consumo=db.engine.execute("Select * from view_ultimo_consumo")
    amounts = consumo
    for teste, id_mesa in enumerate(amounts):
        amounts1 = request.form.getlist('Escolha_Peixe')
        for teste, idx in enumerate(amounts1): 
            sql = "select codigoitems from view_peixe where designacao= '" + idx + "' ;"
            amounts2=db.session.execute(sql)
            for teste, idx1 in enumerate(amounts2): 
                db.session.execute('CALL proc_adiciona_consumo_item(' + str(id_mesa[0]) + ',' + str(idx1[0]) + ')')
                db.session.commit()

    consumo=db.engine.execute("Select * from view_ultimo_consumo")
    amounts = consumo
    for teste, id_mesa in enumerate(amounts):
        amounts1 = request.form.getlist('Escolha_Bebida')
        for teste, idx in enumerate(amounts1): 
            sql = "select codigoitems from view_bebidas where designacao= '" + idx + "' ;"
            amounts2=db.session.execute(sql)
            for teste, idx1 in enumerate(amounts2): 
                db.session.execute('CALL proc_adiciona_consumo_item(' + str(id_mesa[0]) + ',' + str(idx1[0]) + ')')
                db.session.commit()

    consumo=db.engine.execute("Select * from view_ultimo_consumo")
    amounts = consumo
    for teste, id_mesa in enumerate(amounts):
        amounts1 = request.form.getlist('Escolha_Sobremesa')
        for teste, idx in enumerate(amounts1): 
            sql = "select codigoitems from view_sobremesas where designacao= '" + idx + "' ;"
            amounts2=db.session.execute(sql)
            for teste, idx1 in enumerate(amounts2): 
                db.session.execute('CALL proc_adiciona_consumo_item(' + str(id_mesa[0]) + ',' + str(idx1[0]) + ')')
                db.session.commit()


    valor1=int(RestauranteFinal)

    minha = db.engine.execute("Select codigolocaiscons from view_mesa_restaurante where codigorest=%s ",valor1)

    amounts = minha
    for teste, id_mesa in enumerate(amounts):
        if teste==3:
            dadostabela = db.engine.execute("Select * from view_consumo, view_consumo_items, view_items where view_consumo.codigoconsumo=view_consumo_items.codigoconsumo and view_items.codigoitems=view_consumo_items.codigoitems and view_consumo.codigolocaiscons= %s ORDER BY designacao", id_mesa)
    return render_template('mesa4.html',dadostabela=dadostabela,dadosEntradas=dadosEntradas,dadosCarne=dadosCarne,dadosBebidas=dadosBebidas,dadosPeixes=dadosPeixes,dadosSobremesa=dadosSobremesa,dadosEntradas2=dadosEntradas2,dadosCarne2=dadosCarne2,dadosBebidas2=dadosBebidas2,dadosPeixes2=dadosPeixes2,dadosSobremesa2=dadosSobremesa2)




@app.route('/eliminaritemmesa4/<string:id_data>/<string:id_consumo>', methods=['POST','GET'])
def eliminaritemmesa4(id_data,id_consumo):

    dadosEntradas=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa=db.engine.execute("SELECT * FROM view_sobremesas")

    dadosEntradas2=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne2=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes2=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas2=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa2=db.engine.execute("SELECT * FROM view_sobremesas")

    db.session.execute('CALL proc_delete_consumo(' + str(id_data) + ',' + str(id_consumo) +')')
    db.session.commit()

    valor1=int(RestauranteFinal)

    minha = db.engine.execute("Select codigolocaiscons from view_mesa_restaurante where codigorest=%s ",valor1)

    amounts = minha
    for teste, id_mesa in enumerate(amounts):
        if teste==3:
            dadostabela = db.engine.execute("Select * from view_consumo, view_consumo_items, view_items where view_consumo.codigoconsumo=view_consumo_items.codigoconsumo and view_items.codigoitems=view_consumo_items.codigoitems and view_consumo.codigolocaiscons= %s ORDER BY designacao", id_mesa)
    return render_template('mesa4.html',dadostabela=dadostabela,dadosEntradas=dadosEntradas,dadosCarne=dadosCarne,dadosBebidas=dadosBebidas,dadosPeixes=dadosPeixes,dadosSobremesa=dadosSobremesa,dadosEntradas2=dadosEntradas2,dadosCarne2=dadosCarne2,dadosBebidas2=dadosBebidas2,dadosPeixes2=dadosPeixes2,dadosSobremesa2=dadosSobremesa2)




@app.route('/terminarmesa4/<string:id_data>', methods=['POST','GET'])
def terminarmesa4(id_data):


    dadosEntradas=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa=db.engine.execute("SELECT * FROM view_sobremesas")

    dadosEntradas2=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne2=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes2=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas2=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa2=db.engine.execute("SELECT * FROM view_sobremesas")


    nome=request.form['Escolha_Nome']
    NIF=request.form['Escolha_NIF']

    valor1=int(RestauranteFinal)

    minha = db.engine.execute("Select codigolocaiscons from view_mesa_restaurante where codigorest=%s",valor1)

    amounts = minha
    for teste, id_mesa in enumerate(amounts):
        if teste==3:
            db.session.execute("CALL proc_terminar_mesa(" + str(id_data) + ",'"+ str(nome) + "',"+ str(NIF) + ","+ str(id_mesa[0]) +")")
            db.session.commit()
            dadostabela = db.engine.execute("Select * from view_consumo, view_consumo_items, view_items where view_consumo.codigoconsumo=view_consumo_items.codigoconsumo and view_items.codigoitems=view_consumo_items.codigoitems and view_consumo.codigolocaiscons= %s ORDER BY designacao", id_mesa)
            return render_template('mesa4.html',dadostabela=dadostabela,dadosEntradas=dadosEntradas,dadosCarne=dadosCarne,dadosBebidas=dadosBebidas,dadosPeixes=dadosPeixes,dadosSobremesa=dadosSobremesa,dadosEntradas2=dadosEntradas2,dadosCarne2=dadosCarne2,dadosBebidas2=dadosBebidas2,dadosPeixes2=dadosPeixes2,dadosSobremesa2=dadosSobremesa2)

@app.route('/maismesa4/<int:id_data>/<string:quantidade>/<string:consumo>', methods=['POST','GET'])
def maismesa4(id_data,quantidade,consumo):

    dadosEntradas=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa=db.engine.execute("SELECT * FROM view_sobremesas")
    dadosEntradas2=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne2=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes2=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas2=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa2=db.engine.execute("SELECT * FROM view_sobremesas")    

    db.session.execute('CALL proc_mais_mesa1(' + str(id_data) + ','+ str(quantidade) + ','+ str(consumo)+')')
    db.session.commit()
    
    valor1=int(RestauranteFinal)

    minha = db.engine.execute("Select codigolocaiscons from view_mesa_restaurante where codigorest=%s ",valor1)

    amounts = minha
    for teste, id_mesa in enumerate(amounts):
        if teste==3:
            dadostabela = db.engine.execute("Select * from view_consumo, view_consumo_items, view_items where view_consumo.codigoconsumo=view_consumo_items.codigoconsumo and view_items.codigoitems=view_consumo_items.codigoitems and view_consumo.codigolocaiscons= %s ORDER BY designacao", id_mesa)
    return render_template('mesa4.html',dadostabela=dadostabela,dadosEntradas=dadosEntradas,dadosCarne=dadosCarne,dadosBebidas=dadosBebidas,dadosPeixes=dadosPeixes,dadosSobremesa=dadosSobremesa,dadosEntradas2=dadosEntradas2,dadosCarne2=dadosCarne2,dadosBebidas2=dadosBebidas2,dadosPeixes2=dadosPeixes2,dadosSobremesa2=dadosSobremesa2)

@app.route('/menosmesa4/<string:id_data>/<int:quantidade>/<string:consumo>', methods=['POST','GET'])
def menosmesa4(id_data,quantidade,consumo):

    dadosEntradas=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa=db.engine.execute("SELECT * FROM view_sobremesas")
    dadosEntradas2=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne2=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes2=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas2=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa2=db.engine.execute("SELECT * FROM view_sobremesas")    

    db.session.execute('CALL proc_menos_mesa1(' + str(id_data) + ','+ str(quantidade) + ','+ str(consumo)+')')
    db.session.commit()
    
    valor1=int(RestauranteFinal)

    minha = db.engine.execute("Select codigolocaiscons from view_mesa_restaurante where codigorest=%s ",valor1)

    amounts = minha
    for teste, id_mesa in enumerate(amounts):
        if teste==3:
            dadostabela = db.engine.execute("Select * from view_consumo, view_consumo_items, view_items where view_consumo.codigoconsumo=view_consumo_items.codigoconsumo and view_items.codigoitems=view_consumo_items.codigoitems and view_consumo.codigolocaiscons= %s ORDER BY designacao", id_mesa)
    return render_template('mesa4.html',dadostabela=dadostabela,dadosEntradas=dadosEntradas,dadosCarne=dadosCarne,dadosBebidas=dadosBebidas,dadosPeixes=dadosPeixes,dadosSobremesa=dadosSobremesa,dadosEntradas2=dadosEntradas2,dadosCarne2=dadosCarne2,dadosBebidas2=dadosBebidas2,dadosPeixes2=dadosPeixes2,dadosSobremesa2=dadosSobremesa2)

@app.route('/adicionarmesa5/<string:id_data>', methods=['POST','GET'])
def adicionarmesa5(id_data):
    db.session.execute("call proc_adiciona_consumo (" + str(id_data) + "," + str(RestauranteFinal) + ")")
    db.session.commit()
    dadosEntradas=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa=db.engine.execute("SELECT * FROM view_sobremesas")

    dadosEntradas2=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne2=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes2=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas2=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa2=db.engine.execute("SELECT * FROM view_sobremesas")

    consumo=db.engine.execute("Select * from view_ultimo_consumo")
    amounts = consumo
    for teste, id_mesa in enumerate(amounts):
        amounts1 = request.form.getlist('Escolha_Entradas1')
        for teste, idx in enumerate(amounts1): 
            sql = "select codigoitems from view_entradas where designacao= '" + idx + "' ;"
            amounts2=db.session.execute(sql)
            for teste, idx1 in enumerate(amounts2): 
                db.session.execute('CALL proc_adiciona_consumo_item(' + str(id_mesa[0]) + ',' + str(idx1[0]) + ')')
                db.session.commit()
    consumo=db.engine.execute("Select * from view_ultimo_consumo")
    amounts = consumo
    for teste, id_mesa in enumerate(amounts):
        amounts1 = request.form.getlist('Escolha_Carne1')
        for teste, idx in enumerate(amounts1): 
            sql = "select codigoitems from view_carne where designacao= '" + idx + "' ;"
            amounts2=db.session.execute(sql)
            for teste, idx1 in enumerate(amounts2): 
                db.session.execute('CALL proc_adiciona_consumo_item(' + str(id_mesa[0]) + ',' + str(idx1[0]) + ')')
                db.session.commit()

    consumo=db.engine.execute("Select * from view_ultimo_consumo")
    amounts = consumo
    for teste, id_mesa in enumerate(amounts):
        amounts1 = request.form.getlist('Escolha_Peixe1')
        for teste, idx in enumerate(amounts1): 
            sql = "select codigoitems from view_peixe where designacao= '" + idx + "' ;"
            amounts2=db.session.execute(sql)
            for teste, idx1 in enumerate(amounts2): 
                db.session.execute('CALL proc_adiciona_consumo_item(' + str(id_mesa[0]) + ',' + str(idx1[0]) + ')')
                db.session.commit()

    consumo=db.engine.execute("Select * from view_ultimo_consumo")
    amounts = consumo
    for teste, id_mesa in enumerate(amounts):
        amounts1 = request.form.getlist('Escolha_Bebida1')
        for teste, idx in enumerate(amounts1): 
            sql = "select codigoitems from view_bebidas where designacao= '" + idx + "' ;"
            amounts2=db.session.execute(sql)
            for teste, idx1 in enumerate(amounts2): 
                db.session.execute('CALL proc_adiciona_consumo_item(' + str(id_mesa[0]) + ',' + str(idx1[0]) + ')')
                db.session.commit()


    consumo=db.engine.execute("Select * from view_ultimo_consumo")
    amounts = consumo
    for teste, id_mesa in enumerate(amounts):
        amounts1 = request.form.getlist('Escolha_Sobremesa1')
        for teste, idx in enumerate(amounts1): 
            sql = "select codigoitems from view_sobremesas where designacao= '" + idx + "' ;"
            amounts2=db.session.execute(sql)
            for teste, idx1 in enumerate(amounts2): 
                db.session.execute('CALL proc_adiciona_consumo_item(' + str(id_mesa[0]) + ',' + str(idx1[0]) + ')')
                db.session.commit()


    valor1=int(RestauranteFinal)

    minha = db.engine.execute("Select codigolocaiscons from view_mesa_restaurante where codigorest=%s ",valor1)

    amounts = minha
    for teste, id_mesa in enumerate(amounts):
        if teste==4:
            dadostabela = db.engine.execute("Select * from view_consumo, view_consumo_items, view_items where view_consumo.codigoconsumo=view_consumo_items.codigoconsumo and view_items.codigoitems=view_consumo_items.codigoitems and view_consumo.codigolocaiscons= %s ORDER BY designacao", id_mesa)
    return render_template('mesa5.html',dadostabela=dadostabela,dadosEntradas=dadosEntradas,dadosCarne=dadosCarne,dadosBebidas=dadosBebidas,dadosPeixes=dadosPeixes,dadosSobremesa=dadosSobremesa,dadosEntradas2=dadosEntradas2,dadosCarne2=dadosCarne2,dadosBebidas2=dadosBebidas2,dadosPeixes2=dadosPeixes2,dadosSobremesa2=dadosSobremesa2)




@app.route('/contadicionarmesa5', methods=['POST'])
def contadicionarmesa5():
    dadosEntradas=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa=db.engine.execute("SELECT * FROM view_sobremesas")

    dadosEntradas2=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne2=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes2=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas2=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa2=db.engine.execute("SELECT * FROM view_sobremesas")

    consumo=db.engine.execute("Select * from view_ultimo_consumo")
    amounts = consumo
    for teste, id_mesa in enumerate(amounts):
        amounts1 = request.form.getlist('Escolha_Entradas')
        for teste, idx in enumerate(amounts1): 
            sql = "select codigoitems from view_entradas where designacao= '" + idx + "' ;"
            amounts2=db.session.execute(sql)
            for teste, idx1 in enumerate(amounts2): 
                db.session.execute('CALL proc_adiciona_consumo_item(' + str(id_mesa[0]) + ',' + str(idx1[0]) + ')')
                db.session.commit()
    consumo=db.engine.execute("Select * from view_ultimo_consumo")
    amounts = consumo
    for teste, id_mesa in enumerate(amounts):
        amounts1 = request.form.getlist('Escolha_Carne')
        for teste, idx in enumerate(amounts1): 
            sql = "select codigoitems from view_carne where designacao= '" + idx + "' ;"
            amounts2=db.session.execute(sql)
            for teste, idx1 in enumerate(amounts2): 
                db.session.execute('CALL proc_adiciona_consumo_item(' + str(id_mesa[0]) + ',' + str(idx1[0]) + ')')
                db.session.commit()

    consumo=db.engine.execute("Select * from view_ultimo_consumo")
    amounts = consumo
    for teste, id_mesa in enumerate(amounts):
        amounts1 = request.form.getlist('Escolha_Peixe')
        for teste, idx in enumerate(amounts1): 
            sql = "select codigoitems from view_peixe where designacao= '" + idx + "' ;"
            amounts2=db.session.execute(sql)
            for teste, idx1 in enumerate(amounts2): 
                db.session.execute('CALL proc_adiciona_consumo_item(' + str(id_mesa[0]) + ',' + str(idx1[0]) + ')')
                db.session.commit()

    consumo=db.engine.execute("Select * from view_ultimo_consumo")
    amounts = consumo
    for teste, id_mesa in enumerate(amounts):
        amounts1 = request.form.getlist('Escolha_Bebida')
        for teste, idx in enumerate(amounts1): 
            sql = "select codigoitems from view_bebidas where designacao= '" + idx + "' ;"
            amounts2=db.session.execute(sql)
            for teste, idx1 in enumerate(amounts2): 
                db.session.execute('CALL proc_adiciona_consumo_item(' + str(id_mesa[0]) + ',' + str(idx1[0]) + ')')
                db.session.commit()

    consumo=db.engine.execute("Select * from view_ultimo_consumo")
    amounts = consumo
    for teste, id_mesa in enumerate(amounts):
        amounts1 = request.form.getlist('Escolha_Sobremesa')
        for teste, idx in enumerate(amounts1): 
            sql = "select codigoitems from view_sobremesas where designacao= '" + idx + "' ;"
            amounts2=db.session.execute(sql)
            for teste, idx1 in enumerate(amounts2): 
                db.session.execute('CALL proc_adiciona_consumo_item(' + str(id_mesa[0]) + ',' + str(idx1[0]) + ')')
                db.session.commit()


    valor1=int(RestauranteFinal)

    minha = db.engine.execute("Select codigolocaiscons from view_mesa_restaurante where codigorest=%s ",valor1)

    amounts = minha
    for teste, id_mesa in enumerate(amounts):
        if teste==4:
            dadostabela = db.engine.execute("Select * from view_consumo, view_consumo_items, view_items where view_consumo.codigoconsumo=view_consumo_items.codigoconsumo and view_items.codigoitems=view_consumo_items.codigoitems and view_consumo.codigolocaiscons= %s ORDER BY designacao", id_mesa)
    return render_template('mesa5.html',dadostabela=dadostabela,dadosEntradas=dadosEntradas,dadosCarne=dadosCarne,dadosBebidas=dadosBebidas,dadosPeixes=dadosPeixes,dadosSobremesa=dadosSobremesa,dadosEntradas2=dadosEntradas2,dadosCarne2=dadosCarne2,dadosBebidas2=dadosBebidas2,dadosPeixes2=dadosPeixes2,dadosSobremesa2=dadosSobremesa2)







@app.route('/eliminaritemmesa5/<string:id_data>/<string:id_consumo>', methods=['POST','GET'])
def eliminaritemmesa5(id_data,id_consumo):

    dadosEntradas=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa=db.engine.execute("SELECT * FROM view_sobremesas")

    dadosEntradas2=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne2=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes2=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas2=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa2=db.engine.execute("SELECT * FROM view_sobremesas")

    db.session.execute('CALL proc_delete_consumo(' + str(id_data) + ',' + str(id_consumo) +')')
    db.session.commit()

    valor1=int(RestauranteFinal)

    minha = db.engine.execute("Select codigolocaiscons from view_mesa_restaurante where codigorest=%s ",valor1)

    amounts = minha
    for teste, id_mesa in enumerate(amounts):
        if teste==4:
            dadostabela = db.engine.execute("Select * from view_consumo, view_consumo_items, view_items where view_consumo.codigoconsumo=view_consumo_items.codigoconsumo and view_items.codigoitems=view_consumo_items.codigoitems and view_consumo.codigolocaiscons= %s ORDER BY designacao", id_mesa)
    return render_template('mesa5.html',dadostabela=dadostabela,dadosEntradas=dadosEntradas,dadosCarne=dadosCarne,dadosBebidas=dadosBebidas,dadosPeixes=dadosPeixes,dadosSobremesa=dadosSobremesa,dadosEntradas2=dadosEntradas2,dadosCarne2=dadosCarne2,dadosBebidas2=dadosBebidas2,dadosPeixes2=dadosPeixes2,dadosSobremesa2=dadosSobremesa2)


@app.route('/terminarmesa5/<string:id_data>', methods=['POST','GET'])
def terminarmesa5(id_data):


    dadosEntradas=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa=db.engine.execute("SELECT * FROM view_sobremesas")

    dadosEntradas2=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne2=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes2=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas2=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa2=db.engine.execute("SELECT * FROM view_sobremesas")


    nome=request.form['Escolha_Nome']
    NIF=request.form['Escolha_NIF']


    valor1=int(RestauranteFinal)

    minha = db.engine.execute("Select codigolocaiscons from view_mesa_restaurante where codigorest=%s",valor1)

    amounts = minha
    for teste, id_mesa in enumerate(amounts):
        if teste==4:
            db.session.execute("CALL proc_terminar_mesa(" + str(id_data) + ",'"+ str(nome) + "',"+ str(NIF) + ","+ str(id_mesa[0]) +")")
            db.session.commit()
            dadostabela = db.engine.execute("Select * from view_consumo, view_consumo_items, view_items where view_consumo.codigoconsumo=view_consumo_items.codigoconsumo and view_items.codigoitems=view_consumo_items.codigoitems and view_consumo.codigolocaiscons= %s ORDER BY designacao", id_mesa)
            return render_template('mesa5.html',dadostabela=dadostabela,dadosEntradas=dadosEntradas,dadosCarne=dadosCarne,dadosBebidas=dadosBebidas,dadosPeixes=dadosPeixes,dadosSobremesa=dadosSobremesa,dadosEntradas2=dadosEntradas2,dadosCarne2=dadosCarne2,dadosBebidas2=dadosBebidas2,dadosPeixes2=dadosPeixes2,dadosSobremesa2=dadosSobremesa2)


@app.route('/maismesa5/<int:id_data>/<string:quantidade>/<string:consumo>', methods=['POST','GET'])
def maismesa5(id_data,quantidade,consumo):

    dadosEntradas=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa=db.engine.execute("SELECT * FROM view_sobremesas")
    dadosEntradas2=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne2=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes2=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas2=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa2=db.engine.execute("SELECT * FROM view_sobremesas")    

    db.session.execute('CALL proc_mais_mesa1(' + str(id_data) + ','+ str(quantidade) + ','+ str(consumo)+')')
    db.session.commit()
    
    valor1=int(RestauranteFinal)

    minha = db.engine.execute("Select codigolocaiscons from view_mesa_restaurante where codigorest=%s ",valor1)

    amounts = minha
    for teste, id_mesa in enumerate(amounts):
        if teste==4:
            dadostabela = db.engine.execute("Select * from view_consumo, view_consumo_items, view_items where view_consumo.codigoconsumo=view_consumo_items.codigoconsumo and view_items.codigoitems=view_consumo_items.codigoitems and view_consumo.codigolocaiscons= %s ORDER BY designacao", id_mesa)
    return render_template('mesa5.html',dadostabela=dadostabela,dadosEntradas=dadosEntradas,dadosCarne=dadosCarne,dadosBebidas=dadosBebidas,dadosPeixes=dadosPeixes,dadosSobremesa=dadosSobremesa,dadosEntradas2=dadosEntradas2,dadosCarne2=dadosCarne2,dadosBebidas2=dadosBebidas2,dadosPeixes2=dadosPeixes2,dadosSobremesa2=dadosSobremesa2)

@app.route('/menosmesa5/<string:id_data>/<int:quantidade>/<string:consumo>', methods=['POST','GET'])
def menosmesa5(id_data,quantidade,consumo):

    dadosEntradas=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa=db.engine.execute("SELECT * FROM view_sobremesas")
    dadosEntradas2=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne2=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes2=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas2=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa2=db.engine.execute("SELECT * FROM view_sobremesas")    

    db.session.execute('CALL proc_menos_mesa1(' + str(id_data) + ','+ str(quantidade) + ','+ str(consumo)+')')
    db.session.commit()
    
    valor1=int(RestauranteFinal)

    minha = db.engine.execute("Select codigolocaiscons from view_mesa_restaurante where codigorest=%s ",valor1)

    amounts = minha
    for teste, id_mesa in enumerate(amounts):
        if teste==4:
            dadostabela = db.engine.execute("Select * from view_consumo, view_consumo_items, view_items where view_consumo.codigoconsumo=view_consumo_items.codigoconsumo and view_items.codigoitems=view_consumo_items.codigoitems and view_consumo.codigolocaiscons= %s ORDER BY designacao", id_mesa)
    return render_template('mesa5.html',dadostabela=dadostabela,dadosEntradas=dadosEntradas,dadosCarne=dadosCarne,dadosBebidas=dadosBebidas,dadosPeixes=dadosPeixes,dadosSobremesa=dadosSobremesa,dadosEntradas2=dadosEntradas2,dadosCarne2=dadosCarne2,dadosBebidas2=dadosBebidas2,dadosPeixes2=dadosPeixes2,dadosSobremesa2=dadosSobremesa2)

@app.route('/adicionarmesa6/<string:id_data>', methods=['POST','GET'])
def adicionarmesa6(id_data):
    db.session.execute("call proc_adiciona_consumo (" + str(id_data) + "," + str(RestauranteFinal) + ")")
    db.session.commit()
    dadosEntradas=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa=db.engine.execute("SELECT * FROM view_sobremesas")

    dadosEntradas2=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne2=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes2=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas2=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa2=db.engine.execute("SELECT * FROM view_sobremesas")

    consumo=db.engine.execute("Select * from view_ultimo_consumo")
    amounts = consumo
    for teste, id_mesa in enumerate(amounts):
        amounts1 = request.form.getlist('Escolha_Entradas1')
        for teste, idx in enumerate(amounts1): 
            sql = "select codigoitems from view_entradas where designacao= '" + idx + "' ;"
            amounts2=db.session.execute(sql)
            for teste, idx1 in enumerate(amounts2): 
                db.session.execute('CALL proc_adiciona_consumo_item(' + str(id_mesa[0]) + ',' + str(idx1[0]) + ')')
                db.session.commit()
    consumo=db.engine.execute("Select * from view_ultimo_consumo")
    amounts = consumo
    for teste, id_mesa in enumerate(amounts):
        amounts1 = request.form.getlist('Escolha_Carne1')
        for teste, idx in enumerate(amounts1): 
            sql = "select codigoitems from view_carne where designacao= '" + idx + "' ;"
            amounts2=db.session.execute(sql)
            for teste, idx1 in enumerate(amounts2): 
                db.session.execute('CALL proc_adiciona_consumo_item(' + str(id_mesa[0]) + ',' + str(idx1[0]) + ')')
                db.session.commit()

    consumo=db.engine.execute("Select * from view_ultimo_consumo")
    amounts = consumo
    for teste, id_mesa in enumerate(amounts):
        amounts1 = request.form.getlist('Escolha_Peixe1')
        for teste, idx in enumerate(amounts1): 
            sql = "select codigoitems from view_peixe where designacao= '" + idx + "' ;"
            amounts2=db.session.execute(sql)
            for teste, idx1 in enumerate(amounts2): 
                db.session.execute('CALL proc_adiciona_consumo_item(' + str(id_mesa[0]) + ',' + str(idx1[0]) + ')')
                db.session.commit()

    consumo=db.engine.execute("Select * from view_ultimo_consumo")
    amounts = consumo
    for teste, id_mesa in enumerate(amounts):
        amounts1 = request.form.getlist('Escolha_Bebida1')
        for teste, idx in enumerate(amounts1): 
            sql = "select codigoitems from view_bebidas where designacao= '" + idx + "' ;"
            amounts2=db.session.execute(sql)
            for teste, idx1 in enumerate(amounts2): 
                db.session.execute('CALL proc_adiciona_consumo_item(' + str(id_mesa[0]) + ',' + str(idx1[0]) + ')')
                db.session.commit()


    consumo=db.engine.execute("Select * from view_ultimo_consumo")
    amounts = consumo
    for teste, id_mesa in enumerate(amounts):
        amounts1 = request.form.getlist('Escolha_Sobremesa1')
        for teste, idx in enumerate(amounts1): 
            sql = "select codigoitems from view_sobremesas where designacao= '" + idx + "' ;"
            amounts2=db.session.execute(sql)
            for teste, idx1 in enumerate(amounts2): 
                db.session.execute('CALL proc_adiciona_consumo_item(' + str(id_mesa[0]) + ',' + str(idx1[0]) + ')')
                db.session.commit()


    valor1=int(RestauranteFinal)

    minha = db.engine.execute("Select codigolocaiscons from view_mesa_restaurante where codigorest=%s ",valor1)

    amounts = minha
    for teste, id_mesa in enumerate(amounts):
        if teste==5:
            dadostabela = db.engine.execute("Select * from view_consumo, view_consumo_items, view_items where view_consumo.codigoconsumo=view_consumo_items.codigoconsumo and view_items.codigoitems=view_consumo_items.codigoitems and view_consumo.codigolocaiscons= %s ORDER BY designacao", id_mesa)
    return render_template('mesa6.html',dadostabela=dadostabela,dadosEntradas=dadosEntradas,dadosCarne=dadosCarne,dadosBebidas=dadosBebidas,dadosPeixes=dadosPeixes,dadosSobremesa=dadosSobremesa,dadosEntradas2=dadosEntradas2,dadosCarne2=dadosCarne2,dadosBebidas2=dadosBebidas2,dadosPeixes2=dadosPeixes2,dadosSobremesa2=dadosSobremesa2)




@app.route('/contadicionarmesa6', methods=['POST'])
def contadicionarmesa6():
    dadosEntradas=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa=db.engine.execute("SELECT * FROM view_sobremesas")

    dadosEntradas2=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne2=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes2=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas2=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa2=db.engine.execute("SELECT * FROM view_sobremesas")

    consumo=db.engine.execute("Select * from view_ultimo_consumo")
    amounts = consumo
    for teste, id_mesa in enumerate(amounts):
        amounts1 = request.form.getlist('Escolha_Entradas')
        for teste, idx in enumerate(amounts1): 
            sql = "select codigoitems from view_entradas where designacao= '" + idx + "' ;"
            amounts2=db.session.execute(sql)
            for teste, idx1 in enumerate(amounts2): 
                db.session.execute('CALL proc_adiciona_consumo_item(' + str(id_mesa[0]) + ',' + str(idx1[0]) + ')')
                db.session.commit()
    consumo=db.engine.execute("Select * from view_ultimo_consumo")
    amounts = consumo
    for teste, id_mesa in enumerate(amounts):
        amounts1 = request.form.getlist('Escolha_Carne')
        for teste, idx in enumerate(amounts1): 
            sql = "select codigoitems from view_carne where designacao= '" + idx + "' ;"
            amounts2=db.session.execute(sql)
            for teste, idx1 in enumerate(amounts2): 
                db.session.execute('CALL proc_adiciona_consumo_item(' + str(id_mesa[0]) + ',' + str(idx1[0]) + ')')
                db.session.commit()

    consumo=db.engine.execute("Select * from view_ultimo_consumo")
    amounts = consumo
    for teste, id_mesa in enumerate(amounts):
        amounts1 = request.form.getlist('Escolha_Peixe')
        for teste, idx in enumerate(amounts1): 
            sql = "select codigoitems from view_peixe where designacao= '" + idx + "' ;"
            amounts2=db.session.execute(sql)
            for teste, idx1 in enumerate(amounts2): 
                db.session.execute('CALL proc_adiciona_consumo_item(' + str(id_mesa[0]) + ',' + str(idx1[0]) + ')')
                db.session.commit()

    consumo=db.engine.execute("Select * from view_ultimo_consumo")
    amounts = consumo
    for teste, id_mesa in enumerate(amounts):
        amounts1 = request.form.getlist('Escolha_Bebida')
        for teste, idx in enumerate(amounts1): 
            sql = "select codigoitems from view_bebidas where designacao= '" + idx + "' ;"
            amounts2=db.session.execute(sql)
            for teste, idx1 in enumerate(amounts2): 
                db.session.execute('CALL proc_adiciona_consumo_item(' + str(id_mesa[0]) + ',' + str(idx1[0]) + ')')
                db.session.commit()

    consumo=db.engine.execute("Select * from view_ultimo_consumo")
    amounts = consumo
    for teste, id_mesa in enumerate(amounts):
        amounts1 = request.form.getlist('Escolha_Sobremesa')
        for teste, idx in enumerate(amounts1): 
            sql = "select codigoitems from view_sobremesas where designacao= '" + idx + "' ;"
            amounts2=db.session.execute(sql)
            for teste, idx1 in enumerate(amounts2): 
                db.session.execute('CALL proc_adiciona_consumo_item(' + str(id_mesa[0]) + ',' + str(idx1[0]) + ')')
                db.session.commit()


    valor1=int(RestauranteFinal)

    minha = db.engine.execute("Select codigolocaiscons from view_mesa_restaurante where codigorest=%s ",valor1)

    amounts = minha
    for teste, id_mesa in enumerate(amounts):
        if teste==5:
            dadostabela = db.engine.execute("Select * from view_consumo, view_consumo_items, view_items where view_consumo.codigoconsumo=view_consumo_items.codigoconsumo and view_items.codigoitems=view_consumo_items.codigoitems and view_consumo.codigolocaiscons= %s ORDER BY designacao", id_mesa)
    return render_template('mesa6.html',dadostabela=dadostabela,dadosEntradas=dadosEntradas,dadosCarne=dadosCarne,dadosBebidas=dadosBebidas,dadosPeixes=dadosPeixes,dadosSobremesa=dadosSobremesa,dadosEntradas2=dadosEntradas2,dadosCarne2=dadosCarne2,dadosBebidas2=dadosBebidas2,dadosPeixes2=dadosPeixes2,dadosSobremesa2=dadosSobremesa2)




@app.route('/eliminaritemmesa6/<string:id_data>/<string:id_consumo>', methods=['POST','GET'])
def eliminaritemmesa6(id_data,id_consumo):


    dadosEntradas=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa=db.engine.execute("SELECT * FROM view_sobremesas")

    dadosEntradas2=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne2=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes2=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas2=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa2=db.engine.execute("SELECT * FROM view_sobremesas")

    db.session.execute('CALL proc_delete_consumo(' + str(id_data) + ',' + str(id_consumo) +')')
    db.session.commit()

    valor1=int(RestauranteFinal)

    minha = db.engine.execute("Select codigolocaiscons from view_mesa_restaurante where codigorest=%s ",valor1)

    amounts = minha
    for teste, id_mesa in enumerate(amounts):
        if teste==5:
            dadostabela = db.engine.execute("Select * from view_consumo, view_consumo_items, view_items where view_consumo.codigoconsumo=view_consumo_items.codigoconsumo and view_items.codigoitems=view_consumo_items.codigoitems and view_consumo.codigolocaiscons= %s ORDER BY designacao", id_mesa)
    return render_template('mesa6.html',dadostabela=dadostabela,dadosEntradas=dadosEntradas,dadosCarne=dadosCarne,dadosBebidas=dadosBebidas,dadosPeixes=dadosPeixes,dadosSobremesa=dadosSobremesa,dadosEntradas2=dadosEntradas2,dadosCarne2=dadosCarne2,dadosBebidas2=dadosBebidas2,dadosPeixes2=dadosPeixes2,dadosSobremesa2=dadosSobremesa2)

@app.route('/terminarmesa6/<string:id_data>', methods=['POST','GET'])
def terminarmesa6(id_data):


    dadosEntradas=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa=db.engine.execute("SELECT * FROM view_sobremesas")

    dadosEntradas2=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne2=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes2=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas2=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa2=db.engine.execute("SELECT * FROM view_sobremesas")


    nome=request.form['Escolha_Nome']
    NIF=request.form['Escolha_NIF']


    valor1=int(RestauranteFinal)

    minha = db.engine.execute("Select codigolocaiscons from view_mesa_restaurante where codigorest=%s",valor1)

    amounts = minha
    for teste, id_mesa in enumerate(amounts):
        if teste==5:
            db.session.execute("CALL proc_terminar_mesa(" + str(id_data) + ",'"+ str(nome) + "',"+ str(NIF) + ","+ str(id_mesa[0]) +")")
            db.session.commit()
            dadostabela = db.engine.execute("Select * from view_consumo, view_consumo_items, view_items where view_consumo.codigoconsumo=view_consumo_items.codigoconsumo and view_items.codigoitems=view_consumo_items.codigoitems and view_consumo.codigolocaiscons= %s ORDER BY designacao", id_mesa)
            return render_template('mesa6.html',dadostabela=dadostabela,dadosEntradas=dadosEntradas,dadosCarne=dadosCarne,dadosBebidas=dadosBebidas,dadosPeixes=dadosPeixes,dadosSobremesa=dadosSobremesa,dadosEntradas2=dadosEntradas2,dadosCarne2=dadosCarne2,dadosBebidas2=dadosBebidas2,dadosPeixes2=dadosPeixes2,dadosSobremesa2=dadosSobremesa2)

@app.route('/maismesa6/<int:id_data>/<string:quantidade>/<string:consumo>', methods=['POST','GET'])
def maismesa6(id_data,quantidade,consumo):

    dadosEntradas=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa=db.engine.execute("SELECT * FROM view_sobremesas")
    dadosEntradas2=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne2=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes2=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas2=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa2=db.engine.execute("SELECT * FROM view_sobremesas")    

    db.session.execute('CALL proc_mais_mesa1(' + str(id_data) + ','+ str(quantidade) + ','+ str(consumo)+')')
    db.session.commit()
    
    valor1=int(RestauranteFinal)

    minha = db.engine.execute("Select codigolocaiscons from view_mesa_restaurante where codigorest=%s ",valor1)

    amounts = minha
    for teste, id_mesa in enumerate(amounts):
        if teste==5:
            dadostabela = db.engine.execute("Select * from view_consumo, view_consumo_items, view_items where view_consumo.codigoconsumo=view_consumo_items.codigoconsumo and view_items.codigoitems=view_consumo_items.codigoitems and view_consumo.codigolocaiscons= %s ORDER BY designacao", id_mesa)
    return render_template('mesa6.html',dadostabela=dadostabela,dadosEntradas=dadosEntradas,dadosCarne=dadosCarne,dadosBebidas=dadosBebidas,dadosPeixes=dadosPeixes,dadosSobremesa=dadosSobremesa,dadosEntradas2=dadosEntradas2,dadosCarne2=dadosCarne2,dadosBebidas2=dadosBebidas2,dadosPeixes2=dadosPeixes2,dadosSobremesa2=dadosSobremesa2)

@app.route('/menosmesa6/<string:id_data>/<int:quantidade>/<string:consumo>', methods=['POST','GET'])
def menosmesa6(id_data,quantidade,consumo):

    dadosEntradas=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa=db.engine.execute("SELECT * FROM view_sobremesas")
    dadosEntradas2=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne2=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes2=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas2=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa2=db.engine.execute("SELECT * FROM view_sobremesas")    

    db.session.execute('CALL proc_menos_mesa1(' + str(id_data) + ','+ str(quantidade) + ','+ str(consumo)+')')
    db.session.commit()
    
    valor1=int(RestauranteFinal)

    minha = db.engine.execute("Select codigolocaiscons from view_mesa_restaurante where codigorest=%s ",valor1)

    amounts = minha
    for teste, id_mesa in enumerate(amounts):
        if teste==5:
            dadostabela = db.engine.execute("Select * from view_consumo, view_consumo_items, view_items where view_consumo.codigoconsumo=view_consumo_items.codigoconsumo and view_items.codigoitems=view_consumo_items.codigoitems and view_consumo.codigolocaiscons= %s ORDER BY designacao", id_mesa)
    return render_template('mesa6.html',dadostabela=dadostabela,dadosEntradas=dadosEntradas,dadosCarne=dadosCarne,dadosBebidas=dadosBebidas,dadosPeixes=dadosPeixes,dadosSobremesa=dadosSobremesa,dadosEntradas2=dadosEntradas2,dadosCarne2=dadosCarne2,dadosBebidas2=dadosBebidas2,dadosPeixes2=dadosPeixes2,dadosSobremesa2=dadosSobremesa2)

@app.route('/adicionarmesa7/<string:id_data>', methods=['POST','GET'])
def adicionarmesa7(id_data):
    db.session.execute("call proc_adiciona_consumo (" + str(id_data) + "," + str(RestauranteFinal) + ")")
    db.session.commit()
    dadosEntradas=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa=db.engine.execute("SELECT * FROM view_sobremesas")

    dadosEntradas2=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne2=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes2=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas2=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa2=db.engine.execute("SELECT * FROM view_sobremesas")

    consumo=db.engine.execute("Select * from view_ultimo_consumo")
    amounts = consumo
    for teste, id_mesa in enumerate(amounts):
        amounts1 = request.form.getlist('Escolha_Entradas1')
        for teste, idx in enumerate(amounts1): 
            sql = "select codigoitems from view_entradas where designacao= '" + idx + "' ;"
            amounts2=db.session.execute(sql)
            for teste, idx1 in enumerate(amounts2): 
                db.session.execute('CALL proc_adiciona_consumo_item(' + str(id_mesa[0]) + ',' + str(idx1[0]) + ')')
                db.session.commit()
    consumo=db.engine.execute("Select * from view_ultimo_consumo")
    amounts = consumo
    for teste, id_mesa in enumerate(amounts):
        amounts1 = request.form.getlist('Escolha_Carne1')
        for teste, idx in enumerate(amounts1): 
            sql = "select codigoitems from view_carne where designacao= '" + idx + "' ;"
            amounts2=db.session.execute(sql)
            for teste, idx1 in enumerate(amounts2): 
                db.session.execute('CALL proc_adiciona_consumo_item(' + str(id_mesa[0]) + ',' + str(idx1[0]) + ')')
                db.session.commit()

    consumo=db.engine.execute("Select * from view_ultimo_consumo")
    amounts = consumo
    for teste, id_mesa in enumerate(amounts):
        amounts1 = request.form.getlist('Escolha_Peixe1')
        for teste, idx in enumerate(amounts1): 
            sql = "select codigoitems from view_peixe where designacao= '" + idx + "' ;"
            amounts2=db.session.execute(sql)
            for teste, idx1 in enumerate(amounts2): 
                db.session.execute('CALL proc_adiciona_consumo_item(' + str(id_mesa[0]) + ',' + str(idx1[0]) + ')')
                db.session.commit()

    consumo=db.engine.execute("Select * from view_ultimo_consumo")
    amounts = consumo
    for teste, id_mesa in enumerate(amounts):
        amounts1 = request.form.getlist('Escolha_Bebida1')
        for teste, idx in enumerate(amounts1): 
            sql = "select codigoitems from view_bebidas where designacao= '" + idx + "' ;"
            amounts2=db.session.execute(sql)
            for teste, idx1 in enumerate(amounts2): 
                db.session.execute('CALL proc_adiciona_consumo_item(' + str(id_mesa[0]) + ',' + str(idx1[0]) + ')')
                db.session.commit()


    consumo=db.engine.execute("Select * from view_ultimo_consumo")
    amounts = consumo
    for teste, id_mesa in enumerate(amounts):
        amounts1 = request.form.getlist('Escolha_Sobremesa1')
        for teste, idx in enumerate(amounts1): 
            sql = "select codigoitems from view_sobremesas where designacao= '" + idx + "' ;"
            amounts2=db.session.execute(sql)
            for teste, idx1 in enumerate(amounts2): 
                db.session.execute('CALL proc_adiciona_consumo_item(' + str(id_mesa[0]) + ',' + str(idx1[0]) + ')')
                db.session.commit()


    valor1=int(RestauranteFinal)

    minha = db.engine.execute("Select codigolocaiscons from view_mesa_restaurante where codigorest=%s ",valor1)

    amounts = minha
    for teste, id_mesa in enumerate(amounts):
        if teste==6:
            dadostabela = db.engine.execute("Select * from view_consumo, view_consumo_items, view_items where view_consumo.codigoconsumo=view_consumo_items.codigoconsumo and view_items.codigoitems=view_consumo_items.codigoitems and view_consumo.codigolocaiscons= %s ORDER BY designacao", id_mesa)
    return render_template('mesa7.html',dadostabela=dadostabela,dadosEntradas=dadosEntradas,dadosCarne=dadosCarne,dadosBebidas=dadosBebidas,dadosPeixes=dadosPeixes,dadosSobremesa=dadosSobremesa,dadosEntradas2=dadosEntradas2,dadosCarne2=dadosCarne2,dadosBebidas2=dadosBebidas2,dadosPeixes2=dadosPeixes2,dadosSobremesa2=dadosSobremesa2)




@app.route('/contadicionarmesa7', methods=['POST'])
def contadicionarmesa7():
    dadosEntradas=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa=db.engine.execute("SELECT * FROM view_sobremesas")

    dadosEntradas2=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne2=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes2=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas2=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa2=db.engine.execute("SELECT * FROM view_sobremesas")

    consumo=db.engine.execute("Select * from view_ultimo_consumo")
    amounts = consumo
    for teste, id_mesa in enumerate(amounts):
        amounts1 = request.form.getlist('Escolha_Entradas')
        for teste, idx in enumerate(amounts1): 
            sql = "select codigoitems from view_entradas where designacao= '" + idx + "' ;"
            amounts2=db.session.execute(sql)
            for teste, idx1 in enumerate(amounts2): 
                db.session.execute('CALL proc_adiciona_consumo_item(' + str(id_mesa[0]) + ',' + str(idx1[0]) + ')')
                db.session.commit()
    consumo=db.engine.execute("Select * from view_ultimo_consumo")
    amounts = consumo
    for teste, id_mesa in enumerate(amounts):
        amounts1 = request.form.getlist('Escolha_Carne')
        for teste, idx in enumerate(amounts1): 
            sql = "select codigoitems from view_carne where designacao= '" + idx + "' ;"
            amounts2=db.session.execute(sql)
            for teste, idx1 in enumerate(amounts2): 
                db.session.execute('CALL proc_adiciona_consumo_item(' + str(id_mesa[0]) + ',' + str(idx1[0]) + ')')
                db.session.commit()

    consumo=db.engine.execute("Select * from view_ultimo_consumo")
    amounts = consumo
    for teste, id_mesa in enumerate(amounts):
        amounts1 = request.form.getlist('Escolha_Peixe')
        for teste, idx in enumerate(amounts1): 
            sql = "select codigoitems from view_peixe where designacao= '" + idx + "' ;"
            amounts2=db.session.execute(sql)
            for teste, idx1 in enumerate(amounts2): 
                db.session.execute('CALL proc_adiciona_consumo_item(' + str(id_mesa[0]) + ',' + str(idx1[0]) + ')')
                db.session.commit()

    consumo=db.engine.execute("Select * from view_ultimo_consumo")
    amounts = consumo
    for teste, id_mesa in enumerate(amounts):
        amounts1 = request.form.getlist('Escolha_Bebida')
        for teste, idx in enumerate(amounts1): 
            sql = "select codigoitems from view_bebidas where designacao= '" + idx + "' ;"
            amounts2=db.session.execute(sql)
            for teste, idx1 in enumerate(amounts2): 
                db.session.execute('CALL proc_adiciona_consumo_item(' + str(id_mesa[0]) + ',' + str(idx1[0]) + ')')
                db.session.commit()

    consumo=db.engine.execute("Select * from view_ultimo_consumo")
    amounts = consumo
    for teste, id_mesa in enumerate(amounts):
        amounts1 = request.form.getlist('Escolha_Sobremesa')
        for teste, idx in enumerate(amounts1): 
            sql = "select codigoitems from view_sobremesas where designacao= '" + idx + "' ;"
            amounts2=db.session.execute(sql)
            for teste, idx1 in enumerate(amounts2): 
                db.session.execute('CALL proc_adiciona_consumo_item(' + str(id_mesa[0]) + ',' + str(idx1[0]) + ')')
                db.session.commit()


    valor1=int(RestauranteFinal)

    minha = db.engine.execute("Select codigolocaiscons from view_mesa_restaurante where codigorest=%s ",valor1)

    amounts = minha
    for teste, id_mesa in enumerate(amounts):
        if teste==6:
            dadostabela = db.engine.execute("Select * from view_consumo, view_consumo_items, view_items where view_consumo.codigoconsumo=view_consumo_items.codigoconsumo and view_items.codigoitems=view_consumo_items.codigoitems and view_consumo.codigolocaiscons= %s ORDER BY designacao", id_mesa)
    return render_template('mesa7.html',dadostabela=dadostabela,dadosEntradas=dadosEntradas,dadosCarne=dadosCarne,dadosBebidas=dadosBebidas,dadosPeixes=dadosPeixes,dadosSobremesa=dadosSobremesa,dadosEntradas2=dadosEntradas2,dadosCarne2=dadosCarne2,dadosBebidas2=dadosBebidas2,dadosPeixes2=dadosPeixes2,dadosSobremesa2=dadosSobremesa2)







@app.route('/eliminaritemmesa7/<string:id_data>/<string:id_consumo>', methods=['POST','GET'])
def eliminaritemmesa7(id_data,id_consumo):

    dadosEntradas=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa=db.engine.execute("SELECT * FROM view_sobremesas")

    dadosEntradas2=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne2=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes2=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas2=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa2=db.engine.execute("SELECT * FROM view_sobremesas")

    db.session.execute('CALL proc_delete_consumo(' + str(id_data) + ',' + str(id_consumo) +')')
    db.session.commit()

    valor1=int(RestauranteFinal)

    minha = db.engine.execute("Select codigolocaiscons from view_mesa_restaurante where codigorest=%s ",valor1)

    amounts = minha
    for teste, id_mesa in enumerate(amounts):
        if teste==6:
            dadostabela = db.engine.execute("Select * from view_consumo, view_consumo_items, view_items where view_consumo.codigoconsumo=view_consumo_items.codigoconsumo and view_items.codigoitems=view_consumo_items.codigoitems and view_consumo.codigolocaiscons= %s ORDER BY designacao", id_mesa)
    return render_template('mesa7.html',dadostabela=dadostabela,dadosEntradas=dadosEntradas,dadosCarne=dadosCarne,dadosBebidas=dadosBebidas,dadosPeixes=dadosPeixes,dadosSobremesa=dadosSobremesa,dadosEntradas2=dadosEntradas2,dadosCarne2=dadosCarne2,dadosBebidas2=dadosBebidas2,dadosPeixes2=dadosPeixes2,dadosSobremesa2=dadosSobremesa2)

@app.route('/terminarmesa7/<string:id_data>', methods=['POST','GET'])
def terminarmesa7(id_data):


    dadosEntradas=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa=db.engine.execute("SELECT * FROM view_sobremesas")

    dadosEntradas2=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne2=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes2=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas2=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa2=db.engine.execute("SELECT * FROM view_sobremesas")

    nome=request.form['Escolha_Nome']
    NIF=request.form['Escolha_NIF']


    valor1=int(RestauranteFinal)

    minha = db.engine.execute("Select codigolocaiscons from view_mesa_restaurante where codigorest=%s",valor1)

    amounts = minha
    for teste, id_mesa in enumerate(amounts):
        if teste==6:
            db.session.execute("CALL proc_terminar_mesa(" + str(id_data) + ",'"+ str(nome) + "',"+ str(NIF) + ","+ str(id_mesa[0]) +")")
            db.session.commit()
            dadostabela = db.engine.execute("Select * from view_consumo, view_consumo_items, view_items where view_consumo.codigoconsumo=view_consumo_items.codigoconsumo and view_items.codigoitems=view_consumo_items.codigoitems and view_consumo.codigolocaiscons= %s ORDER BY designacao", id_mesa)
            return render_template('mesa7.html',dadostabela=dadostabela,dadosEntradas=dadosEntradas,dadosCarne=dadosCarne,dadosBebidas=dadosBebidas,dadosPeixes=dadosPeixes,dadosSobremesa=dadosSobremesa,dadosEntradas2=dadosEntradas2,dadosCarne2=dadosCarne2,dadosBebidas2=dadosBebidas2,dadosPeixes2=dadosPeixes2,dadosSobremesa2=dadosSobremesa2)



@app.route('/maismesa7/<int:id_data>/<string:quantidade>/<string:consumo>', methods=['POST','GET'])
def maismesa7(id_data,quantidade,consumo):

    dadosEntradas=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa=db.engine.execute("SELECT * FROM view_sobremesas")
    dadosEntradas2=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne2=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes2=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas2=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa2=db.engine.execute("SELECT * FROM view_sobremesas")    

    db.session.execute('CALL proc_mais_mesa1(' + str(id_data) + ','+ str(quantidade) + ','+ str(consumo)+')')
    db.session.commit()
    
    valor1=int(RestauranteFinal)

    minha = db.engine.execute("Select codigolocaiscons from view_mesa_restaurante where codigorest=%s ",valor1)

    amounts = minha
    for teste, id_mesa in enumerate(amounts):
        if teste==6:
            dadostabela = db.engine.execute("Select * from view_consumo, view_consumo_items, view_items where view_consumo.codigoconsumo=view_consumo_items.codigoconsumo and view_items.codigoitems=view_consumo_items.codigoitems and view_consumo.codigolocaiscons= %s ORDER BY designacao", id_mesa)
    return render_template('mesa7.html',dadostabela=dadostabela,dadosEntradas=dadosEntradas,dadosCarne=dadosCarne,dadosBebidas=dadosBebidas,dadosPeixes=dadosPeixes,dadosSobremesa=dadosSobremesa,dadosEntradas2=dadosEntradas2,dadosCarne2=dadosCarne2,dadosBebidas2=dadosBebidas2,dadosPeixes2=dadosPeixes2,dadosSobremesa2=dadosSobremesa2)

@app.route('/menosmesa7/<string:id_data>/<int:quantidade>/<string:consumo>', methods=['POST','GET'])
def menosmesa7(id_data,quantidade,consumo):

    dadosEntradas=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa=db.engine.execute("SELECT * FROM view_sobremesas")
    dadosEntradas2=db.engine.execute("SELECT * FROM view_entradas")
    dadosCarne2=db.engine.execute("SELECT * FROM view_carne")
    dadosPeixes2=db.engine.execute("SELECT * FROM view_peixe")
    dadosBebidas2=db.engine.execute("SELECT * FROM view_bebidas")
    dadosSobremesa2=db.engine.execute("SELECT * FROM view_sobremesas")    

    db.session.execute('CALL proc_menos_mesa1(' + str(id_data) + ','+ str(quantidade) + ','+ str(consumo)+')')
    db.session.commit()
    
    valor1=int(RestauranteFinal)

    minha = db.engine.execute("Select codigolocaiscons from view_mesa_restaurante where codigorest=%s ",valor1)

    amounts = minha
    for teste, id_mesa in enumerate(amounts):
        if teste==6:
            dadostabela = db.engine.execute("Select * from view_consumo, view_consumo_items, view_items where view_consumo.codigoconsumo=view_consumo_items.codigoconsumo and view_items.codigoitems=view_consumo_items.codigoitems and view_consumo.codigolocaiscons= %s ORDER BY designacao", id_mesa)
    return render_template('mesa7.html',dadostabela=dadostabela,dadosEntradas=dadosEntradas,dadosCarne=dadosCarne,dadosBebidas=dadosBebidas,dadosPeixes=dadosPeixes,dadosSobremesa=dadosSobremesa,dadosEntradas2=dadosEntradas2,dadosCarne2=dadosCarne2,dadosBebidas2=dadosBebidas2,dadosPeixes2=dadosPeixes2,dadosSobremesa2=dadosSobremesa2)



@app.route('/listafunc')
def listafunc():

    dadostabela = db.engine.execute("SELECT DISTINCT view_funcionarios.codigofunc, view_funcionarios.nome, view_funcionarios.contacto, view_funcionarios.salario FROM view_funcionarios, view_locaiscons WHERE view_funcionarios.codigofunc=view_locaiscons.codigofunc AND view_locaiscons.codigorest=%s", RestauranteFinal)
    return render_template('listafunc.html',dadostabela=dadostabela)


@app.route('/updatefunc',methods=['POST','GET'])
def updatefunc():
    id2=request.form['id']
    salario=request.form['salario']
    contacto=request.form['contacto']
    db.session.execute('CALL proc_update_func(' + str(id2) + ',' + str(contacto) + ',' + str(salario) + ')')
    db.session.commit()
    dadostabela = db.engine.execute("SELECT DISTINCT view_funcionarios.codigofunc, view_funcionarios.nome, view_funcionarios.contacto, view_funcionarios.salario FROM view_funcionarios, view_locaiscons WHERE view_funcionarios.codigofunc=view_locaiscons.codigofunc AND view_locaiscons.codigorest=%s", RestauranteFinal)
    return render_template('listafunc.html',dadostabela=dadostabela)

@app.route('/adicionarfuncionario', methods = ['POST'])
def adicionarfuncionario():

    nome=request.form['nome']
    salario=request.form['salario1']
    contacto=request.form['contacto1']
    mesas=1
    dados=Funcionarios(nome,contacto,salario)
    db.session.add(dados)
    db.session.flush()
    dados2=LocaisCons(dados.codigofunc,RestauranteFinal,mesas)
    db.session.add(dados2)
    db.session.commit()
    dadostabela = db.engine.execute("SELECT DISTINCT view_funcionarios.codigofunc, view_funcionarios.nome, view_funcionarios.contacto, view_funcionarios.salario FROM view_funcionarios, view_locaiscons WHERE view_funcionarios.codigofunc=view_locaiscons.codigofunc AND view_locaiscons.codigorest=%s", RestauranteFinal)
    return render_template('listafunc.html',dadostabela=dadostabela)

@app.route('/eliminarfunc/<string:id_data>', methods=['GET'])
def eliminarfunc(id_data):

    db.session.execute('CALL proc_eliminar_func(' + str(id_data)  + ')')
    db.session.commit()
    dadostabela = db.engine.execute("SELECT DISTINCT view_funcionarios.codigofunc, view_funcionarios.nome, view_funcionarios.contacto, view_funcionarios.salario FROM view_funcionarios, view_locaiscons WHERE view_funcionarios.codigofunc=view_locaiscons.codigofunc AND view_locaiscons.codigorest=%s", RestauranteFinal)
    return render_template('listafunc.html',dadostabela=dadostabela)

@app.route('/consumosterminados')
def consumosterminados():

    obj = db.session.query(LocaisCons).filter(LocaisCons.codigorest==RestauranteFinal).first()
    print(obj)
    valor=str(obj)
    splitted = valor.split()
    final = splitted[1]
    newstr = final.replace(">", "")
    newstr1 = int(newstr) + 1
    newstr2 = int(newstr) + 2
    newstr3 = int(newstr) + 3
    newstr4 = int(newstr) + 4
    newstr5 = int(newstr) + 5
    newstr6 = int(newstr) + 6

    print(newstr)
    print(newstr1)
    print(newstr2)
    print(newstr3)
    print(newstr4)
    print(newstr5)
    print(newstr6)

    dadostabela = db.session.query(Consumo,Funcionarios,LocaisCons).filter(Consumo.codigolocaiscons==LocaisCons.codigolocaiscons).filter(LocaisCons.codigofunc==Funcionarios.codigofunc).filter(LocaisCons.codigorest==RestauranteFinal).all()


    dadosEntradas=db.session.query(Consumo,ConsumoItems,Items).filter(Consumo.codigoconsumo==ConsumoItems.codigoconsumo).filter(ConsumoItems.codigoitems==Items.codigoitems).filter(Items.codigotipoitem==1).all()
    dadosCarne=db.session.query(Consumo,ConsumoItems,Items).filter(Consumo.codigoconsumo==ConsumoItems.codigoconsumo).filter(ConsumoItems.codigoitems==Items.codigoitems).filter(Items.codigotipoitem==2).all()
    dadosPeixe=db.session.query(Consumo,ConsumoItems,Items).filter(Consumo.codigoconsumo==ConsumoItems.codigoconsumo).filter(ConsumoItems.codigoitems==Items.codigoitems).filter(Items.codigotipoitem==3).all()
    dadosBebidas=db.session.query(Consumo,ConsumoItems,Items).filter(Consumo.codigoconsumo==ConsumoItems.codigoconsumo).filter(ConsumoItems.codigoitems==Items.codigoitems).filter(Items.codigotipoitem==4).all()
    dadosSobremesas=db.session.query(Consumo,ConsumoItems,Items).filter(Consumo.codigoconsumo==ConsumoItems.codigoconsumo).filter(ConsumoItems.codigoitems==Items.codigoitems).filter(Items.codigotipoitem==5).all()

    return render_template('consumosterminados.html',dadostabela=dadostabela,dadosSobremesas=dadosSobremesas,dadosBebidas=dadosBebidas,dadosPeixe=dadosPeixe,dadosCarne=dadosCarne,dadosEntradas=dadosEntradas)

@app.route('/eliminarementa/<string:id_data>', methods=['GET'])
def eliminarementa(id_data):
    db.session.execute("CALL proc_apaga_ementa (" + str(id_data) + ")")
    db.session.commit()

    data= datetime.now()
    date_time = data.strftime("%Y/%m/%d")
    valor1=int(RestauranteFinal)

    dados=db.session.query(Ementas.data,Ementas.codigoementa,Ementas.codigotiporef,Ementas.codigotipoement,Ementas.codigotiporef,RestaurantesEmentas.codigoementa,RestaurantesEmentas.codigorest,TiposEmentas.codigotipoement,TiposEmentas.designacao).filter(TiposEmentas.codigotipoement==Ementas.codigotipoement).filter(RestaurantesEmentas.codigoementa==Ementas.codigoementa).filter(RestaurantesEmentas.codigorest==valor1).filter(Ementas.data>date_time).order_by(Ementas.data,Ementas.codigotiporef,Ementas.codigotipoement).all()
    print (valor1)
    dadosEntradas=db.session.query(Ementas,EmentasItems,Items).filter(Ementas.codigoementa==EmentasItems.codigoementa).filter(EmentasItems.codigoitems==Items.codigoitems).filter(Items.codigotipoitem==1).all()
    dadosCarne=db.session.query(Ementas,EmentasItems,Items).filter(Ementas.codigoementa==EmentasItems.codigoementa).filter(EmentasItems.codigoitems==Items.codigoitems).filter(Items.codigotipoitem==2).all()
    dadosPeixes=db.session.query(Ementas,EmentasItems,Items).filter(Ementas.codigoementa==EmentasItems.codigoementa).filter(EmentasItems.codigoitems==Items.codigoitems).filter(Items.codigotipoitem==3).all()
    dadosBebidas=db.session.query(Ementas,EmentasItems,Items).filter(Ementas.codigoementa==EmentasItems.codigoementa).filter(EmentasItems.codigoitems==Items.codigoitems).filter(Items.codigotipoitem==4).all()
    dadosSobremesa=db.session.query(Ementas,EmentasItems,Items).filter(Ementas.codigoementa==EmentasItems.codigoementa).filter(EmentasItems.codigoitems==Items.codigoitems).filter(Items.codigotipoitem==5).all()
                            
   
    return render_template('removerementa.html',dados=dados,dadosEntradas=dadosEntradas,dadosCarne=dadosCarne,dadosPeixes=dadosPeixes,dadosBebidas=dadosBebidas,dadosSobremesa=dadosSobremesa)


@app.route('/removerementa')
def removerementa():

    
    data= datetime.now()
    date_time = data.strftime("%Y/%m/%d")
    valor1=int(RestauranteFinal)

    dados=db.session.query(Ementas.data,Ementas.codigoementa,Ementas.codigotiporef,Ementas.codigotipoement,Ementas.codigotiporef,RestaurantesEmentas.codigoementa,RestaurantesEmentas.codigorest,TiposEmentas.codigotipoement,TiposEmentas.designacao).filter(TiposEmentas.codigotipoement==Ementas.codigotipoement).filter(RestaurantesEmentas.codigoementa==Ementas.codigoementa).filter(RestaurantesEmentas.codigorest==valor1).filter(Ementas.data>date_time).order_by(Ementas.data,Ementas.codigotiporef,Ementas.codigotipoement).all()
    print (valor1)
    dadosEntradas=db.session.query(Ementas,EmentasItems,Items).filter(Ementas.codigoementa==EmentasItems.codigoementa).filter(EmentasItems.codigoitems==Items.codigoitems).filter(Items.codigotipoitem==1).all()
    dadosCarne=db.session.query(Ementas,EmentasItems,Items).filter(Ementas.codigoementa==EmentasItems.codigoementa).filter(EmentasItems.codigoitems==Items.codigoitems).filter(Items.codigotipoitem==2).all()
    dadosPeixes=db.session.query(Ementas,EmentasItems,Items).filter(Ementas.codigoementa==EmentasItems.codigoementa).filter(EmentasItems.codigoitems==Items.codigoitems).filter(Items.codigotipoitem==3).all()
    dadosBebidas=db.session.query(Ementas,EmentasItems,Items).filter(Ementas.codigoementa==EmentasItems.codigoementa).filter(EmentasItems.codigoitems==Items.codigoitems).filter(Items.codigotipoitem==4).all()
    dadosSobremesa=db.session.query(Ementas,EmentasItems,Items).filter(Ementas.codigoementa==EmentasItems.codigoementa).filter(EmentasItems.codigoitems==Items.codigoitems).filter(Items.codigotipoitem==5).all()
                            
   
    return render_template('removerementa.html',tempo=date_time,dados=dados,dadosEntradas=dadosEntradas,dadosCarne=dadosCarne,dadosPeixes=dadosPeixes,dadosBebidas=dadosBebidas,dadosSobremesa=dadosSobremesa)

















































































"""
@app.route('/updateentradas/<string:id_data>',methods=['GET'])
def updateentradas(id_data):

    designacao=request.form['id_data']
    preco=request.form['id_data']
    db.engine.execute("UPDATE items SET designacao=%s, preco=%s", (designacao, preco))
    db.session.commit()
    dados=db.session.query(Items,TiposItem).filter(Items.codigotipoitem==1).filter(Items.codigotipoitem == TiposItem.codigotipoitem).all()
    return render_template('itens_entradas.html',dados=dados)



@app.route('/criarementa')
def criarementa():
    data=request.form['Escolha_Tipo']
    cod1=1
    cod2=2
    cod3=3
    date=0
    data=Ementas(observacoes)
    db.session.add(cod1,cod2,cod3,data,date)
    db.session.commit()
    return render_template('adicionarementa.html')

"""

"""

@app.route('/')
def index():
    return render_template('pessoa.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        nome=request.form['nome']
        #print(id,nome)
        if nome=='':
            return render_template('index.html', mensagem='Preenche os campos!')

        data=Pessoas(nome)
        db.session.add(data)
        db.session.commit()

        return render_template('inserido.html')


@app.route('/pessoas', methods=['POST'])
def pessoas():
        if request.method == 'POST':
            dados=db.session.query(Pessoas).all()
            #print(dados[0].nome)
            return render_template('pessoas.html', dados=dados)
   
"""

if __name__ == '__main__':
    app.debug=True
    app.run()


