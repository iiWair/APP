from app import create_app, bcrypt

app = create_app()
with app.app_context():
    pw_hash = bcrypt.generate_password_hash('admin').decode('utf-8')
    print(pw_hash)
