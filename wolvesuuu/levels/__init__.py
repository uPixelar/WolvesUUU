import os, glob
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
    
    background_surface = image.load(os.path.join(PATH, "background.jpg")).convert()
    background_surface = transform.scale(background_surface, (WINDOW_WIDTH, WINDOW_HEIGHT))
    
    terrain_surface = image.load(os.path.join(PATH, "terrain.png")).convert_alpha()
    terrain_surface = transform.scale(terrain_surface, (WINDOW_WIDTH, WINDOW_HEIGHT))
    
    return (background_surface, terrain_surface)
