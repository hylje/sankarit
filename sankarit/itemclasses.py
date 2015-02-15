import random

SLOTS = HELM, CHEST, GLOVES, BOOTS, BELT = range(5)

RARITY = POOR, COMMON, UNCOMMON, RARE, EPIC = range(5)

def roll_rarity():
    """Gets a rarity according to standard distribution"""
    for rarity in RARITY:
        if random.random() < 0.9:
            break
    return rarity

class BaseItem(object):
    pass

class Helmet(object):
    id = 1
    slot = HELM

class Chest(object):
    id = 2
    slot = CHEST

class Gloves(object):
    id = 3
    slot = GLOVES

class Boots(object):
    id = 4
    slot = BOOTS

class Belt(object):
    id = 5
    slot = BELT

CLASSES = [Helmet(), Chest(), Gloves(), Boots(), Belt()]
