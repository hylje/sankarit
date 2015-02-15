# -*- encoding: utf-8 -*-

import datetime

class BaseAdventure(object):
    pass

class ShortAdventure(BaseAdventure):
    id = 1
    timedelta = datetime.timedelta(hours=2)
    cost = 0
    name = u"Lyhyt seikkailu (Hinta: 0)"

class MediumAdventure(BaseAdventure):
    id = 2
    timedelta = datetime.timedelta(hours=8)
    cost = 500
    name = u"Keskipitkä seikkailu (Hinta: 500)"

class EpicAdventure(BaseAdventure):
    id = 3
    timedelta = datetime.timedelta(hours=48)
    cost = 10000
    name = u"Eeppinen seikkailu (Hinta: 10000)"

CLASSES = [ShortAdventure(), MediumAdventure(), EpicAdventure()]

def get_adventureclass(id):
    for adventure in CLASSES:
        if adventure.id == id:
            return adventure
    raise IndexError()
