from typing import Literal, TYPE_CHECKING
if TYPE_CHECKING:
    from sprites.player import Player
    from pygame import Surface

import pygame, math, numpy as np, random

from pygame import Vector2, mouse, math as pmath
from config import PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_STEP, PLAYER_SPEED, WINDOW_WIDTH, WINDOW_HEIGHT, PLAYER_JUMP, PLYOFF_HEAD, PLYOFF_BODY, PLYOFF_LEGS, PLAYER_CRIT_CHANCE
from sprites.damagetext import DamageText


class Character(pygame.sprite.Sprite):
    def __init__(self, player:"Player", spawn_point:list[int, int]):
        # base lines
        super().__init__()
        self.player = player
        
        self.image = pygame.image.load("assets/images/wolf.png")
        self.image = pygame.transform.scale(
            self.image, (PLAYER_WIDTH, PLAYER_HEIGHT)
        )
        self.rect = self.image.get_rect(center=(spawn_point[0], spawn_point[1]))

        # flipped images
        self.looking_left = pygame.transform.flip(self.image, True, False)
        self.looking_right = self.image.copy()

        # actual position (float) (for better physics and movement)
        self.pos = Vector2(self.rect.topleft)
        self.acceleration = Vector2(0, 9.8)  # gravity acceleration
        self.velocity = Vector2(0, 0)
        self.health = 100

        self.jump = False
        self.facing = True  # False: facing left, True: facing right
        self.grounded = False  # ground check for jump etc.

    def damage(self, damage, type:Literal["critical", "normal"]="normal"):
        self.player.visuals.add(DamageText(Vector2(self.rect.centerx, self.rect.top - 10), damage, type))
        self.health = pmath.clamp(self.health - damage, 0, 100)
        if self.health == 0:
            self.kill()
            
    def bullet_damage(self, damage, bullet_pos:"Vector2"):
        bullet_offset = abs(self.rect.top-bullet_pos.y)
        if bullet_offset < PLYOFF_BODY: # HEADSHOT
            if random.random() < PLAYER_CRIT_CHANCE:
                self.damage(damage * 1.35, "critical")
            else:
                self.damage(damage)
        elif bullet_offset < PLYOFF_LEGS: # BODYSHOT
            self.damage(damage * 0.65)
        else: # LEGSHOT
            self.damage(damage * 0.35)
            
    def blast_damage(self, damage:float, blast_pos:"Vector2", radius:float):
        pos = Vector2(self.rect.center)
        dist = math.hypot(pos.distance_to(blast_pos))
        
        critical_radius = radius * 0.3
        critical_damage = damage * 1.35
        
        soft_radius = radius + radius * 2
        soft_damage = damage * 0.5
        
        player_radius = (PLAYER_HEIGHT+PLAYER_WIDTH) / 2
        
        if dist < critical_radius: # in critical area
            self.damage(critical_damage, "critical")
        elif dist < radius: # in blast area
            area = radius - critical_radius
            drange = damage-soft_damage
            actd = dist - critical_radius
            ratio = actd / area
            ndmg = ratio*drange
            self.damage(damage-ndmg)
        else:
            actd = dist - radius - player_radius
            ratio = actd / (soft_radius - radius)
            ndmg = ratio * soft_damage
            dmg = damage-ndmg
            if dmg > 1:
                self.damage(dmg)
            
            
        
        
        

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
        
        if end_y > WINDOW_HEIGHT:
            self.kill()
            return 
        
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