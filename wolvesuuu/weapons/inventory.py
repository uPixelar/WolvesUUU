import math


class Inventory:
    def __init__(self):
        self.inventory:dict[str, int] = {}
    
    def buy(self, cost:dict[str, int]):
        for key, value in cost.items():
            if self.inventory.get(key, 0) - value < 0:
                print("Not enough resources")
                print(self.inventory)
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
        print(self.inventory)
            
    def get_inventory(self) -> dict[str, int]:
        return self.inventory