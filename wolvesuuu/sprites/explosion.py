from pygame import image, transform, sprite, Vector2, math as pmath
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sprites import Character, Player

_image =  image.load("assets/images/explosion.png").convert_alpha()
_image.set_alpha(180)


class Explosion(sprite.Sprite):
    def __init__(self, pos:Vector2, shooter:"Player", radius: float, min_speed:float=0.01):
        super().__init__()
        
        self.pos = pos
        self.radius = radius
        self.min_speed = min_speed
        self.size = 5
        self.image = transform.scale(_image, (self.size, self.size))
        self.rect = self.image.get_rect(center=self.pos)
        
        shooter.visuals.add(self)
        
    def update(self):
        self.size += max(min(2, (self.radius*3 - self.size)/6), self.min_speed)
        self.image = transform.scale(_image, (self.size, self.size))
        self.rect = self.image.get_rect(center=self.pos)
        self.image.set_alpha(pmath.lerp(180, 0, min(1, self.size/(self.radius*3))))
        
        
        if self.size > self.radius * 3:
            self.kill()