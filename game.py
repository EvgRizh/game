import math
import time

import pygame
import random

from pygame.locals import (
    RLEACCEL,
    K_SPACE,
    K_a,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("player.png")
        self.rect = self.surf.get_rect()

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -2)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 2)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-2, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(2, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("enemy.png")
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(2, 6)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load("cloud.png")
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(1, 3)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


class Laser(pygame.sprite.Sprite):
    def __init__(self):
        super(Laser, self).__init__()
        self.surf = pygame.image.load("laser.png")
        self.rect = self.surf.get_rect(center=(0, 0,))
        self.speed = 15

    def update(self):
        self.rect.move_ip(self.speed, 0)

class Button(pygame.sprite.Sprite):
    def __init__(self):
        super(Button, self).__init__()
        self.surf = pygame.image.load("knopka.png")
        self.rect = self.surf.get_rect(topleft=(0, 0,))

    def update(self, surface):
        surface.blit(self.surf, (SCREEN_WIDTH/2 - self.surf.get_width()/2, SCREEN_HEIGHT/2 - self.surf.get_height()/2))

black = (0, 0, 0)
pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# m = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 500)
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)

button = Button()

enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
lasers = pygame.sprite.Group()
all_sprite = pygame.sprite.Group()

running = False
menu = True

clock = pygame.time.Clock()
n = 30
while menu:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                menu = False
        elif event.type == QUIT:
            menu = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and (300 < event.pos[0] < 500 and 280 < event.pos[1] < 360):
                live = 15
                score = 0
                running = True
                player = Player()
                all_sprite.add(player)
                time.sleep(1)
            else: x = 0

    screen.fill((100, 206, 250))
    button.update(screen)

    pygame.display.flip()

    while running:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                elif event.key == K_SPACE:
                    new_laser = Laser()
                    new_laser.rect = new_laser.surf.get_rect(center=(player.rect.right,
                    player.rect .top+23, ))
                    lasers.add(new_laser)
                    all_sprite.add(new_laser)
            elif event.type == QUIT:
                running = False
            elif event.type == ADDENEMY:
                new_enemy = Enemy()
                enemies.add(new_enemy)
                all_sprite.add(new_enemy)
            elif event.type == ADDCLOUD:
                new_cloud = Cloud()
                clouds.add(new_cloud)
                all_sprite.add(new_cloud)

        pressed_key = pygame.key.get_pressed()

        enemies.update()
        clouds.update()
        lasers.update()

        player.update(pressed_key)

        screen.fill((100, 206, 250))

        font_live = pygame.font.Font(None, 30)
        text_surf1 = font_live.render("Жизни: {}".format(live), True, black, None)
        text_rect1 = text_surf1.get_rect()
        text_rect1.center = (650, 50)
        text_surf2 = font_live.render("Врагов убито: {}".format(score), True, black, None)
        text_rect2 = text_surf2.get_rect()
        text_rect2.center = (650, 110)
        screen.blit(text_surf1, text_rect1)
        screen.blit(text_surf2, text_rect2)

        for entity in all_sprite:
            screen.blit(entity.surf, entity.rect)

        if pygame.sprite.spritecollide(player, enemies, True):
            live -= 1
            if live == 0:
                player.kill()
                running = False

        for laser in lasers:
            hint = pygame.sprite.spritecollide(laser, enemies, True)
            if hint:
                score += 1
                laser.kill()

        pygame.display.flip()

        clock.tick(100)

pygame.quit()