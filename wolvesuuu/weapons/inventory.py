from sprites import Player
import math


class Inventory:
    def __init__(self, player:Player):
        self.player = player
        self.inventory:dict[str, int] = {}
    
    def buy(self, cost:dict[str, int]):
        for key, value in cost.items():
            if self.inventory.get(key, 0) - value < 0:
                return False
        for key, value in cost.items():
            self.inventory[key] -= value
        return True
    
    def scrap(self, cost:dict[str, int]):
        for key, value in cost.items():
            self.inventory[key] += math.floor(value/2)