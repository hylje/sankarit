# -*- encoding: utf-8 -*-

import itertools
import random
import datetime
from collections import defaultdict

from flask import g

from sankarit import itemclasses, adventureclasses
from sankarit.models.item import Item

class Adventure(object):
    @classmethod
    def create(cls, adventureclass, heroes):
        c = g.db.cursor()

        start_time = datetime.datetime.now()
        end_time = start_time + adventureclass.timedelta

        c.execute("""
        INSERT INTO adventure (start_time, end_time, class, gold)
        VALUES (%(start_time)s, %(end_time)s, %(class)s, %(gold)s)
        RETURNING id
        """, {
            "start_time": start_time,
            "end_time": end_time,
            "class": adventureclass.id,
            "gold": 0
        })

        aid, = c.fetchone()

        # Create relation to all heroes

        values = list(itertools.chain(*((hero.hid, aid) for hero in heroes)))
        query = """
        INSERT INTO adventure_hero (hero_id, adventure_id)
        VALUES """ + ", ".join("(%s, %s)" for hero in heroes)

        c.execute(query, values)

        g.db.commit()

        return cls(aid, start_time, end_time, adventureclass.id, 0, heroes=heroes, adventureclass=adventureclass)

    def __init__(self, aid, start_time, end_time, adventureclass_id,
                 gold, heroes=None, adventureclass=None):
        self.aid = aid
        self.start_time = start_time
        self.end_time = end_time
        self.adventureclass_id = adventureclass_id
        self.adventureclass = adventureclass or adventureclasses.get_adventureclass(adventureclass_id)
        self.gold = gold

        self.heroes = heroes or self.get_heroes()

    def get_heroes(self):
        from sankarit.models.hero import Hero

        c = g.db.cursor()

        c.execute("""
        SELECT h.id as id, h.name as name, h.class as class, h.xp as xp, h.player_id as player_id
        FROM hero h, adventure_hero ah
        WHERE ah.adventure_id=%(aid)s AND h.id=ah.hero_id
        """, {"aid": self.aid})

        ret = []
        for hero in c.fetchall():
            ret.append(Hero(*hero))
        return ret

    def can_be_claimed(self):
        if self.end_time < datetime.datetime.now() and self.gold == 0:
            return True
        else:
            return False

    def resolve_reward(self):
        # XXX maybe split this into more functions
        c = g.db.cursor()

        offense = (sum(hero.offense() for hero in self.heroes)
                   * random.random() * 4
                   * (self.adventureclass.timedelta.total_seconds() / 2400))
        defense = (sum(hero.defense() for hero in self.heroes)
                   * sum(hero.defense_factor() for hero in self.heroes)
                   * random.random() * 3
                   * (self.adventureclass.timedelta.total_seconds() / 2400))

        success_rating = min(offense, defense*3/2) * 5

        loot_ratio = random.random()
        gold_ratio = 1 - loot_ratio

        loot_rating = int(success_rating * loot_ratio)
        gold_rating = int(success_rating * gold_ratio)
        xp_rating = int(success_rating * 0.5)

        c.execute("""
        UPDATE adventure SET gold=%(gold)s WHERE id=%(aid)s
        """, {"gold": gold_rating, "aid": self.aid})

        level_total = sum(hero.get_level() for hero in self.heroes)
        gold_per_player = defaultdict(int)
        loot_per_player = defaultdict(int)

        for hero in self.heroes:
            contrib_ratio = hero.get_level() / level_total

            gained_loot = contrib_ratio * loot_rating
            gained_gold = contrib_ratio * gold_rating
            gained_xp = contrib_ratio * xp_rating

            c.execute("""
            UPDATE hero SET xp=xp+%(gained_xp)s WHERE id=%(hero_id)s
            """, {"gained_xp": gained_xp, "hero_id": hero.hid})

            gold_per_player[hero.player_id] += gained_gold
            loot_per_player[hero.player_id] += gained_loot

        for player_id, gold_total in gold_per_player.iteritems():
            c.execute("""
            UPDATE player SET gold=gold+%(gold_total)s WHERE id=%(player_id)s
            """, {"gold_total": gold_total, "player_id": player_id})

        itemobjs = Item.generate(loot_per_player, self.heroes)

        # commit the entire thing
        g.db.commit()

        return gold_per_player, itemobjs

    def started_ago(self):
        now = datetime.datetime.now()

        if self.start_time > now:
            return "Tulossa"

        td = now - self.start_time

        bits = [
            (td.days, u"päivää"),
            (td.seconds / 3600, u"tuntia"),
            ((td.seconds / 60) % 60, u"minuuttia"),
            (td.seconds % 60, u"sekuntia")
        ]

        valid_bits = [(time, text) for time, text in bits if time > 0]

        if valid_bits:
            valid_bits = valid_bits[:2]
            return u", ".join(u"%s %s" % b for b in valid_bits) + u" sitten"
        else:
            return u"Juuri nyt"


    def progress(self):
        now = datetime.datetime.now()

        if self.end_time < now:
            return 1
        if self.start_time > now:
            return 0

        factor = (self.end_time - now).total_seconds() / float((self.end_time - self.start_time).total_seconds())
        complement = 1 - factor
        percent = 100 * complement

        return "%.04f" % percent
