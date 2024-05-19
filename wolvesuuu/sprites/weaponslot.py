import pygame
from pygame import image, Surface, draw, transform, sprite, font, mouse
from config import WEP_SELECTOR_SIZE


_font = font.SysFont("Arial", 24, True)

class WeaponSlot(sprite.Sprite):
    def __init__(self, weapon_name:str, count:int=0):
        super().__init__()
        self.image = Surface((WEP_SELECTOR_SIZE, WEP_SELECTOR_SIZE), pygame.SRCALPHA).convert_alpha()
        
        draw.rect(self.image, (0, 35, 128, 128), (0, 0, WEP_SELECTOR_SIZE, WEP_SELECTOR_SIZE), border_radius=5)

        weapon_image = image.load(f"weapons/{weapon_name}/weapon.png").convert_alpha()
        weapon_image = transform.rotate(weapon_image, 45)
        weapon_width, weapon_height = weapon_image.get_size()
        
        factor = (WEP_SELECTOR_SIZE - 3) / (weapon_width if weapon_width > weapon_height else weapon_height)
        
        weapon_image = transform.scale_by(weapon_image, factor)
        weapon_width, weapon_height = weapon_image.get_size()
        
        self.image.blit(weapon_image, ((WEP_SELECTOR_SIZE - weapon_width) // 2, (WEP_SELECTOR_SIZE - weapon_height) // 2))
        
        self.original_image = self.image.copy()
        self.rect = self.image.get_rect()
        self.equipped = False
        
        self.set_count(count)
       
    def set_count(self, count:int):
        if count == 0:
            self.image = transform.grayscale(self.original_image)
            return
        print("set count method called", count)
        self.image = self.original_image.copy()
        text = _font.render(f"{count}", True, (190, 190, 10, 128))
        self.image.blit(text, (WEP_SELECTOR_SIZE-17, WEP_SELECTOR_SIZE-29))
    
    def set_equipped(self, equipped:bool):
        self.equipped = equipped
    
    def update(self):
        mx, my = mouse.get_pos()
        
        if self.equipped:
            draw.rect(self.image, (10, 220, 35, 255), (0, 0, WEP_SELECTOR_SIZE, WEP_SELECTOR_SIZE), 2, border_radius=5)
        elif self.rect.collidepoint(mx, my):
            draw.rect(self.image, (0, 128, 30, 128), (0, 0, WEP_SELECTOR_SIZE, WEP_SELECTOR_SIZE), 2, border_radius=5)
        else:
            draw.rect(self.image, (255, 255, 255, 128), (0, 0, WEP_SELECTOR_SIZE, WEP_SELECTOR_SIZE), 2, border_radius=5)