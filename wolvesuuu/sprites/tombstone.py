from pygame import image, transform, sprite
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sprites import Character

tombstone_img = image.load("assets/images/tombstone.png").convert_alpha()
tombstone_img = transform.scale_by(tombstone_img, 0.075)

class Tombstone(sprite.Sprite):
    def __init__(self, character:"Character"):
        super().__init__()
        
        self.image = tombstone_img
        
        self.rect = self.image.get_rect(midbottom=character.rect.midbottom)
        character.player.visuals.add(self)