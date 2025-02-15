import pygame
from classes import buttons


class GameOver:
    def __init__(self, app, score):
        self.app = app
        self.debug = False

        self.BSOD_BLUE = (0, 0, 170)
        self.BSOD_WHITE = (255, 255, 255)

        self.margin_left = 50 * self.app.scale
        self.margin_right = self.app.width - (50 * self.app.scale)
        self.line_spacing = 40 * self.app.scale
        self.start_y = 100 * self.app.scale

        self.font = pygame.font.Font("fonts/Windows98.ttf", int(28 * self.app.scale))
        self.font_bold = pygame.font.Font("fonts/Windows98.ttf", int(32 * self.app.scale))

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

        self.minutes = str(int(self.score) // 60)
        self.seconds = str(int(self.score) % 60)

        self.attack_types = {
            "Dictionary attack": "This type of attack uses databases of known words or passwords to find the correct one",
            "Brute force attack": "This type of attack relies on generating every possible combination of characters to break the users password",
            "Number attack": "This type of attack works just like bruteforce, with the difference that it only generates sequences of numbers, which makes it much faster",
            "Known password": "You reset your password to a one that has been previously compromised, which makes it extremely unsafe to use again",
            "FREE RAM": "RAM (Random Access Memory) is a hardware component which is essential for any PC to work. More RAM means better performance",

            "UNKNOWN": "UNKNOWN"
        }

        self.attack_help = {
            "Dictionary attack": "To prevent this attack, try making your password more unique, add numbers and special characters and try not to use words at all",
            "Brute force attack": "This attack is inevitable, you can't do much to stop it except making your password longer and adding special characters",
            "Number attack": "Try using a combination of letters and numbers instead of just digits",
            "Known password": "Try to not re-use passwords",
            "FREE RAM": "Simply don't download RAM. It is a hardware component, so it cannot be acquired digitally. Also try to avoid sketchy websites.",

            "UNKNOWN": "UNKNOWN"
        }

        self.attack = self.app.inactive_simulation.hack_method if self.app.inactive_simulation.hack_method else 'UNKNOWN'

        self.error_text = [
            "A fatal exception 0E has occurred at 0028:C0011E36 in VXD VMM(01) +",
            "00010E36. The current process will be terminated.",
            "",
            f"* Time survived before crash: {self.minutes}m {self.seconds}s",
            f"* Attack method: {self.attack}",
            f"* Attempts: {self.app.inactive_simulation.tries}"
        ]

        # Add wrapped text for attack description and help
        self.error_text.extend(self.wrap_text(f"* How it works: {self.attack_types[self.attack]}", self.font))
        self.error_text.extend(self.wrap_text(f"* How to prevent it: {self.attack_help[self.attack]}", self.font))
        self.error_text.extend(["", "SYSTEM HALTED"])

        self.app.newSimulation()

    def wrap_text(self, text, font):
        """Wrap text to fit within the screen margins."""
        words = text.split(' ')
        lines = []
        current_line = words[0]

        for word in words[1:]:
            test_line = current_line + ' ' + word
            text_surface = font.render(test_line, True, self.BSOD_WHITE)

            if text_surface.get_width() > (self.margin_right - self.margin_left):
                if lines or current_line.startswith('*'):
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
        self.window.fill(self.BSOD_BLUE)

        header = self.font_bold.render("Windows", True, self.BSOD_WHITE)
        self.window.blit(header, (self.margin_left, self.start_y))

        current_y = self.start_y + self.line_spacing * 2
        for line in self.error_text:
            text_surface = self.font.render(line, True, self.BSOD_WHITE)
            self.window.blit(text_surface, (self.margin_left, current_y))
            current_y += self.line_spacing

        for button in self.buttons:
            button.render(self.app.screen)

    def events(self):
        pass