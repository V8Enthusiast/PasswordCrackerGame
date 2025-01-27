import pygame
from classes import buttons

class MainMenu:
    def __init__(self, app):
        self.app = app
        self.debug = False

        self.main_text_rect_center = (self.app.width // 2, 250 * self.app.scale)
        self.font = pygame.font.Font("fonts/main_font.ttf", 36)
        self.font_color = (255, 255, 255)
        self.bg_color = (33, 33, 33)
        self.buttons = [
            buttons.Button(200 * self.app.scale, 75 * self.app.scale, self.app.width / 2 - 100 * self.app.scale,
                           self.app.height / 2 - 75 * self.app.scale / 2, self.font, "Play", 'play',self.app,(0, 0, 0),
                           self.font_color)]
        self.window = self.app.screen
    def render(self):
        self.window.fill(self.bg_color)
        for button in self.buttons:
            button.render(self.app.screen)
        font = pygame.font.Font("fonts/main_font.ttf", int(72 * self.app.scale))
        display_text = font.render("P A S S W O R D  G A M E", True, self.font_color)
        display_text_rect = display_text.get_rect()
        display_text_rect.center = self.main_text_rect_center
        self.app.screen.blit(display_text, display_text_rect)

    # Overrides the default events function in app.py
    def events(self):
        pass