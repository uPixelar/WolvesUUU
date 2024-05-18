# wep_musket

from .. import WeaponSprite

config = {
    "surface_size": (40, 40),
    "handle_offset": (13, 25),
    "weapon_cost": {
        "plank": 10,
        "metal": 3,
        "usd": 700
    }
}

class Weapon(WeaponSprite):
    def shoot(self):
        raise NotImplementedError