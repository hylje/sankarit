# -*- encoding: utf-8 -*-

class HeroClass(object):
    str_rate = 1
    str_base = 10
    int_rate = 1
    int_base = 10
    agi_rate = 1
    agi_base = 10
    con_rate = 1
    con_base = 10

    name = "Tuntematon"
    description = "Tekee kaikkea huonosti"

    def level(self, xp):
        return 1 + xp / 1000

    def base_stats(self, xp):
        level = self.level(xp)
        return {
            "str": self.str_base + level*self.str_rate,
            "agi": self.agi_base + level*self.agi_rate,
            "int": self.int_base + level*self.int_rate,
            "con": self.con_base + level*self.con_rate
        }

    def get_defense_factor(self, stats):
        return 1

class Warrior(HeroClass):
    id = 1
    str_rate = 1.5
    str_base = 15
    con_rate = 1.5
    con_base = 20
    name = u"Taistelija"
    description = u"""
Lähitaisteluun erikoistunut taistelija pitää joukkuettaan
turvassa, vähentäen sen kärsimää rasitusta.
"""

    def get_offense(self, stats):
        return stats["str"]*2 + stats["agi"]

    def get_defense(self, stats):
        return stats["con"]*2 + stats["agi"] + stats["int"]

class Archer(HeroClass):
    id = 2
    name = u"Jousimies"
    agi_rate = 1.5
    agi_base = 15
    con_rate = 1.3
    con_base = 13
    description = u"""
Kaukotaisteluun erikoistunut taistelija turvaa joukkuettaan vähemmän
ja tekee enemmän vahinkoa.
"""

    def get_offense(self, stats):
        return 2 * (stats["agi"] + stats["str"])

    def get_defense(self, stats):
        return stats["con"] + stats["agi"] + stats["int"]

class Cleric(HeroClass):
    id = 3
    name = "Parantaja"
    int_rate = 1.2
    description = u"""
Parantaja ei kestä rasitusta paljoa eikä tee paljoa vahinkoa, mutta vähentää
koko joukkueensa rasitusta kertoimella.
"""

    def get_offense(self, stats):
        return stats["int"]

    def get_defense(self, stats):
        return stats["con"] + stats["agi"]

    def get_defense_factor(self, stats):
        return math.log(stats["int"], 10)

class Mage(HeroClass):
    id = 4
    int_rate = 1.5
    int_base = 15
    name = "Noita"
    description = u"""
Noita tekee paljon vahinkoa mutta tarvitsee suojelua pysyäkseen
toimintakuntoisena. Taikuus aiheuttaa rasitusta, vaikka suojelu pelaisi.
"""

    def get_offense(self, stats):
        return stats["int"]*4

    def get_defense(self, stats):
        return stats["con"] + stats["agi"] + stats["str"]

CLASSES = [Warrior(), Archer(), Cleric(), Mage()]
def get_heroclass(cid):
    for heroclass in CLASSES:
        if heroclass.id == cid:
            return heroclass
    raise IndexError()
