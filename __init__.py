from .auth import auth_bp
from .basket import basket_bp
from .cliente import cliente_bp
from .paginas import paginas_bp
from .produto import produto_bp


def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(basket_bp)
    app.register_blueprint(cliente_bp)
    app.register_blueprint(paginas_bp)
    app.register_blueprint(produto_bp)
