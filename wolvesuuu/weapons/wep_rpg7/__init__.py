# wep_rpg7

from .. import WeaponSprite

config = {
    "surface_size": (50, 14),
    "handle_offset": (26, 9)
}

class Weapon(WeaponSprite):
    def shoot(self):
        raise NotImplementedError