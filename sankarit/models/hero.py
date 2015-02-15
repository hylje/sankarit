import datetime

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

    def get_equipment(self):
        # XXX move to Item
        from sankarit.models.item import Item

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

    # XXX implement final offense/defense stats based on class, items and level

    def offense(self):
        return 1

    def defense(self):
        return 1

    def defense_factor(self):
        return 1

    STATUS = IDLE, RECOVERING, ADVENTURE = range(3)
    STATUS_CHOICES = (
        (IDLE, "Vapaalla"),
        (RECOVERING, "Palautuu seikkailusta"),
        (ADVENTURE, "Seikkailee")
    )

    def status(self):
        """Check if this hero is or has recently been on an adventure
        """
        from sankarit.models.adventure import Adventure

        # XXX do this in adventure model
        c = g.db.cursor()
        c.execute("""
        SELECT a.id, a.start_time, a.end_time, a.class, a.gold
        FROM adventure a, adventure_hero ah
        WHERE ah.hero_id=%(hid)s
          AND ah.adventure_id=a.id
          AND a.end_time + (a.end_time - a.start_time)*2 > now()
        ORDER BY a.end_time
        """,
                  {"hid": self.hid})

        adventures = [Adventure(*row) for row in c.fetchall()]

        # since a hero shouldn't be able to go on an adventure while
        # recovering, we should have 1 or 0 rows here. but race
        # conditions are possible.
        for adventure in adventures:
            if adventure.end_time > datetime.datetime.now():
                return self.ADVENTURE
            else:
                return self.RECOVERING
        else:
            return self.IDLE

    def status_text(self):
        status = self.status()
        for i, text in self.STATUS_CHOICES:
            if i == status:
                return text
        return "Tuntematon"

    def available(self):
        return self.status() == self.IDLE
