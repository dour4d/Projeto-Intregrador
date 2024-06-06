from flask import Flask,  render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'secret123'

app.config['SQLALCHEMY_DATABASE_URI'] = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD = 'mysql+pymysql',
        usuario = 'root',
        senha = 'root',
        servidor = 'localhost',
        database = 'dados'
    )

db = SQLAlchemy(app)

class Carros(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    modelo = db.Column(db.String(50),nullable=False)
    cor = db.Column(db.String(40), nullable=False)
    ano = db.Column(db.String(5), nullable=False)
    
    def __repr__(self):
        return '<Name %r>' % self.name

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    nome = db.Column(db.String(20), nullable=False)
    senha = db.Column(db.String(20), nullable=False)
    cpf = db.Column(db.String(11), nullable=False)
    cidade = db.Column(db.String(20), nullable=False)
    bairro = db.Column(db.String(20), nullable=False)
    rua = db.Column(db.String(20), nullable=False)
    def __repr__(self):
        return '<Name %r>' % self.name

#deslogar
@app.route('/logout')
def logout():
    session['usuarioLogado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('index'))

#tela inicial
@app.route('/')
def index():
    return render_template('Index.html')

#tela de login
@app.route('/login')
def login():
    proxima =  request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

#tela de cadastro
@app.route('/cad')
def cadastro():
    return render_template('Cadastro.html')

# cadastro de usuarios 
@app.route('/criar', methods=['POST'])
def criar():
    if 'usuarioLogado' not in session or session['usuarioLogado'] == None:
        if request.method == 'POST':
            nome = request.form['l_nome']
            senha = request.form['l_senha']
            cpf = request.form['cpf']
            cidade = request.form['cidade']
            bairro = request.form['bairro']
            rua = request.form['rua']
            # if senha.isdigit():
            #     if len(cpf) == 11 and cpf.isdigit:
            
            try:
                novoUser = User(nome=nome, senha=senha, cpf=cpf, cidade=cidade, bairro=bairro, rua=rua)
                db.session.add(novoUser)
                db.session.commit()
                return redirect(url_for('index'))
            except Exception as e:
                return str(e)
        else:
            return render_template('Cadastro.html')
    else:
        return redirect(url_for('index'))
        #     else:
        #         flash('CPF inválida!')
        #         return redirect('cad')
        # else:
        #     flash('Senha inválida!')
        #     return redirect('cad')

#Rota para autenticar login
@app.route('/autenticar', methods=['POST',])
def autenticar():
    usuario = User.query.filter_by(nome=request.form['nome']).first()
    if usuario:
        if request.form['senha'] == usuario.senha:
            session['usuarioLogado'] = usuario.nome
            flash(usuario.nome + ' logado com sucesso!')
            proximaPagina = request.form['proxima']
            return redirect(proximaPagina)
    else:
        flash('Usuario não logado.')
        return redirect(url_for('login'))

#rota para tela de compra
@app.route('/comprar/<int:id>')
def comprar(id):
    if 'usuarioLogado' not in session or session['usuarioLogado'] == None:
        return redirect (url_for('login'))
    else:
        carro_escolhido =  id
        try:
            user_log = session['usuarioLogado']
            usuario_logado = User.query.filter(User.nome == user_log).first()
            carro_selecionado = Carros.query.filter(Carros.id == carro_escolhido).all()
            return render_template('t_compra.html', dados=carro_selecionado, user=usuario_logado )
        except Exception as e:
            return str(e)
    

    


















app.run(debug=True)