# wep_revolver

from .. import WeaponSprite

config = {
    "surface_size": (25, 25),
    "handle_offset": (5, 15),
    "weapon_cost": {
        "plank": 4,
        "metal": 2,
        "usd": 200
    }
}

class Weapon(WeaponSprite):
    def shoot(self):
        raise NotImplementedError