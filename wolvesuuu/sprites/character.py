from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from sprites.player import Player
    

import pygame, math, numpy as np

from pygame import Vector2, mouse
from config import PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_STEP, PLAYER_SPEED, WINDOW_WIDTH, WINDOW_HEIGHT, PLAYER_JUMP




class Character(pygame.sprite.Sprite):
    def __init__(self, player:"Player"):
        # base lines
        super().__init__()
        self.player = player
        
        self.image = pygame.image.load("assets/images/wolf.png")
        self.image = pygame.transform.scale(
            self.image, (PLAYER_WIDTH, PLAYER_HEIGHT)
        )
        self.rect = self.image.get_rect(center=(640, 50))

        # flipped images
        self.looking_left = pygame.transform.flip(self.image, True, False)
        self.looking_right = self.image.copy()

        # actual position (float) (for better physics and movement)
        self.pos = Vector2(self.rect.topleft)
        self.acceleration = Vector2(0, 9.8)  # gravity acceleration
        self.velocity = Vector2(0, 0)

        self.jump = False
        self.facing = True  # False: facing left, True: facing right
        self.grounded = False  # ground check for jump etc.

    def collide_up(self, terrain: np.ndarray):
        # BUG: When player flies it doesn't fall back ???
        start_x = round(self.pos.x)
        end_x = start_x + PLAYER_WIDTH

        start_y = round(self.pos.y) - 1
        end_y = round(self.pos.y + self.velocity.y) - 1

        collision = None

        for y in range(start_y, end_y, -1):
            for x in range(start_x, end_x):
                if terrain[x][y]:
                    collision = Vector2(x, y)
                    break
            if collision:
                break

        if collision:
            self.pos.y = collision.y + 1
            self.velocity.y = 0
        else:
            self.pos.y += self.velocity.y

    def collide_down(self, terrain: np.ndarray):
        # TODO: Update start and end positions according to window size, so if its outside don't check
        start_x = round(self.pos.x)
        end_x = start_x + PLAYER_WIDTH

        start_y = round(self.pos.y) + PLAYER_HEIGHT
        end_y = round(self.pos.y + self.velocity.y) + PLAYER_HEIGHT

        collision = None

        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                if terrain[x][y]:
                    collision = Vector2(x, y)
                    break
            if collision:
                break

        if collision:
            self.pos.y = collision.y - PLAYER_HEIGHT
            self.velocity.y = 0
            self.grounded = True
        else:
            self.pos.y += self.velocity.y

    def collide_left(self, terrain: np.ndarray):
        start_x = round(self.pos.x) - 1  # left
        end_x = round(self.pos.x + self.velocity.x) - 1  # right

        start_y = round(self.pos.y)  # up
        end_y = round(self.pos.y) + PLAYER_HEIGHT  # bottom
        step_y = end_y - PLAYER_STEP  # mid

        collision = None

        for x in range(start_x, end_x, -1):
            for y in range(start_y, step_y):  # block
                if terrain[x][y]:
                    collision = Vector2(x, y)
                    break
            if collision:
                break
            for y in range(step_y, end_y):  # climb
                if terrain[x][y]:
                    start_y = y - PLAYER_HEIGHT
                    self.pos.y = start_y
                    break

        if collision:
            self.pos.x = collision.x + 1
        else:
            self.pos.x += self.velocity.x

    def collide_right(self, terrain: np.ndarray):
        start_x = round(self.pos.x) + PLAYER_WIDTH  # left
        end_x = round(self.pos.x + self.velocity.x) + PLAYER_WIDTH  # right

        start_y = round(self.pos.y)  # up
        end_y = round(self.pos.y) + PLAYER_HEIGHT  # bottom
        step_y = end_y - PLAYER_STEP  # mid

        collision = None

        for x in range(start_x, end_x):
            for y in range(start_y, step_y):  # block
                if terrain[x][y]:
                    collision = Vector2(x, y)
                    break
            if collision:
                break
            for y in range(step_y, end_y):  # climb
                if terrain[x][y]:
                    start_y = y - PLAYER_HEIGHT
                    self.pos.y = start_y
                    break

        if collision:
            self.pos.x = collision.x - PLAYER_WIDTH
        else:
            self.pos.x += self.velocity.x

    def collide_all(self, terrain: np.ndarray):
        if self.velocity.x < 0:
            self.collide_left(terrain)
            self.set_facing(False)

        elif self.velocity.x > 0:
            self.collide_right(terrain)
            self.set_facing(True)

        if self.velocity.y < 0:
            self.collide_up(terrain)
        elif self.velocity.y > 0:
            self.collide_down(terrain)
            
    def set_facing(self, facing:bool):
        if self.facing != facing:
            self.facing = facing
            self.image = self.looking_right if facing else self.looking_left

    def get_shooting_angle(self):
        mx, my = mouse.get_pos()
        # TODO: calculate between weapon handle pos and mouse pos
        rads = math.atan2(self.rect.centery-my, mx-self.rect.centerx)
        deg = math.degrees(rads)
        return deg

    def handle_movement_keys(self, keys:pygame.key.ScancodeWrapper):
        if keys[pygame.K_a]:
            self.velocity.x = -PLAYER_SPEED
        elif keys[pygame.K_d]:
            self.velocity.x = PLAYER_SPEED
        else:
            self.velocity.x = 0
            
        # handle jump
        if self.grounded and keys[pygame.K_w]:
            self.velocity.y = -PLAYER_JUMP
            self.grounded = False
    
    def update(self, dt: int, terrain: np.ndarray):         
        self.velocity.y += self.acceleration.y*dt
        self.collide_all(terrain)

        # update rect with custom position (float to int)
        self.rect.topleft = self.pos