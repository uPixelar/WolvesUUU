# wep_smg

from .. import WeaponSprite

config = {
    "surface_size": (25, 25),
    "handle_offset": (5, 15),
    "weapon_cost": {
        "plank": 5,
        "metal": 3,
        "usd": 500
    }
}

class Weapon(WeaponSprite):
    def shoot(self):
        raise NotImplementedError