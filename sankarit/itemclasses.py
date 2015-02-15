# -*- coding: utf-8 -*-

import random

SLOTS = HELM, CHEST, GLOVES, BOOTS, BELT = range(5)

RARITY = POOR, COMMON, UNCOMMON, RARE, EPIC = range(5)

RARITY_CHOICES = (
    (POOR, u"Huonolaatuinen"),
    (COMMON, u"Yleinen"),
    (UNCOMMON, u"Epätavallinen"),
    (RARE, u"Harvinainen"),
    (EPIC, u"Ebin :D"),
)

def roll_rarity():
    """Gets a rarity according to standard distribution"""
    for rarity in RARITY:
        if random.random() < 0.9:
            break
    return rarity

class BaseItem(object):
    name = "Placeholder"
    str_factor = 0
    agi_factor = 0
    int_factor = 0
    con_factor = 0

    def get_str(self, level, rarity):
        return int((self.str_factor + rarity*2) * level)

    def get_agi(self, level, rarity):
        return int((self.agi_factor + rarity*2) * level)

    def get_int(self, level, rarity):
        return int((self.int_factor + rarity*2) * level)

    def get_con(self, level, rarity):
        return int((self.con_factor + rarity*2) * level)

class StrItem(object):
    str_factor = 4
    prefix = u"Voimakas"

class AgiItem(object):
    agi_factor = 4
    prefix = u"Ripeä"

class IntItem(object):
    int_factor = 4
    prefix = u"Nokkela"

class ConItem(object):
    con_factor = 4
    prefix = u"Luja"

class StrAndConItem(object):
    str_factor = 2
    con_factor = 2
    prefix = u"Puolustajan"

class AgiAndConItem(object):
    agi_factor = 2
    con_factor = 2
    prefix = u"Samoojan"

class IntAndConItem(object):
    int_factor = 2
    con_factor = 2
    prefix = u"Tietäjän"

class BasicItem(object):
    str_factor = 1
    agi_factor = 1
    int_factor = 1
    con_factor = 1
    prefix = u"Sotilaan"

MODIFIERS = [BasicItem,
             StrItem, AgiItem, IntItem, ConItem,
             StrAndConItem, AgiAndConItem, IntAndConItem]

class Helmet(BaseItem):
    slot_name = u"Kypärä"
    #id = 1
    slot = HELM

class Chest(BaseItem):
    slot_name = u"Rintapanssari"
    #id = 2
    slot = CHEST

class Gloves(BaseItem):
    slot_name = u"Hanskapari"
    #id = 3
    slot = GLOVES

class Boots(BaseItem):
    slot_name = u"Saapaspari"
    #id = 4
    slot = BOOTS

class Belt(BaseItem):
    slot_name = u"Vyö"
    #id = 5
    slot = BELT

SLOTS = [Helmet, Chest, Gloves, Boots, Belt]

CLASSES = [] #Helmet(), Chest(), Gloves(), Boots(), Belt()]

mkid = iter(xrange(1, 1+len(SLOTS)*len(MODIFIERS)))

for modifier in MODIFIERS:
    for slot in SLOTS:
        class Item(modifier, slot):
            id = mkid.next()
            name = modifier.prefix + u" " + slot.slot_name

        CLASSES.append(Item())

def get_itemclass(itemclass_id):
    for class_ in CLASSES:
        if class_.id == itemclass_id:
            return class_
    raise ValueError("no such itemclass")
