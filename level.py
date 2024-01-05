import pygame 
from settings import *
from player import Player
from sprites import Generic
from overlay import Overlay
from enemy import Enemy
import time
import random

class Level:
    def __init__(self):

        # get display surface
        self.display_surface = pygame.display.get_surface()

        #sprite groups
        self.all_sprites = CameraGroup()
        self.collision_sprites = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()

        self.invincibility_duration = 1.0 
        self.invincible_time = 0

        self.setup()
        self.overlay = Overlay(self.player)
        self.enemy_damage_cooldown = 0.5
    
    def reset(self):
        self.all_sprites.empty()  # Clear all sprites
        self.collision_sprites.empty()  # Clear collision sprites
        self.enemy_group.empty()  # Clear enemy group
        self.setup()  # Re-setup the level
        self.overlay = Overlay(self.player)


    def setup(self):
        background_image = pygame.image.load('data/dungeon.png')
        self.original_player_position = (1560, 780)
        scaled_background = pygame.transform.scale(background_image, (3380, 1920))
        Generic(
            pos=(0, 0),
            surf=scaled_background,
            groups=self.all_sprites
        )

        self.enemy1 = Enemy((1560, 1180), self.all_sprites, self.enemy_group)
        self.enemy2 = Enemy((1660, 1280), self.all_sprites, self.enemy_group)
        self.enemy3 = Enemy((1760, 1380), self.all_sprites, self.enemy_group)
        self.player = Player((1560, 780), self.all_sprites)
        self.enemy_group.add(self.enemy1)
        self.enemy_group.add(self.enemy2)
        self.enemy_group.add(self.enemy3)

    def run(self, dt, screen):
        self.all_sprites.custom_draw(self.player, self.invincible_time)
        self.all_sprites.update(dt)
        self.overlay.display()

        player_hitbox = self.player.hitbox


        for enemy in self.enemy_group.sprites():
            enemy.update(dt)

        player_position = (self.player.rect.centerx, self.player.rect.centery)

        # for enemy in self.enemy_group.sprites():
        collisions = pygame.sprite.spritecollide(self.player, self.enemy_group, False)


        if collisions and self.player.status.endswith('_swing'):
            # self.enemy1.health -= 1
            # print(f"Enemy health: {self.enemy1.health}")
            # print(f"Enemy health: {self.enemy2.health}")
            for enemy in collisions:
                if time.time() > self.invincible_time:
                    # Check if the enemy is not on cooldown
                    if time.time() > enemy.last_damage_time + self.enemy_damage_cooldown:
                        if enemy.health > 0:
                            enemy.health -= 1
                            enemy.last_damage_time = time.time()  # Update the last damage time
                            print(f"Enemy health: {enemy.health}")
                        else:
                            enemy.status = 'dead'
                            enemy.direction = pygame.math.Vector2(0, 0)
            # print(f"collisions: {collisions}")
            # print("Player collided with an enemy!")
            # if self.player.status.endswith('_swing') and time.time() > self.invincible_time:
            #     print("Player is attacking!")
        elif collisions:
            for c in collisions:
                print(f"player rect {self.player.rect}")
                print(f"enemy rect {c.rect}")
                print(f"enemy image rect {c.image.get_rect(center=c.pos)}")
                pygame.draw.rect(screen, "red", c.rect)
                # import pdb; pdb.set_trace()

            if time.time() > self.invincible_time and enemy.health > 0:
                self.player.health -= 1
                print(f"Player health: {self.player.health}")

                self.invincible_time = time.time() + self.invincibility_duration

                if self.player.health <= 0:
                    print("Player is dead!")
                    # self.reset()

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

        self.black_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.black_surface.fill((0, 0, 0))
    
    
    def custom_draw(self, player, invincible_time):
        if time.time() < invincible_time:
            # Draw a transparent red surface over the screen
            red_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            red_surface.fill((255, 0, 0, 128))  # Red color with 50% transparency
            self.display_surface.blit(red_surface, (0, 0))

        self.display_surface.blit(self.black_surface, (0, 0))
        self.offset.x = player.rect.centerx - SCREEN_WIDTH / 2
        self.offset.y = player.rect.centery - SCREEN_HEIGHT / 2

        for sprite in self.sprites():
            offset_rect = sprite.rect.copy()
            offset_rect.center -= self.offset
            self.display_surface.blit(sprite.image, offset_rect)
