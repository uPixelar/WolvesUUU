# wep_rpg7

from .. import WeaponSprite

config = {
    "surface_size": (25, 25),
    "handle_offset": (5, 15)
}

class Weapon(WeaponSprite):
    def shoot(self):
        raise NotImplementedError