import configparser
import random

import pygame
from random import randint
class Particle(pygame.sprite.Sprite):
    def __init__(self,
                 groups: pygame.sprite.Group,
                 pos: list[int],
                 color: str,
                 direction: pygame.math.Vector2,
                 speed: int):
        super().__init__(groups)
        self.color = color
        self.direction = direction
        self.positon = pos
        self.speed = speed
        self.alpha = 255
        self.fade_speed = random.randint(65, 300)
        self.size = random.randint(4, 14)

        self.create_surf()

    def create_surf(self):
        self.image = pygame.Surface((self.size, self.size)).convert_alpha()
        self.image.set_colorkey("black")
        pygame.draw.circle(surface=self.image, color=self.color, center=(self.size / 2, self.size / 2), radius=self.size / 2)
        self.rect = self.image.get_rect(center=self.positon)

    def move(self, dt):
        self.positon += self.direction * self.speed * dt
        self.rect.center = self.positon

    def fade(self, dt):
        self.alpha -= self.fade_speed * dt
        self.image.set_alpha(self.alpha)

    def check_pos(self, WIDTH, MAIN_HEIGHT):
        if (
            self.positon[0] < -50 or
            self.positon[0] > WIDTH + 50 or
            self.positon[1] < -50 or
            self.positon[1] > MAIN_HEIGHT + 50
        ):
            self.kill()

    def check_alpha(self):
        if self.alpha <= 0:
            self.kill()

    def update(self, dt):
        self.move(dt)
        self.fade(dt)
        self.check_pos(1000, 1000)
        self.check_alpha()
