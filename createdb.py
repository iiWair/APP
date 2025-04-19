from app import create_app, db
from app.models import User  # Si tu as un modèle User, tu peux l'importer ici

# Crée une instance de l'application Flask
app = create_app()

# Utiliser le contexte d'application pour exécuter les opérations sur la base de données
with app.app_context():
    # Créer la base de données et toutes les tables définies dans les modèles
    db.create_all()
    print("Base de données et tables créées avec succès !")

    # Ajouter un utilisateur de test si nécessaire
    from werkzeug.security import generate_password_hash
    import secrets

    hashed_pw = generate_password_hash('password123').decode('utf-8')
    secret_key = secrets.token_hex(32)
    
    # Ajouter un utilisateur de test
    user = User(username='thom', email='thomasboundaoui91180@gmail.com', password=hashed_pw, secret_key=secret_key)
    
    db.session.add(user)
    db.session.commit()
    
    print("Utilisateur de test ajouté avec succès !")
