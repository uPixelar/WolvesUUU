from typing import TYPE_CHECKING
from pygame import transform, image, font
from config import WINDOW_WIDTH
if TYPE_CHECKING:
    from sprites.player import Player
    from pygame import Surface
    
import math

item_names = [
    "item_usd",
    "item_plank",
    "item_metal"
]

images = {item_name:(transform.scale(image.load(f"assets/items/{item_name}.png").convert_alpha(), (30, 30))) for item_name in item_names}

count_font = font.SysFont("Arial", 30)
exchange_font = font.SysFont("Arial", 14)

class Inventory:
    def __init__(self, player:"Player"):
        self.inventory:dict[str, int] = {}
        self.player = player
    
    def buy(self, cost:dict[str, int]):
        for key, value in cost.items():
            if self.inventory.get(key, 0) - value < 0:
                return False
        for key, value in cost.items():
            self.inventory[key] -= value
        return True
    
    def scrap(self, cost:dict[str, int]):
        for key, value in cost.items():
            if key in self.inventory:
                self.inventory[key] += math.floor(value/2)
            else:
                self.inventory[key] = math.floor(value/2)
                
    def scrapped(self, cost:dict[str, int]):
        scrap = cost.copy()
        
        for key, value in cost.items():
            scrap[key] = math.floor(value/2)
            
        return scrap
            
    def draw(self, surface:"Surface", bgsurf=None, special_flags=0):
        index = 0
        for item, image in images.items():
            count = self.inventory.get(item, 0)
            count_image = count_font.render(f"{count}", True, (255, 255, 255))
            count_rect = count_image.get_rect(topleft=(WINDOW_WIDTH - 60, index*40 + 10))
            
            surface.blit(image, (WINDOW_WIDTH - 100, index*40 + 10))
            surface.blit(count_image, count_rect)
            index += 1
            
    def draw_cost(self, surface:"Surface", cost:dict[str, int]):
        scrap = self.scrapped(cost.copy())
        
        index = 0
        for item, image in images.items():
            cost_amount = cost.get(item, 0)
            scrap_amount = scrap.get(item, 0)
            
            topright = (WINDOW_WIDTH - 110, index*40 + 10)
            
            cost_image = exchange_font.render(f"-{cost_amount}", True, (0, 255, 0))
            cost_rect = cost_image.get_rect(topright=topright)
            
            scrap_image = exchange_font.render(f"+{scrap_amount}", True, (255, 0, 0))
            scrap_rect = scrap_image.get_rect(topright=(topright[0], topright[1]+16))
            
            surface.blit(scrap_image, scrap_rect)
            surface.blit(cost_image, cost_rect)
            index += 1
            