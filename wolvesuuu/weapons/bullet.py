from pygame import sprite, Vector2, Surface, draw, rect, display
import random

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from sprites import Player, WeaponSprite, Character
    from typing import Callable

class Bullet(sprite.Sprite):
    def __init__(self, weapon:"WeaponSprite", shooter:"Player", players:list["Player"], terrain: "Surface", callback:"Callable[[], None]"):
        speed = 4 # TODO: take this as optional parameter
        
        super().__init__()
        self.pos = Vector2(weapon.rect.center)
        self.starting_pos = self.pos.copy()
        
        self.shooter = shooter
        self.players = players
        self.terrain = terrain
        self.callback = callback
        
        self.moving_vector = Vector2(4.0, 0)
        self.moving_vector.rotate_ip(-shooter.current_character.get_shooting_angle() + random.random()*5 - 2.5)
        
        self.image = Surface((3,3))
        draw.circle(self.image, (255, 0, 0), (1, 1), 1.5)
        
        self.rect = self.image.get_rect(center=self.pos)
        shooter.projectiles.add(self)
        
    def update(self):
        collided = False
        new_pos = self.pos+self.moving_vector
        for player in self.players:
            if player == self.shooter: continue
            for character in player.character_group.sprites():
                clipline = character.rect.clipline(self.pos, new_pos)
                if clipline:                 
                    collided = True
                    character.kill()
                    self.kill()
                    break
                    
        # BUG: bullet can jump over pixels shorter than speed, check every pixel to fix
        if self.terrain.get_at((int(new_pos.x), int(new_pos.y)))[3] > 0:
            draw.circle(self.terrain, (0,0,0,0), (new_pos.x, new_pos.y), 5)
            collided = True
            self.kill()
            
        if not collided:
            self.pos =  new_pos
            self.rect.center = self.pos
            