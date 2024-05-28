from pygame import sprite, Vector2, Surface, draw, rect, display, image, transform, mixer, math as pmath
import threading
from config import WINDOW_WIDTH, WINDOW_HEIGHT
from game import game
from sprites.explosion import Explosion

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from sprites import Player, WeaponSprite, Character
    from typing import Callable

GRENADE_STEP = 4

sfx_blast = mixer.Sound("assets/audio/rocket_blast.wav")

class Grenade(sprite.Sprite):
    def __init__(self, weapon: "WeaponSprite", shooter: "Player", players: list["Player"], terrain: "Surface", callback: "Callable[[], None]", damage, charge: float = 0.1):
        super().__init__()

        self.weapon = weapon
        self.shooter = shooter
        self.players = players
        self.terrain = terrain
        self.callback = callback
        self.damage = damage
        self.charge = charge

        self.speed = pmath.lerp(3, 6, charge)
        self.pos = Vector2(self.weapon.rect.center)
        self.angle = -self.shooter.current_character.get_shooting_angle()
        self.moving_angle = self.angle
        self.moving_vector = Vector2(self.speed, 0)
        self.moving_vector.rotate_ip(self.angle)
        self.range = 30

        self.image = weapon.image.copy()
        self.image_org = self.image.copy()
        self.rect = self.image.get_rect(center=self.pos)
        
        self.width, self.height = self.image.get_size()

        shooter.projectiles.add(self)
        
        threading.Timer(5, self.blast).start()

    def apply_physics(self):
        # BUG: Grenade rotates too much mid air
        
        # gravity
        self.moving_vector.y += 0.05

        # air drag
        self.moving_vector.x += min(-self.moving_vector.x, 0.01) if self.moving_vector.x < 0 else max(-self.moving_vector.x, -0.01)

        angle = 160/(self.speed*self.speed) * (0.1 if abs(self.moving_angle) < 90 else -0.1)
        self.moving_angle += angle
        if self.moving_angle > 180: self.moving_angle -= 360
        elif self.moving_angle < -180: self.moving_angle += 360
        self.moving_vector.rotate_ip(angle)
        
        
        self.angle += self.moving_vector.x
        self.image = transform.rotate(self.image_org, -self.angle)
        self.rect = self.image.get_rect(center=self.pos)
        self.width, self.height = self.image.get_size()

    def blast(self):
        if not self.alive(): return
        sfx_blast.play()
        Explosion(self.pos, self.shooter, self.range)
        self.kill()
        draw.circle(self.terrain, (0,0,0,0), (self.pos.x, self.pos.y), self.range)
        
        for player in self.players:
            for character in player.character_group.sprites():
                character:Character
                character.blast_damage(self.damage, self.pos, self.range)

        self.callback()
        
    def update(self):
        new_pos = self.pos+self.moving_vector

        # ScreenSafe check
        if new_pos.x < 0 or new_pos.x > WINDOW_WIDTH or new_pos.y < 0 or new_pos.y > WINDOW_HEIGHT:
            self.kill()
            self.callback()
            return
        
    
        self.apply_physics()
        self.collide_all()
        self.rect.center = self.pos

    def collide_up(self):
        # BUG: When player flies it doesn't fall back ???
        start_x = round(self.pos.x)
        end_x = start_x + self.width

        start_y = round(self.pos.y) - 1
        end_y = round(self.pos.y + self.moving_vector.y) - 1

        collision = None

        for y in range(start_y, end_y, -1):
            for x in range(start_x, end_x):
                if self.terrain.get_at((x, y))[3]:
                    collision = Vector2(x, y)
                    break
            if collision:
                break

        if collision:
            self.pos.y = collision.y + 1
            self.moving_vector.y = 0
        else:
            self.pos.y += self.moving_vector.y

    def collide_down(self):
        # TODO: Update start and end positions according to window size, so if its outside don't check
        start_x = round(self.pos.x)
        end_x = start_x + self.width

        start_y = round(self.pos.y) + self.height
        end_y = round(self.pos.y + self.moving_vector.y) + self.height

        if end_y > WINDOW_HEIGHT:
            self.kill()
            return

        collision = None

        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                if self.terrain.get_at((x, y))[3]:
                    collision = Vector2(x, y)
                    break
            if collision:
                break

        if collision:
            self.pos.y = collision.y - self.height
            self.moving_vector.y = 0
            self.grounded = True
        else:
            self.pos.y += self.moving_vector.y

    def collide_left(self):
        start_x = round(self.pos.x) - 1  # left
        end_x = round(self.pos.x + self.moving_vector.x) - 1  # right

        start_y = round(self.pos.y)  # up
        end_y = round(self.pos.y) + self.height  # bottom
        step_y = end_y - GRENADE_STEP  # mid

        if end_x < 0:
            self.kill()
            return

        collision = None

        for x in range(start_x, end_x, -1):
            for y in range(start_y, step_y):  # block
                if self.terrain.get_at((x, y))[3]:
                    collision = Vector2(x, y)
                    break
            if collision:
                break
            for y in range(step_y, end_y):  # climb
                if self.terrain.get_at((x, y))[3]:
                    start_y = y - self.height
                    self.pos.y = start_y
                    break

        if collision:
            self.pos.x = collision.x + 1
        else:
            self.pos.x += self.moving_vector.x

    def collide_right(self):
        start_x = round(self.pos.x) + self.width  # left
        end_x = round(self.pos.x + self.moving_vector.x) + self.width  # right

        start_y = round(self.pos.y)  # up
        end_y = round(self.pos.y) + self.height  # bottom
        step_y = end_y - GRENADE_STEP  # mid

        collision = None

        if end_x > WINDOW_WIDTH:
            self.kill()
            return

        for x in range(start_x, end_x):
            for y in range(start_y, step_y):  # block
                if self.terrain.get_at((x, y))[3]:
                    collision = Vector2(x, y)
                    break
            if collision:
                break
            for y in range(step_y, end_y):  # climb
                if self.terrain.get_at((x, y))[3]:
                    start_y = y - self.height
                    self.pos.y = start_y
                    break

        if collision:
            self.pos.x = collision.x - self.width
        else:
            self.pos.x += self.moving_vector.x

    def collide_all(self):
        # BUG: MUST CHECK SCREEN SPACE BEFORE TERRAIN COLLISION CHECK
        if self.moving_vector.x < 0:
            self.collide_left()

        elif self.moving_vector.x > 0:
            self.collide_right()

        if self.moving_vector.y < 0:
            self.collide_up()
            
        elif self.moving_vector.y > 0:
            self.collide_down()
