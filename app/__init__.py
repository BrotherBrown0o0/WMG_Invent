from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect

# Initialize Flask extensions
db = SQLAlchemy()  # Database ORM
login_manager = LoginManager()  # Authentication manager
migrate = Migrate()  # Database migration tool
csrf = CSRFProtect()  # CSRF protection

def create_app(config_class=Config):
    # Create and configure the Flask application
    app = Flask(__name__)  # Use built-in static folder in app/static
    app.config.from_object(config_class)

    # Initialize extensions with the app
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    # Configure the login manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    from app.models.category import Category

    # Make categories available in all templates
    @app.context_processor
    def inject_categories():
        return dict(categories=Category.query.all())

    # Register all blueprints
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
    # Initialize database tables
    from app.models import user, product, category, order
    with create_app().app_context():
        db.create_all()

if __name__ == '__main__':
    init_db() 