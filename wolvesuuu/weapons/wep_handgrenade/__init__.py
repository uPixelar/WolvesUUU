# wep_musket
from .. import WeaponSprite
from ..ammunition.grenade import Grenade

import threading
from pygame import mixer

from game import game

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from sprites import Player
    from pygame import Surface

config = {
    "surface_size": (10, 15),
    "handle_offset": (-10, 7),
    "damage": 50,
    "should_charge": True,
    "weapon_cost": {
        "item_plank": 10,
        "item_metal": 3,
        "item_usd": 700
    }
}

sfx_click = mixer.Sound("assets/audio/wep_handgrenade_click.wav")
sfx_throw = mixer.Sound("assets/audio/wep_handgrenade_throw.wav")


class Weapon(WeaponSprite):
    def custom_init(self):
        self.grenade_on_way = False
        
    def bullet_hit(self):
        self.player.next_player()
    
    def shoot(self, shooter:"Player", players:list["Player"], terrain:"Surface", charge:float=0.1, *args, **kwargs):
        if self.grenade_on_way: return
        self.grenade_on_way = True
        game.should_count = False
        sfx_throw.play()
        Grenade(self, shooter, players, terrain, self.bullet_hit, config['damage'], charge)
        
    def start_charging(self):
        if self.grenade_on_way: return
        sfx_click.play()
            
            
            