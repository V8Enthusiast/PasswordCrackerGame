import pygame
import random
import math


class Particle(pygame.sprite.Sprite):
    def __init__(self, groups, pos, color, direction, speed):
        super().__init__(groups)
        self.color = color
        self.direction = direction
        self.positon = pos
        self.speed = speed
        self.alpha = 255
        self.fade_speed = random.randint(65, 300)
        self.size = random.randint(4, 14)

        self.spinning = True

        if self.spinning:
            self.angle = random.randint(0, 360)
            self.rotation_speed = random.uniform(-5, 5)
            self.original_image = None

        self.create_surf()

    def create_surf(self):
        self.original_image = pygame.Surface((self.size, self.size)).convert_alpha()
        self.original_image.set_colorkey("black")
        self.original_image.fill((0, 0, 0, 0))

        center_x = self.size / 2
        center_y = self.size / 2
        height = self.size
        base = self.size
        points = [
            (center_x, center_y - height / 2),
            (center_x - base / 2, center_y + height / 2),
            (center_x + base / 2, center_y + height / 2)
        ]
        pygame.draw.polygon(surface=self.original_image, color=self.color, points=points)

        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.positon)

    def rotate(self, dt):
        self.angle += self.rotation_speed * dt * 60
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center

        self.image.set_alpha(self.alpha)

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
        if self.spinning:
            self.rotate(dt)
        self.fade(dt)
        self.check_pos(1000, 1000)
        self.check_alpha()