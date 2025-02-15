import asyncio
import math
import random
import pygame
from classes.window import Window


class Segment:
    def __init__(self, z, curve=0, elevation=0):
        self.x = 0
        self.y = 0
        self.z = z
        self.curve = curve
        self.elevation = elevation


class VroomVroom(Window):
    def __init__(self, x, y, width, height, title, font, icon):
        super().__init__(x, y, width, height, title, font, icon)
        self.width = width
        self.height = height
        self.clock = pygame.time.Clock()
        self.clock.tick()
        pygame.time.wait(16)

        self.road_texture = pygame.image.load("img/road.png").convert()

        self.car = pygame.image.load("img/m3.png").convert_alpha()
        self.car = pygame.transform.scale(self.car, (168, 123))
        self.car.set_colorkey((0, 0, 0))

        self.FOV = 100
        self.start_FOV = 150
        self.ROAD_WIDTH = 2000
        self.SEGMENT_LENGTH = 200
        self.CAMERA_Z = 1000
        self.NUM_SEGMENTS = 500
        self.offset = 0

        self.segments = []
        for i in range(1, self.NUM_SEGMENTS):
            curve = math.sin(i / 30) * 2
            elevation = math.sin(i / 15) * 20
            self.segments.append(Segment(i * self.SEGMENT_LENGTH, curve, elevation))

        self.camera_x, self.camera_y, self.camera_z = 0, 500, 0
        self.q_active = False
        self.e_active = False
        self.a_active = False
        self.d_active = False
        self.w_active = False
        self.curvature_factor = 100
        self.start_offset = 100
        self.speed = 0

        self.desert_image = pygame.image.load('img/desert.png').convert()
        self.desert_image = pygame.transform.scale(self.desert_image,
                                                   (self.width, self.height))


    def draw(self, screen):
        super().draw(screen)
        if self.q_active:
            self.camera_y += 10
            self.FOV += 10
        elif self.e_active:
            self.camera_y -= 10
            self.FOV -= 10

        if self.a_active:
            self.camera_x += 10
        elif self.d_active:
            self.camera_x -= 10

        if self.w_active:
            self.speed = min(55, self.speed + 2)
            self.FOV = max(self.FOV - 1, 0)
        else:
            self.speed = max(0, self.speed - 1)
            self.FOV = min(self.FOV + 2, 100)

        self.surface.fill((135, 206, 235))

        self.camera_z += self.speed

        for n in range(500 + self.start_FOV - self.start_offset):
            scale = (500 + self.start_FOV - self.start_offset - n) / 300
            x = self.camera_z + n / scale
            y = self.curvature_factor * math.sin(x / 1170) + self.curvature_factor / 4 * math.sin(
                x / 580) + self.camera_x
            horizontal = self.width // 2 - (self.width // 2 - y) * scale

            pygame.draw.rect(self.surface, (180, 179, 113), (0, self.height + 100 - n + self.start_offset, self.width, 1))

            road_slice = self.road_texture.subsurface((0, x % 360, 320, 1))
            scaled_slice = pygame.transform.scale(road_slice, (self.width * scale, 1))
            #desert_slice = self.desert_image.subsurface((0, x % 360, 600, 1))
            #scaled_desert_slice = pygame.transform.scale(desert_slice, (self.width * (1 + scale), 1))
            #self.surface.blit(scaled_desert_slice, (-horizontal, self.height + 100 - n + self.start_offset))
            self.surface.blit(scaled_slice, (horizontal, self.height + 100 - n + self.start_offset))
        car_x = self.width // 2 - self.car.get_width() // 2
        car_y = self.height - self.car.get_height() - 50

        self.surface.blit(self.car, (car_x, car_y))

        screen.blit(self.surface, (self.rect.x, self.rect.y + self.title_bar_height))
        #self.clock.tick(30)

    def render_hotbar(self):
        pass

    def handle_event(self, event):
        super().handle_event(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                self.q_active = True
            if event.key == pygame.K_e:
                self.e_active = True
            if event.key == pygame.K_a:
                self.a_active = True
            if event.key == pygame.K_d:
                self.d_active = True
            if event.key == pygame.K_w:
                self.w_active = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_q:
                self.q_active = False
            if event.key == pygame.K_e:
                self.e_active = False
            if event.key == pygame.K_a:
                self.a_active = False
            if event.key == pygame.K_d:
                self.d_active = False
            if event.key == pygame.K_w:
                self.w_active = False