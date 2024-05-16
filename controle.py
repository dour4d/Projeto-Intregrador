from flask import Flask,  render_template, request, redirect, url_for, session, flash
from classes.classes import Login, Cad, Carro

user1 = Login('nath', '123')
user2 = Login('carol', '123')
users = {
    user1.nome: user1,
    user2.nome: user2
}
lista_cad = []
car1 = Carro('Fusca', 'Preto', '1990')
car1 = Carro('Ferrari', 'Amarelo', '1990')
car1 = Carro('Buga', 'preto', '1990')
car1 = Carro('fusca', 'preto', '1990')
car1 = Carro('fusca', 'preto', '1990')
lista_carros = [car1]
app = Flask(__name__)
app.secret_key = 'secret123'

@app.route('/')
def index():
    return render_template('Index.html'  )

@app.route('/login')
def login():
    proxima =  request.args.get('proxima')
    return render_template('login.html', proxima=proxima)



























if __name__ == '__main__':
    app.run(debug=True)