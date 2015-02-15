import hashlib
import os
import binascii

from flask import g

PBKDF2_ROUNDS = 100000
PBKDF2_ALGO = "sha256"

def make_password(password):
    salt = binascii.hexlify(os.urandom(16))

    return "$".join((
        PBKDF2_ALGO,
        str(PBKDF2_ROUNDS),
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
    def register(cls, username, email, password):
        row = {
            "username": username,
            "password": make_password(password),
            "email": email
        }
        c = g.db.cursor()

        c.execute("""
        INSERT INTO player (username, password, email, gold)
        VALUES (%(username)s, %(password)s, %(email)s, 0)""", row)

        g.db.commit()

        c.execute("""
        SELECT id FROM player WHERE username=%(username)s
        """, {"username": username})

        uid, = c.fetchone()

        return cls(uid, username, email, 0)

    @classmethod
    def login(cls, username, password):
        c = g.db.cursor()

        c.execute("""
        SELECT id, email, password, gold FROM player WHERE username=%(username)s
        """, {"username": username})

        uid, email, password_pack, gold = c.fetchone()

        if not check_password(password_pack, password):
            return None

        if pack_needs_upgrading(password_pack):
            new_pack = make_password(password)

            c.execute("""
            UPDATE player
            SET password=%(password)s
            WHERE username=%(username)s
            """, {"password": new_pack, "username": username})

            g.db.commit()

        return cls(uid, username, email, gold)

    @classmethod
    def get(cls, uid):
        c = g.db.cursor()
        c.execute("""
        SELECT id, username, email, gold
        FROM player
        WHERE id=%(uid)s
        """, {"uid": uid})

        return cls(*c.fetchone())

    def __init__(self, uid, username, email, gold):
        self.uid = uid
        self.username = username
        self.email = email
        self.gold = gold

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

    def get_item_count(self):
        c = g.db.cursor()

        c.execute("SELECT count(id) FROM item WHERE player_id=%(player_id)s",
                  {"player_id": self.uid})

        count, = c.fetchone()

        return count

    def get_items(self, offset=None):
        from sankarit.models.item import Item
        from sankarit.models.hero import Hero

        c = g.db.cursor()

        if offset is None:
            offset = 0

        c.execute("""
        SELECT i.id, i.level, i.class, i.slot, i.rarity,
               i.player_id, i.hero_id, i.adventure_id,
               h.id, h.name, h.class, h.xp, h.player_id
        FROM item i
        LEFT OUTER JOIN hero h ON i.hero_id=h.id
        WHERE i.player_id=%(player_id)s
        ORDER BY i.rarity DESC, i.level DESC
        LIMIT 100 OFFSET %(offset)s
        """, {"player_id": self.uid, "offset": offset})

        ret = []

        for row in c.fetchall():
            item = row[:8]
            hero = row[8:]
            if hero[0] is not None:
                hero = Hero(*hero)
            else:
                hero = None
            ret.append(Item(*item, player=self, hero=hero))

        return ret

    def get_adventures(self):
        from sankarit.models.adventure import Adventure

        c = g.db.cursor()
        c.execute("""
        SELECT DISTINCT ON (a.id) a.id, a.start_time, a.end_time, a.class, a.gold
        FROM adventure a, adventure_hero ah, hero h
        WHERE h.player_id=%(player_id)s
          AND ah.hero_id=h.id
          AND ah.adventure_id=a.id
          AND a.gold=0
        """, {"player_id": self.uid})

        ret = []
        for adventure in c.fetchall():
            ret.append(Adventure(*adventure))

        return ret

    def deduct_gold(self, amount):
        c = g.db.cursor()
        c.execute("UPDATE player SET gold=gold-%(cost)s WHERE id=%(uid)s",
                  {"cost": amount, "uid": self.uid})
        g.db.commit()
