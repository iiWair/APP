import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import Offer


app = create_app()

with app.app_context():
    new_offer = Offer(
        name="Billet Natation - Finales",
        description="Accès aux finales de natation aux JO 2024, catégorie Or",
        price=150.00
    )
    db.session.add(new_offer)
    db.session.commit()
    print("Offre créée avec succès !")
