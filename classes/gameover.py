import pygame
from classes import buttons


class GameOver:
    def __init__(self, app, score):
        self.app = app
        self.debug = False

        # Windows 98 BSOD colors
        self.BSOD_BLUE = (0, 0, 170)
        self.BSOD_WHITE = (255, 255, 255)

        # Screen positioning
        self.margin_left = 50 * self.app.scale
        self.line_spacing = 40 * self.app.scale
        self.start_y = 100 * self.app.scale

        # Font setup for that authentic look
        self.font = pygame.font.Font("fonts/Windows98.ttf", int(28 * self.app.scale))
        self.font_bold = pygame.font.Font("fonts/Windows98.ttf", int(32 * self.app.scale))

        # Button setup
        self.buttons = [
            buttons.Button(
                200 * self.app.scale,
                75 * self.app.scale,
                self.app.width / 2 - 100 * self.app.scale,
                self.app.height - 150 * self.app.scale,
                self.font,
                "Reboot",
                'play',
                self.app,
                self.BSOD_BLUE,
                self.BSOD_WHITE
            )
        ]

        self.window = self.app.screen
        self.score = score

        # Format time for display
        self.minutes = str(int(self.score) // 60)
        self.seconds = str(int(self.score) % 60)

        self.attack_types = {
            "Dictionary attack" : "This type of attack uses databases of known words or passwords to find tre correct one",
            "Bruteforce attack" : "This type of attack relies on generating every possible combination of characters to break the users password",
            "Number attack" : "This type of attack works just like bruteforce, with the difference that it only generates sequences of numbers, which makes it much faster",
            "UNKNOWN": "UNKNOWN"
        }

        self.attack_help = {
            "Dictionary attack" : "To prevent this attack, try making your password more unique, add numbers and special characters or try not using words at all",
            "Bruteforce attack" : "This attack is inevitable, you can't do much to stop it except making your password longer",
            "Number attack" : "Try using a combination of letters and numbers instead of just digits",
            "UNKNOWN" : "UNKNOWN"
        }

        self.attack = self.app.inactive_simulation.hack_method if self.app.inactive_simulation.hack_method else 'UNKNOWN'

        # Prepare error messages
        self.error_text = [
            "A fatal exception 0E has occurred at 0028:C0011E36 in VXD VMM(01) +",
            "00010E36. The current process will be terminated.",
            "",
            f"* Time survived before crash: {self.minutes}m {self.seconds}s",
            f"* Attack method: {self.attack}",
            f"* How it works: {self.attack_types[self.attack]}",
            f"* How to prevent it: {self.attack_help[self.attack]}",
            "",
            "SYSTEM HALTED"
        ]

        self.app.newSimulation()

    def render(self):
        # Fill screen with BSOD blue
        self.window.fill(self.BSOD_BLUE)

        # Render main error header
        header = self.font_bold.render("Windows", True, self.BSOD_WHITE)
        self.window.blit(header, (self.margin_left, self.start_y))

        # Render all error messages
        current_y = self.start_y + self.line_spacing * 2
        for line in self.error_text:
            text_surface = self.font.render(line, True, self.BSOD_WHITE)
            self.window.blit(text_surface, (self.margin_left, current_y))
            current_y += self.line_spacing

        # Render button
        for button in self.buttons:
            button.render(self.app.screen)

    def events(self):
        # Handle any events if needed
        pass