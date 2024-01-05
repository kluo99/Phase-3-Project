import pygame 
from settings import *
from os import path
from support import *


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)

        self.import_assets()
        self.status = 'r_idle'
        self.frame_index = 0


        #general setup
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)

        self.direction = pygame.math.Vector2(0, 0)
        self.pos = pygame.math.Vector2(self.rect.center)
        # self.pos = pos

        self.hitbox_radius = 50  # Adjust the radius based on your game
        # self.hitbox = pygame.Rect(0, 0, self.hitbox_radius * 2, self.hitbox_radius * 2)
        self.hitbox = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height)

        self.swing_hitbox = pygame.Rect(0, 0, 0, 0)

        #movement attributes
        self.direction = pygame.math.Vector2(0, 0)
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 570

        self.health = 5

        self.scale_factor = 3



    def import_assets(self):
        self.animations = {'up': [], 'down': [], 'r': [], 'l':[], 'down_idle': [], 'up_idle': [], 'r_idle': [], 'l_idle': [], 'l_swing': [], 'r_swing': [], 'up_swing': [], 'down_swing':[], 'dead': []}    

        for animation in self.animations.keys():
            full_path = 'img/' + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self, dt):
        self.frame_index += 10 * dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0

        original_frame = self.animations[self.status][int(self.frame_index)]
        self.image = pygame.transform.scale(original_frame,
                                            (int(original_frame.get_width() * self.scale_factor),
                                             int(original_frame.get_height() * self.scale_factor)))
        
    
    def animatedeath(self, dt):
        self.frame_index += 10 * dt

        # Check if the animation has reached the end
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = len(self.animations[self.status]) - 1  # Set to the last frame

        original_frame = self.animations[self.status][int(self.frame_index)]
        self.image = pygame.transform.scale(original_frame,
                                        (int(original_frame.get_width() * self.scale_factor),
                                         int(original_frame.get_height() * self.scale_factor)))

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.direction.y = -1
            self.status = 'up'
        elif keys[pygame.K_s]:
            self.direction.y = 1
            self.status = 'down'
        else:
            self.direction.y = 0

        if keys[pygame.K_d]:
            self.direction.x = 1
            self.status = 'r'
        elif keys[pygame.K_a]:
            self.direction.x = -1
            self.status = 'l'
        else:
            self.direction.x = 0

        
        
        if keys[pygame.K_w] and keys[pygame.K_SPACE]:
            self.direction.y = -1
            self.status = 'up_swing'
        elif keys[pygame.K_s] and keys[pygame.K_SPACE]:
            self.direction.y = 1
            self.status = 'down_swing'
        elif keys[pygame.K_d] and keys[pygame.K_SPACE]:
            self.direction.x = 1
            self.status = 'r_swing'
        elif keys[pygame.K_a] and keys[pygame.K_SPACE]:
            self.direction.x = -1
            self.status = 'l_swing'
        

    def get_status(self):
        #if player is not moving put idle status
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] and self.direction.magnitude() == 0:
            self.status = 'r_swing'
        elif keys[pygame.K_SPACE] and self.direction.magnitude() == 0 and self.status == 'l_idle':
            self.status = 'l_swing'
        elif keys[pygame.K_SPACE] and self.direction.magnitude() == 0 and self.status == 'up_idle':
            self.status = 'up_swing'
        elif keys[pygame.K_SPACE] and self.direction.magnitude() == 0 and self.status == 'down_idle':
            self.status = 'down_swing'
        elif keys[pygame.K_SPACE] and self.direction.magnitude() == 0 and self.status == 'r_idle':
            self.status = 'r_swing'
        elif keys[pygame.K_SPACE] and self.direction.magnitude() == 0 and self.status == 'up_idle':
            self.status = 'up_swing'
        elif self.direction.magnitude() == 0:
            self.status = self.status.split('_')[0] + '_idle'
        



    def move(self, dt):

        #normalizing vector
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()
        
        new_pos = self.pos + self.direction * self.speed * dt

        # Check for collisions with the boundaries of the map
        min_x = 0
        max_x = 3380 - self.rect.width 
        min_y = 0
        max_y = 1890 - self.rect.height  

        # Update the position only if it stays within the map boundaries
        if min_x <= new_pos.x <= max_x and min_y <= new_pos.y <= max_y:
            self.pos = new_pos
            self.rect.centerx = self.pos.x
            self.rect.centery = self.pos.y
    
    def update(self, dt):
        self.hitbox.topleft = self.rect.topleft
        if self.health <= 0:
            self.direction = pygame.math.Vector2(0, 0)
            self.status = 'dead'
            self.animatedeath(dt)
        else:
            self.input()
            self.move(dt)
            self.get_status()
            self.animate(dt)

