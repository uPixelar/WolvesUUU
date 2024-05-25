# wep_ak47

from .. import WeaponSprite

config = {
    "surface_size": (50, 20),
    "handle_offset": (17, 13),
    "weapon_cost": {
        "item_plank": 5,
        "item_metal": 7,
        "item_usd": 700
    }
}

class Weapon(WeaponSprite):
    def shoot(self):
        pass