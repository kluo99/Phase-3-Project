import pygame 
from settings import *
from os import path
from support import *
import math
import random


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, group, *args):
        super().__init__(group)

        self.import_assets()
        self.status = 'idle'
        self.frame_index = 0
        self.scale_factor = 4

        self.image = self.animations[self.status][self.frame_index]
        self.original_rect = self.image.get_rect(center=pos)
        self.rect = self.image.get_rect(center = pos)
        self.direction = pygame.math.Vector2(0, 0)

        self.hitbox_radius = 60  # Adjust the hitbox radius based on your game
        self.hitbox = pygame.Rect(0, 0, self.hitbox_radius * 2, self.hitbox_radius * 2)


        self.direction = pygame.math.Vector2(0, 0)
        self.pos = pygame.math.Vector2(self.rect.center)

        self.health = 3
        self.last_damage_time = 0 

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
    
        # self.image = scaled_frame
        self.image = pygame.Surface(scaled_frame.get_size(), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 128))  # Black color with 50% transparency
        self.image.blit(scaled_frame, (0, 0))
        self.rect = scaled_frame.get_rect(center=self.rect.center)

    def animatedeath(self, dt):
        self.frame_index += 10 * dt

        # Check if the animation has reached the end
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = len(self.animations[self.status]) - 1  # Set to the last frame

        original_frame = self.animations[self.status][int(self.frame_index)]
        self.image = pygame.transform.scale(original_frame,
                                        (int(original_frame.get_width() * self.scale_factor),
                                         int(original_frame.get_height() * self.scale_factor)))

    def update(self, dt):
        if self.health <= 0:
            self.direction = pygame.math.Vector2(0, 0)
            self.status = 'dead'
            self.animatedeath(dt)
        else:
            direction = random.choice(['left', 'right', 'up', 'down'])

            # Adjust the speed to make the enemy move slower
            speed = 1
            # if self.rect.colliderect(player_hitbox):
            #     print("Enemy hit by player's swing!")
            #     self.enemyhealth -= 1
            #     if self.enemyhealth <= 0:
            #         print("Enemy is defeated!")

            if direction == 'left':
                self.direction.x -= speed
            elif direction == 'right':
                self.direction.x += speed
            elif direction == 'up':
                self.direction.y -= speed
            elif direction == 'down':
                self.direction.y += speed

            angle = 0.1 * dt  # Adjust the angular speed as needed
            self.direction.rotate_ip(angle)
            self.animate(dt)
            self.pos += self.direction * dt
            # self.rect.center = self.pos
            self.original_rect.center = self.pos

            enlarged_rect = self.original_rect.inflate(20, 20)  # Adjust the inflation values as needed
            self.rect = enlarged_rect

            self.hitbox.center = self.rect.center
        
        