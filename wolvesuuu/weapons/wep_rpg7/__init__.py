# wep_ak47

from .. import WeaponSprite

config = {
    "surface_size": (50, 20),
    "handle_offset": (26, 13)
}

class Weapon(WeaponSprite):
    def shoot(self):
        raise NotImplementedError