from pygame import Vector2, image, transform, Surface
from pygame.sprite import Sprite, GroupSingle

from collections.abc import Callable
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .player import Player
class SurfaceOffset:
    def __init__(self, surface:Surface, offset: Vector2):
        self.surface = surface
        self.offset = offset
        
class WeaponSprite(Sprite):
    def __init__(self, 
                 weapon_name:str, 
                 handle_offset: tuple[int, int],
                 rotation_offset: int,
                 surface_size: tuple[int, int],
                 weapon_cost: dict[str, int],
                 ):

        super().__init__()
        self.image = image.load(f"weapons/{weapon_name}/weapon.png").convert_alpha()
        if rotation_offset != 0:
            self.image = transform.rotate(self.image, rotation_offset)
        self.image = transform.scale(self.image, surface_size)
        
        self.rect = self.image.get_rect()
        
        self.weapon_name = weapon_name
        self.handle_offset = handle_offset
        self.rotation_offset = rotation_offset
        self.weapon_cost = weapon_cost
        
        self.generate_rotated_images()
        
        # self.degrees = {deg: self.get_surface_offset(deg) for deg in range(-180, 181, 5)}

    
    def get_rotated_image(self, angle:int):
        angle = round(angle/5) * 5
        return self.degrees[angle]

    def generate_rotated_images(self):
        self.degrees:dict[int,SurfaceOffset] = {}
        _center = self.image.get_rect().center
        handle_offset = Vector2(self.handle_offset[0] - _center[0], self.handle_offset[1] - _center[1])
        for angle in range(-180, 181, 5):
            surface = self.image.copy()
            at_left = abs(angle) > 90
            if at_left:
                surface = transform.flip(surface, False, True)
            
            surface = transform.rotate(surface, angle)

            offset = handle_offset.rotate(angle if at_left else -angle)
            
            offset.y = -offset.y if at_left else offset.y
            
            offset = surface.get_rect().center + offset
            
            
            self.degrees[angle] = SurfaceOffset(surface, offset)
           
    def set_angle(self, angle):
        surface_offset = self.get_rotated_image(angle)
        self.image = surface_offset.surface
        self.offset = surface_offset.offset

    def create_group(self):
        return GroupSingle(self)
    
    def shoot(self, shooter:"Player", players:list["Player"], terrain:"Surface", callback:Callable[[], None]) -> bool: 
        """This method will be called on every mouse click when the weapon is equipped.

        Returns:
            bool: Whether the turn should end or not
            
            If returns false the weapon MUST shoot again
        """