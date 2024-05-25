# wep_musket
from .. import WeaponSprite
from ..ammunition.bullet import Bullet

import threading
from pygame import mixer

from game import game

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from sprites import Player
    from pygame import Surface

config = {
    "surface_size": (40, 40),
    "handle_offset": (13, 25),
    "rotation_offset": -45,
    "weapon_cost": {
        "item_plank": 10,
        "item_metal": 3,
        "item_usd": 700
    }
}

class Weapon(WeaponSprite):
    def custom_init(self):
        self.bullet_on_way = False
        self.hit_count = 0
        self.musket_sfx = mixer.Sound("assets/audio/musket_shot.wav")
        
    def bullet_hit(self):
        self.player.next_player()
    
    def shoot(self, shooter:"Player", players:list["Player"], terrain:"Surface"):
        if self.bullet_on_way: return
        self.bullet_on_way = True

        self.musket_sfx.play().set_volume(game.vol_sound_effects * game.vol_overall)
        Bullet(self, shooter, players, terrain, self.bullet_hit)
            
            
            