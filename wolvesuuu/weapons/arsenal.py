from sprites import WeaponSlot
from pygame import sprite, Rect
from . import weapon_names
from config import WEP_SELECTOR_COLS, WEP_SELECTOR_SIZE, WEP_SELECTOR_GAP, WINDOW_WIDTH, WINDOW_HEIGHT

import math

class Arsenal:
    def __init__(self):
        self.group = sprite.Group()
        self.arsenal:dict[str, int] = {}
        self.sprites:dict[str, WeaponSlot] = {}
        
        for i in range(len(weapon_names)):
            weapon_name = weapon_names[i]
            _sprite = WeaponSlot(weapon_name)
            
            ix = i % WEP_SELECTOR_COLS + 1
            iy = math.floor(i/WEP_SELECTOR_COLS) + 1
            _sprite.rect = Rect((WINDOW_WIDTH-WEP_SELECTOR_GAP*ix-WEP_SELECTOR_SIZE*ix, WINDOW_HEIGHT-WEP_SELECTOR_GAP*iy-WEP_SELECTOR_SIZE*iy, WEP_SELECTOR_SIZE, WEP_SELECTOR_SIZE))
            
            self.group.add(_sprite)
            self.sprites[weapon_name] = _sprite
            self.arsenal[weapon_name] = 0
            
    def get_group(self):
        return self.group