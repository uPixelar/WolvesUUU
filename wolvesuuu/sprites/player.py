from weapons.arsenal import Arsenal
from weapons.inventory import Inventory
from sprites.character import Character

class Player():
    def __init__(self) -> None:
        self.inventory = Inventory(self)
        self.arsenal = Arsenal(self)
        self.characters = [Character(self)]
        self.lastCharacterId = -1
