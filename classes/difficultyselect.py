import pygame
from classes import buttons
from classes import inputBox
class DifficultySelect:
    def __init__(self, app):
        self.app = app
        self.main_text_rect_center = (self.app.width // 2, 150 * self.app.scale)
        self.font = pygame.font.Font("fonts/Windows98.ttf", 24)
        self.arrow_font = pygame.font.Font("fonts/arrows.ttf", 24)
        self.font_color = (255, 255, 255)
        self.password = ""

        self.buttons = [
            buttons.Button(100 * self.app.scale, 75 * self.app.scale,
                           self.app.width / 2 - 200 * self.app.scale,
                           self.app.height / 2 - 150 * self.app.scale,
                           self.arrow_font, "Q", 'minus', self.app),
            buttons.Button(100 * self.app.scale, 75 * self.app.scale,
                           self.app.width / 2 + 100 * self.app.scale,
                           self.app.height / 2 - 150 * self.app.scale,
                           self.arrow_font, "U", 'plus', self.app),
            buttons.Button(200 * self.app.scale, 75 * self.app.scale,
                           self.app.width / 2 - 100 * self.app.scale,
                           self.app.height / 2 + 150 * self.app.scale,
                           self.font, "Start", 'start_game', self.app),
            buttons.Button(200 * self.app.scale, 75 * self.app.scale,
                           self.app.width / 2 - 100 * self.app.scale,
                           self.app.height / 2 + 250 * self.app.scale,
                           self.font, "Back", 'back_to_menu', self.app)
        ]
        self.selected_length = 5
        self.diffs = {
            4 : "Hard",
            5: "Normal",
            6: "Easy",
            7: "Sandbox mode"
        }

        input_box_rect = pygame.Rect(
            self.app.width / 2 - 150 * self.app.scale,
            self.app.height / 2 + 50 * self.app.scale,
            300 * self.app.scale,
            40 * self.app.scale
        )

        self.passwordbox = inputBox.InputBox(input_box_rect.x, input_box_rect.y, input_box_rect.w, input_box_rect.h,
                                             self.font, max_length=self.selected_length, font_color=(192, 192, 192))
        self.pwdText = "Initial password"

    def render(self):
        self.app.screen.fill((0, 0, 0))

        for button in self.buttons:
            button.render(self.app.screen)

        title_font = pygame.font.Font("fonts/Windows98.ttf", int(48 * self.app.scale))
        section_font = pygame.font.Font("fonts/Windows98.ttf", int(36 * self.app.scale))
        number_font = pygame.font.Font("fonts/Windows98.ttf", int(48 * self.app.scale))

        length_text = title_font.render("Choose max password length", True, self.font_color)
        length_text_rect = length_text.get_rect()
        length_text_rect.center = (self.app.width // 2, 100 * self.app.scale)

        diff_text = section_font.render(self.diffs[self.selected_length], True, self.font_color)
        diff_text_rect = diff_text.get_rect()
        diff_text_rect.center = (self.app.width // 2, 220 * self.app.scale)

        length_number = number_font.render(f"{self.selected_length}", True, self.font_color)
        if self.selected_length == 7:
            length_number = number_font.render(f"None", True, self.font_color)
        number_rect = pygame.Rect(
            self.app.width / 2 - 50 * self.app.scale,
            self.app.height / 2 - 150 * self.app.scale,
            100 * self.app.scale,
            75 * self.app.scale
        )
        length_number_rect = length_number.get_rect()
        length_number_rect.center = number_rect.center

        initial_text = section_font.render(self.pwdText, True, self.font_color)
        if self.selected_length == 7:
            initial_text = section_font.render("Enjoy Windows95 without worrying about passwords", True, self.font_color)
        initial_text_rect = initial_text.get_rect()
        initial_text_rect.center = (self.app.width // 2, self.app.height / 2)



        # pygame.draw.rect(self.app.screen, (64, 64, 64), input_box_rect)
        # pygame.draw.rect(self.app.screen, (128, 128, 128), input_box_rect, 2)
        if self.selected_length != 7:
            self.passwordbox.draw(self.app.screen)

        self.app.screen.blit(length_text, length_text_rect)
        self.app.screen.blit(diff_text, diff_text_rect)
        self.app.screen.blit(length_number, length_number_rect)
        self.app.screen.blit(initial_text, initial_text_rect)

    def add(self):
        if self.selected_length < 7:
            self.passwordbox.max_length += 1
            self.selected_length += 1

    def subtract(self):
        if self.selected_length > 4 and self.selected_length -1 >= len(self.passwordbox.text):
            self.passwordbox.max_length -= 1
            self.selected_length -= 1

    def events(self):
        for event in pygame.event.get():
            self.passwordbox.handle_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if event.button == 1: #LMB
                    for button in self.buttons:
                        if button.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                            button.selected = True
                            button.click()
            if event.type == pygame.MOUSEBUTTONUP:
                for button in self.buttons:
                    button.selected = False
            if event.type == pygame.QUIT:
                self.app.run = False
