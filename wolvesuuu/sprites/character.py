from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import numpy
    from sprites.player import Player
    

import pygame
import math
from pygame import Vector2, mouse

from config import PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_STEP, PLAYER_SPEED, WINDOW_WIDTH, WINDOW_HEIGHT, PLAYER_JUMP

from weapons import load_weapon, WeaponSprite


class Character(pygame.sprite.Sprite):
    # TODO: include weapon and arsenal system in player to make connection
    # maybe exporting sprite.Group() with all arsenal, weapon, player in it??
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

        self.weapon = pygame.sprite.GroupSingle()  # weapon group
        self.weapon_equipped = False  # whether weapon is equipped or not

        self.is_armed = False  # armed mode: cannot move, can shoot, display arsenal

    def collide_up(self, terrain: "numpy.ndarray"):
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

    def collide_down(self, terrain: "numpy.ndarray"):
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

    def collide_left(self, terrain: "numpy.ndarray"):
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

    def collide_right(self, terrain: "numpy.ndarray"):
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

    def collide_all(self, terrain: "numpy.ndarray"):
        # TODO: Implement possible collisions for terrain
        if self.velocity.x < 0:
            self.collide_left(terrain)
            if self.facing:
                self.image = self.looking_left
                self.facing = False

        elif self.velocity.x > 0:
            self.collide_right(terrain)
            if not self.facing:
                self.image = self.looking_right
                self.facing = True

        if self.velocity.y < 0:
            self.collide_up(terrain)
        elif self.velocity.y > 0:
            self.collide_down(terrain)

    def equip(self, weapon_name: str):
        weapon = load_weapon(weapon_name)
        self.weapon.add(weapon)
        self.weapon_equipped = True

    def dequip(self):
        self.weapon.empty()
        self.weapon_equipped = False

    def update_weapon_angle(self):
        mx, my = mouse.get_pos()
        rads = math.atan2(-(my-self.rect.centery), (mx-self.rect.centerx))
        self.weapon.sprite.set_angle(math.degrees(rads))
        self.weapon.sprite.rect.topleft = self.rect.center - self.weapon.sprite.offset

    def toggle_armed(self):
        self.is_armed = not self.is_armed

    def update(self, dt: int, terrain: "numpy.ndarray"):
        if self.is_armed:  # armed mode
            # reset horizontal velocity
            self.velocity.x = 0
            
        else:  # disarmed mode
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                self.velocity.x = -PLAYER_SPEED
            elif keys[pygame.K_d]:
                self.velocity.x = PLAYER_SPEED
            else:
                self.velocity.x = 0

            # handle jump
            if self.grounded and keys[pygame.K_SPACE]:
                self.velocity.y = -PLAYER_JUMP
                self.grounded = False

            
        self.velocity.y += self.acceleration.y*dt
        self.collide_all(terrain)

        # update rect with custom position (float to int)
        self.rect.topleft = self.pos

        if self.is_armed and self.weapon_equipped:
            self.update_weapon_angle()
