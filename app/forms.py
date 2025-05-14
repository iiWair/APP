from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from wtforms import ValidationError
import re


class RegistrationForm(FlaskForm):
    username = StringField('Nom d’utilisateur', validators=[DataRequired(), Length(min=3, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email(message="Format de l'email incorrect")])
    password = PasswordField('Mot de passe', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirmez le mot de passe', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Créer un compte')

    def validate_password(self, field):
        password = field.data

        # Majuscule
        if not any(c.isupper() for c in password):
            raise ValidationError("Le mot de passe doit contenir au moins une lettre majuscule.")

        # Caractère spécial
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise ValidationError("Le mot de passe doit contenir au moins un caractère spécial.")


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    submit = SubmitField('Se connecter')
    
