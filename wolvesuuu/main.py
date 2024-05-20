# Change directory to the directory of main.py
import os
BASE_DIR = os.path.dirname(__file__)
os.chdir(BASE_DIR)

# Initialize pygame
import pygame
pygame.init()

# Secondary imports
import sys, pygame_menu, pygame_menu.themes
from pygame_menu.widgets.widget.dropselect import DropSelect

# Local imports
from sprites import Cursor, Player
from levels import loadLevel, LEVEL_NAMES
from pygame import display, mouse, sprite, time, event, surfarray, image
from config import FPS, WINDOW_WIDTH, WINDOW_HEIGHT

# Setup
display.set_caption('Wolves UUU')
mouse.set_visible(False)
icon_image = image.load("assets/images/icon.png")
display.set_icon(icon_image)
screen = display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Menu
def start_local_game():
    index = level_selector.get_index()
    if index == -1: return
    
    level = level_selector.get_value()[0][0]
    
    global in_menu, background, terrain, player1, player2, current_player, current_player_id
    
    background, terrain = loadLevel(level)
    
    player1 = Player(next_player)
    player2 = Player(next_player)
    
    player1.is_playing = True    
    current_player_id = 1
    current_player = player1
    
    in_menu = False

menu = pygame_menu.Menu(
    title="Wolves UUU",
    width=WINDOW_WIDTH, 
    height=WINDOW_HEIGHT, 
    mouse_visible=False,
    theme=pygame_menu.themes.THEME_DARK
)
menu.add.image("assets/images/icon.png")
menu.add.button("Start Local Game", start_local_game)
level_selector:DropSelect = menu.add.dropselect(title="Map:", items=[ [level_name] for level_name in LEVEL_NAMES], placeholder="Select a Map", default=1)

# Variables
in_menu = True

# Functions
def next_player():
    # TODO: find more modular way to handle players (maybe more than 2)
    global current_player_id, current_player
    
    if current_player_id == 1:
        current_player.end_turn()
        
        current_player_id = 2
        current_player = player2
        player2.is_playing = True
    else:
        current_player.end_turn()
        
        current_player_id = 1
        current_player = player1
        player1.is_playing = True
        
        

# Sprites
cursor = Cursor().create_group()

# Main Loop
clock = time.Clock()
dt = 1000/FPS/1000

while True:
    events = event.get()
    mx, my = mouse.get_pos()

    for e in events:
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif not in_menu:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_q:
                    current_player.toggle_arsenal_pressed()
                elif e.key == pygame.K_SPACE:
                    current_player.shoot_pressed()
            elif e.type == pygame.KEYUP:
                if e.key == pygame.K_SPACE:
                    current_player.shoot_released()
            elif e.type == pygame.MOUSEBUTTONUP:
                current_player.mouse_clicked(mx, my, e.button)
            

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
        
        player1.update(dt=dt, terrain_alpha=surfarray.pixels_alpha(terrain))
        player2.update(dt=dt, terrain_alpha=surfarray.pixels_alpha(terrain))
        
        player1.draw(screen)
        player2.draw(screen)
        
        # for i, player in enumerate(players):
        #     character = player.characters[player.last_character_id]
        #     character_group = sprite.GroupSingle(character)
        #     arsenal = player.arsenal

        #     # Only update the active player
            
            # character_group.update(dt, surfarray.pixels_alpha(terrain))
        #     arsenal.group.update()
        #     character_group.draw(screen)
        #     if character.is_armed and i == turn_of_player:
        #         character.weapon.draw(screen)
        #         arsenal.group.draw(screen)
        #         if character.weapon_equipped:
        #             pygame.draw.circle(screen, (255, 0, 0), (character.weapon.sprite.rect.x+character.weapon.sprite.offset.x, character.weapon.sprite.rect.y + character.weapon.sprite.offset.y), 2)
                
            

            
            
            
            
        # pygame.draw.circle(screen, (255, 0, 0), (player1.characters[0].weapon.sprite.rect.x))
        # if player.characters[0].weapon_equipped:
        #     pygame.draw.circle(screen, (255, 0, 0), (player1.characters[0].weapon.sprite.rect.x+player1.characters[0].weapon.sprite.offset.x, player1.characters[0].weapon.sprite.rect.y + player1.characters[0].weapon.sprite.offset.y), 2)
        
        # draw.rect(screen, (255, 0, 0), weapon1.sprite.rect, 1)
        # draw.rect(screen, (255, 0, 0), local_player.sprite.rect, 1)

    cursor.update()
    cursor.draw(screen)
    
    

    display.update()
    dt = clock.tick(FPS)/1000
