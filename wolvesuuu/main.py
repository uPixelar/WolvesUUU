import pygame
import os, math
import sys
import pygame_menu
from sprites import Cursor, Player
from levels import loadLevel
from pygame import display, mouse, sprite, time, event, draw, surfarray


# Change directory to the directory of main.py
BASE_DIR = os.path.dirname(__file__)
os.chdir(BASE_DIR)

# Initialize pygame
pygame.init()

# Setup display window
display.set_caption('Wolves UUU')
mouse.set_visible(False)

# Setup game variables
fps = 144
width = 1280
height = 720
screen = display.set_mode((width, height))
in_menu = True

# Define other variables
cursor = Cursor().get_group()

# Menu
def start_local_game():
    global in_menu
    in_menu = False


menu = pygame_menu.Menu("Wolves UUU", width, height, mouse_visible=False)
menu.add.button("Start Local Game", start_local_game)

# Game
level = "developer"
background, terrain = loadLevel(level)
# terrain_array = surfarray.pixels_alpha(terrain)

# Player 1
player1 = Player()
player1_group = sprite.GroupSingle(player1)
weapon1: sprite.GroupSingle = player1.weapon


# Main Loop
clock = time.Clock()
dt = 1000/fps/1000



while True:
    events = event.get()
    for e in events:
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            

    if in_menu:
        menu.update(events)
        menu.draw(screen)
    else:
        btns = pygame.mouse.get_pressed()
        if btns[0]:
            x, y = pygame.mouse.get_pos()
            pygame.draw.circle(terrain, (0, 0, 0, 0), (x,y), 10)
            
        screen.blit(background, (0, 0))
        screen.blit(terrain, (0, 0))
        
        player1_group.update(dt, surfarray.pixels_alpha(terrain))
        player1_group.draw(screen)
        if player1.weapon_equipped:
            weapon1.draw(screen)
        # pygame.draw.circle(screen, (255, 0, 0), (weapon1.sprite.rect.x+weapon1.sprite.offset.x, weapon1.sprite.rect.y + weapon1.sprite.offset.y), 5)
        
        # draw.rect(screen, (255, 0, 0), weapon1.sprite.rect, 1)
        # draw.rect(screen, (255, 0, 0), local_player.sprite.rect, 1)

    cursor.update()
    cursor.draw(screen)

    display.update()
    dt = clock.tick(fps)/1000
