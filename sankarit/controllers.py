# -*- encoding: utf-8 -*-

from flask import render_template, session, request, redirect, flash

from sankarit import app
from sankarit import forms
from sankarit.models.player import Player
from sankarit.utils import login_required

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
    return render_template("game.html")

@app.route("/adventure")
@login_required
def adventure():
    return render_template("adventure.html")

@app.route("/inventory")
@login_required
def inventory():
    return render_template("inventory.html")

@app.route("/hero")
@login_required
def hero():
    return render_template("hero.html")

@app.route("/equip")
@login_required
def equip():
    return render_template("equip.html")
