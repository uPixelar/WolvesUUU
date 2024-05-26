# wep_ak47

from .. import WeaponSprite
from ..ammunition.bullet import Bullet
import threading
from pygame import mixer
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sprites import Player
    from pygame import Surface
config = {
    "surface_size": (50, 15),
    "handle_offset": (17, 13),
    "damage": 11,
    "burst": 4,
    "weapon_cost": {
        "item_plank": 5,
        "item_metal": 7,
        "item_usd": 700
    }
}

sfx_shoot = mixer.Sound("assets/audio/wep_ak47_shot.wav")

class Weapon(WeaponSprite):
    def custom_init(self):
        self.bullet_on_way = False
        self.hit_count = 0
    
    def bullet_hit(self):
        self.hit_count += 1
        if self.hit_count == config['burst']:
            self.player.next_player()
    
    def _shoot(self, shooter:"Player", players:list["Player"], terrain:"Surface", callback, damage):
        sfx_shoot.play()
        Bullet(self, shooter, players, terrain, callback, damage)
    
    def shoot(self, shooter:"Player", players:list["Player"], terrain:"Surface", *args, **kwargs):
        if self.bullet_on_way: return
        self.bullet_on_way = True
        for i in range(0,config['burst']):
            threading.Timer ( i * 0.1, self._shoot, [shooter, players, terrain, self.bullet_hit, config['damage']]).start()
            