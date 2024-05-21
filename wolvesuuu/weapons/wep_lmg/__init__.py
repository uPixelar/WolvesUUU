# wep_lmg

from .. import WeaponSprite

config = {
    "surface_size": (70, 50),
    "handle_offset": (26, 29),
    "weapon_cost": {
        "plank": 10,
        "metal": 10,
        "usd": 1200
    }
}

class Weapon(WeaponSprite):
    def shoot(self):
        pass