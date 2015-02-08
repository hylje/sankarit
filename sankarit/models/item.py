class Item(object):
    def __init__(self, iid, level, class_, slot, rarity, player_id, hero_id, adventure_id, player=None, hero=None, adventure=None):
        self.iid = iid
        self.level = level
        self.class_ = class_
        self.slot = slot
        self.rarity = rarity
        self.player_id = player_id
        self.player = player
        self.hero_id = hero_id
        self.adventure_id = adventure_id
