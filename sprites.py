import arcade
from random import choice
from config import *

# =============== EXPLOSÕES ==================================================================
class Explosion(arcade.Sprite):
    def __init__(self, texture_list):
        super().__init__()
        self.current_texture = 0
        self.textures = texture_list

    def update(self):
        self.current_texture += 1
        if self.current_texture < len(self.textures):
            self.set_texture(self.current_texture)
        else:
            self.remove_from_sprite_lists()

# ============ ASTERÓIDES ====================================================================
class Asteroids(arcade.Sprite):
    def __init__(self,filename):
        super().__init__(filename)
        self.center_x = choice([15, WIDTH + 15])
        self.center_y = choice([15, HEIGHT + 15])
        self.change_x = choice([2,3,4])
        self.change_y = choice([2,3,4])
    
    def animate(self):
        if self.right >= WIDTH + 100 or self.left <= -100:
            self.change_x *= -1
        if self.top  >= HEIGHT + 100 or self.bottom <= -100:
            self.change_y *= -1  
        # era 30 ao invés de 100
# ============ TIROS =========================================================================
class Shoot(arcade.Sprite):
    def __init__(self, filename, player_angle,player_center_x, player_center_y):
        super().__init__(filename,scale=SCALE_SPRITE)
        self.player_angle = player_angle
        match (self.player_angle):
            case (0):
                self.center_x = player_center_x 
                self.center_y = player_center_y + DISTANCE_SHOOT_PLAYER
                self.angle = 90
                self.change_x = 0
                self.change_y = VELOCITY_SHOOT
            case (90):
                self.center_x = player_center_x - DISTANCE_SHOOT_PLAYER
                self.center_y = player_center_y 
                self.angle = 180
                self.change_x = -VELOCITY_SHOOT
                self.change_y = 0
            case (180):
                self.center_x = player_center_x 
                self.center_y = player_center_y - DISTANCE_SHOOT_PLAYER
                self.angle = 270
                self.change_x = 0
                self.change_y = -VELOCITY_SHOOT
            case (270):
                self.center_x = player_center_x + DISTANCE_SHOOT_PLAYER
                self.center_y = player_center_y 
                self.angle = 0
                self.change_x = VELOCITY_SHOOT
                self.change_y = 0
# =========== NAVE ===========================================================================
class Player(arcade.Sprite):
    def __init__(self, filename):
        super().__init__(filename,scale=SCALE_SPRITE)
        self.center_x = WIDTH / 2
        self.center_y = HEIGHT / 2

    def animate(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.top >= HEIGHT - 50:
            self.top = HEIGHT - 50
        if self.bottom <= 50:
            self.bottom = 50
        if self.left <= 50:
            self.left = 50 
        if self.right >= WIDTH - 50:
            self.right = WIDTH - 50       

    def key_press(self, key):  
        match (key):
            case (arcade.key.W):
                self.change_y = +VELOCITY_PLAYER
                self.angle = 0
            case (arcade.key.S):
                self.change_y = -VELOCITY_PLAYER
                self.angle = 180
            case (arcade.key.A):
                self.change_x = -VELOCITY_PLAYER
                self.angle = 90
            case (arcade.key.D):
                self.change_x = +VELOCITY_PLAYER
                self.angle = 270

    def key_release(self,key):
        if key == arcade.key.W or key == arcade.key.S:
            self.change_y = 0
        if key == arcade.key.A or key == arcade.key.D:
            self.change_x = 0