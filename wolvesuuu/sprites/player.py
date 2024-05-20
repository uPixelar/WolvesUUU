from pygame import sprite, key
import numpy as np

# local imports
from weapons.arsenal import Arsenal
from weapons.inventory import Inventory
from weapons import load_weapon

from sprites import Character, WeaponSprite

from collections.abc import Callable


class Player():
    def __init__(self, next_player:Callable[[], None]) -> None:
        self.next_player = next_player
        
        self.inventory = Inventory(self)
        self.arsenal = Arsenal(self)
        self.characters = [Character(self)]
        self.weapon = None
        self.weapon_group = sprite.GroupSingle()
        self.current_character_id = 0
        self.current_character = self.characters[self.current_character_id]
        
        self.is_playing = False
        self.is_armed = False

        self.update_groups()

        # TODO: Remove before release
        self.inventory.inventory = {
            "plank": 9999,
            "metal": 9999,
            "usd": 9999
        }

    def update_groups(self):
        self.character_group = sprite.Group(self.characters)

    def equip(self, weapon_name: str | None = None):
        if weapon_name:
            self.weapon = load_weapon(weapon_name)
            self.weapon_group.add(self.weapon)
        else:
            self.weapon_group.empty()
            self.weapon = None

    def next_character(self):
        self.current_character_id = (
            self.current_character_id+1) % len(self.characters)
        self.current_character = self.characters[self.current_character_id]
        return self.current_character

    def update_weapon_angle(self):
        deg = self.current_character.get_shooting_angle()
        self.current_character.set_facing(abs(deg) <= 90)
        self.weapon.set_angle(deg)
        self.weapon.rect.topleft = self.current_character.rect.center - self.weapon.offset

    # Update & Draw 
       
    def update(self, dt: float, terrain_alpha: np.ndarray):
        keys = key.get_pressed()

        if self.is_playing and not self.is_armed:
            self.current_character.handle_movement_keys(keys)
        else:
            self.current_character.velocity.x = 0

        self.arsenal.update()
        self.character_group.update(dt, terrain_alpha)
        
        if self.is_armed and self.weapon:
            self.update_weapon_angle()

    def draw(self, surface, bgsurf=None, special_flags=0):  # from pygame.sprite.Group.draw
        self.character_group.draw(surface, bgsurf, special_flags)

        if self.is_playing and self.is_armed:
            self.arsenal.draw(surface, bgsurf, special_flags)
            self.weapon_group.draw(surface, bgsurf, special_flags)

    def end_turn(self):
        self.equip()
        self.is_armed = False
        self.is_playing = False
        
    # Event Functions

    def toggle_arsenal_pressed(self):
        self.is_armed = not self.is_armed

    def mouse_clicked(self, mx: int, my: int, button: int):
        self.arsenal.handle_click(mx, my, button)

    def shoot_pressed(self):
        pass

    def shoot_released(self):
        if self.is_armed and self.weapon:
            self.next_player()
