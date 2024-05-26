# wep_revolver

from .. import WeaponSprite
from ..ammunition.bullet import Bullet
from pygame import mixer
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from sprites import Player
    from pygame import Surface
    
config = {
    "surface_size": (25, 25),
    "handle_offset": (7, 15),
    "rotation_offset": -45,
    "damage": 35,
    "weapon_cost": {
        "item_plank": 4,
        "item_metal": 2,
        "item_usd": 200
    }
}

sfx_shoot = mixer.Sound("assets/audio/wep_revolver_shot.wav")

class Weapon(WeaponSprite):
    def custom_init(self):
        self.bullet_on_way = False
        self.hit_count = 0
    
    def bullet_hit(self):
        self.player.next_player()
    
    def shoot(self, shooter:"Player", players:list["Player"], terrain:"Surface", *args, **kwargs):
        if self.bullet_on_way: return
        self.bullet_on_way = True
        sfx_shoot.play()
        Bullet(self, shooter, players, terrain, self.bullet_hit, config['damage'])
            
            