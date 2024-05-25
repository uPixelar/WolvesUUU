# wep_smg

from .. import WeaponSprite

config = {
    "surface_size": (25, 25),
    "handle_offset": (5, 15),
    "rotation_offset": -25,
    "weapon_cost": {
        "item_plank": 5,
        "item_metal": 3,
        "item_usd": 500
    }
}

class Weapon(WeaponSprite):
    def shoot(self):
        pass