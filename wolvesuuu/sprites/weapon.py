import pygame 

from pygame import Vector2

class SurfaceOffset:
    def __init__(self, surface, offset):
        self.surface = surface
        self.offset:Vector2 = offset
        

class WeaponSprite(pygame.sprite.Sprite):
    def __init__(self, 
                 weapon_name:str, 
                 handle_offset: tuple[int, int],
                 surface_size: tuple[int, int]
                 ):

        super().__init__()
        
        self.image = pygame.image.load(f"weapons/{weapon_name}/weapon.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, surface_size)
        self.rect = self.image.get_rect()
        self.rect.x+=20
        self.rect.y+=30
        
        self.weapon_name = weapon_name
        self.holding_offset = handle_offset
        self.degrees = {deg: self.get_surface_offset(deg) for deg in range(-180, 181, 5)}

    def get_surface_offset(self, angle):
        surface = self.image
        if abs(angle) > 90:
            surface = pygame.transform.flip(surface, False, True)
        surface = pygame.transform.rotate(surface, angle)
        
            
        offset = self.find_offset(angle)
        
        return SurfaceOffset(surface, offset)

    def find_offset(self, angle):
        handle = Vector2(-15, 0)
        offset = handle.rotate(-angle)
        return offset

    def set_angle(self, angle):
        angle = round(angle / 5) * 5
        surface_offset = self.degrees[angle]
        
        self.image = surface_offset.surface
        self.rect.update(self.image.get_rect(center=self.rect.center))
        self.offset = surface_offset.offset

    def create_group(self):
        return pygame.sprite.GroupSingle(self)
    
    def shoot(self) -> bool: 
        """This method will be called on every mouse click when the weapon is equipped.

        Returns:
            bool: Whether the turn should end or not
            
            If returns false the weapon MUST shoot again
        """