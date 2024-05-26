# Change directory to the directory of main.py
import os
BASE_DIR = os.path.dirname(__file__)
os.chdir(BASE_DIR)

# Initialize pygame
import pygame
pygame.init()

from config import FPS, WINDOW_WIDTH, WINDOW_HEIGHT
from pygame import display, mouse, sprite, time, event, surfarray, image, font, mixer, math as pmath
display.set_caption('Wolves UUU')
mouse.set_visible(False)
icon_image = image.load("assets/images/logo.jpg")
display.set_icon(icon_image)
screen = display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), )

# Secondary imports
import sys, pygame_menu, pygame_menu.themes, random
from pygame_menu.widgets.widget.dropselect import DropSelect

# Local imports
from sprites import Cursor, Player
from levels import loadLevel, LEVEL_NAMES
from utils.repeatingtimer import RepeatingTimer

from game import game

# Setup

menu_music = mixer.Sound("assets/audio/mainmenu_background.mp3") if random.random() > 0.25 else mixer.Sound("assets/audio/mainmenu_background_easter.ogg")
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
    ingame_music.play().set_volume(game.vol_overall * game.vol_ingame_music)

def open_settings():
    global in_settings
    in_settings = True

def quit_game():
    global should_quit
    should_quit = True

splash_font = font.Font("assets/fonts/Minecraftia-Regular.ttf", 30)

custom_theme = pygame_menu.themes.THEME_DARK.copy()
custom_theme.title = False
custom_theme.background_color = (170, 170, 170)
custom_theme.selection_color = (60, 60, 60)
custom_theme.widget_font_color = (60, 60, 60)

menu = pygame_menu.Menu(
    title="",
    width=WINDOW_WIDTH, 
    height=WINDOW_HEIGHT, 
    mouse_visible=False,
    theme=custom_theme
)

menu.add.image("assets/images/logo_transparent.png", scale=(0.3, 0.3), margin=(0, 100))


winner_label = menu.add.label("", font_name=splash_font, font_color=(255, 255, 0),font_shadow = True, font_shadow_color=(75, 75, 0), font_shadow_offset=4, font_shadow_position="position-southeast", float=True)
level_selector:DropSelect = menu.add.dropselect(title="Map:", items=[ [level_name] for level_name in LEVEL_NAMES], placeholder="Select a Map", default=0, border_width = 2, border_color = (0, 0, 0, 40))
menu.add.button("Start Local Game", start_local_game, border_width = 2, border_color = (0, 0, 0, 40))
menu.add.button("Settings", open_settings, border_width = 2, border_color = (0, 0, 0, 40))
menu.add.button("Quit Game", quit_game, border_width = 2, border_color = (0, 0, 0, 40))

# Settings Menu
def return_to_menu():
    global in_menu, in_settings
    if not in_menu:
        ingame_music.stop()
        menu_music.play().set_volume(game.vol_overall * game.vol_menu_music)
        
    game.resplash()
    in_menu = True
    in_settings = False
    
    
def back_to_game():
    global in_settings
    in_settings = False

def slider_overall(val):
    game.vol_overall = val
    update_volumes()

def slider_sound_effects(val):
    game.vol_sound_effects = val
    update_volumes()

def slider_menu_muisc(val):
    game.vol_menu_music = val
    update_volumes()

def slider_ingame_music(val):
    game.vol_ingame_music = val
    update_volumes()

def update_volumes():
    menu_music.set_volume(game.vol_overall * game.vol_menu_music)
    ingame_music.set_volume(game.vol_overall * game.vol_ingame_music)

settings = pygame_menu.Menu(
    title="",
    width=WINDOW_WIDTH, 
    height=WINDOW_HEIGHT, 
    mouse_visible=False,
    theme=custom_theme
)


settings.add.label("Audio")
settings.add.range_slider("Overall", 1, (0, 1), 0.001, onchange=slider_overall, range_text_value_enabled = False)
settings.add.range_slider("Sound Effects", 1, (0, 1), 0.001, onchange=slider_sound_effects, range_text_value_enabled = False)
settings.add.range_slider("Mainmenu Music", 0.5, (0, 1), 0.001, onchange=slider_menu_muisc, range_text_value_enabled = False)
settings.add.range_slider("Ingame Music", 0.5, (0, 1), 0.001, onchange=slider_ingame_music, range_text_value_enabled = False, margin=(0, 40))

backtogame = settings.add.button("Back to fight!", back_to_game, border_width = 2, border_color = (0, 0, 0, 40))
settings.add.button("Return to Mainmenu", return_to_menu, border_width = 2, border_color = (0, 0, 0, 40))


# Variables
in_menu = True
in_settings = False
should_quit = False

# Animation
step = 0
def animate():
    if in_menu or in_settings or not current_player.current_character.grounded or current_player.current_character.velocity.x == 0: return
    
    global step
    if step == 0:
        footstep_1.play().set_volume(game.vol_overall * game.vol_sound_effects)
        step = 1
    else:
        footstep_2.play().set_volume(game.vol_overall * game.vol_sound_effects)
        step = 0
    current_player.current_character.step()
        
footstep_1 = mixer.Sound("assets/audio/footstep_1.wav")
footstep_2 = mixer.Sound("assets/audio/footstep_2.wav")

animation_timer = RepeatingTimer(0.4, animate)
animation_timer.start()

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

menu_music.play().set_volume(game.vol_overall * game.vol_menu_music)

while True:
    if should_quit:
        animation_timer.cancel()
        pygame.quit()
        sys.exit()
    
    events = event.get()
    mx, my = mouse.get_pos()

    for e in events:
        if e.type == pygame.QUIT:
            animation_timer.cancel()
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
                    if in_settings:
                        in_settings = False
                    else:
                        in_settings = True                            
            elif e.type == pygame.KEYUP:
                if e.key == pygame.K_SPACE:
                    current_player.shoot_released(current_player, [player1, player2], terrain)
            elif e.type == pygame.MOUSEBUTTONUP:
                current_player.mouse_clicked(mx, my, e.button)
        else:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    if in_settings:
                        in_settings = False
                
            

    if in_settings:
        if in_menu:
            backtogame.hide()
        else:
            backtogame.show()
        settings.update(events)
        settings.draw(screen)
    elif in_menu:
        winner_label.set_title(game.winner_text)
        winner_label.translate(155, 255)
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
            menu_music.play().set_volume(game.vol_overall * game.vol_menu_music)
        elif len(player2.character_group.sprites()) == 0:
            game.winner_text = "Player 1 won!"
            in_menu = True
            ingame_music.stop()
            menu_music.play().set_volume(game.vol_overall * game.vol_menu_music)
        
        player1.draw(screen)
        player2.draw(screen)
        
       

    cursor.update()
    cursor.draw(screen)
    
    

    display.update()
    dt = clock.tick(FPS)/1000
