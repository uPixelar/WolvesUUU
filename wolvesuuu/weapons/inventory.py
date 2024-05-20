from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from sprites.player import Player
    
import math


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
            
    def get_inventory(self) -> dict[str, int]:
        return self.inventory