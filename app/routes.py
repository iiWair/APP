# app/routes.py

from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, login_required, current_user, logout_user
from app.forms import RegistrationForm, LoginForm
from app import db, bcrypt
from app.models import User, Ticket, Offer, CartItem
import secrets
import qrcode
import os

main = Blueprint('main', __name__)
admin = Blueprint('admin', __name__)

# -----------------------
# ROUTES UTILISATEUR
# -----------------------




@main.route('/')
def home():
    return render_template('index.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        secret_key = secrets.token_hex(32)
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw, secret_key=secret_key)
        db.session.add(user)
        db.session.commit()
        flash('Compte créé avec succès ! Vous pouvez maintenant vous connecter.', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@main.route('/profil')
@login_required
def profil():
    return render_template('profil.html', user=current_user)

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Connexion réussie !', 'success')

            # Redirection en fonction du rôle
            if user.is_admin:
                return redirect(url_for('admin.admin_dashboard'))
            else:
                return redirect(url_for('main.dashboard'))
        else:
            flash('Identifiants invalides. Réessayez.', 'danger')
    return render_template('login.html', form=form)

@main.route('/dashboard')
@login_required
def dashboard():
    tickets = Ticket.query.filter_by(user_id=current_user.id).all()
    offres = Offer.query.all()
    return render_template('dashboard.html', user=current_user, tickets=tickets, offres=offres)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

@main.route('/offers')
def offers():
    offers_list = Offer.query.filter_by(available=True).all()
    return render_template('offers.html', offers=offers_list)

@main.route('/add-to-cart/<int:offer_id>', methods=['GET', 'POST'])  # ← accepte GET maintenant
@login_required
def add_to_cart(offer_id):
    offer = Offer.query.get_or_404(offer_id)
    existing_item = CartItem.query.filter_by(user_id=current_user.id, offer_id=offer.id).first()
    if existing_item:
        flash("Cette offre est déjà dans votre panier.")
    else:
        new_item = CartItem(user_id=current_user.id, offer_id=offer.id)
        db.session.add(new_item)
        db.session.commit()
        flash("Offre ajoutée au panier !")
    return redirect(url_for('main.dashboard'))

@main.route('/cart')
@login_required
def cart():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    offers_in_cart = [item.offer for item in cart_items]
    return render_template('cart.html', cart_items=cart_items, offers=offers_in_cart)

@main.route('/remove-from-cart/<int:offer_id>', methods=['POST'])
@login_required
def remove_from_cart(offer_id):
    # Supprimer l'élément du panier
    cart_item = CartItem.query.filter_by(user_id=current_user.id, offer_id=offer_id).first()
    if cart_item:
        db.session.delete(cart_item)
        db.session.commit()
        flash("Offre retirée du panier", "success")
    else:
        flash("L'offre n'est pas dans votre panier", "danger")
    return redirect(url_for('main.cart'))


from datetime import datetime
import secrets

@main.route('/checkout', methods=['POST'])  # ← On ajoute POST ici
@login_required
def checkout():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    if not cart_items:
        flash("Votre panier est vide.", 'warning')
        return redirect(url_for('main.cart'))

    for item in cart_items:
        offer = Offer.query.get(item.offer_id)
        if offer is None:
            db.session.delete(item)
            continue

        # Générer la clé et le QR Code
        purchase_key = secrets.token_hex(16)
        qr_path = generate_qr_code(purchase_key=purchase_key, user_id=current_user.id)

        # Créer le ticket avec le QR Code
        ticket = Ticket(
            user_id=current_user.id,
            offer_id=offer.id,
            purchase_key=purchase_key,
            qr_code_path=qr_path,
            timestamp=datetime.now()
        )
        db.session.add(ticket)

    # Vider le panier
    CartItem.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()

    flash("Achat validé avec succès ! Vos QR Codes sont disponibles dans vos billets.", 'success')
    return redirect(url_for('main.dashboard'))

def generate_qr_code(purchase_key, user_id):
    qr_folder = os.path.join('static', 'qr_codes')
    os.makedirs(qr_folder, exist_ok=True)

    filename = f"qr_{user_id}_{purchase_key}.png"
    file_path = os.path.join(qr_folder, filename)

    img = qrcode.make(purchase_key)
    img.save(file_path)

    # Normaliser le chemin pour qu'il utilise les barres obliques correctes
    qr_code_path = os.path.normpath(os.path.join('qr_codes', filename))

    return qr_code_path  # Retourne le chemin relatif du fichier



# -----------------------
# ROUTES ADMIN
# -----------------------

# Route d'accueil du blueprint admin
@admin.route('/', methods=['GET'])
@login_required
def index():
    return redirect(url_for('admin.admin_dashboard'))  # Assure-toi que le nom est bien admin.admin_dashboard

# Route du tableau de bord admin
@admin.route('/dashboard')
@login_required
def admin_dashboard():
    print("DASHBOARD ADMIN ACCÉDÉ")
    offers = Offer.query.all()
    return render_template('admin/dashboard.html', user=current_user, offers=offers)

@admin.route('/add-offer', methods=['GET', 'POST'])
@login_required
def add_offer():
    if not current_user.is_admin:
        flash("Accès réservé aux administrateurs.", "danger")
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = float(request.form['price'])
        available = 'available' in request.form

        new_offer = Offer(name=name, description=description, price=price, available=available)
        db.session.add(new_offer)
        db.session.commit()

        flash('Nouvelle offre ajoutée avec succès !', 'success')
        return redirect(url_for('admin.admin_dashboard'))  # CORRECTION: Utilisation du bon endpoint 'admin.admin_dashboard'

    return render_template('admin/add_offer.html', user=current_user)


@admin.route('/admin/edit-offer/<int:offer_id>', methods=['GET', 'POST'])
@login_required
def edit_offer(offer_id):
    offer = Offer.query.get_or_404(offer_id)

    if request.method == 'POST':
        offer.name = request.form['name']
        offer.description = request.form['description']
        offer.price = float(request.form['price'])
        offer.available = 'available' in request.form
        db.session.commit()
        flash("Offre mise à jour avec succès", "success")
        return redirect(url_for('admin.admin_dashboard'))

    return render_template('admin/edit_offer.html', offer=offer, user=current_user)


@admin.route('/admin/delete-offer/<int:offer_id>', methods=['POST'])
@login_required
def delete_offer(offer_id):
    offer = Offer.query.get_or_404(offer_id)
    db.session.delete(offer)
    db.session.commit()
    flash("Offre supprimée avec succès.", "success")
    return redirect(url_for('admin.admin_dashboard'))



   