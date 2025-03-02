from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
csrf = CSRFProtect()

def create_app(config_class=Config):
    app = Flask(__name__, static_folder='../static')
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    from app.models.category import Category

    @app.context_processor
    def inject_categories():
        return dict(categories=Category.query.all())

    from app.routes import auth, main, products, admin, orders, reorders
    app.register_blueprint(auth.bp)
    app.register_blueprint(main.bp)
    app.register_blueprint(products.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(orders.bp)
    app.register_blueprint(reorders.bp)

    print(f"Static folder path: {app.static_folder}")
    return app

def init_db():
    from app.models import user, product, category, order
    with create_app().app_context():
        db.create_all()

if __name__ == '__main__':
    init_db() 