# wep_rpg7
from .. import WeaponSprite
from ..ammunition.rocket import Rocket

import threading
from pygame import mixer, time

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from sprites import Player
    from pygame import Surface
    
config = {
    "surface_size": (50, 14),
    "handle_offset": (26, 9),
    "weapon_cost": {
        "item_plank": 10,
        "item_metal": 15,
        "item_usd": 1000
    }
}

class Weapon(WeaponSprite):
    def custom_init(self):
        self.rocket_on_way = False
        self.launch_sfx = mixer.Sound("assets/audio/rpg_launch.wav")
        
    def bullet_hit(self):
        self.player.next_player()
        
    def launch(self, shooter:"Player", players:list["Player"], terrain:"Surface"):
        self.rocket = Rocket(self, shooter, players, terrain, self.bullet_hit, self.launch_sfx)
    
    def shoot(self, shooter:"Player", players:list["Player"], terrain:"Surface"):
        if self.rocket_on_way: return
        self.launch_sfx.play()
        self.rocket_on_way = True
        
        threading.Timer(0.753, self.launch, [shooter, players, terrain]).start()