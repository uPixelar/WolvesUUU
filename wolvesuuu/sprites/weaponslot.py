from pygame import image, Surface, draw, transform, sprite
from config import WEP_SELECTOR_SIZE
import pygame

class WeaponSlot(sprite.Sprite):
    def __init__(self, weapon_name:str):
        super().__init__()
        self.image = Surface((WEP_SELECTOR_SIZE, WEP_SELECTOR_SIZE), pygame.SRCALPHA).convert_alpha()
        
        draw.rect(self.image, (0, 20, 70, 128), (0, 0, WEP_SELECTOR_SIZE, WEP_SELECTOR_SIZE), border_radius=5)
        draw.rect(self.image, (255, 255, 255, 128), (0, 0, WEP_SELECTOR_SIZE, WEP_SELECTOR_SIZE), 2, border_radius=5)

        
        weapon_image = image.load(f"weapons/{weapon_name}/weapon.png").convert_alpha()
        weapon_image = transform.rotate(weapon_image, 45)
        weapon_width, weapon_height = weapon_image.get_size()
        
        factor = (WEP_SELECTOR_SIZE - 3) / (weapon_width if weapon_width > weapon_height else weapon_height)
        
        weapon_image = transform.scale_by(weapon_image, factor)
        weapon_width, weapon_height = weapon_image.get_size()
        
        self.image.blit(weapon_image, ((WEP_SELECTOR_SIZE - weapon_width) // 2, (WEP_SELECTOR_SIZE - weapon_height) // 2))
        self.original_image = self.image.copy()
        self.rect = self.image.get_rect()
    
    def draw_count(self, count:int):
        pass
    
    def set_count(self, count:int):
        if count == 0:
            self.image = transform.grayscale(self.original_image)
            return
        
        self.image = self.original_image.copy()
        self.draw_count(count)
    
    def set_equipped(self):
        pass
        
    def set_unlocked(self):
        pass
    
    def set_locked(self):
        pass
    
    def update(self):
        raise NotImplementedError