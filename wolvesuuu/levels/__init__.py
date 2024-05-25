import os
import glob
import importlib
from pygame import image, transform
from config import WINDOW_WIDTH, WINDOW_HEIGHT
# https://code.visualstudio.com/docs/editor/glob-patterns
# remove files starting with __
LEVEL_NAMES = glob.glob("[!__]*", root_dir="levels/")

default_items = {
    "weapons": {
        "wep_ak47": 3,
        "wep_rpg7": 1,
        "wep_musket": 10
    },
    "items": {
        "item_plank": 100,
        "item_metal": 100,
        "item_usd": 5000
    }
}


def loadLevel(level_name: str):
    """Loads the level images into surfaces.

    Args:
        level_name (str): Unique name of the level registered in game

    Returns:
        tuple(Surface, Surface):(<background surface>, <terrain surface>) 
        """

    PATH = os.path.join("levels", level_name)

    _module = importlib.import_module(f"levels.{level_name}")
    _spawnpoints: list[list[list[int, int]]] = _module.spawnpoints
    _starting_items: dict[str,
                          int] = _module.starting_items if hasattr(_module, "starting_items") else default_items

    background_surface = image.load(
        os.path.join(PATH, "background.jpg")).convert()
    terrain_surface = image.load(os.path.join(
        PATH, "terrain.png")).convert_alpha()

    ratio = WINDOW_WIDTH / background_surface.get_width()

    background_surface = transform.scale_by(background_surface, ratio)
    terrain_surface = transform.scale_by(terrain_surface, ratio)

    spawnpoints: list[list[list[int, int]]] = []
    for _player in range(len(_spawnpoints)):
        player = _spawnpoints[_player]
        spawnpoints.append([])
        for _character in range(len(player)):
            character = player[_character]
            spawnpoints[_player].append([])

            spawnpoints[_player][_character] = [
                int(character[0] * ratio), int(character[1] * ratio)]

    return (background_surface, terrain_surface, spawnpoints, _starting_items)
