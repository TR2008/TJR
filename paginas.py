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
@paginas_bp.route('/politica-privacidade', endpoint='politica_privacidade')
def politica_privacidade():
    return render_template('paginas/politica_privacidade.html')

@paginas_bp.route('/termos-uso', endpoint='termos_uso')
def sobre():
    return render_template('paginas/sobre.html')


# Nova rota para Referências
@paginas_bp.route('/referencias', endpoint='referencias')
def referencias():
    # Permite acesso apenas se autenticado; ajuste conforme necessário
    if 'utilizador' not in session:
        return redirect(url_for('auth.login'))
    return render_template('paginas/referencias.html')
