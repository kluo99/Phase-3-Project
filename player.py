import pygame 
from settings import *
from os import path
from support import *


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)

        self.import_assets()
        self.status = 'rl_swing'
        self.frame_index = 0

        #general setup
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center = pos)


        #movement attributes
        self.direction = pygame.math.Vector2(0, 0)
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 200

        self.scale_factor = 2



    def import_assets(self):
        self.animations = {'up': [], 'down': [], 'rl': [], 'idle_down': [], 'idle_up': [], 'idle_rl': [], 'rl_swing': [], 'top_swing': [], 'down_swing':[], 'dead': []}    

        for animation in self.animations.keys():
            full_path = 'img/' + animation
            self.animations[animation] = import_folder(full_path)
        print(self.animations)

    def animate(self, dt):
        self.frame_index += 4 * dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0

        original_frame = self.animations[self.status][int(self.frame_index)]
        self.image = pygame.transform.scale(original_frame,
                                            (int(original_frame.get_width() * self.scale_factor),
                                             int(original_frame.get_height() * self.scale_factor)))
        # self.image = self.animations[self.status][int(self.frame_index)]

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
            self.status = 'rl'
        elif keys[pygame.K_a]:
            self.direction.x = -1
        else:
            self.direction.x = 0

    def move(self, dt):

        #normalizing vector
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()
        
        #horizontal movement
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.centerx = self.pos.x

        #vertical movement
        self.pos.y += self.direction.y * self.speed * dt
        self.rect.centery = self.pos.y
    
    def update(self, dt):
        self.input()
        self.move(dt)
        self.animate(dt)