import os

from flask import Flask, render_template

from lib import pg

app = Flask("sankarit")
app.config.update(
    PG_USERNAME=None,
    PG_PASSWORD=None,
    PG_DATABASE="sankarit",
    DEBUG=True
)

if "SANKARIT_SETTINGS_FILE" in os.environ:
    app.config.from_envvar("SANKARIT_SETTINGS_FILE")

@app.route("/")
def main():
    return render_template("main.html")

@app.route("/test")
def test():
    cursor = pg.get_cursor(app)
    cursor.execute("""
SELECT username FROM player;
""")
    player_names = [p for p, in cursor.fetchall()]

    return "Pelaajien nimet: " + ", ".join(player_names)


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

if __name__ == "__main__":
    app.run()
