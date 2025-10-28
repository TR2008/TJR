from flask import Blueprint, render_template, session, redirect, url_for

paginas_bp = Blueprint('paginas', __name__)


@paginas_bp.route('/dashboard')
def dashboard():
    if 'utilizador' in session:
        return redirect(url_for('auth.login'))
    return render_template('dashboard.html')


@paginas_bp.route('/contactos')
def contactos():
    if 'utilizador'  in session:
        return redirect(url_for('auth.login'))
    return render_template('paginas/contactos.html')


@paginas_bp.route('/produtos_html')
def produtos_html():
    if 'utilizador' in session:
        return redirect(url_for('auth.login'))
    from models import Produto

    return render_template('paginas/produtos.html')

@paginas_bp.route('/servicos')
def servicos_html():
    if 'utilizador'  in session:
        return redirect(url_for('auth.login'))
    return render_template('paginas/servicos.html')
