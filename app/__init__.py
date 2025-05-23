# app/__init__.py
from flask import Flask
from flask_migrate import Migrate  # ← Ajouté
from app.extensions import db, login_manager, bcrypt
from app.models import User
from app.routes import admin as admin_blueprint  # ← Correction ici
import  os
from flask_wtf.csrf import CSRFProtect


csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    app.config['SECRET_KEY'] = 'SECRETKEY'

    # import secret 
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres.mnjkqaykkrlatiokegux:ThomasBpassword2025@aws-0-eu-west-3.pooler.supabase.com:6543/postgres"
    app.config['STRIPE_PUBLIC_KEY'] = os.environ.get("STRIPE_PUBLIC_KEY")
    app.config['STRIPE_SECRET_KEY'] = os.environ.get("STRIPE_SECRET_KEY")

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
    app.register_blueprint(admin_blueprint, url_prefix='/admin')  # ← Correction ici

    return app
