🎟️ Application de Billetterie – Jeux Olympiques 2024
Cette application web permet aux utilisateurs de réserver des billets pour les Jeux Olympiques 2024 via une interface sécurisée. Développée en Flask (Python), elle intègre un panier, une génération de QR code, une base PostgreSQL, et une interface d’administration.

🔧 Prérequis
Python 3.10+
Git
PostgreSQL installé et un utilisateur créé
Un environnement virtuel Python

🚀 Installation locale
1. Cloner le dépôt
   
git clone https://github.com/iiWair/APP.git
cd APP

3. Créer un environnement virtuel

python -m venv venv
source venv/bin/activate  # Sur Windows : venv\Scripts\activate
4. Installer les dépendances

pip install -r requirements.txt

5. Configurer les variables d’environnement
Crée un fichier .env à la racine du projet avec :


FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your_secret_key
DATABASE_URL=postgresql://postgres:admin@localhost:5432/jo_billeterie


5. Initialiser la base de données

flask db init
flask db migrate -m "Initial migration"
flask db upgrade
⚠️ Assurez vous que PostgreSQL tourne bien localement et que la base existe déjà.

6. Lancer l’application

flask run
L’application sera accessible à l’adresse : http://127.0.0.1:5000

📦 Structure du projet

APP/
├── app/                 # Code principal
│   ├── routes/
│   ├── models/
│   ├── templates/
│   └── static/
├── migrations/          # Migrations Alembic
├── .env                 # Variables d’environnement
├── run.py               # Point d'entrée de l'app
└── requirements.txt     # Dépendances Python

📌 Fonctions principales

🔒 Inscription / Connexion sécurisée

🛒 Gestion de panier

💳 Simulation de paiement

🎫 Génération de QR code avec clé unique

⚙️ Interface administrateur

