from typing import TYPE_CHECKING
from pygame import transform, image
if TYPE_CHECKING:
    from sprites.player import Player
    
import math

item_names = [
    "item_usd",
    "item_plank",
    "item_metal"
]

images = {item_name:(transform.scale(image.load(f"assets/items/{item_name}.png").convert_alpha(), (40, 40))) for item_name in item_names}

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
    
    def draw(self):
        index = 0
        for item, image in images.items():
            count = self.inventory.get(item, 0)