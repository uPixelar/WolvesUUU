# wep_ak47

from .. import WeaponSprite
from ..ammunition.bullet import Bullet
from ..ammunition.a10 import A10
import threading
import pygame
from pygame import mixer, Surface, draw, mouse, display, Vector2
from typing import TYPE_CHECKING
from game import game

if TYPE_CHECKING:
    from sprites import Player
config = {
    "surface_size": (15, 40),
    "handle_offset": (-5, 30),
    "damage": 11,
    "burst": 4,
    "weapon_cost": {
        "item_plank": 5,
        "item_metal": 7,
        "item_usd": 700
    }
}

sfx_shoot = mixer.Sound("assets/audio/radio_call.wav")
inner_beam = Surface((8, 8), pygame.SRCALPHA)
outer_beam = Surface((20, 20), pygame.SRCALPHA)

draw.circle(inner_beam, (255, 0, 0), (4, 4), 4)
draw.circle(outer_beam, (255, 0, 0), (10, 10), 10)

inner_beam.set_alpha(200)
outer_beam.set_alpha(100)

class Weapon(WeaponSprite):
    def custom_init(self):
        self.a10_on_way = False
    
    def operation_completed(self):
        self.player.next_player()
    
    def _shoot(self, shooter:"Player", target:Vector2, players:list["Player"], terrain:"Surface"):
        A10(self, shooter, target, players, terrain, self.operation_completed)
    
    def shoot(self, shooter:"Player", players:list["Player"], terrain:"Surface", *args, **kwargs):
        if self.a10_on_way: return
        self.a10_on_way = True
        sfx_shoot.play()
        game.should_count = False
        self.locked_on = mouse.get_pos()
        threading.Timer(3.299, self._shoot, [shooter, Vector2(self.locked_on), players, terrain]).start()
    
    # override to show laser        
    def __getattribute__(self, name):
        if name == "image":
            screen = display.get_surface()
            mx, my = getattr(self, "locked_on", mouse.get_pos())
            screen.blit(outer_beam, outer_beam.get_rect(center=(mx, my)))
            screen.blit(inner_beam, inner_beam.get_rect(center=(mx, my)))
            
        return object.__getattribute__(self, name)