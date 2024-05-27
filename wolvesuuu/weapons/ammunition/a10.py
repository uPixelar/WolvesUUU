from pygame import sprite, Vector2, Surface, draw, rect, display, image, transform, mixer
import threading, random
from config import WINDOW_WIDTH, WINDOW_HEIGHT
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from sprites import Player, WeaponSprite, Character
    from typing import Callable
    
from .a10bullet import A10Bullet

_image = image.load("assets/ammunition/a10.png").convert_alpha()
_image = transform.scale_by(_image, 0.4)

sfx_fly = mixer.Sound("assets/audio/a10_flight.wav")
sfx_shot = mixer.Sound("assets/audio/a10_shot.wav")

class A10(sprite.Sprite):
    def __init__(self, weapon:"WeaponSprite", shooter:"Player", target:Vector2, players:list["Player"], terrain: "Surface", callback:"Callable[[], None]"):
        super().__init__()
        self.from_left = target.x > WINDOW_WIDTH / 2
        self.width, self.height = _image.get_size()
        
        self.pos = Vector2(-self.width, 20) if self.from_left else Vector2(WINDOW_WIDTH, 50)
        
        self.image = _image if self.from_left else transform.flip(_image, True, False)
        self.rect = self.image.get_rect(topleft=(self.pos))
        
        sfx_fly.play(-1)
        
        self.weapon = weapon
        self.shooter = shooter
        self.target = target
        self.players = players
        self.terrain = terrain
        self.callback = callback
        
        self.did_shoot = False 
        self.first_hit = True
        self.bullet_count = 0
        
        self.moving_vector = Vector2(6 if self.from_left else -6, 0)

        shooter.projectiles.add(self)
        
    def update(self):
        self.pos += self.moving_vector
        self.rect.topleft = self.pos
        
        if self.rect.left > WINDOW_WIDTH + 500 or self.rect.right < -500:
            self.kill()
            sfx_fly.stop()
        
        if not self.did_shoot:
            if abs(self.target.x - self.pos.x) < 500 + self.width:
                self.did_shoot = True
                
                for i in range(20):
                    threading.Timer(0.05*i, self.shoot, [Vector2(self.target.x + (i-9.5) * 10 + random.random()*2 - 1, self.target.y)]).start()
         
    def shoot(self, target):
        gun_pos = Vector2(self.rect.right - 5, self.rect.bottom-5) if self.from_left else Vector2(self.rect.left + 5, self.rect.bottom-5)
        A10Bullet(gun_pos, target, self.players, self.terrain, self.bullet_hit, 5)
                
    def bullet_hit(self):
        if self.first_hit:
            self.first_hit = False
            sfx_shot.play()
            
        self.bullet_count += 1
        if self.bullet_count == 20:
            self.callback()