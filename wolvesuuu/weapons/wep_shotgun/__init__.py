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
    "surface_size": (50, 30),
    "handle_offset": (10, 13),
    "rotation_offset": -45,
    "damage": 10,
    "burst": 5,
    "weapon_cost": {
        "item_plank": 10,
        "item_metal": 10,
        "item_usd": 1200
    }
}

sfx_shoot = mixer.Sound("assets/audio/wep_shotgun_shot.wav")

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
        sfx_shoot.play()
        for i in range(0,config['burst']):
           Bullet(self, shooter, players, terrain, self.bullet_hit, config['damage'])