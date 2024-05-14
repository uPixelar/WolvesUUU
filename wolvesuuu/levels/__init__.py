import os
import pygame


def loadLevel(level_name: str):
    """Loads the level images into surfaces.

    Args:
        level_name (str): Unique name of the level registered in game

    Returns:
        tuple(Surface, Surface):(<background surface>, <terrain surface>) 
        """

    PATH = os.path.join("levels", level_name)
    
    WIDTH, HEIGHT = pygame.display.get_window_size()
    
    background_surface = pygame.image.load(os.path.join(PATH, "background.jpg")).convert()
    background_surface = pygame.transform.scale(background_surface, (WIDTH, HEIGHT))
    
    terrain_surface = pygame.image.load(os.path.join(PATH, "terrain.png")).convert_alpha()
    terrain_surface = pygame.transform.scale(terrain_surface, (WIDTH, HEIGHT))
    
    return (background_surface, terrain_surface)
