# wep_rpg7

from .. import WeaponSprite

config = {
    "surface_size": (50, 14),
    "handle_offset": (26, 9),
    "weapon_cost": {
        "plank": 10,
        "metal": 15,
        "usd": 1000
    }
}

class Weapon(WeaponSprite):
    def shoot(self):
        pass