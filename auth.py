from flask import Blueprint, render_template, redirect, url_for, flash
from models import Utilizador, db
from forms import RegisterForm
from werkzeug.security import generate_password_hash
from forms import LoginForm
from flask_login import logout_user, login_required

auth_bp = Blueprint('auth', __name__)



@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        nome = form.nome.data
        email = form.email.data
        senha = form.senha.data

        # Verifica se o e-mail já existe
        if Utilizador.query.filter_by(email=email).first():
            flash('Este e-mail já está em uso.', 'danger')
            return render_template('auth/criar_utilizador.html', form=form)

        # Cria novo utilizador
        novo_utilizador = Utilizador(
            nome=nome,
            email=email,
            senha_hash=generate_password_hash(senha)
        )
        db.session.add(novo_utilizador)
        db.session.commit()

        flash('Conta criada com sucesso! Faça login.', 'success')
        return redirect(url_for('auth.login'))

    # Aqui é onde a função é usada para mostrar o formulário
    return render_template('auth/criar_utilizador.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        # lógica de autenticação
        return redirect(url_for('paginas.dashboard'))  # ou outro destino

    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sessão terminada com sucesso.', 'info')
    return redirect(url_for('auth.login'))
@auth_bp.route('/auth', methods=['GET', 'POST'])
def auth():
    login_form = LoginForm()
    register_form = RegisterForm()
    modo = request.args.get('modo', 'login')  # 'login' ou 'cadastro'

    if modo == 'cadastro' and register_form.validate_on_submit():
        if Utilizador.query.filter_by(email=register_form.email.data).first():
            flash('Este e-mail já está em uso.', 'danger')
        else:
            novo_utilizador = Utilizador(
                nome=register_form.nome.data,
                email=register_form.email.data,
                senha_hash=generate_password_hash(register_form.senha.data)
            )
            db.session.add(novo_utilizador)
            db.session.commit()
            flash('Conta criada com sucesso!', 'success')

    elif modo == 'login' and login_form.validate_on_submit():
        # lógica de login
        return redirect(url_for('paginas.dashboard'))

    return render_template('auth/autenticacao.html', login_form=login_form, register_form=register_form, modo=modo)

