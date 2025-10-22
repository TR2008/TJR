from flask import Blueprint, session, jsonify, request
from models import Produto

basket_bp = Blueprint('basket', __name__)

# Função auxiliar para obter o cesto da sessão
def get_basket():
    return session.get('basket', {})

# Função auxiliar para calcular o total
def calculate_total(basket):
    total = 0
    num_items = 0
    for item in basket.values():
        total += item['price'] * item['quantity']
        num_items += item['quantity']
    return {'total': total, 'num_items': num_items}

# GET: Ver cesto atual
@basket_bp.route('/api/basket', methods=['GET'])
def ver_cesto():
    if 'utilizador' not in session:
        return jsonify({'success': False, 'message': 'Não autenticado'}), 401

    basket = get_basket()
    summary = calculate_total(basket)
    return jsonify({'success': True, 'basket': basket, 'summary': summary})

# POST: Adicionar item ao cesto
@basket_bp.route('/api/basket/add', methods=['POST'])
def adicionar_ao_cesto():
    if 'utilizador' not in session:
        return jsonify({'success': False, 'message': 'Não autenticado'}), 401

    data = request.get_json()
    produto_id = str(data.get('id'))
    quantidade = int(data.get('quantity', 1))

    produto = Produto.query.get(produto_id)
    if not produto:
        return jsonify({'success': False, 'message': 'Produto não encontrado'}), 404

    basket = get_basket()
    if produto_id in basket:
        basket[produto_id]['quantity'] += quantidade
    else:
        basket[produto_id] = {
            'name': produto.nome,
            'price': produto.preco,
            'quantity': quantidade
        }

    session['basket'] = basket
    summary = calculate_total(basket)
    return jsonify({'success': True, 'basket': basket, 'summary': summary})

# POST: Remover item do cesto
@basket_bp.route('/api/basket/remove', methods=['POST'])
def remover_do_cesto():
    if 'utilizador' not in session:
        return jsonify({'success': False, 'message': 'Não autenticado'}), 401

    data = request.get_json()
    produto_id = str(data.get('id'))
    remover_tudo = data.get('remove_all', False)

    basket = get_basket()
    if produto_id not in basket:
        return jsonify({'success': False, 'message': 'Item não está no cesto'}), 404

    if remover_tudo or basket[produto_id]['quantity'] <= 1:
        del basket[produto_id]
    else:
        basket[produto_id]['quantity'] -= 1

    session['basket'] = basket
    summary = calculate_total(basket)
    return jsonify({'success': True, 'basket': basket, 'summary': summary})