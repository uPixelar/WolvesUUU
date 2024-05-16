# weapons/__init__.py

import importlib, glob
from sprites.weapon import WeaponSprite
from typing import Type, ClassVar

weapon_names = glob.glob("wep_*", root_dir="weapons/")

def load_weapon(weapon_name: str):
    """Loads the weapon as sprite.

    Args:
        weapon_name (str): Unique name of the weapon registered in game

    Returns:
        Weapon sprite
        """

    _module = importlib.import_module(f"weapons.{weapon_name}")
    _class: Type["WeaponSprite"] = _module.Weapon
    _config:dict = _module.config
    
    weapon = _class(
        weapon_name = weapon_name,
        handle_offset = _config.get("handle_offset", (5, 5)),
        surface_size = _config.get("surface_size", (40, 20))
    )
    
    return weapon