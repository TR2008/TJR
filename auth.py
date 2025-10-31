from flask import Blueprint, request, render_template, redirect, url_for, session, flash
from models import Utilizador, db
from forms import LoginForm, RegistrationForm

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def home():
    if 'utilizador_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('auth.login'))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # Use WTForms validate_on_submit() — it handles POST and CSRF checks.
    if form.validate_on_submit():
        email = form.email.data
        senha = form.senha.data  # match field name in LoginForm
        utilizador = Utilizador.query.filter_by(email=email).first()
        if utilizador and utilizador.verificar_senha(senha):
            session['utilizador_id'] = utilizador.id
            return redirect(url_for('dashboard'))
        else:
            erro = "Email ou password incorretos."
            flash(erro, "danger")
            return render_template('auth/login.html', form=form, erro=erro)
    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout')
def logout():
    session.pop('utilizador_id', None)
    return redirect(url_for('auth.login'))

@auth_bp.route('/criar_utilizador', methods=['GET', 'POST'])
def criar_utilizador():
    form = RegistrationForm()
    if form.validate_on_submit():
        nome = form.nome.data
        email = form.email.data
        senha = form.senha.data

        if Utilizador.query.filter_by(email=email).first():
            flash("Email já está registado.", "danger")
            return render_template('criar_utilizador.html', form=form)

        novo = Utilizador(nome=nome, email=email)
        novo.definir_senha(senha)
        db.session.add(novo)
        db.session.commit()

        flash("Conta criada com sucesso. Pode iniciar sessão.", "success")
        return redirect(url_for('auth.login'))

    return render_template('criar_utilizador.html', form=form)

# Alias so templates that call url_for('auth.register') work without changing them
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    return criar_utilizador()

