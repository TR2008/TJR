from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from routes.basket import basket_bp
from flask_wtf import CSRFProtect

db = SQLAlchemy()
csrf = CSRFProtect()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['SECRET_KEY'] = 'algum_valor_secreto'

    db.init_app(app)
    csrf.init_app(app)  # ← Aplica CSRF depois de criar o app

    with app.app_context():
        db.create_all()

    # Importar e registar blueprints
    from routes.auth import auth_bp
    from routes.cliente import cliente_bp
    from routes.produto import produto_bp
    from routes.paginas import paginas_bp
    from routes.basket import basket_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(cliente_bp)
    app.register_blueprint(produto_bp)
    app.register_blueprint(paginas_bp)
    app.register_blueprint(basket_bp)

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
