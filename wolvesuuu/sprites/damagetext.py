from typing import Literal, TYPE_CHECKING
if TYPE_CHECKING:
    from pygame import Surface

import random, colorsys
from pygame import sprite, Vector2, font, math as pmath

critical_font = font.SysFont("Arial", 40, True)
normal_font = font.SysFont("Arial", 35)
weak_font = font.SysFont("Arial", 25)

class DamageText(sprite.Sprite):
    def __init__(self, pos:Vector2, damage:float, type:Literal["critical", "normal"]="normal"):
        super().__init__()

        text = f"{damage:.1f}"

        if type == "critical":
            self.image = critical_font.render(text + "!!!", True, (255, 0, 0))
        else:
            rgb = colorsys.hsv_to_rgb(0, 1, 0.5+pmath.clamp(damage/200, 0, 0.5))
            color = [int(c*255) for c in rgb]
            if damage > 30:
                self.image = normal_font.render(text, True, color)
            else:
                self.image = weak_font.render(text, True, color)
        
        self.image.set_alpha(128)
        self.rect = self.image.get_rect(center=pos)
        
        self.alpha = 128
        self.moving_vector = Vector2(random.random()*3 - 1.5, -(random.random()*1 + 1))
        
    def update(self):
        self.image.set_alpha(self.alpha)
        self.rect.center += self.moving_vector
        
        self.alpha -= 2
        if self.alpha < 1:
            self.kill()