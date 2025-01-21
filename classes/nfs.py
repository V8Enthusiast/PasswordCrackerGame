import asyncio
import math
import random

import pygame

from classes.window import Window

class Segment:
    def __init__(self, z, curve=0, elevation=0):
        self.x = 0            # Horizontal position (default is 0)
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
        # self.mountains_texture = pygame.image.load("img/mountains.png").convert()
        # self.car_sprite = pygame.image.load("img/car.png").convert()
        # self.car_sprite.set_colorkey((255, 0, 255))
        # self.car_sprite2 = pygame.image.load("img/car2.png").convert()
        # self.car_sprite2.set_colorkey((255, 0, 255))
        # self.tree_sprite = pygame.image.load("img/tree.png").convert()
        # self.tree_sprite.set_colorkey((255, 0, 255))

        # Constants
        self.FOV = 100
        self.ROAD_WIDTH = 2000
        self.SEGMENT_LENGTH = 200
        self.CAMERA_Z = 1000
        self.NUM_SEGMENTS = 500
        self.offset = 0
        # Create segments
        self.segments = []
        for i in range(1, self.NUM_SEGMENTS):
            curve = math.sin(i / 30) * 2  # Example curve
            elevation = math.sin(i / 15) * 20  # Example hill
            self.segments.append(Segment(i * self.SEGMENT_LENGTH, curve, elevation))

        self.camera_x, self.camera_y, self.camera_z = 0, 500, 0

        # self.button_names = ['sand', 'water', 'stone', 'acid', 'plastic', 'fire', 'oil', 'iron', 'gold', 'copper', 'hydrogen', 'chlorine', 'eraser', 'settings', 'exit']
        # button_amount = len(self.button_names)
        # #button_size = (self.app.width - 2 * self.side_margin) // button_amount
        # button_size = int(64 * self.app.scale)
        # space_between_buttons = (self.app.width - self.side_margin * 2 - button_amount * button_size) // (button_amount - 1)
        # height = (self.app.hotbar_height - button_size) // 2
        # self.hotbar_buttons = []
        # for idx, button_name in enumerate(self.button_names):
        #     self.hotbar_buttons.append(hotbar_button.HotbarButton(button_size, button_size, self.side_margin + idx * (button_size + space_between_buttons), self.app.height + height, False, "fonts/main_font.ttf", button_name, (0, 0, 0), (255, 255, 255), button_name, self.app, self))
        #
        # self.selected_button = None
        self.q_active = False
        self.e_active = False

        self.a_active = False
        self.d_active = False

        self.w_active = False

        self.curvature_factor = 100
        self.start_offset = 100
        self.speed = 0

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
            self.FOV = max(self.FOV - 1, 10)
        else:
            self.speed = max(0, self.speed - 1)
            self.FOV = min(self.FOV + 1, 100)


        self.surface.fill((135, 206, 235))  # Sky blue
        #pygame.draw.rect(self.screen, (60, 179, 113), (0, self.height // 2, self.width, self.height))  # Grass

        # Update camera
        #delta = self.clock.tick()/1000 + 0.00001

        self.camera_z += self.speed #delta*100  # Move forward

        base_segment = int(self.camera_z / self.SEGMENT_LENGTH) % self.NUM_SEGMENTS

        for n in range(500 + self.FOV - self.start_offset):

            scale = (500 + self.FOV - self.start_offset - n) / 300
            x = self.camera_z + n/scale
            y = self.curvature_factor*math.sin(x/1170) + self.curvature_factor/4 * math.sin(x/580) + self.camera_x
            horizontal = self.width//2 - (self.width//2 - y) * scale
            road_slice = self.road_texture.subsurface((0, x%360, 320, 1))
            scaled_slice = pygame.transform.scale(road_slice, (self.width * scale, 1))
            #color = (int(50 - (n % (500 + self.FOV)) / 3), int(500 + self.FOV - n), int(50 + 30 * math.sin(x)))
            pygame.draw.rect(self.surface, (180, 179, 113), (0, self.height + 100 - n, self.width, 1))
            # Map the texture onto the trapezoid
            self.surface.blit(scaled_slice, (horizontal, self.height + 100 - n))

        # Refresh display
        screen.blit(self.surface, (self.rect.x, self.rect.y + self.title_bar_height))
        self.clock.tick(60)

    def render_hotbar(self):
        # hotbar_rect = pygame.Rect(0, self.app.height - 2, self.app.width, self.app.hotbar_height)
        # pygame.draw.rect(self.window, self.hotbar_color ,hotbar_rect)
        # for button in self.hotbar_buttons:
        #     button.render()
        pass

    # Overrides the default events function in app.py
    def handle_event(self,event):
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