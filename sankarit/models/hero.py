from flask import g

from sankarit import heroclasses

class Hero(object):
    def __init__(self, hid, name, heroclass_id, xp, player_id, player=None):
        self.hid = hid
        self.name = name
        self.heroclass_id = heroclass_id
        self.heroclass = heroclasses.get_heroclass(heroclass_id)

        self.xp = xp
        if player:
            self.player = player
        else:
            from sankarit.models.player import Player
            self.player = Player.get(player_id)
        self.player_id = player_id

        self.equipment = self.get_equipment()

    @classmethod
    def create(cls, name, heroclass, player_id):
        c = g.db.cursor()

        c.execute("""
        INSERT INTO hero (name, class, xp, player_id)
        VALUES (%(name)s, %(heroclass)s, %(xp)s, %(player_id)s)
        """, {
            "name": name,
            "heroclass": heroclass,
            "player_id": player_id,
            "xp": 0
        })

        g.db.commit()

        c.execute("""
        SELECT id, name, class, xp, player_id
        FROM hero
        WHERE name=%(heroname)s AND player_id=%(player_id)s
        """, {
            "heroname": name,
            "player_id": player_id
        })

        return cls(*c.fetchone())

    def get_class_name(self):
        return self.heroclass.name

    def get_level(self):
        return self.heroclass.level(self.xp)

    def get_item_level(self):
        if self.equipment:
            return sum(e.level for e in self.equipment) / len(self.equipment)
        return 0

    def get_status_text(self):
        # XXX get status based from last adventure;
        # 0.5*adventure_length if it was successful,
        # 1.5*adventure_length if not
        return u"Kunnossa"

    def get_equipment(self):
        c = g.db.cursor()

        c.execute("""
        SELECT id, level, class, slot, rarity, player_id,
        hero_id, adventure_id
        FROM item
        WHERE hero_id=%(hero_id)s
        """, {"hero_id": self.hid})

        ret = []
        for item in c.fetchall():
            ret.append(Item(*item, player=self.player, hero=self))

        return ret
