from typing import Literal, TYPE_CHECKING
if TYPE_CHECKING:
    from sprites.player import Player
    from pygame import Surface

import pygame, math, numpy as np, random, threading

from pygame import Vector2, mouse, math as pmath, mixer, time as ptime
from config import PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_STEP, PLAYER_SPEED, WINDOW_WIDTH, PLAYER_MAX_SPEED, WINDOW_HEIGHT, PLAYER_JUMP, PLYOFF_HEAD, PLYOFF_BODY, PLYOFF_LEGS, PLAYER_CRIT_CHANCE
from sprites.damagetext import DamageText
from sprites.tombstone import Tombstone

from game import game

flesh_impact_head = mixer.Sound("assets/audio/flesh_impact_head.wav")
flesh_impact_1 = mixer.Sound("assets/audio/flesh_impact_1.wav")
flesh_impact_2 = mixer.Sound("assets/audio/flesh_impact_2.wav")

jump = mixer.Sound("assets/audio/jump.wav")

class Character(pygame.sprite.Sprite):
    # BUG: IDK how but sometimes same player plays the next turn after killing next enemy character
    def __init__(self, player:"Player", spawn_point:list[int, int]):
        # base lines
        super().__init__()
        self.player = player
        self.footsteps = [pygame.transform.scale(pygame.image.load("assets/images/wolf1.png"), (PLAYER_WIDTH, PLAYER_HEIGHT)), pygame.transform.scale(pygame.image.load("assets/images/wolf2.png"), (PLAYER_WIDTH, PLAYER_HEIGHT))]
        
        self.image_org = self.footsteps[1]
        self.image = self.footsteps[1]
        
        
        self.rect = self.image.get_rect(center=(spawn_point[0], spawn_point[1]))

        # flipped images
        self.looking_left = pygame.transform.flip(self.image, True, False)
        self.looking_right = self.image.copy()

        # actual position (float) (for better physics and movement)
        self.pos = Vector2(self.rect.topleft)
        self.acceleration = Vector2(0, 9.8)  # gravity acceleration
        self.velocity = Vector2(0, 0)
        self.health = 100
        
        self.footstep = 0

        self.jump = False
        self.facing = True  # False: facing left, True: facing right
        self.grounded = False  # ground check for jump etc.

    def damage(self, damage, type:Literal["critical", "normal"]="normal"):
        self.player.visuals.add(DamageText(Vector2(self.rect.centerx, self.rect.top - 10), damage, type))
        self.health = pmath.clamp(self.health - damage, 0, 100)
        if self.health == 0:
            Tombstone(self)
            self.kill()
    
    def step(self):
        self.image_org = self.footsteps[self.footstep]
        self.image = pygame.transform.flip(self.image_org, self.facing, False)
        
        self.footstep += 1
        if self.footstep == len(self.footsteps):
            self.footstep = 0

    
    def bullet_damage(self, damage, bullet_pos:"Vector2"):
        bullet_offset = abs(self.rect.top-bullet_pos.y)
        if bullet_offset < PLYOFF_BODY: # HEADSHOT
            if random.random() < PLAYER_CRIT_CHANCE:
                self.damage(damage * 1.35, "critical")
                flesh_impact_head.play().set_volume(game.vol_overall * game.vol_sound_effects)
            else:
                self.damage(damage)
                (flesh_impact_1 if random.random() < 0.5 else flesh_impact_2).play().set_volume(game.vol_overall * game.vol_sound_effects)
        elif bullet_offset < PLYOFF_LEGS: # BODYSHOT
            self.damage(damage * 0.65)
            (flesh_impact_1 if random.random() < 0.5 else flesh_impact_2).play().set_volume(game.vol_overall * game.vol_sound_effects)
        else: # LEGSHOT
            self.damage(damage * 0.35)
            (flesh_impact_1 if random.random() < 0.5 else flesh_impact_2).play().set_volume(game.vol_overall * game.vol_sound_effects)
            
            
    def blast_damage(self, damage:float, blast_pos:"Vector2", radius:float):
        pos = Vector2(self.rect.center)
        dist = math.hypot(pos.distance_to(blast_pos))
        
        critical_radius = radius * 0.3
        critical_damage = damage * 1.35
        
        soft_radius = radius + radius * 2
        soft_damage = damage * 0.5
        
        player_radius = (PLAYER_HEIGHT+PLAYER_WIDTH) / 2
        
        if dist < critical_radius: # in critical area
            dmg = critical_damage
            self.damage(critical_damage, "critical")
        elif dist < radius: # in blast area
            area = radius - critical_radius
            actd = dist - critical_radius
            ratio = actd / area
            dmg = pmath.lerp(30, 20, ratio)
            self.damage(dmg)
        elif dist<soft_radius+player_radius:
            actd = dist - radius
            area = soft_radius + player_radius - radius
            ratio = actd / area
            dmg = pmath.lerp(20, 0, ratio)
            self.damage(dmg)
        else: return
            
        vec = pos - blast_pos
        vec.normalize_ip()
        vec *= pmath.lerp(6, 0, dist/(soft_radius + player_radius))
        self.velocity += vec
            
        
        
        

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
        # BUG: MUST CHECK SCREEN SPACE BEFORE TERRAIN COLLISION CHECK
        if self.velocity.x < 0:
            self.collide_left(terrain)
            self.set_facing(True)

        elif self.velocity.x > 0:
            self.collide_right(terrain)
            self.set_facing(False)

        if self.velocity.y < 0:
            self.collide_up(terrain)
        elif self.velocity.y > 0:
            self.collide_down(terrain)
            
    def set_facing(self, facing:bool):
        if self.facing != facing:
            self.facing = facing
            self.image = pygame.transform.flip(self.image_org, self.facing, False)


    def get_shooting_angle(self):
        mx, my = mouse.get_pos()
        # TODO: calculate between weapon handle pos and mouse pos
        rads = math.atan2(self.rect.centery-my, mx-self.rect.centerx)
        deg = math.degrees(rads)
        return deg

    def handle_movement_keys(self, dt, keys:pygame.key.ScancodeWrapper):
        if keys[pygame.K_a]:
            self.acceleration.x = -PLAYER_SPEED
        elif keys[pygame.K_d]:
            self.acceleration.x = PLAYER_SPEED
        else:
           self.acceleration.x = 0
            
        # handle jump
        if self.grounded and keys[pygame.K_w]:
            jump.play().set_volume(game.vol_overall * game.vol_sound_effects)
            self.velocity.y = -PLAYER_JUMP
            self.grounded = False
    
    def update(self, dt: int, terrain: np.ndarray):
        self.velocity.x += -min(0.1, self.velocity.x) if self.velocity.x > 0 else -max(-0.1, self.velocity.x)
        increase = self.acceleration * dt
        if increase.x > 0:
            self.velocity.x += min(increase.x, (PLAYER_MAX_SPEED - self.velocity.x))
        elif increase.x < 0:
            self.velocity.x += max(increase.x, (-PLAYER_MAX_SPEED - self.velocity.x))
        self.velocity.y += increase.y
        self.collide_all(terrain)

        # update rect with custom position (float to int)
        self.rect.topleft = self.pos        