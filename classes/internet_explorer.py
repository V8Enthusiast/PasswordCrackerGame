import asyncio
import math
import random

import pygame

from classes.window import Window

class InternetExplorer(Window):
    def __init__(self, x, y, width, height, title, font, icon):
        super().__init__(x, y, width, height, title, font, icon)
        self.width = width
        self.height = height


    def draw(self, screen):
        super().draw(screen)

    # Overrides the default events function in app.py
    def handle_event(self,event):
        super().handle_event(event)