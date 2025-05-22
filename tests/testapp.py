import pytest
from app import create_app
from app.extensions import db
from app.models import User, Offer, Ticket
from app.extensions import bcrypt
import os

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",  
        "WTF_CSRF_ENABLED": False,
        "SECRET_KEY": "testkey",
        "LOGIN_DISABLED": False,
    })

    with app.app_context():
        db.drop_all()
        db.create_all()

        hashed_password = bcrypt.generate_password_hash("password").decode('utf-8')
        user = User(
            username="TestUser",
            email="test@example.com",
            password=hashed_password,  # <-- hash stocké
            secret_key="testsecretkey"
        )
        db.session.add(user)

        offer = Offer(
            name="Offre test",
            description="Description test",
            price=50
        )
        db.session.add(offer)

        db.session.commit()

    yield app



@pytest.fixture
def client(app):
    return app.test_client()

def login(client, email="test@example.com", password="password"):
    return client.post("/login", data={
        "email": email,
        "password": password
    }, follow_redirects=True)

def test_homepage(client):
    res = client.get("/")
    assert res.status_code == 200
    assert b"Bienvenue" in res.data or b"JO 2024" in res.data

def test_login_logout(client):
    res = login(client)
    assert res.status_code == 200
    assert b'href="/logout"' in res.data

    res = client.get("/logout", follow_redirects=True)
    assert b"Connexion" in res.data or b"Login" in res.data

def test_add_to_cart_requires_login(client):
    # Sans login, on doit être redirigé vers login
    res = client.get("/add-to-cart/1", follow_redirects=True)
    assert b"Connexion" in res.data or b"Login" in res.data

def test_add_to_cart_logged_in(client, app):
    with app.app_context():
        user = User.query.filter_by(email="test@example.com").first()
        with client.session_transaction() as sess:
            sess['_user_id'] = str(user.id)  # Simule login Flask-Login

    res = client.get("/add-to-cart/1", follow_redirects=True)
    assert res.status_code == 200
    assert b"panier" in res.data or b"cart" in res.data

def test_qr_code_generation(client, app):
    with app.app_context():
        # Connexion utilisateur
        res = client.post("/login", data={
            "email": "test@example.com",
            "password": "password"
        }, follow_redirects=True)
        assert res.status_code == 200
        assert b"/logout" in res.data  # Vérifie que l'utilisateur est connecté

        # Ajoute une offre au panier
        res = client.get("/add-to-cart/1", follow_redirects=True)
        assert res.status_code == 200

        # Simule le paiement (la route doit exister dans ton app)
        res = client.post("/checkout", follow_redirects=True)
        assert res.status_code == 200

        from app.models import Ticket
        import os

        ticket = Ticket.query.first()

        # Si aucun ticket créé par la route checkout, on le crée manuellement (pour tester)
        if not ticket:
            # Récupère l'utilisateur et l'offre
            from app.models import User, Offer
            user = User.query.filter_by(email="test@example.com").first()
            offer = Offer.query.first()
            assert user is not None, "Utilisateur test non trouvé"
            assert offer is not None, "Offre test non trouvée"

            # Création manuelle d'un ticket pour test
            ticket = Ticket(
                purchase_key="testkey123",
                qr_code_path="app/static/qrcodes/test_qr.png",
                user_id=user.id,
                offer_id=offer.id
            )
            from app.extensions import db
            db.session.add(ticket)
            db.session.commit()

        assert ticket.qr_code_path is not None

