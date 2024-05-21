# wep_ak47

from .. import WeaponSprite

config = {
    "surface_size": (50, 20),
    "handle_offset": (17, 13),
    "weapon_cost": {
        "plank": 5,
        "metal": 7,
        "usd": 700
    }
}

class Weapon(WeaponSprite):
    def shoot(self):
        pass