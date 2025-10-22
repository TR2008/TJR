from flask import Flask
from app.extensions import db
from app.routes.auth import auth_bp
from app.routes.produto import produto_bp


# ... outros blueprints

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')  # ou config.BaseConfig

    db.init_app(app)

    with app.app_context():
        db.create_all()  # opcional, se não usar migrations
        app.register_blueprint(auth_bp)
        app.register_blueprint(produto_bp)
        # ... outros blueprints

    return app
