import asyncio
import math
import random
from classes import inputBox
import pygame

from classes.window import Window

class InternetExplorer(Window):
    def __init__(self, x, y, width, height, title, font, icon):
        super().__init__(x, y, width, height, title, font, icon)
        self.width = width
        self.height = height
        self.passwordBox = inputBox.InputBox(self.surface.get_width() // 2 - 100, self.surface.get_width() // 2 - 225,
                                             200, 50, self.font)
        self.passwordBox.rect.x = self.rect.x + self.passwordBox.x
        self.passwordBox.rect.y = self.rect.y + self.passwordBox.y

    def draw(self, screen):
        super().draw(screen)
        self.passwordBox.update()
        self.passwordBox.draw(screen)

    # Overrides the default events function in app.py
    def handle_event(self,event):
        super().handle_event(event)
        if event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.rect.x = event.pos[0] + self.offset_x
                self.rect.y = event.pos[1] + self.offset_y
                self.passwordBox.rect.x = self.rect.x + self.passwordBox.x
                self.passwordBox.rect.y = self.rect.y + self.passwordBox.y