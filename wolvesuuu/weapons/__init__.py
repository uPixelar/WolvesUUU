# weapons/__init__.py

import importlib
import glob
from sprites.weapon import WeaponSprite
from typing import Type, ClassVar



weapon_names = glob.glob("wep_*", root_dir="weapons/")

def import_weapon(weapon_name:str):
    _module = importlib.import_module(f"weapons.{weapon_name}")
    _class: Type["WeaponSprite"] = _module.Weapon
    _config: dict = _module.config
    
    return _class, _config

def load_weapon(weapon_name: str):
    """Loads the weapon as sprite.

    Args:
        weapon_name (str): Unique name of the weapon registered in game

    Returns:
        Weapon sprite
        """

    _class, _config = import_weapon(weapon_name)

    weapon = _class(
        weapon_name=weapon_name,
        handle_offset=_config.get("handle_offset", (5, 5)),
        rotation_offset=_config.get("rotation_offset", 0),
        surface_size=_config.get("surface_size", (40, 20)),
        weapon_cost=_config.get("weapon_cost", {}),
    )

    return weapon
