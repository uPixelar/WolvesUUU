# Change directory to the directory of main.py
import os
BASE_DIR = os.path.dirname(__file__)
os.chdir(BASE_DIR)

# Initialize pygame
import pygame
pygame.init()

from config import FPS, WINDOW_WIDTH, WINDOW_HEIGHT
from pygame import display, mouse, sprite, time, event, surfarray, image, font, mixer
display.set_caption('Wolves UUU')
mouse.set_visible(False)
icon_image = image.load("assets/images/logo.jpg")
display.set_icon(icon_image)
screen = display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), )

# Secondary imports
import sys, pygame_menu, pygame_menu.themes
from pygame_menu.widgets.widget.dropselect import DropSelect

# Local imports
from sprites import Cursor, Player
from levels import loadLevel, LEVEL_NAMES

from game import game

# Setup

menu_music = mixer.Sound("assets/audio/mainmenu_background.mp3")
ingame_music = mixer.Sound("assets/audio/ingame_background.mp3")


# Menu
def start_local_game():
    index = level_selector.get_index()
    if index == -1: return
    
    level = level_selector.get_value()[0][0]
    
    global in_menu, background, terrain, player1, player2, current_player, current_player_id
    
    background, terrain, spawnpoints, starting_equipment = loadLevel(level)
    
    player_count = len(spawnpoints)
    
    player1 = Player(spawnpoints[0], starting_equipment, next_player)
    player2 = Player(spawnpoints[1], starting_equipment, next_player)
    
    player1.is_playing = True    
    current_player_id = 1
    current_player = player1
    
    in_menu = False
    menu_music.stop()
    ingame_music.play()

def quit_game():
    global should_quit
    should_quit = True

splash_font = font.Font("assets/fonts/Minecraftia-Regular.ttf", 40)

custom_theme = pygame_menu.themes.THEME_DARK.copy()
custom_theme.title = False

menu = pygame_menu.Menu(
    title="",
    width=WINDOW_WIDTH, 
    height=WINDOW_HEIGHT, 
    mouse_visible=False,
    theme=custom_theme
    
)

menu.add.image("assets/images/logo_transparent.png", scale=(0.3, 0.3), margin=(0, 200))


winner_label = menu.add.label("", font_name=splash_font, font_color=(255, 255, 0),font_shadow = True, font_shadow_color=(75, 75, 0), font_shadow_offset=4, font_shadow_position="position-southeast")
level_selector:DropSelect = menu.add.dropselect(title="Map:", items=[ [level_name] for level_name in LEVEL_NAMES], placeholder="Select a Map", default=0)
menu.add.button("Start Local Game", start_local_game)
menu.add.button("Quit Game", quit_game)

# Variables
in_menu = True
should_quit = False

# Functions
def next_player():
    # TODO: find more modular way to handle players (maybe more than 2)
    global current_player_id, current_player
    
    if current_player_id == 1:
        current_player.end_turn()
        
        current_player_id = 2
        current_player = player2
    else:
        current_player.end_turn()
        
        current_player_id = 1
        current_player = player1
    
    current_player.is_playing = True
    current_player.next_character()
        
        

# Sprites
cursor = Cursor().create_group()

# Main Loop
clock = time.Clock()
dt = 1000/FPS/1000

menu_music.play()

while True:
    if should_quit:
        pygame.quit()
        sys.exit()
    
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
                elif e.key == pygame.K_TAB:
                    current_player.next_player()
                elif e.key == pygame.K_ESCAPE:
                    game.winner_text = None
                    in_menu = True
                    ingame_music.stop()
                    menu_music.play()
            elif e.type == pygame.KEYUP:
                if e.key == pygame.K_SPACE:
                    current_player.shoot_released(current_player, [player1, player2], terrain)
            elif e.type == pygame.MOUSEBUTTONUP:
                current_player.mouse_clicked(mx, my, e.button)
            

    if in_menu:
        winner_label.set_title(game.winner_text)
        winner_label.translate(175, -250)
        winner_label.rotate(10)
        menu.update(events)
        menu.draw(screen)
        
    else:
        screen.blit(background, (0, 0))
        screen.blit(terrain, (0, 0))
        
        player1.update(dt=dt, terrain_alpha=surfarray.pixels_alpha(terrain))
        player2.update(dt=dt, terrain_alpha=surfarray.pixels_alpha(terrain))
        
        if len(player1.character_group.sprites()) == 0:
            game.winner_text = "Player 2 won!"
            in_menu = True
            ingame_music.stop()
            menu_music.play()
        elif len(player2.character_group.sprites()) == 0:
            game.winner_text = "Player 1 won!"
            in_menu = True
            ingame_music.stop()
            menu_music.play()
        
        player1.draw(screen)
        player2.draw(screen)
        
       

    cursor.update()
    cursor.draw(screen)
    
    

    display.update()
    dt = clock.tick(FPS)/1000
