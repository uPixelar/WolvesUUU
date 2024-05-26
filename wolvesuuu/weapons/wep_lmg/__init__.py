# wep_lmg

from .. import WeaponSprite
from ..ammunition.bullet import Bullet
from pygame import mixer
import threading
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from sprites import Player
    from pygame import Surface
    
config = {
    "surface_size": (70, 50),
    "handle_offset": (26, 29),
    "damage": 13,
    "burst": 5,
    "weapon_cost": {
        "item_plank": 10,
        "item_metal": 10,
        "item_usd": 1200
    }
}

sfx_shoot = mixer.Sound("assets/audio/wep_lmg_shot.wav")

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