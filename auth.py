from flask import Blueprint, request, render_template, redirect, url_for, session
from models import Utilizador, db
from forms import LoginForm

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def home():
    if 'utilizador_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('auth.login'))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        senha = form.password.data
        utilizador = Utilizador.query.filter_by(email=email).first()
        if utilizador and utilizador.verificar_senha(senha):
            session['utilizador_id'] = utilizador.id
            return redirect(url_for('dashboard'))
        else:
            erro = "Email ou password incorretos."
            return render_template('index.html', form=form, erro=erro)
    return render_template('index.html', form=form)

@auth_bp.route('/logout')
def logout():
    session.pop('utilizador_id', None)
    return redirect(url_for('auth.login'))

@auth_bp.route('/criar_utilizador', methods=['GET', 'POST'])
def criar_utilizador():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')

        if not nome or not email or not senha:
            return render_template('criar_utilizador.html', erro="Todos os campos são obrigatórios.")

        if Utilizador.query.filter_by(email=email).first():
            return render_template('criar_utilizador.html', erro="Email já está registado.")

        novo = Utilizador(nome=nome, email=email)
        novo.definir_senha(senha)
        db.session.add(novo)
        db.session.commit()
        return redirect(url_for('auth.login'))

    return render_template('criar_utilizador.html')

