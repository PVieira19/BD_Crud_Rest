from flask import Flask, render_template, request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from datetime import timedelta


app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost/BD_testes'

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
    observacoes=db.Column(db.String(100), nullable=False)
    data=db.Column(db.Date, nullable=False)

    def __init__(self, codigotiporef, codigotipoement, observacoes, data):
        self.codigotiporef=codigotiporef
        self.codigotipoement=codigotipoement
        self.observacoes=observacoes
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
    codigoconsumoitem=db.Column(db.Integer ,primary_key=True)
    codigoconsumo=db.Column(db.Integer, db.ForeignKey('consumo.codigoconsumo') ,primary_key=True)
    codigoitems=db.Column(db.Integer, db.ForeignKey('items.codigoitems') ,primary_key=True)
    estado=db.Column(db.Integer, nullable=False)

    def __init__(self, codigoconsumo,codigoitems,estado):
        self.codigoconsumo=codigoconsumo
        self.codigoitems=codigoitems
        self.estado=estado

class ClientesLocaisCons(db.Model):
    __tablename__ = 'clienteslocaiscons'
    codigocli=db.Column(db.Integer, db.ForeignKey('clientes.codigocli') ,primary_key=True)
    codigolocaiscons=db.Column(db.Integer, db.ForeignKey('locaiscons.codigolocaiscons') ,primary_key=True)

    def __init__(self, codigocli,codigolocaiscons):
        self.codigocli=codigocli
        self.codigolocaiscons=codigolocaiscons




@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ementa')
def ementa():
    return render_template('ementa.html')

@app.route('/mesa')
def mesa():
    return render_template('mesa.html')

@app.route('/mesa1')
def mesa1():

    dadosRestaurantes=db.session.query(Locais).all()
    dadosEntradas=db.session.query(Items).filter(Items.codigotipoitem==1).all()
    dadosCarne=db.session.query(Items).filter(Items.codigotipoitem==2).all()
    dadosPeixes=db.session.query(Items).filter(Items.codigotipoitem==3).all()
    dadosBebidas=db.session.query(Items).filter(Items.codigotipoitem==4).all()
    dadosSobremesa=db.session.query(Items).filter(Items.codigotipoitem==5).all()

    dadostabela=db.session.query(ConsumoItems,Items,LocaisCons).filter(Items.codigoitems==ConsumoItems.codigoitems).order_by(Items.designacao).all()


    return render_template('mesa1.html',dadostabela=dadostabela,dadosRestaurantes=dadosRestaurantes,dadosEntradas=dadosEntradas,dadosCarne=dadosCarne,dadosBebidas=dadosBebidas,dadosPeixes=dadosPeixes,dadosSobremesa=dadosSobremesa)

@app.route('/mesa2')
def mesa2():
    return render_template('mesa2.html')

@app.route('/mesa3')
def mesa3():
    return render_template('mesa3.html')

@app.route('/mesa4')
def mesa4():
    return render_template('mesa4.html')

@app.route('/mesa5')
def mesa5():
    return render_template('mesa5.html')

@app.route('/mesa6')
def mesa6():
    return render_template('mesa6.html')

@app.route('/mesa7')
def mesa7():
    return render_template('mesa7.html')

@app.route('/mesa8')
def mesa8():
    return render_template('mesa8.html')

@app.route('/itens')
def itens():
    return render_template('itens.html',)

@app.route('/itens_entradas')
def itens_entradas():
    tipo=db.session.query(TiposItem).all()
    dados=db.session.query(Items,TiposItem).filter(Items.codigotipoitem==1).filter(Items.codigotipoitem == TiposItem.codigotipoitem).order_by(Items.codigoitems).all()
    return render_template('itens_entradas.html',dados=dados,tipo=tipo)

@app.route('/itens_pratos_carne')
def itens_pratos_carne():
    dados=db.session.query(Items,TiposItem).filter(Items.codigotipoitem==2).filter(Items.codigotipoitem == TiposItem.codigotipoitem).order_by(Items.designacao).all()
    return render_template('itens_pratos_carne.html',dados=dados)

@app.route('/itens_pratos_peixe')
def itens_pratos_peixe():
    dados=db.session.query(Items,TiposItem).filter(Items.codigotipoitem==3).filter(Items.codigotipoitem == TiposItem.codigotipoitem).order_by(Items.designacao).all()
    return render_template('itens_pratos_peixe.html',dados=dados)

@app.route('/itens_bebidas')
def itens_bebidas():
    dados=db.session.query(Items,TiposItem).filter(Items.codigotipoitem==4).filter(Items.codigotipoitem == TiposItem.codigotipoitem).order_by(Items.designacao).all()
    return render_template('itens_bebidas.html',dados=dados)

@app.route('/itens_sobremesas')
def itens_sobremesas():
    dados=db.session.query(Items,TiposItem).filter(Items.codigotipoitem==5).filter(Items.codigotipoitem == TiposItem.codigotipoitem).order_by(Items.designacao).all()
    return render_template('itens_sobremesas.html',dados=dados)

@app.route('/adicionarementa')
def adicionarementa():
    dados=db.session.query(Items).all()
    return render_template('adicionarementa.html', dados=dados)

@app.route('/ementafinal')
def ementafinal():
    dados=db.session.query(Restaurantes, Locais).filter(Restaurantes.codigoloc == Locais.codigoloc).all()
    dadosCarne=db.session.query(Items).filter(Items.codigotipoitem==2).all()
    dadosEntradas=db.session.query(Items).filter(Items.codigotipoitem==1).all()
    dadosPeixes=db.session.query(Items).filter(Items.codigotipoitem==3).all()
    dadosBebidas=db.session.query(Items).filter(Items.codigotipoitem==4).all()
    dadosSobremesa=db.session.query(Items).filter(Items.codigotipoitem==5).all()

    return render_template('ementafinal.html', dados=dados,dadosCarne=dadosCarne,dadosEntradas=dadosEntradas,dadosPeixes=dadosPeixes,dadosBebidas=dadosBebidas,dadosSobremesa=dadosSobremesa)

@app.route('/adicionarmesa')
def adicionarmesa():
    dados=db.session.query(TiposEmentas).all()
    dadosCarne=db.session.query(Items).filter(Items.codigotipoitem==2).all()
    dadosEntradas=db.session.query(Items).filter(Items.codigotipoitem==1).all()
    dadosPeixes=db.session.query(Items).filter(Items.codigotipoitem==3).all()
    dadosBebidas=db.session.query(Items).filter(Items.codigotipoitem==4).all()
    dadosSobremesa=db.session.query(Items).filter(Items.codigotipoitem==5).all()

    return render_template('adicionarmesa.html', dados=dados,dadosCarne=dadosCarne,dadosEntradas=dadosEntradas,dadosPeixes=dadosPeixes,dadosBebidas=dadosBebidas,dadosSobremesa=dadosSobremesa)

@app.route('/pratododia')
def pratododia():
    dados=db.session.query(Restaurantes, Locais).filter(Restaurantes.codigoloc == Locais.codigoloc).all()
    dadosCarne=db.session.query(Items).filter(Items.codigotipoitem==2).all()
    dadosEntradas=db.session.query(Items).filter(Items.codigotipoitem==1).all()
    dadosPeixes=db.session.query(Items).filter(Items.codigotipoitem==3).all()
    dadosBebidas=db.session.query(Items).filter(Items.codigotipoitem==4).all()
    dadosSobremesa=db.session.query(Items).filter(Items.codigotipoitem==5).all()

    return render_template('pratododia.html', dados=dados,dadosCarne=dadosCarne,dadosEntradas=dadosEntradas,dadosPeixes=dadosPeixes,dadosBebidas=dadosBebidas,dadosSobremesa=dadosSobremesa)


@app.route('/adicionarpratodia', methods=['POST'])
def adicionarpratodia():
      
    amounts = request.form.getlist('Escolha_Data')
    for teste, data_selecionada in enumerate(amounts):
        
        data = datetime.now()

        if data_selecionada == 'Segunda-Feira':
            data_ementa = datetime.now()
        
        if data_selecionada == 'Terça-Feira':
            data_ementa = data + timedelta(days=1)
            
        if data_selecionada == 'Quarta-Feira':
            data_ementa = data + timedelta(days=2)
            
        if data_selecionada == 'Quinta-Feira':
            data_ementa = data + timedelta(days=3)
            
        if data_selecionada == 'Sexta-Feira':
            data_ementa = data + timedelta(days=4)
            
        if data_selecionada == 'Sabado':
            data_ementa = data + timedelta(days=5)
        
        if data_selecionada == 'Domingo':
            data_ementa = data + timedelta(days=6)

        tipo = 1
        teste = request.form['Escolha_Tipo']
        if teste == 'Almoço':
            tipo = 1
        else: 
            tipo = 2
            
        dados=Ementas(tipo,1,"Nao ha",data_ementa)
        db.session.add(dados)
        db.session.flush()
    
        amounts = request.form.getlist('Escolha_Entradas')
        for teste, idx in enumerate(amounts):
            novo=db.session.query(Items.codigoitems).filter(Items.codigotipoitem==1,).filter(Items.designacao==idx)
            dadosentradas=EmentasItems(dados.codigoementa,novo)
            db.session.add(dadosentradas)

        amounts = request.form.getlist('Escolha_Carne')
        for teste, idx in enumerate(amounts):
            novo=db.session.query(Items.codigoitems).filter(Items.codigotipoitem==2,).filter(Items.designacao==idx)
            dadoscarne=EmentasItems(dados.codigoementa,novo)
            db.session.add(dadoscarne)

        amounts = request.form.getlist('Escolha_Peixe')
        for teste, idx in enumerate(amounts):
            novo=db.session.query(Items.codigoitems).filter(Items.codigotipoitem==3,).filter(Items.designacao==idx)
            dadospeixe=EmentasItems(dados.codigoementa,novo)
            db.session.add(dadospeixe)

        amounts = request.form.getlist('Escolha_Bebida')
        for teste, idx in enumerate(amounts):
            novo=db.session.query(Items.codigoitems).filter(Items.codigotipoitem==4,).filter(Items.designacao==idx)
            dadosbebidas=EmentasItems(dados.codigoementa,novo)
            db.session.add(dadosbebidas)

        amounts = request.form.getlist('Escolha_Sobremesa')
        for teste, idx in enumerate(amounts):
            novo=db.session.query(Items.codigoitems).filter(Items.codigotipoitem==5,).filter(Items.designacao==idx)
            dadossobremesas=EmentasItems(dados.codigoementa,novo)
            db.session.add(dadossobremesas)

        """ dadoscarne=EmentasItems(dados.codigoementa,request.form['Escolha_Carne'])
        dadospeixe=EmentasItems(dados.codigoementa,request.form['Escolha_Peixe'])
        dadosbebidas=EmentasItems(dados.codigoementa,request.form['Escolha_Bebida'])
        dadossobremesas=EmentasItems(dados.codigoementa,request.form['Escolha_Sobremesa']) 

        db.session.add(dadosentradas)
        db.session.add(dadoscarne)
        db.session.add(dadospeixe)
        db.session.add(dadosbebidas)
        db.session.add(dadossobremesas) """

        db.session.commit()

    return render_template('index.html')


@app.route('/adicionarementafinal', methods=['POST'])
def adicionarementafinal():
      
    amounts = request.form.getlist('Escolha_Data')
    for teste, data_selecionada in enumerate(amounts):
        
        data = datetime.now()

        if data_selecionada == '1':
            data_ementa = datetime.now()
        
        if data_selecionada == '2':
            data_ementa = data + timedelta(days=1)
            
        if data_selecionada == '3':
            data_ementa = data + timedelta(days=2)
            
        if data_selecionada == '4':
            data_ementa = data + timedelta(days=3)
            
        if data_selecionada == '5':
            data_ementa = data + timedelta(days=4)
            
        if data_selecionada == '6':
            data_ementa = data + timedelta(days=5)
        
        if data_selecionada == '7':
            data_ementa = data + timedelta(days=6)

        dados=Ementas(request.form['Escolha_Tipo'],2,"Nao ha",data_ementa)
        db.session.add(dados)
        db.session.flush()
    
        amounts = request.form.getlist('Escolha_Entradas')
        for teste, idx in enumerate(amounts):
            dadosentradas=EmentasItems(dados.codigoementa,idx)
            db.session.add(dadosentradas)

        amounts = request.form.getlist('Escolha_Carne')
        for teste, idx in enumerate(amounts):
            dadoscarne=EmentasItems(dados.codigoementa,idx)
            db.session.add(dadoscarne)

        amounts = request.form.getlist('Escolha_Peixe')
        for teste, idx in enumerate(amounts):
            dadospeixe=EmentasItems(dados.codigoementa,idx)
            db.session.add(dadospeixe)

        amounts = request.form.getlist('Escolha_Bebida')
        for teste, idx in enumerate(amounts):
            dadosbebidas=EmentasItems(dados.codigoementa,idx)
            db.session.add(dadosbebidas)

        amounts = request.form.getlist('Escolha_Sobremesa')
        for teste, idx in enumerate(amounts):
            dadossobremesas=EmentasItems(dados.codigoementa,idx)
            db.session.add(dadossobremesas)

        """ dadoscarne=EmentasItems(dados.codigoementa,request.form['Escolha_Carne'])
        dadospeixe=EmentasItems(dados.codigoementa,request.form['Escolha_Peixe'])
        dadosbebidas=EmentasItems(dados.codigoementa,request.form['Escolha_Bebida'])
        dadossobremesas=EmentasItems(dados.codigoementa,request.form['Escolha_Sobremesa']) 

        db.session.add(dadosentradas)
        db.session.add(dadoscarne)
        db.session.add(dadospeixe)
        db.session.add(dadosbebidas)
        db.session.add(dadossobremesas) """

        db.session.commit()

    return render_template('index.html')

def funcao (teste):
    print(x)

@app.route('/eliminaritemsobremesa/<string:id_data>', methods=['GET'])
def eliminaritemsobremesa(id_data):
    db.engine.execute("DELETE FROM items WHERE codigoitems=%s", (id_data,))
    db.session.commit()
    dados=db.session.query(Items,TiposItem).filter(Items.codigotipoitem==5).filter(Items.codigotipoitem == TiposItem.codigotipoitem).order_by(Items.designacao).all()
    return render_template('itens_sobremesas.html',dados=dados)

@app.route('/eliminaritementradas/<string:id_data>', methods=['GET'])
def eliminaritementradas(id_data):
    db.engine.execute("DELETE FROM items WHERE codigoitems=%s", (id_data,))
    db.session.commit()
    tipo=db.session.query(TiposItem).all()
    dados=db.session.query(Items,TiposItem).filter(Items.codigotipoitem==1).filter(Items.codigotipoitem == TiposItem.codigotipoitem).order_by(Items.designacao).all()
    return render_template('itens_entradas.html',dados=dados,tipo=tipo)

@app.route('/eliminaritemcarne/<string:id_data>', methods=['GET'])
def eliminaritemcarne(id_data):
    db.engine.execute("DELETE FROM items WHERE codigoitems=%s", (id_data,))
    db.session.commit()
    dados=db.session.query(Items,TiposItem).filter(Items.codigotipoitem==2).filter(Items.codigotipoitem == TiposItem.codigotipoitem).order_by(Items.designacao).all()
    return render_template('itens_pratos_carne.html',dados=dados)

@app.route('/eliminaritempeixe/<string:id_data>', methods=['GET'])
def eliminaritempeixe(id_data):
    db.engine.execute("DELETE FROM items WHERE codigoitems=%s", (id_data,))
    db.session.commit()
    dados=db.session.query(Items,TiposItem).filter(Items.codigotipoitem==3).filter(Items.codigotipoitem == TiposItem.codigotipoitem).order_by(Items.designacao).all()
    return render_template('itens_pratos_peixe.html',dados=dados)

@app.route('/eliminaritembebidas/<string:id_data>', methods=['GET'])
def eliminaritembebidas(id_data):
    db.engine.execute("DELETE FROM items WHERE codigoitems=%s", (id_data,))
    db.session.commit()
    dados=db.session.query(Items,TiposItem).filter(Items.codigotipoitem==4).filter(Items.codigotipoitem == TiposItem.codigotipoitem).order_by(Items.designacao).all()
    return render_template('itens_bebidas.html',dados=dados)

@app.route('/historicoementas')
def historicoementas():

    dados=db.session.query(Ementas).order_by(Ementas.data,Ementas.codigotiporef).all()

    dadosEntradas=db.session.query(Ementas,EmentasItems,Items).filter(Items.codigotipoitem==1).all()
    dadosCarne=db.session.query(Ementas,EmentasItems,Items).filter(Items.codigotipoitem==2).all()
    dadosPeixes=db.session.query(Ementas,EmentasItems,Items).filter(Items.codigotipoitem==3).all()
    dadosBebidas=db.session.query(Ementas,EmentasItems,Items).filter(Items.codigotipoitem==4).all()
    dadosSobremesa=db.session.query(Ementas,EmentasItems,Items).filter(Items.codigotipoitem==5).all()
                            
    return render_template('historicoementas.html',dados=dados,dadosEntradas=dadosEntradas,dadosCarne=dadosCarne,dadosPeixes=dadosPeixes,dadosBebidas=dadosBebidas,dadosSobremesa=dadosSobremesa)


@app.route('/updateentradas',methods=['POST','GET'])
def updateentradas():
    id2=request.form['id']
    designacao=request.form['designacao']
    preco=request.form['custo']
    db.engine.execute("UPDATE items SET designacao=%s, custo=%s WHERE codigoitems=%s", (designacao, preco, id2))
    db.session.commit()
    tipo=db.session.query(TiposItem).all()
    dados=db.session.query(Items,TiposItem).filter(Items.codigotipoitem==1).filter(Items.codigotipoitem == TiposItem.codigotipoitem).order_by(Items.designacao).all()
    return render_template('itens_entradas.html',dados=dados,tipo=tipo)

@app.route('/updatecarne',methods=['POST','GET'])
def updatecarne():
    id2=request.form['id']
    designacao=request.form['designacao']
    preco=request.form['custo']
    db.engine.execute("UPDATE items SET designacao=%s, custo=%s WHERE codigoitems=%s", (designacao, preco, id2))
    db.session.commit()
    tipo=db.session.query(TiposItem).all()
    dados=db.session.query(Items,TiposItem).filter(Items.codigotipoitem==2).filter(Items.codigotipoitem == TiposItem.codigotipoitem).order_by(Items.designacao).all()
    return render_template('itens_pratos_carne.html',dados=dados,tipo=tipo)

@app.route('/updatepeixe',methods=['POST','GET'])
def updatepeixe():
    id2=request.form['id']
    designacao=request.form['designacao']
    preco=request.form['custo']
    db.engine.execute("UPDATE items SET designacao=%s, custo=%s WHERE codigoitems=%s", (designacao, preco, id2))
    db.session.commit()
    tipo=db.session.query(TiposItem).all()
    dados=db.session.query(Items,TiposItem).filter(Items.codigotipoitem==3).filter(Items.codigotipoitem == TiposItem.codigotipoitem).order_by(Items.designacao).all()
    return render_template('itens_pratos_peixe.html',dados=dados,tipo=tipo)

@app.route('/updatebebidas',methods=['POST','GET'])
def updatebebidas():
    id2=request.form['id']
    designacao=request.form['designacao']
    preco=request.form['custo']
    db.engine.execute("UPDATE items SET designacao=%s, custo=%s WHERE codigoitems=%s", (designacao, preco, id2))
    db.session.commit()
    tipo=db.session.query(TiposItem).all()
    dados=db.session.query(Items,TiposItem).filter(Items.codigotipoitem==4).filter(Items.codigotipoitem == TiposItem.codigotipoitem).order_by(Items.designacao).all()
    return render_template('itens_bebidas.html',dados=dados,tipo=tipo)

@app.route('/updatesobremesas',methods=['POST','GET'])
def updatesobremesas():
    id2=request.form['id']
    designacao=request.form['designacao']
    preco=request.form['custo']
    db.engine.execute("UPDATE items SET designacao=%s, custo=%s WHERE codigoitems=%s", (designacao, preco, id2))
    db.session.commit()
    tipo=db.session.query(TiposItem).all()
    dados=db.session.query(Items,TiposItem).filter(Items.codigotipoitem==5).filter(Items.codigotipoitem == TiposItem.codigotipoitem).order_by(Items.designacao).all()
    return render_template('itens_sobremesas.html',dados=dados,tipo=tipo)

@app.route('/adicionarentrada', methods = ['POST'])
def adicionarentrada():

    designacao = request.form['item']
    custo = request.form['preco1']
    db.engine.execute("INSERT INTO items (designacao,codigotipoitem, custo) VALUES (%s,%s,%s)", (designacao,1 ,custo))
    db.session.commit()
    tipo=db.session.query(TiposItem).all()
    dados=db.session.query(Items,TiposItem).filter(Items.codigotipoitem==1).filter(Items.codigotipoitem == TiposItem.codigotipoitem).order_by(Items.designacao).all()
    return render_template('itens_entradas.html',dados=dados,tipo=tipo)

@app.route('/adicionarcarne', methods = ['POST'])
def adicionarcarne():

    designacao = request.form['item']
    custo = request.form['preco1']
    db.engine.execute("INSERT INTO items (designacao,codigotipoitem, custo) VALUES (%s,%s,%s)", (designacao,2 ,custo))
    db.session.commit()
    tipo=db.session.query(TiposItem).all()
    dados=db.session.query(Items,TiposItem).filter(Items.codigotipoitem==2).filter(Items.codigotipoitem == TiposItem.codigotipoitem).order_by(Items.designacao).all()
    return render_template('itens_pratos_carne.html',dados=dados,tipo=tipo)

@app.route('/adicionarpeixe', methods = ['POST'])
def adicionarpeixe():

    designacao = request.form['item']
    custo = request.form['preco1']
    db.engine.execute("INSERT INTO items (designacao,codigotipoitem, custo) VALUES (%s,%s,%s)", (designacao,3 ,custo))
    db.session.commit()
    tipo=db.session.query(TiposItem).all()
    dados=db.session.query(Items,TiposItem).filter(Items.codigotipoitem==3).filter(Items.codigotipoitem == TiposItem.codigotipoitem).order_by(Items.designacao).all()
    return render_template('itens_pratos_peixe.html',dados=dados,tipo=tipo)

@app.route('/adicionarbebidas', methods = ['POST'])
def adicionarbebidas():

    designacao = request.form['item']
    custo = request.form['preco1']
    db.engine.execute("INSERT INTO items (designacao,codigotipoitem, custo) VALUES (%s,%s,%s)", (designacao,4 ,custo))
    db.session.commit()
    tipo=db.session.query(TiposItem).all()
    dados=db.session.query(Items,TiposItem).filter(Items.codigotipoitem==4).filter(Items.codigotipoitem == TiposItem.codigotipoitem).order_by(Items.designacao).all()
    return render_template('itens_bebidas.html',dados=dados,tipo=tipo)

@app.route('/adicionarsobremesas', methods = ['POST'])
def adicionarsobremesas():

    designacao = request.form['item']
    custo = request.form['preco1']
    db.engine.execute("INSERT INTO items (designacao,codigotipoitem, custo) VALUES (%s,%s,%s)", (designacao,5 ,custo))
    db.session.commit()
    tipo=db.session.query(TiposItem).all()
    dados=db.session.query(Items,TiposItem).filter(Items.codigotipoitem==5).filter(Items.codigotipoitem == TiposItem.codigotipoitem).order_by(Items.designacao).all()
    return render_template('itens_sobremesas.html',dados=dados,tipo=tipo)


@app.route('/adicionarmesa1', methods=['POST'])
def adicionarmesa1():
      
    horas = datetime.now()
    restaurante = request.form['local2']
    mesa1=db.session.query(LocaisCons.codigolocaiscons).filter(LocaisCons.codigorest==restaurante).first()
    dadosconsumo=Consumo(1,mesa1,horas)
    db.session.add(dadosconsumo)
    db.session.flush()

    dadosRestaurantes=db.session.query(Locais).all()
    dadosEntradas=db.session.query(Items).filter(Items.codigotipoitem==1).all()
    dadosCarne=db.session.query(Items).filter(Items.codigotipoitem==2).all()
    dadosPeixes=db.session.query(Items).filter(Items.codigotipoitem==3).all()
    dadosBebidas=db.session.query(Items).filter(Items.codigotipoitem==4).all()
    dadosSobremesa=db.session.query(Items).filter(Items.codigotipoitem==5).all()

    obj = db.session.query(Consumo).order_by(Consumo.codigoconsumo.desc()).first()
    """x = db.engine.execute("SELECT codigoconsumo FROM consumo ORDER BY codigoconsumo DESC LIMIT 1;")"""
    print(obj)

    amounts = request.form.getlist('Escolha_Entradas')
    for teste, idx in enumerate(amounts):
        novo=db.session.query(Items.codigoitems).filter(Items.codigotipoitem==1,).filter(Items.designacao==idx)
        dadosentradas=ConsumoItems(dadosconsumo.codigoconsumo,novo,1,1)
        db.session.add(dadosentradas)

    amounts = request.form.getlist('Escolha_Carne')
    for teste, idx in enumerate(amounts):
        novo=db.session.query(Items.codigoitems).filter(Items.codigotipoitem==2,).filter(Items.designacao==idx)
        dadoscarne=ConsumoItems(dadosconsumo.codigoconsumo,novo,1,1)
        db.session.add(dadoscarne)

    amounts = request.form.getlist('Escolha_Peixe')
    for teste, idx in enumerate(amounts):
        novo=db.session.query(Items.codigoitems).filter(Items.codigotipoitem==3,).filter(Items.designacao==idx)
        dadospeixe=ConsumoItems(dadosconsumo.codigoconsumo,novo,1,1)
        db.session.add(dadospeixe)

    amounts = request.form.getlist('Escolha_Bebida')
    for teste, idx in enumerate(amounts):
        novo=db.session.query(Items.codigoitems).filter(Items.codigotipoitem==4,).filter(Items.designacao==idx)
        dadosbebidas=ConsumoItems(dadosconsumo.codigoconsumo,novo,1,1)
        db.session.add(dadosbebidas)

    amounts = request.form.getlist('Escolha_Sobremesa')
    for teste, idx in enumerate(amounts):
        novo=db.session.query(Items.codigoitems).filter(Items.codigotipoitem==5,).filter(Items.designacao==idx)
        dadossobremesas=ConsumoItems(dadosconsumo.codigoconsumo,novo,1,1)
        db.session.add(dadossobremesas)

    db.session.commit()
    dadostabela=db.session.query(ConsumoItems,Items,LocaisCons).filter(Items.codigoitems==ConsumoItems.codigoitems).filter(ConsumoItems.codigoconsumo==dadosconsumo.codigoconsumo).order_by(Items.designacao).all()
    return render_template('mesa1.html',dadostabela=dadostabela,dadosEntradas=dadosEntradas,dadosCarne=dadosCarne,dadosBebidas=dadosBebidas,dadosPeixes=dadosPeixes,dadosSobremesa=dadosSobremesa)




@app.route('/contadicionarmesa1', methods=['POST'])
def contadicionarmesa1():

    horas = datetime.now()
    restaurante = request.form['local2']
    mesa1=db.session.query(LocaisCons.codigolocaiscons).filter(LocaisCons.codigorest==restaurante).first()
    dadosconsumo=Consumo(1,mesa1,horas)


    dadosRestaurantes=db.session.query(Locais).all()
    dadosEntradas=db.session.query(Items).filter(Items.codigotipoitem==1).all()
    dadosCarne=db.session.query(Items).filter(Items.codigotipoitem==2).all()
    dadosPeixes=db.session.query(Items).filter(Items.codigotipoitem==3).all()
    dadosBebidas=db.session.query(Items).filter(Items.codigotipoitem==4).all()
    dadosSobremesa=db.session.query(Items).filter(Items.codigotipoitem==5).all()

    obj = db.session.query(Consumo).order_by(Consumo.codigoconsumo.desc()).first()
    valor=str(obj)

    splitted = valor.split()

    final = splitted[1]

    newstr = final.replace(">", "")

    amounts = request.form.getlist('Escolha_Entradas')
    for teste, idx in enumerate(amounts):
        novo=db.session.query(Items.codigoitems).filter(Items.codigotipoitem==1,).filter(Items.designacao==idx)
        dadosentradas=ConsumoItems(newstr,novo,1,1)
        db.session.add(dadosentradas)

    amounts = request.form.getlist('Escolha_Carne')
    for teste, idx in enumerate(amounts):
        novo=db.session.query(Items.codigoitems).filter(Items.codigotipoitem==2,).filter(Items.designacao==idx)
        dadoscarne=ConsumoItems(newstr,novo,1,1)
        db.session.add(dadoscarne)

    amounts = request.form.getlist('Escolha_Peixe')
    for teste, idx in enumerate(amounts):
        novo=db.session.query(Items.codigoitems).filter(Items.codigotipoitem==3,).filter(Items.designacao==idx)
        dadospeixe=ConsumoItems(newstr,novo,1,1)
        db.session.add(dadospeixe)

    amounts = request.form.getlist('Escolha_Bebida')
    for teste, idx in enumerate(amounts):
        novo=db.session.query(Items.codigoitems).filter(Items.codigotipoitem==4,).filter(Items.designacao==idx)
        dadosbebidas=ConsumoItems(newstr,novo,1,1)
        db.session.add(dadosbebidas)

    amounts = request.form.getlist('Escolha_Sobremesa')
    for teste, idx in enumerate(amounts):
        novo=db.session.query(Items.codigoitems).filter(Items.codigotipoitem==5,).filter(Items.designacao==idx)
        dadossobremesas=ConsumoItems(newstr,novo,1,1)
        db.session.add(dadossobremesas)

    db.session.commit()
    dadostabela=db.session.query(ConsumoItems,Items,LocaisCons).filter(Items.codigoitems==ConsumoItems.codigoitems).filter(ConsumoItems.codigoconsumo==newstr).order_by(Items.designacao).all()
    return render_template('mesa1.html',dadosRestaurantes=dadosRestaurantes,dadostabela=dadostabela,dadosEntradas=dadosEntradas,dadosCarne=dadosCarne,dadosBebidas=dadosBebidas,dadosPeixes=dadosPeixes,dadosSobremesa=dadosSobremesa)







@app.route('/eliminaritemmesa1/<string:id_data>', methods=['GET'])
def eliminaritemmesa1(id_data):

    dadosRestaurantes=db.session.query(Locais).all()
    dadosEntradas=db.session.query(Items).filter(Items.codigotipoitem==1).all()
    dadosCarne=db.session.query(Items).filter(Items.codigotipoitem==2).all()
    dadosPeixes=db.session.query(Items).filter(Items.codigotipoitem==3).all()
    dadosBebidas=db.session.query(Items).filter(Items.codigotipoitem==4).all()
    dadosSobremesa=db.session.query(Items).filter(Items.codigotipoitem==5).all()

    db.engine.execute("DELETE FROM consimoitems WHERE codigoitems=%s", (id_data,))
    db.session.commit()
    dadostabela=db.session.query(ConsumoItems,Items,LocaisCons).filter(Items.codigoitems==ConsumoItems.codigoitems).order_by(Items.designacao).all()
    return render_template('mesa1.html',dadosRestaurantes=dadosRestaurantes,dadostabela=dadostabela,dadosEntradas=dadosEntradas,dadosCarne=dadosCarne,dadosBebidas=dadosBebidas,dadosPeixes=dadosPeixes,dadosSobremesa=dadosSobremesa)

@app.route('/terminarmesa1', methods=['POST'])
def terminarmesa1():

    dadosRestaurantes=db.session.query(Locais).all()
    dadosEntradas=db.session.query(Items).filter(Items.codigotipoitem==1).all()
    dadosCarne=db.session.query(Items).filter(Items.codigotipoitem==2).all()
    dadosPeixes=db.session.query(Items).filter(Items.codigotipoitem==3).all()
    dadosBebidas=db.session.query(Items).filter(Items.codigotipoitem==4).all()
    dadosSobremesa=db.session.query(Items).filter(Items.codigotipoitem==5).all()


    db.engine.execute("UPDATE consimoitems SET estado=0")
    db.session.commit()


    return render_template('mesa1.html',dadosRestaurantes=dadosRestaurantes,dadosEntradas=dadosEntradas,dadosCarne=dadosCarne,dadosBebidas=dadosBebidas,dadosPeixes=dadosPeixes,dadosSobremesa=dadosSobremesa)


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


