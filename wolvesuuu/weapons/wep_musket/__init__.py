# wep_musket
from pygame import Vector2

from .. import WeaponSprite
from ..bullet import Bullet

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from sprites import Player
    from pygame import Surface
    from typing import Callable

config = {
    "surface_size": (40, 40),
    "handle_offset": (13, 25),
    "rotation_offset": -45,
    "weapon_cost": {
        "plank": 10,
        "metal": 3,
        "usd": 700
    }
}

class Weapon(WeaponSprite):
    def shoot(self, shooter:"Player", players:list["Player"], terrain:"Surface", callback:"Callable[[], None]"):
        bullet = Bullet(self, shooter, players, terrain, callback)