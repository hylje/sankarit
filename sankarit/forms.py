# -*- coding: utf-8 -*-

from flask_wtf import Form
from wtforms import TextField, PasswordField, validators

class RegistrationForm(Form):
    username = TextField(u'Käyttäjänimi', [
        validators.Length(min=3, max=30),
        validators.Regexp("^[a-zA-Z0-9]+$", message=u"Vain numerot ja kirjaimet a-z hyväksytään")
    ])
    email = TextField(u'Sähköposti', [
        validators.Length(min=6, max=100),
        validators.Email()
    ])
    password1 = PasswordField(u'Salasana', [
        validators.Required(),
        validators.EqualTo('password2', message=u"Vahvista salasana")
    ])
    password2 = PasswordField(u"Vahvista salasana")

class LoginForm(Form):
    username = TextField(u'Käyttäjänimi', [validators.Length(min=3, max=30)])
    password = PasswordField(u'Salasana', [validators.Required()])
