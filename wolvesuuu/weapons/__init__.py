# weapons/__init__.py

import os, importlib
from sprites.weapon import WeaponSprite

def load_weapon(weapon_name: str):
    """Loads the weapon as sprite.

    Args:
        weapon_name (str): Unique name of the weapon registered in game

    Returns:
        Weapon sprite
        """

    PATH = os.path.join("weapons", weapon_name)
    module = importlib.import_module(f"weapons.{weapon_name}")
    weapon:WeaponSprite = module.Weapon(weapon_name)
    return weapon