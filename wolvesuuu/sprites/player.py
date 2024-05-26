from pygame import sprite, key, Surface, draw, math as pmath, mixer
import numpy as np
import random
# local imports
from weapons.arsenal import Arsenal
from weapons.inventory import Inventory, item_names
from weapons import load_weapon

from sprites import Character, WeaponSprite

from collections.abc import Callable

sfx_select_weapon = mixer.Sound("assets/audio/select_weapon.wav")

class Player():
    def __init__(self, spawn_points:list[list[int, int]], starting_items:dict[dict[str, int]], next_player:Callable[[], None], color=(255, 0, 0)) -> None:
        self.next_player = next_player
        
        self.inventory = Inventory(self, starting_items["items"])
        self.arsenal = Arsenal(self, starting_items["weapons"])
        self.weapon = None
        self.weapon_group = sprite.GroupSingle()
        self.character_group = sprite.Group()
        self.projectiles = sprite.Group()
        self.visuals = sprite.Group()
        
        for spawn_point in spawn_points:
            self.character_group.add(Character(self, spawn_point))
        
        self.current_character_id = 0
        self.current_character = self.get_characters()[self.current_character_id]
        
        self.is_playing = False
        self.is_armed = False
        self.weapon_used = False
        self.charging = False
        self.charge = 0
        self.charge_fill = True
        self.color = color

    def get_characters(self) -> list["Character"]:
        return self.character_group.sprites()

    def equip(self, weapon_name: str | None = None):
        if weapon_name:
            sfx_select_weapon.play()
            self.weapon = load_weapon(weapon_name, self)
            self.weapon_group.add(self.weapon)
        else:
            self.weapon_group.empty()
            self.weapon = None
            self.arsenal.set_equipped()

    def next_character(self):
        if len(self.get_characters()) == 0: return
        self.current_character_id = (
            self.current_character_id+1) % len(self.get_characters())
        self.current_character = self.get_characters()[self.current_character_id]
        return self.current_character

    def update_weapon_angle(self):
        deg = self.current_character.get_shooting_angle()
        self.current_character.set_facing(abs(deg) > 90)
        self.weapon.set_angle(deg)
        self.weapon.rect.topleft = self.current_character.rect.center - self.weapon.offset
    
    def add_resources(self):
        for item_name in item_names:
            amount = random.randrange(0,3,1)
            self.inventory.inventory[item_name] = amount + self.inventory.inventory.get(item_name, 0)
        self.inventory.inventory['item_usd'] += random.randrange(100,300,1)
    
    def end_turn(self):
        if self.weapon_used:
            self.arsenal.decrease_weapon()
        
        self.equip()
        self.is_armed = False
        self.is_playing = False
        self.weapon_used = False
    
    def draw_character_indicators(self, surface:"Surface"):
        surf = surface.copy()
        surf.set_alpha(128)
        
        for character in self.get_characters():
            if self.is_playing:
                color = (255, 255, 255)
                if character == self.current_character:
                    color = self.color
                
                draw.polygon(surf, color, [
                    (character.rect.centerx-5, character.rect.top - 20),
                    (character.rect.centerx+5, character.rect.top - 20),
                    (character.rect.centerx, character.rect.top - 15)
                ])
            
            draw.rect(surf, (0, 0, 0), (character.rect.left - 10, character.rect.top - 10, character.rect.width + 20, 6), 1)
            draw.rect(surf, (255, 0, 0), (character.rect.left - 9, character.rect.top - 9, character.rect.width + 18, 4))
            draw.rect(surf, (0, 255, 0), (character.rect.left - 9, character.rect.top - 9, (character.rect.width + 18) * character.health / 100, 4))
            
            # TODO: Move charge bar to character
            if self.is_playing and self.charging:
                def line(x):
                    return 0.1*x
                    
                x1 = 150
                x2 = x1 + 70
                
                draw.polygon(surface, (70, 70, 70), [
                    (x1, 140),
                    (x1, 150),
                    (x2, 150 + line(x2 - x1)),
                    (x2, 140 - line(x2 - x1))
                ])
            
                x1 = 150
                x2 = x1 + pmath.lerp(10, 70, self.charge)
                
                draw.polygon(surface, (70, 200, 70), [
                    (x1, 140),
                    (x1, 150),
                    (x2, 150 + line(x2 - x1)),
                    (x2, 140 - line(x2 - x1))
                ])
            
        surface.blit(surf, (0, 0))

    # Update & Draw 
       
    def update(self, dt: float, terrain_alpha: np.ndarray):
        if self.is_playing and not self.character_group.has(self.current_character):
            self.next_player()
            
        keys = key.get_pressed()

        if self.is_playing and not self.is_armed:
            self.current_character.handle_movement_keys(dt, keys)
        else:
            self.current_character.acceleration.x = 0

        self.arsenal.update()
        self.character_group.update(dt, terrain_alpha)
        self.projectiles.update()
        
        if self.is_armed and self.weapon:
            self.update_weapon_angle()
            if self.charging:
                self.charge += 0.01 if self.charge_fill else -0.01
                if self.charge >= 1:
                    self.charge_fill = False
                    self.charge = 1
                elif self.charge <=0:
                    self.charge_fill = True
                    self.charge = 0
            
        self.visuals.update()

    def draw(self, surface, bgsurf=None, special_flags=0):  # from pygame.sprite.Group.draw
        self.projectiles.draw(surface, bgsurf, special_flags)
        self.character_group.draw(surface, bgsurf, special_flags)

        if self.is_playing and self.is_armed:
            self.weapon_group.draw(surface, bgsurf, special_flags)
        
        
        self.draw_character_indicators(surface)
            
        if self.is_playing and self.is_armed:
            self.arsenal.draw(surface, bgsurf, special_flags)
            self.inventory.draw(surface, bgsurf, special_flags)
        
        self.visuals.draw(surface, bgsurf, special_flags)
    # Event Functions

    def toggle_arsenal_pressed(self):
        if self.weapon_used: return
        self.is_armed = not self.is_armed

    def mouse_clicked(self, mx: int, my: int, button: int):
        if self.weapon_used: return
        self.arsenal.handle_click(mx, my, button)

    def shoot_pressed(self):
        if self.is_armed and self.weapon and self.weapon.should_charge:
            self.charge = 0
            self.charging = True

    def shoot_released(self, shooter:"Player", players:list["Player"], terrain:Surface):
        self.charging = False
        if self.is_armed and self.weapon:
            self.weapon_used = True
            self.weapon.shoot(shooter=shooter, players=players, terrain=terrain, charge=self.charge)
