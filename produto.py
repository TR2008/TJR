from flask import Blueprint, request, jsonify, session, redirect, url_for
from models import Produto, db

produto_bp = Blueprint('produto', __name__)



@produto_bp.route('/inserir_preco', methods=['POST'])
def inserir_preco():
    # Verifica se o utilzador está autenticado
    if 'utilizador' not in session:
        return redirect(url_for('auth.login'))

    data = request.get_json()
    nome = data.get('nome')
    categoria = data.get('categoria')
    preco = data.get('preco')

    # Validação dos campos obrigatórios
    if not nome or not categoria or preco is None:
        return jsonify({'erro': 'Todos os campos são obrigatórios'}), 400

    # Validação do tipo de preço
    try:
        preco = float(preco)
    except (TypeError, ValueError):
        return jsonify({'erro': 'Preço inválido'}), 400

    # Verifica se o produto já existe (opcional)
    produto_existente = Produto.query.filter_by(nome=nome, categoria=categoria).first()
    if produto_existente:
        return jsonify({'erro': 'Produto já existe'}), 409

    # Criação e inserção do novo produto
    novo_produto = Produto(nome=nome, categoria=categoria, preco=preco)
    db.session.add(novo_produto)
    db.session.commit()

    return jsonify({
        'mensagem': 'Produto inserido com sucesso!',
        'item': {
            'nome': nome,
            'categoria': categoria,
            'preco': preco
        }
    }), 201
