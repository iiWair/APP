from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash
import secrets

app = create_app()

with app.app_context():
    db.create_all()
    print("Base de données et tables créées avec succès !")

    hashed_pw = generate_password_hash('password123')
    secret_key = secrets.token_hex(32)

    user = User(username='test', email='test@gmail.com', password=hashed_pw, secret_key=secret_key)

    db.session.add(user)
    db.session.commit()
    
    print("Utilisateur de test ajouté avec succès !")
