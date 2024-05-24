import os, glob, importlib
from pygame import image, transform
from config import WINDOW_WIDTH, WINDOW_HEIGHT
# https://code.visualstudio.com/docs/editor/glob-patterns
# remove files starting with __
LEVEL_NAMES = glob.glob("[!__]*", root_dir="levels/")

def loadLevel(level_name: str):
    """Loads the level images into surfaces.

    Args:
        level_name (str): Unique name of the level registered in game

    Returns:
        tuple(Surface, Surface):(<background surface>, <terrain surface>) 
        """

    PATH = os.path.join("levels", level_name)
    
    _module = importlib.import_module(f"levels.{level_name}")
    spawnpoints: list[list[list[int, int]]] = _module.spawnpoints
    
    background_surface = image.load(os.path.join(PATH, "background.jpg")).convert()
    terrain_surface = image.load(os.path.join(PATH, "terrain.png")).convert_alpha()
    
    ratio = WINDOW_WIDTH / background_surface.get_width()
   
    background_surface = transform.scale_by(background_surface, ratio)
    terrain_surface = transform.scale_by(terrain_surface, ratio)
    
    for player in spawnpoints:
        for character in player:
            character[0] = int(character[0] * ratio)
            character[1] = int(character[1] * ratio)
    
    return (background_surface, terrain_surface, spawnpoints)
