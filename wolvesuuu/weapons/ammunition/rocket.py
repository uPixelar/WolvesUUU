from pygame import sprite, Vector2, Surface, draw, rect, display, image, transform, mixer, math as pyg_math
import random, math
from config import WINDOW_WIDTH, WINDOW_HEIGHT
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from sprites import Player, WeaponSprite, Character
    from typing import Callable
    

class Rocket(sprite.Sprite):
    def __init__(self, weapon:"WeaponSprite", shooter:"Player", players:list["Player"], terrain: "Surface", callback:"Callable[[], None]", launch_sfx:"mixer.Sound"):
        speed = 6 # TODO: take this as optional parameter
        
        super().__init__()
        self.pos = Vector2(weapon.rect.center)
        self.starting_pos = self.pos.copy()
        
        self.shooter = shooter
        self.players = players
        self.terrain = terrain
        self.callback = callback
        self.launch_sfx = launch_sfx
        self.blast_sfx = mixer.Sound("assets/audio/rpg_blast.wav")
        self.volume = 1

        
        self.angle = -shooter.current_character.get_shooting_angle()
        
        self.moving_vector = Vector2(speed, 0)
        self.moving_vector.rotate_ip(self.angle + random.random()*4 - 2)
        self.image_org = image.load("assets/ammunition/rpg7_rocket.png").convert_alpha()
        self.image_org = transform.scale_by(self.image_org, 0.2)
        
        self.image = transform.rotate(self.image_org, -self.angle)
        self.rect = self.image.get_rect(center=self.pos)
        
        shooter.projectiles.add(self)
    
    def apply_physics(self):
        self.angle += 0.05
        self.moving_vector.rotate_ip(0.05)
        self.image = transform.rotate(self.image_org, -self.angle)
    
    def update_volume(self):
        dist = math.hypot(self.rect.x-self.shooter.current_character.rect.x, self.rect.y-self.shooter.current_character.rect.y)
        self.volume = pyg_math.clamp(200/dist, 0.01, 1)
        self.launch_sfx.set_volume(self.volume)
    
    def blast(self):
        self.launch_sfx.stop()
        self.blast_sfx.play().set_volume(self.volume)
    
    def catch_collision(self, new_pos:"Vector2"):
        collided = False
        
        for player in self.players:
            if player == self.shooter: continue
            for character in player.character_group.sprites():
                collision = self.rect.colliderect(character.rect)
                if collision:                 
                    collided = True
                    self.blast()
                    character.kill()
                    self.kill()
                    self.callback()
                    break
                    
        # BUG: bullet can jump over pixels shorter than speed, check every pixel to fix
        if self.terrain.get_at((int(new_pos.x), int(new_pos.y)))[3] > 0:
            draw.circle(self.terrain, (0,0,0,0), (new_pos.x, new_pos.y), 35)
            collided = True
            self.blast()
            self.kill()
            self.callback()
            
        return collided
    
    def update(self):
        new_pos = self.pos+self.moving_vector
        # ScreenSafe check
        if new_pos.x < 0 or new_pos.x > WINDOW_WIDTH or new_pos.y < 0 or new_pos.y > WINDOW_HEIGHT:
            self.kill()
            self.callback()
            return
        
        collision = self.catch_collision(new_pos)
        
        if collision:
            pass
        else:
            self.pos =  new_pos
            self.rect.center = self.pos
            
        self.apply_physics()
        self.update_volume()