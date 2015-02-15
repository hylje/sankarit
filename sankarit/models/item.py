# -*- encoding: utf-8 -*-

import random

from flask import g

from sankarit import itemclasses

class Item(object):
    def __init__(self, iid, level, itemclass_id, slot, rarity, player_id, hero_id,
                 adventure_id, player=None, hero=None, adventure=None):
        self.iid = iid
        self.level = level
        self.itemclass_id = itemclass_id
        self.itemclass = itemclasses.get_itemclass(itemclass_id)
        self.slot = slot
        self.rarity = rarity
        self.player_id = player_id
        self.player = player
        self.hero_id = hero_id
        self.hero = hero
        self.adventure_id = adventure_id
        self.adventure = adventure

    @classmethod
    def get(cls, iid, player_id=None):
        c = g.db.cursor()

        query = """
        SELECT id, level, class, slot, rarity, player_id, hero_id, adventure_id
        FROM item
        WHERE id=%(iid)s
        """
        kwargs = {"iid": iid}

        if player_id is not None:
            query += " AND player_id=%(pid)s"
            kwargs["pid"] = player_id

        c.execute(query, kwargs)

        return cls(*c.fetchone())

    @classmethod
    def generate(cls, loot_per_player, all_heroes):
        """Generates new items for the given heroes. Inserts the items into
        the database, but does not commit.
        """

        c = g.db.cursor()

        for player_id, loot_total in loot_per_player.iteritems():
            our_heroes = [h for h in all_heroes if h.player_id == player_id]
            max_items = len(our_heroes) * 2
            max_level = max(h.get_level() for h in our_heroes) + 2
            min_level = max(
                # never less than 1
                1,
                min(
                    # either the lowest level hero minus 3
                    max(
                        1,
                        min(h.get_level() for h in our_heroes)-3),
                    # or the maximum item level minus ten
                    max_level-10))

            # no item drops if loot_total < 100
            retries = loot_total / 100

            item_qualities = []
            for i in range(retries):
                level = random.randrange(min_level, max_level)
                rarity = itemclasses.roll_rarity()
                item_qualities.append((level, rarity))
                # drop the worst item (weighing rarity)
                if len(items) > max_items:
                    item_qualities.sort(
                        key=lambda (l, r): l+(r*2),
                        reverse=True
                    )
                    item_qualities.pop()

            for level, rarity in item_qualities:
                itemclass = random.choice(itemclasses.CLASSES)
                items.append((level, itemclass.id, itemclass.slot,
                              rarity, player_id, self.aid))

        if items:
            c.execute("""
            INSERT INTO item (level, class, slot, rarity, player_id,
                              adventure_id)
            VALUES """
            + ", ".join("(%s, %s, %s, %s, %s, %s)" for i in items)
            + """
            RETURNING id, level, class, slot, rarity, player_id,
            hero_id, adventure_id
            """, list(itertools.chain(*items)))

            itemobjs = [cls(*row, adventure=self) for row in c.fetchall()]
        else:
            itemobjs = []

        return itemobjs

    def equip(self, hero):
        if hero.player_id != self.player_id:
            raise ValueError("can't equip on stranger heroes")

        self.hero = hero
        self.hero_id = hero.hid

        c = g.db.cursor()

        # null the item that occupied our slot (if any)
        c.execute("UPDATE item SET hero_id=null WHERE hero_id=%(hid)s AND slot=%(slot)s", {"hid": hero.hid, "slot": self.slot})

        # take its place

        print 1111, self.iid
        c.execute("UPDATE item SET hero_id=%(hid)s WHERE id=%(iid)s",
                  {"hid": hero.hid, "iid": self.iid})

        g.db.commit()

    def get_stats_display(self):
        base_stats = self.get_stats()

        stats = [
            (u"Voima", base_stats["str"]),
            (u"Ketteryys", base_stats["agi"]),
            (u"Älykkyys", base_stats["int"]),
            (u"Kestävyys", base_stats["con"])
        ]

        return [(k,v) for k,v in stats if v>0]

    def get_stats(self):
        return {
            "str": self.itemclass.get_str(self.level, self.rarity),
            "agi": self.itemclass.get_agi(self.level, self.rarity),
            "int": self.itemclass.get_int(self.level, self.rarity),
            "con": self.itemclass.get_con(self.level, self.rarity)
        }


    def get_rarity_display(self):
        for i, text in itemclasses.RARITY_CHOICES:
            if i == self.rarity:
                return text
        return u"Tuntematon"
