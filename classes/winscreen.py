import pygame
from classes import buttons


class WinScreen:
    def __init__(self, app, score):
        self.app = app
        self.debug = False

        self.VICTORY_GREEN = (0, 100, 0)
        self.VICTORY_LIGHT = (144, 238, 144)

        self.margin_left = 50 * self.app.scale
        self.margin_right = self.app.width - (50 * self.app.scale)
        self.line_spacing = 40 * self.app.scale
        self.start_y = 100 * self.app.scale

        self.font = pygame.font.Font("fonts/Windows98.ttf", int(28 * self.app.scale))
        self.font_bold = pygame.font.Font("fonts/Windows98.ttf", int(32 * self.app.scale))

        button_width = 200 * self.app.scale
        button_height = 75 * self.app.scale
        button_spacing = 50 * self.app.scale
        total_width = (button_width * 2) + button_spacing
        start_x = (self.app.width - total_width) / 2

        self.buttons = [
            buttons.Button(
                button_width,
                button_height,
                start_x,
                self.app.height - 150 * self.app.scale,
                self.font,
                "Continue",
                'back',
                self.app,
                self.VICTORY_GREEN,
                self.VICTORY_LIGHT
            ),
            buttons.Button(
                button_width,
                button_height,
                start_x + button_width + button_spacing,
                self.app.height - 150 * self.app.scale,
                self.font,
                "Main Menu",
                'back_to_menu',
                self.app,
                self.VICTORY_GREEN,
                self.VICTORY_LIGHT
            )
        ]

        self.window = self.app.screen
        self.score = score

        self.victory_text = [
            "SECURITY TEST PASSED!",
            "",
            f"Money left: ${self.score//1000},{self.score%1000:03d}.00",
            ""
        ]

        self.victory_text.extend(self.wrap_text(f"Congratulations! Your password managed to withstand a bruteforce attack for {self.app.inactive_simulation.timeout // 60}m {self.app.inactive_simulation.timeout % 60}s", self.font))
        self.victory_text.extend([""])
        self.victory_text.extend(self.wrap_text(f"You may go back to the current simulation if you want to, but beware that it may take upwards of 2 hours to break your password.", self.font))

    def wrap_text(self, text, font):
        """Wrap text to fit within the screen margins."""
        words = text.split(' ')
        lines = []
        current_line = words[0]

        for word in words[1:]:
            test_line = current_line + ' ' + word
            text_surface = font.render(test_line, True, self.VICTORY_LIGHT)

            if text_surface.get_width() > (self.margin_right - self.margin_left):
                if lines or current_line.startswith(('Result:', 'Tip:')):
                    lines.append(current_line)
                    current_line = "  " + word
                else:
                    lines.append(current_line)
                    current_line = word
            else:
                current_line += ' ' + word

        lines.append(current_line)
        return lines

    def render(self):
        self.window.fill(self.VICTORY_GREEN)

        header = self.font_bold.render("Password Security Test", True, self.VICTORY_LIGHT)
        self.window.blit(header, (self.margin_left, self.start_y))

        current_y = self.start_y + self.line_spacing * 2
        for line in self.victory_text:
            text_surface = self.font.render(line, True, self.VICTORY_LIGHT)
            self.window.blit(text_surface, (self.margin_left, current_y))
            current_y += self.line_spacing

        for button in self.buttons:
            button.render(self.app.screen)

    def events(self):
        pass