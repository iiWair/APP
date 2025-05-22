# app/routes.py

from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, jsonify
from flask_login import login_user, login_required, current_user, logout_user
from app.forms import RegistrationForm, LoginForm
from app import db, bcrypt
from app.models import User, Ticket, Offer, CartItem
import secrets
import qrcode
import os
import re
import uuid
import stripe

main = Blueprint('main', __name__)
admin = Blueprint('admin', __name__)

# -----------------------
# ROUTES UTILISATEUR
# -----------------------

def email_valide(email):
    regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(regex, email) is not None

def mot_de_passe_valide(mot_de_passe):
    majuscule = any(c.isupper() for c in mot_de_passe)
    special = any(c in "!@#$%^&*()-_=+[]{}|;:'\",.<>?/`~" for c in mot_de_passe)
    return majuscule and special


@main.route('/')
def home():
    return render_template('index.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        print("✅ Formulaire validé")

        # Vérification email personnalisé
        if not email_valide(form.email.data):
            flash('Format email incorrect.', 'danger')
            return redirect(url_for('main.register'))

        # Vérification de l'unicité de l'email
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Cette adresse email est déjà utilisée.', 'danger')
            return redirect(url_for('main.register'))

        try:
            hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            secret_key = secrets.token_hex(32)

            user = User(
                username=form.username.data,
                email=form.email.data,
                password=hashed_pw,
                secret_key=secret_key
            )

            db.session.add(user)
            db.session.commit()

            flash('Compte créé avec succès ! Vous pouvez maintenant vous connecter.', 'success')
            return redirect(url_for('main.login'))

        except Exception as e:
            print("❌ Erreur lors de la création de l'utilisateur :", e)
            db.session.rollback()
            flash("Une erreur est survenue lors de l'inscription.", 'danger')

    elif request.method == 'POST':
        print("❌ Formulaire invalide :", form.errors)
        flash("Veuillez corriger les erreurs du formulaire.", "danger")

    return render_template('register.html', form=form)




@main.route('/profil')
@login_required
def profil():
    return render_template('profil.html', user=current_user)

@main.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        new_email = request.form['email']
        current_user.email = new_email

        # Changement de mot de passe (optionnel)
        if request.form['password']:
            hashed_password = bcrypt.generate_password_hash(request.form['password'])
            current_user.password = hashed_password

        db.session.commit()
        flash("Profil mis à jour avec succès.", "success")
        return redirect(url_for('main.profil'))

    return render_template('edit_profile.html', user=current_user)



@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        print("🔁 Utilisateur déjà connecté, redirection vers le dashboard")
        return redirect(url_for('main.dashboard'))  # Redirige s'il est déjà connecté

    form = LoginForm()
    
    if form.validate_on_submit():
        print("✅ Formulaire validé")
        user = User.query.filter_by(email=form.email.data).first()
        
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user)
            flash('Connexion réussie !', 'success')

            next_page = request.args.get('next')
            if next_page:
                print(f"➡️ Redirection vers la page d’origine : {next_page}")
                return redirect(next_page)

            if user.is_admin:
                print("➡️ Redirection vers le dashboard admin")
                return redirect(url_for('admin.admin_dashboard'))
            else:
                print("➡️ Redirection vers le dashboard utilisateur")
                return redirect(url_for('main.dashboard'))
        else:
            flash('Identifiants invalides. Réessayez.', 'danger')
            print("❌ Identifiants invalides")
    else:
        if request.method == 'POST':
            print("❌ Formulaire non valide :", form.errors)

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

@main.route('/add_to_cart_ajax', methods=['POST'])
@login_required
def add_to_cart_ajax():
    data = request.get_json()
    offer_id = data.get('offer_id')

    if not offer_id:
        return jsonify({'success': False, 'message': 'ID de l’offre manquant.'}), 400

    existing_item = CartItem.query.filter_by(user_id=current_user.id, offer_id=offer_id).first()
    if existing_item:
        return jsonify({'success': False, 'message': 'Offre déjà dans le panier.'}), 409

    new_item = CartItem(user_id=current_user.id, offer_id=offer_id)
    db.session.add(new_item)
    db.session.commit()

    return jsonify({'success': True, 'message': 'Offre ajoutée au panier.'})


@main.route('/remove-from-cart-ajax', methods=['POST'])
@login_required
def remove_from_cart_ajax():
    data = request.get_json()
    offer_id = data.get('offer_id')
    if not offer_id:
        return jsonify({"success": False, "message": "ID d'offre manquant."}), 400

    cart_item = CartItem.query.filter_by(user_id=current_user.id, offer_id=offer_id).first()
    if cart_item:
        db.session.delete(cart_item)
        db.session.commit()
        return jsonify({"success": True, "message": "Offre retirée du panier."})
    else:
        return jsonify({"success": False, "message": "Offre introuvable dans le panier."}), 404


@main.route('/checkout', methods=['POST'])
@login_required
def checkout():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()

    if not cart_items:
        flash("Votre panier est vide.")
        return redirect(url_for('main.cart'))

    stripe.api_key = current_app.config['STRIPE_SECRET_KEY']

    line_items = []
    for item in cart_items:
        line_items.append({
            'price_data': {
                'currency': 'eur',
                'unit_amount': int(item.offer.price * 100),  # Converti € -> centimes
                'product_data': {
                    'name': item.offer.name,
                    'description': item.offer.description,
                },
            },
            'quantity': 1,
        })

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=url_for('main.payment_success', _external=True),
            cancel_url=url_for('main.cart', _external=True),
        )
        return redirect(session.url, code=303)
    except Exception as e:
        return str(e)

@main.route('/success')
def success():
    return "<h2>Paiement réussi ! Merci pour votre achat 🎉</h2>"

@main.route('/cancel')
def cancel():
    return "<h2>Paiement annulé. Vous pouvez réessayer.</h2>"


@main.route('/payment_success')
@login_required
def payment_success():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()

    if not cart_items:
        flash("Aucun article trouvé pour la validation du paiement.")
        return redirect(url_for('main.cart'))

    for item in cart_items:
        purchase_key = str(uuid.uuid4())
        base_dir = os.path.dirname(os.path.abspath(__file__))
        qr_code_folder = os.path.join(base_dir, "static", "qrcodes")
        os.makedirs(qr_code_folder, exist_ok=True)

        qr_filename = f"{purchase_key}.png"
        qr_path = os.path.join(qr_code_folder, qr_filename)

        qr = qrcode.make(f"Billet: {item.offer.name} | Clé: {purchase_key}")
        qr.save(qr_path)

        ticket = Ticket(
            purchase_key=purchase_key,
            qr_code_path=os.path.join("qrcodes", qr_filename),
            user_id=current_user.id,
            offer_id=item.offer.id
        )
        db.session.add(ticket)

    CartItem.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()

    flash("Paiement réussi ! Vos billets sont disponibles.", "success")
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

    # Supprimer d'abord les CartItem liés à cette offre
    CartItem.query.filter_by(offer_id=offer_id).delete()

    # Puis supprimer l'offre
    db.session.delete(offer)
    db.session.commit()
    
    flash("Offre supprimée avec succès.", "success")
    return redirect(url_for('admin.admin_dashboard'))



   