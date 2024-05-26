# wep_ak47

from .. import WeaponSprite
from ..ammunition.bullet import Bullet
import threading
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sprites import Player
    from pygame import Surface
config = {
    "surface_size": (50, 20),
    "handle_offset": (17, 13),
    "damage": 11,
    "burst": 4,
    "weapon_cost": {
        "item_plank": 5,
        "item_metal": 7,
        "item_usd": 700
    }
}

class Weapon(WeaponSprite):
    def custom_init(self):
        self.bullet_on_way = False
        self.hit_count = 0
    
    def bullet_hit(self):
        self.hit_count += 1
        if self.hit_count == config['burst']:
            self.player.next_player()
        
    def shoot(self, shooter:"Player", players:list["Player"], terrain:"Surface", *args, **kwargs):
        if self.bullet_on_way: return
        self.bullet_on_way = True
        for i in range(0,config['burst']):
            threading.Timer ( i * 0.1, lambda:  Bullet(self, shooter, players, terrain, self.bullet_hit, config['damage'])).start()
            