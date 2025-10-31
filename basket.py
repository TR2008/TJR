from flask import Blueprint, session, jsonify, request, current_app, redirect, url_for
from decimal import Decimal

basket_bp = Blueprint('basket', __name__)

# Produtos de exemplo / fallback caso não exista modelo Product
PRODUCTS = {
    "1": {"name": "Instalação Simples", "price": 150.00},
    "2": {"name": "Instalação Normal", "price": 200.00},
    "3": {"name": "Instalação Multi II", "price": 350.00},
    "4": {"name": "Instalação Multi III", "price": 550.00},
    "5": {"name": "Montagem Ventiladores", "price": 300.00},
    "6": {"name": "Bombas de Calor", "price": 500.00},
}


def _get_product_from_db_or_fallback(product_id):
    """
    Tenta obter produto de um modelo 'Product' (se existir),
    senão usa PRODUCTS como fallback.
    """
    product = None
    try:
        # tenta importar um modelo Product do seu projecto
        from models import Product  # ajuste o caminho se necessário
        prod = Product.query.get(product_id)
        if prod:
            # ajuste os nomes de atributos conforme o seu modelo real
            name = getattr(prod, 'nome', None) or getattr(prod, 'name', None) or 'Produto'
            price = float(getattr(prod, 'preco', None) or getattr(prod, 'price', 0.0))
            product = {"name": name, "price": price}
    except Exception:
        # se qualquer erro, cai para fallback
        product = None

    if not product:
        product = PRODUCTS.get(str(product_id))
    return product


def _compute_summary(basket):
    total = 0.0
    num_items = 0
    for item in basket.values():
        try:
            total += float(item.get('price', 0)) * int(item.get('quantity', 0))
            num_items += int(item.get('quantity', 0))
        except Exception:
            continue
    return {"total": float(total), "num_items": int(num_items)}


@basket_bp.route('/api/basket', methods=['GET'])
def api_get_basket():
    basket = session.get('basket', {}) or {}
    summary = _compute_summary(basket)
    return jsonify({"success": True, "basket": basket, "summary": summary})


@basket_bp.route('/api/basket/add', methods=['POST'])
def api_add_to_basket():
    data = request.get_json(silent=True) or {}
    product_id = str(data.get('id') or data.get('product_id') or '')
    quantity = int(data.get('quantity', 1) or 1)
    if not product_id:
        return jsonify({"success": False, "message": "ID do produto em falta"}), 400

    product = _get_product_from_db_or_fallback(product_id)
    if not product:
        return jsonify({"success": False, "message": "Produto não encontrado"}), 404

    basket = session.get('basket', {}) or {}
    item = basket.get(product_id, {"name": product["name"], "price": float(product["price"]), "quantity": 0})
    item["quantity"] = int(item.get("quantity", 0)) + quantity
    basket[product_id] = item

    session['basket'] = basket
    session.modified = True

    summary = _compute_summary(basket)
    return jsonify({"success": True, "basket": basket, "summary": summary})


@basket_bp.route('/api/basket/remove', methods=['POST'])
def api_remove_from_basket():
    data = request.get_json(silent=True) or {}
    product_id = str(data.get('id') or '')
    remove_all = bool(data.get('remove_all', False))

    if not product_id:
        return jsonify({"success": False, "message": "ID do produto em falta"}), 400

    basket = session.get('basket', {}) or {}
    if product_id not in basket:
        return jsonify({"success": False, "message": "Produto não no cesto"}), 404

    if remove_all:
        basket.pop(product_id, None)
    else:
        basket[product_id]["quantity"] = max(0, int(basket[product_id].get("quantity", 0)) - 1)
        if basket[product_id]["quantity"] <= 0:
            basket.pop(product_id, None)

    session['basket'] = basket
    session.modified = True
    summary = _compute_summary(basket)
    return jsonify({"success": True, "basket": basket, "summary": summary})


@basket_bp.route('/api/basket/clear', methods=['POST'])
def api_clear_basket():
    session.pop('basket', None)
    session.modified = True
    empty = {"basket": {}, "summary": {"total": 0.0, "num_items": 0}}
    return jsonify({"success": True, **empty})


@basket_bp.route('/api/basket/checkout', methods=['POST'])
def api_checkout():
    """
    Aqui deve integrar com o seu fluxo real de pagamentos/pedidos.
    Por enquanto, simula uma finalização e limpa o cesto.
    """
    # Simular processamento...
    session.pop('basket', None)
    session.modified = True
    empty = {"basket": {}, "summary": {"total": 0.0, "num_items": 0}}
    return jsonify({"success": True, **empty})


# Rota para lidar com o form POST (se usar o botão Comprar (Form) no template)
@basket_bp.route('/adicionar_ao_carrinho', methods=['POST'])
def adicionar_ao_carrinho():
    product_id = request.form.get('produto_id') or request.form.get('product_id')
    if not product_id:
        # pode redirecionar para uma página com mensagem de erro
        return redirect(url_for('produtos'))  # ajuste conforme o seu endpoint de lista de produtos

    # adiciona 1 unidade por formulário
    product = _get_product_from_db_or_fallback(product_id)
    if not product:
        return redirect(url_for('produtos'))

    basket = session.get('basket', {}) or {}
    item = basket.get(str(product_id), {"name": product["name"], "price": float(product["price"]), "quantity": 0})
    item["quantity"] = int(item.get("quantity", 0)) + 1
    basket[str(product_id)] = item
    session['basket'] = basket
    session.modified = True

    # redireciona de volta para a página de produtos (ou para o carrinho)
    return redirect(url_for('paginas.produtos'))  # ajuste para o endpoint correto do seu template