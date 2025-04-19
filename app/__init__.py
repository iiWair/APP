# app/__init__.py
from flask import Flask
from flask_migrate import Migrate  # ← Ajouté
from app.extensions import db, login_manager, bcrypt
from app.models import User
from app.routes import admin as admin_blueprint



def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Initialisation des extensions
    db.init_app(app)
    migrate = Migrate(app, db)  # ← Ajouté
    login_manager.init_app(app)
    bcrypt.init_app(app)

    login_manager.login_view = 'main.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(admin_blueprint, url_prefix='/admin')


    return app
