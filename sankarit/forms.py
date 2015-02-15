# -*- coding: utf-8 -*-

from flask import g, session
from flask_wtf import Form
from wtforms import fields, validators, ValidationError

from sankarit import heroclasses, adventureclasses

class RegistrationForm(Form):
    username = fields.TextField(u'Käyttäjänimi', [
        validators.Length(min=3, max=30),
        validators.Regexp("^[a-zA-Z0-9]+$", message=u"Vain numerot ja kirjaimet a-z hyväksytään")
    ])
    email = fields.TextField(u'Sähköposti', [
        validators.Length(min=6, max=100),
        validators.Email()
    ])
    password1 = fields.PasswordField(u'Salasana', [
        validators.Required(),
        validators.EqualTo('password2', message=u"Vahvista salasana")
    ])
    password2 = fields.PasswordField(u"Vahvista salasana")

    def validate_username(self, field):
        c = g.db.cursor()

        row_count = c.execute("""
        SELECT id FROM player WHERE username=%(username)s
        """, {"username": field.data})

        if row_count:
            raise ValidationError(u"Käyttäjätunnus on jo käytössä. Valitse toinen käyttäjätunnus.")

class LoginForm(Form):
    username = fields.TextField(u'Käyttäjänimi', [validators.Length(min=3, max=30)])
    password = fields.PasswordField(u'Salasana', [validators.Required()])

class HeroCreateForm(Form):
    name = fields.TextField(u"Sankarin nimi", [validators.Length(min=3, max=30)])
    heroclass = fields.SelectField(
        "Sankarin luokka",
        [validators.Required()],
        coerce=int,
        choices=[(c.id, c.name) for c in heroclasses.CLASSES]
    )

    def validate_name(self, field):
        c = g.db.cursor()

        row_count = c.execute("""
        SELECT id FROM hero WHERE name=%(name)s AND player_id=%(player_id)s
        """, {
            "name": field.data,
            "player_id": session["playerid"]
        })

        if row_count:
            raise ValidationError(u"Sankareillasi pitää olla eri nimet.")

class NewAdventureForm(Form):
    adventureclass = fields.SelectField(
        u"Seikkailun pituus",
        [validators.Required()],
        coerce=int,
        choices=[(a.id, a.name) for a in adventureclasses.CLASSES]
    )
    heroes = fields.SelectMultipleField(
        u"Sankarit",
        [validators.Required()],
        coerce=int
    )

    def validate_adventureclass(self, field):
        from sankarit.models.player import Player
        aclass = adventureclasses.get_adventureclass(field.data)
        player = Player.get(session["playerid"])
        if aclass.cost > player.gold:
            raise ValidationError(u"Sinulla ei ole varaa näin pitkään seikkailuun.")

class EquipHeroForm(Form):
    hero = fields.SelectField(
        u"Varusta sankari",
        [validators.Required()],
        coerce=int
    )
