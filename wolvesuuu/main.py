# Change directory to the directory of main.py
import os
BASE_DIR = os.path.dirname(__file__)
os.chdir(BASE_DIR)

# Initialize pygame
import pygame
pygame.init()

import sys, pygame_menu
from sprites import Cursor, player
from levels import loadLevel
from pygame import display, mouse, sprite, time, event, draw, surfarray



from weapons.arsenal import Arsenal



# Setup display window
display.set_caption('Wolves UUU')
mouse.set_visible(False)

# Setup game variables
fps = 60
width = 1280
height = 720
screen = display.set_mode((width, height))
in_menu = True

# Define other variables
cursor = Cursor().create_group()

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
player1 = player.Player()
character1 = player1.characters[player1.lastCharacterId]
player1_group = sprite.GroupSingle(character1)
weapon1: sprite.GroupSingle = character1.weapon
arsenal1 = player1.arsenal

# Player 2
player2 = player.Player()
character2 = player2.characters[0]
player2_group = sprite.GroupSingle(character2)
weapon2: sprite.GroupSingle = character2.weapon
arsenal2 = player2.arsenal

players = [player1, player2]
turn_of_player = 0
players[turn_of_player].isPlaying = True

def switch_turn():
    global turn_of_player
    players[turn_of_player].isPlaying = False
    turn_of_player = (turn_of_player + 1) % len(players)
    players[turn_of_player].isPlaying = True

# Main Loop
clock = time.Clock()
dt = 1000/fps/1000



while True:
    events = event.get()
    mx, my = mouse.get_pos()
    
    active_player = players[turn_of_player]
    character = active_player.characters[active_player.lastCharacterId]
    character_group = sprite.GroupSingle(character)
    arsenal = active_player.arsenal

    for e in events:
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_TAB:
                switch_turn()
            if e.key == pygame.K_q:
                active_player.characters[active_player.lastCharacterId].toggle_armed()
        elif e.type == pygame.MOUSEBUTTONUP:
            if active_player.characters[active_player.lastCharacterId].is_armed:
                active_player.arsenal.handle_click(mx, my, e.button)
            

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
        
        for i, player in enumerate(players):
            character = player.characters[player.lastCharacterId]
            character_group = sprite.GroupSingle(character)
            arsenal = player.arsenal

            # Only update the active player
            
            character_group.update(dt, surfarray.pixels_alpha(terrain))
            arsenal.group.update()
            character_group.draw(screen)
            if character.is_armed and i == turn_of_player:
                character.weapon.draw(screen)
                arsenal.group.draw(screen)

            
            
            
            
        
        # pygame.draw.circle(screen, (255, 0, 0), (weapon1.sprite.rect.x+weapon1.sprite.offset.x, weapon1.sprite.rect.y + weapon1.sprite.offset.y), 2)
        
        # draw.rect(screen, (255, 0, 0), weapon1.sprite.rect, 1)
        # draw.rect(screen, (255, 0, 0), local_player.sprite.rect, 1)

    cursor.update()
    cursor.draw(screen)
    
    

    display.update()
    dt = clock.tick(fps)/1000
