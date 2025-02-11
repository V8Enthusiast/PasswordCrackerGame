import pygame
from classes import buttons

class GameOver:
    def __init__(self, app, score):
        self.app = app
        self.debug = False

        self.main_text_rect_center = (self.app.width // 2, 250 * self.app.scale)
        self.score_text_rect_center = (self.app.width // 2,750 * self.app.scale)
        self.font_small = pygame.font.Font("fonts/Windows98.ttf", 36)
        self.font = pygame.font.Font("fonts/Windows98.ttf", 72)
        self.font_color = (192, 192, 192)
        self.bg_color = (0, 0, 128)
        self.buttons = [
            buttons.Button(200 * self.app.scale, 75 * self.app.scale, self.app.width / 2 - 100 * self.app.scale,
                           self.app.height / 2 - 75 * self.app.scale / 2, self.font_small, "Play again", 'play',self.app,(0, 0, 0),
                           self.font_color)]
        self.window = self.app.screen
        self.score = score

        self.app.newSimulation()
        self.minutes = str(int(self.score)//60)
        self.seconds = str(int(self.score)%60)
        
    def render(self):
        self.window.fill(self.bg_color)
        for button in self.buttons:
            button.render(self.app.screen)

        display_text = self.font.render("You have been hacked!", True, self.font_color)
        score_text = self.font_small.render("You survived for " + self.minutes + " minutes and " + self.seconds + " seconds", True, self.font_color)

        display_text_rect = display_text.get_rect()
        score_text_rect = display_text.get_rect()
        display_text_rect.center = self.main_text_rect_center
        score_text_rect.center = self.score_text_rect_center
        self.app.screen.blit(display_text, display_text_rect)
        self.app.screen.blit(score_text, score_text_rect)

    # Overrides the default events function in app.py
    def events(self):
        pass