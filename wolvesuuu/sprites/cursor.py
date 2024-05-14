import pygame

class Cursor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        self.image = pygame.image.load("assets/images/cursor.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 40))
        
        self.rect = self.image.get_rect()
        
    def update(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.rect.center = (mouse_x, mouse_y)
        
    def get_group(self):
        return pygame.sprite.GroupSingle(self)