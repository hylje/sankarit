from flask import render_template

from sankarit import app

@app.route("/")
def main():
    return render_template("main.html")

@app.route("/game")
def game():
    return render_template("game.html")

@app.route("/adventure")
def adventure():
    return render_template("adventure.html")

@app.route("/inventory")
def inventory():
    return render_template("inventory.html")

@app.route("/hero")
def hero():
    return render_template("hero.html")

@app.route("/equip")
def equip():
    return render_template("equip.html")
