import pygame

class Simulation:
    def __init__(self, app):
        self.app = app
        self.debug = False
        self.bg_color = (33, 33, 33)
        self.window = self.app.screen
        self.buttons = []

        self.side_margin = int(20 * self.app.scale)

        self.selected_button = None

    def render(self):
        self.window.fill(self.bg_color)

    # Overrides the default events function in app.py
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.app.run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    pass