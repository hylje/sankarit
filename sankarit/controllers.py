# -*- encoding: utf-8 -*-

from flask import render_template, session, request, redirect, flash, g

from sankarit import app
from sankarit import forms
from sankarit.models.player import Player
from sankarit.models.hero import Hero
from sankarit.models.adventure import Adventure
from sankarit.utils import login_required
from sankarit import heroclasses, adventureclasses

@app.route("/login", methods=["GET", "POST"])
def login():
    form = forms.LoginForm(request.form)

    if request.method == "POST" and form.validate():
        player = Player.login(form.username.data, form.password.data)
        if player:
            session["playerid"] = player.uid
            return redirect("game")
        flash(u"Käyttäjänimi tai salasana ei kelpaa.", "error")

    return render_template("login.html", form=form)

@app.route("/register", methods=["GET", "POST"])
def register():
    form = forms.RegistrationForm(request.form)

    if request.method == "POST" and form.validate():
        player = Player.register(form.username.data, form.email.data, form.password1.data)
        session["playerid"] = player.uid
        flash(u"Rekisteröinti onnistui.")
        return redirect("game")

    return render_template("register.html", form=form)

@app.route("/logout", methods=["GET", "POST"])
def logout():
    if request.method == "POST":
        del session["playerid"]
        return redirect(".")

    return render_template("logout.html")

@app.route("/")
def main():
    if session.get("playerid"):
        return redirect("game")
    return render_template("main.html", login_form=forms.LoginForm(), reg_form=forms.RegistrationForm())

@app.route("/game")
@login_required
def game():
    player = Player.get(session["playerid"])

    heroes = player.get_heroes()
    adventures = player.get_adventures()

    return render_template("game.html",
                           heroes=heroes,
                           player=player,
                           adventures=adventures)

@app.route("/adventure", methods=["GET", "POST"])
@login_required
def adventure():
    form = forms.NewAdventureForm(request.form)

    player = Player.get(session["playerid"])
    heroes = player.get_heroes()
    form.heroes.choices = [(h.hid, h.name) for h in heroes]

    if request.method == "POST" and form.validate():
        selected_heroes = []
        for heroid in form.heroes.data:
            for hero in heroes:
                if hero.hid == heroid:
                    selected_heroes.append(hero)
        adventureclass = adventureclasses.get_adventureclass(
            form.adventureclass.data
        )

        player.deduct_gold(adventureclass.cost)

        Adventure.create(adventureclass, selected_heroes)
        flash(u"Seikkailu aloitettu!")
        return redirect("game")

    return render_template("adventure.html", form=form)

@app.route("/inventory")
@login_required
def inventory():
    return render_template("inventory.html")

@app.route("/hero", methods=["GET", "POST"])
@login_required
def hero():
    form = forms.HeroCreateForm(request.form)

    if request.method == "POST" and form.validate():
        Hero.create(form.name.data, form.heroclass.data, session["playerid"])
        return redirect("game")

    return render_template("hero.html", form=form, classes=heroclasses.CLASSES)

@app.route("/equip")
@login_required
def equip():
    return render_template("equip.html")
