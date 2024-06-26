from pygame import sprite, Vector2, Surface, draw, rect, display, mixer
import random
from config import WINDOW_WIDTH, WINDOW_HEIGHT
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from sprites import Player, WeaponSprite, Character
    from typing import Callable

sfx_hits = [mixer.Sound("assets/audio/bullet_hit_1.wav"), mixer.Sound("assets/audio/bullet_hit_2.wav"), mixer.Sound("assets/audio/bullet_hit_3.wav"), mixer.Sound("assets/audio/bullet_hit_4.wav")]

class Bullet(sprite.Sprite):
    def __init__(self, weapon:"WeaponSprite", shooter:"Player", players:list["Player"], terrain: "Surface", callback:"Callable[[], None]", damage: int,):
        speed = 6 # TODO: take this as optional parameter
        
        super().__init__()
        self.pos = Vector2(weapon.rect.center)
        self.starting_pos = self.pos.copy()
        
        self.shooter = shooter
        self.players = players
        self.terrain = terrain
        self.callback = callback
        self.damage = damage
        
        self.moving_vector = Vector2(speed, 0)
        self.moving_vector.rotate_ip(-shooter.current_character.get_shooting_angle() + random.random()*4 - 2)
        
        self.image = Surface((3,3))
        draw.circle(self.image, (255, 0, 0), (1, 1), 1.5)
        
        self.rect = self.image.get_rect(center=self.pos)
        shooter.projectiles.add(self)
        
    def update(self):
        collided = False
        new_pos = self.pos+self.moving_vector
        if new_pos[0] < 0 or new_pos[0] > WINDOW_WIDTH or new_pos[1] < 0 or new_pos[1] > WINDOW_HEIGHT:
            self.kill()
            self.callback()
            return
        
        for player in self.players:
            if player == self.shooter: continue
            for character in player.character_group.sprites():
                character:"Character"
                clipline = character.rect.clipline(self.pos, new_pos)
                if clipline:                 
                    collided = True
                    character.bullet_damage(self.damage, Vector2(clipline[0]))
                    self.kill()
                    self.callback()
                    break
                    
        # BUG: bullet can jump over pixels shorter than speed, check every pixel to fix
        if self.terrain.get_at((int(new_pos.x), int(new_pos.y)))[3] > 0:
            draw.circle(self.terrain, (0,0,0,0), (new_pos.x, new_pos.y), 5)
            collided = True
            random.choice(sfx_hits).play()
            self.kill()
            self.callback()
            
        if not collided:
            self.pos =  new_pos
            self.rect.center = self.pos
        
         