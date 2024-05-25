from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from sprites.player import Player
    
import math, pygame
import pygame.locals

from sprites import WeaponSlot
import weapons
from pygame import sprite, Rect, mouse
from . import weapon_names
from config import WEP_SELECTOR_COLS, WEP_SELECTOR_SIZE, WEP_SELECTOR_GAP, WINDOW_WIDTH, WINDOW_HEIGHT


class Arsenal:
    def __init__(self, player:"Player"):
        self.player = player
        self.group = sprite.Group()
        self.arsenal:dict[str, int] = {}
        self.sprites:dict[str, WeaponSlot] = {}
        self.current_weapon = "wep_ak47"
        
        for i in range(len(weapon_names)):
            weapon_name = weapon_names[i]
            _sprite = WeaponSlot(weapon_name)
            
            ix = i % WEP_SELECTOR_COLS + 1
            iy = math.floor(i/WEP_SELECTOR_COLS) + 1
            _sprite.rect = Rect((WINDOW_WIDTH-WEP_SELECTOR_GAP*ix-WEP_SELECTOR_SIZE*ix, WINDOW_HEIGHT-WEP_SELECTOR_GAP*iy-WEP_SELECTOR_SIZE*iy, WEP_SELECTOR_SIZE, WEP_SELECTOR_SIZE))
            
            self.group.add(_sprite)
            self.sprites[weapon_name] = _sprite
            self.arsenal[weapon_name] = 0
    
    def set_count(self, weapon_name:str, count:int):
        self.sprites[weapon_name].set_count(count)
        self.arsenal[weapon_name] = count
    
    def set_equipped(self, weapon_name:str=None):
        self.sprites[self.current_weapon].set_equipped(False)
        
        if weapon_name:
            self.sprites[weapon_name].set_equipped(True)
        
    def increase_weapon(self, weapon_name:str=None):
        if not weapon_name: weapon_name = self.current_weapon
        
        self.set_count(weapon_name, self.arsenal[weapon_name] + 1)
        
    def decrease_weapon(self, weapon_name:str=None):
        if not weapon_name: weapon_name = self.current_weapon
        new_count = max(self.arsenal[weapon_name] - 1, 0)
        
        self.set_count(weapon_name, new_count)
        if new_count == 0 and weapon_name == self.current_weapon:
            self.player.equip()
    
    def handle_click(self, x:int, y:int, button:int):
        if button == pygame.BUTTON_LEFT: # equip
            for weapon_name, _sprite in self.sprites.items():
                if _sprite.rect.collidepoint(x, y):
                    if self.arsenal[weapon_name] > 0:
                        self.sprites[self.current_weapon].set_equipped(False)
                        
                        self.current_weapon = weapon_name
                        self.sprites[weapon_name].set_equipped(True)
                        self.player.equip(weapon_name)
                        
                    break
                
        elif button == pygame.BUTTON_RIGHT: # buy/craft
            for weapon_name, _sprite in self.sprites.items():
                if _sprite.rect.collidepoint(x, y):
                    weapon = weapons.load_weapon(weapon_name)
                    if self.player.inventory.buy(weapon.weapon_cost):
                        self.increase_weapon(weapon_name)
                    
                    break
                
        elif button == pygame.BUTTON_MIDDLE: # decrease
            for weapon_name, _sprite in self.sprites.items():
                if _sprite.rect.collidepoint(x, y):
                    if self.arsenal[weapon_name] > 0:
                        weapon = weapons.load_weapon(weapon_name)
                        self.player.inventory.scrap(weapon.weapon_cost)
                        self.decrease_weapon(weapon_name)

                    break
    
    # Draw & Update

    def draw(self, surface, bgsurf=None, special_flags=0):
        mx, my = mouse.get_pos()
        
        self.group.draw(surface, bgsurf, special_flags)
        
        for weapon_name, _sprite in self.sprites.items():
            if _sprite.rect.collidepoint(mx, my):
                weapon = weapons.load_weapon(weapon_name)
                self.player.inventory.draw_cost(surface, weapon.weapon_cost)
                

    def update(self):
        self.group.update()
    
    # other
    
    def get_group(self):
        return self.group