# wep_ak47

from .. import WeaponSprite

config = {
    "surface_size": (50, 20),
}

class Weapon(WeaponSprite):
    def shoot(self):
        raise NotImplementedError