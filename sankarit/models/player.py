import hashlib
import os
import binascii

from flask import g

PBKDF2_ROUNDS = 100000
PBKDF2_ALGO = "sha256"

def make_password(password):
    salt = os.urandom(16)

    return "$".join((
        PBKDF2_ALGO,
        PBKDF2_ROUNDS,
        salt,
        binascii.hexlify(
            hashlib.pbkdf2_hmac(PBKDF2_ALGO, password, salt, PBKDF2_ROUNDS)
        )
    ))

def check_password(pack, password):
    algo, rounds, salt, old_hash = pack.split("$")

    new_hash = binascii.hexlify(
        hashlib.pbkdf2_hmac(algo, password, salt, int(rounds))
    )

    if new_hash == old_hash:
        return True

    return False

def pack_needs_upgrading(pack):
    algo, rounds, _, _ = pack.split("$")
    if algo != PBKDF2_ALGO or int(rounds) != PBKDF2_ROUNDS:
        return True
    return False

class Player(object):
    @classmethod
    def register(cls, username, password):
        row = {
            "username": username,
            "password": make_password(password)
        }
        c = g.db.cursor()

        c.execute("""
        INSERT INTO player (username, password)
        VALUES (%(username)s, %(password)s)""", row)

        c.commit()

        c.execute("""
        SELECT id FROM player WHERE username=%(username)s
        """, {"username": username})

        uid, = c.fetchone()

        return cls(uid, username)

    @classmethod
    def login(cls, username, password):
        c = g.db.cursor()

        c.execute("""
        SELECT id, password FROM player WHERE username=%(username)s
        """, {"username": username})

        uid, password_pack = c.fetchone()

        if not check_password(password_pack, password):
            return None

        if pack_needs_upgrading(password_pack):
            new_pack = make_password(password)

            c.execute("""
            UPDATE player
            SET password=%(password)s
            WHERE username=%(username)s
            """, {"password": new_pack, "username": username})

            c.commit()

        return cls(uid, username)

    def __init__(self, uid, username):
        self.uid = uid
        self.username = username

    def get_heroes(self):
        from sankarit.models.hero import Hero

        c = g.db.cursor()

        c.execute("""
        SELECT id, name, class, xp, player_id
        FROM hero
        WHERE player_id=%(player_id)s
        """, {"player_id": self.uid})

        ret = []

        for row in c.fetchall():
            ret.append(Hero(*row, player=self))

        return ret

    def get_items(self):
        from sankarit.models.item import Item

        c = g.db.cursor()

        c.execute("""
        SELECT id, level, class, slot, rarity, player_id, hero_id, adventure_id
        FROM item
        WHERE player_id=%(player_id)s
        """, {"player_id": self.uid})

        ret = []

        for row in c.fetchall():
            ret.append(Item(*row, player=self))

        return ret
