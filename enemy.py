import pygame 
from settings import *
from os import path
from support import *
import math


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, group, *args):
        super().__init__(group)

        self.import_assets()
        self.status = 'idle'
        self.frame_index = 0
        self.scale_factor = 3

        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center = pos)

        self.direction = pygame.math.Vector2(0, 0)
        self.pos = pygame.math.Vector2(self.rect.center)

        self.radius = 100  # Adjust the radius of the circle as needed
        self.angle = 0

    def import_assets(self):
        self.animations = {'idle': [], 'move': [], 'attacked': [], 'dead': []}    

        for animation in self.animations.keys():
            full_path = 'img/slime/' + animation
            self.animations[animation] = import_folder(full_path)
        
    def animate(self, dt):
        self.frame_index += 6 * dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0

        original_frame = self.animations[self.status][int(self.frame_index)]
        scaled_frame = pygame.transform.scale(original_frame,
                        (int(original_frame.get_width() * self.scale_factor),
                        int(original_frame.get_height() * self.scale_factor)))
    
        self.image = scaled_frame
        self.rect = scaled_frame.get_rect(center=self.rect.center)

    def update(self, dt):
        self.animate(dt)
        