# wep_revolver

from .. import WeaponSprite

config = {
    "surface_size": (25, 25),
    "handle_offset": (7, 15),
    "rotation_offset": -45,
    "weapon_cost": {
        "item_plank": 4,
        "item_metal": 2,
        "item_usd": 200
    }
}

class Weapon(WeaponSprite):
    def shoot(self):
        pass