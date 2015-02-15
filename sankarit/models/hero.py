# -*- encoding: utf-8 -*-

import datetime

from flask import g

from sankarit import heroclasses, itemclasses

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

    @classmethod
    def get(cls, hid, player_id=None):
        c = g.db.cursor()

        query = """
        SELECT id, name, class, xp, player_id
        FROM hero
        WHERE id=%(hid)s
        """
        kwargs = {"hid": hid}

        if player_id is not None:
            query += " AND player_id=%(pid)s"
            kwargs["pid"] = player_id

        c.execute(query, kwargs)

        return cls(*c.fetchone())

    def get_class_name(self):
        return self.heroclass.name

    def get_level(self):
        return self.heroclass.level(self.xp)

    def get_item_level(self):
        if self.equipment:
            return sum(e.level for e in self.equipment) / float(len(itemclasses.SLOTS))
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

    def get_stats_display(self):
        base_stats = self.heroclass.base_stats(self.xp)
        stats = self.get_stats()

        return (
            (u"Voima", base_stats["str"], stats["str"]),
            (u"Ketteryys", base_stats["agi"], stats["agi"]),
            (u"Älykkyys", base_stats["int"], stats["int"]),
            (u"Kestävyys", base_stats["con"], stats["con"])
        )

    def get_stats(self):
        stats = self.heroclass.base_stats(self.xp)

        for item in self.get_equipment():
            for k, v in item.get_stats().iteritems():
                stats[k] += v

        return stats

    # XXX implement final offense/defense stats based on class, items and level

    def offense(self):
        return self.heroclass.get_offense(self.get_stats())

    def defense(self):
        return self.heroclass.get_defense(self.get_stats())

    def defense_factor(self):
        return self.heroclass.get_defense_factor(self.get_stats())

    def get_secondary_stats_display(self):
        stats = (
            (u"Hyökkäys", self.offense()),
            (u"Puolustus", self.defense()),
        )

        if self.defense_factor() != 1:
            stats += (u"Puolustuskerroin", self.defense_factor())

        return stats

    STATUS = IDLE, RECOVERING, ADVENTURE = range(3)
    STATUS_CHOICES = (
        (IDLE, u"Vapaalla"),
        (RECOVERING, u"Palautumassa seikkailusta"),
        (ADVENTURE, u"Seikkailemassa")
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
