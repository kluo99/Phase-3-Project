import pygame 
from settings import *
from player import Player
from sprites import Generic
from overlay import Overlay
from enemy import Enemy

class Level:
    def __init__(self):

        # get display surface
        self.display_surface = pygame.display.get_surface()

        #sprite groups
        self.all_sprites = CameraGroup()
        self.collision_sprites = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()

        self.setup()
        self.overlay = Overlay(self.player)



    def setup(self):
        background_image = pygame.image.load('data/dungeon.png')
        scaled_background = pygame.transform.scale(background_image, (3380, 1920))
        Generic(
            pos = (0,0),
            surf = scaled_background,
            groups = self.all_sprites
        )

        self.enemy1 = Enemy((1560, 1180), self.all_sprites, self.enemy_group)
        self.enemy2 = Enemy((1660, 1280), self.all_sprites, self.enemy_group)
        self.player = Player((1560, 780), self.all_sprites)
        self.enemy_group.add(self.enemy1)
        self.enemy_group.add(self.enemy2)


    def run(self, dt):
        self.all_sprites.custom_draw(self.player)
        self.all_sprites.update(dt)
        self.overlay.display()

        for enemy in self.enemy_group.sprites():
            enemy.update(dt)
    
        collisions = pygame.sprite.spritecollide(self.player, self.enemy_group, False)
        # print(self.enemy_group)
        # for enemy in self.enemy_group:
        #      print(enemy)
        #      collisions.append(pygame.sprite.collide_rect(self.player, enemy))
        
        if collisions:
            print(f"collisions: {collisions}")
            print("Player collided with an enemy!")

            


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

        self.black_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.black_surface.fill((0, 0, 0))
    
    
    def custom_draw(self, player):
        self.display_surface.blit(self.black_surface, (0, 0))
        self.offset.x = player.rect.centerx - SCREEN_WIDTH / 2
        self.offset.y = player.rect.centery - SCREEN_HEIGHT / 2


        for sprite in self.sprites():
            offset_rect = sprite.rect.copy()
            offset_rect.center -= self.offset
            self.display_surface.blit(sprite.image, offset_rect)
