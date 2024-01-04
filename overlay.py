import pygame
from settings import *

class Overlay():
    def __init__(self, player):
        self.display_surface = pygame.display.get_surface()
        self.player = player

        heart = pygame.image.load('img/heart.png')
        heart = heart.convert_alpha()
        self.heart_surface = {'heart' :heart}

    def display(self):

        heart_surface = self.heart_surface['heart']
        # self.display_surface.blit(heart_surface, (0,0))
        num_hearts = self.player.health
        for i in range(num_hearts):
            x_offset = i * (heart_surface.get_width() + 5)  # Adjust 5 for spacing between hearts
            self.display_surface.blit(heart_surface, (x_offset, 0))