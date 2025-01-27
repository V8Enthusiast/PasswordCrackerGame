from classes.window import Window
import pygame

class StartMenu(Window):
    import img
    def draw(self, screen):
        super().draw(screen)
        self.surface.fill((0, 0, 0))
        self.surface.blit("A", self.button_width)
        self.shift = False