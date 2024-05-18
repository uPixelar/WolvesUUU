# wep_rpg7

from .. import WeaponSprite

config = {
    "surface_size": (70, 50),
    "handle_offset": (26, 29)
}

class Weapon(WeaponSprite):
    def shoot(self):
        raise NotImplementedError