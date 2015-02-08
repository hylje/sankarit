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

class Cleric(HeroClass):
    id = 3
    name = "Parantaja"
    int_rate = 1.2
    description = u"""
Parantaja ei kestä rasitusta paljoa eikä tee paljoa vahinkoa, mutta vähentää
jatkuvasti koko joukkueensa rasitusta.
"""

class Mage(HeroClass):
    id = 4
    int_rate = 1.5
    int_base = 15
    name = "Noita"
    description = u"""
Noita tekee paljon vahinkoa mutta tarvitsee suojelua pysyäkseen
toimintakuntoisena. Taikuus aiheuttaa rasitusta, vaikka suojelu pelaisi.
"""

CLASSES = [Warrior(), Archer(), Cleric(), Mage()]
def get_heroclass(cid):
    for heroclass in CLASSES:
        if heroclass.id == cid:
            return heroclass
    raise IndexError()
