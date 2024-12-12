import datetime
import random

from classes import inputBox
import pygame

class Simulation:
    def __init__(self, app):
        self.app = app
        self.debug = False
        self.bg_color = (0, 142, 144)
        self.screen = self.app.screen
        self.buttons = []
        self.font = pygame.font.SysFont("Arial", 32)
        self.font98 = pygame.font.Font("fonts/Windows98.ttf", 24)
        self.passwordBox = inputBox.InputBox(300, 150 , 200, 50, self.font)
        self.passwordToCrack = None
        self.side_margin = int(20 * self.app.scale)

        self.selected_button = None
        self.current_guess = ""
        self.dictionary = []
        self.current_dictionary_index = 0
        f = open("Words.list", "r")
        for line in f:
            self.dictionary.append(line.strip())

        # Define taskbar and buttons
        self.taskbar_height = 40
        self.taskbar_color = (192, 192, 192)  # Light gray color for Windows 98 look
        self.button_color = (160, 160, 160)  # Slightly darker gray for buttons
        self.button_hover_color = (128, 128, 128)  # Even darker gray for hover effect
        self.button_shadow_color = (10, 10, 10)  # Darker gray for shadow
        self.button_highlight_color = (220, 220, 220)  # Lighter gray for highlight
        self.buttons = [
            pygame.Rect(10, self.screen.get_height() - self.taskbar_height + 5, 90, 30),  # Start button
            pygame.Rect(110, self.screen.get_height() - self.taskbar_height + 5, 190, 30),  # My Computer button
            pygame.Rect(307, self.screen.get_height() - self.taskbar_height + 5, 190, 30)  # Internet Explorer button
        ]
        self.button_labels = ["Start", "My Computer", "Internet Explorer"]

        # Load icons
        self.icons = [
            pygame.transform.scale(pygame.image.load('img/win98.png'), (32, 32)),
            pygame.transform.scale(pygame.image.load('img/MyComputer98.png'), (32, 32)),
            pygame.transform.scale(pygame.image.load('img/InternetExplorer98.png'), (24, 24))  # Ensure icons are the same size
        ]

    def bruteforce(self): # Assuming the hacker knows the password length
        while True:
            self.current_guess = ""
            for i in range(len(self.passwordToCrack)):
                self.current_guess += chr(random.randint(97,122))

            if self.current_guess == self.passwordToCrack:
                self.passwordToCrack = None
                return self.current_guess
    def dictionaryAttack(self):
        while True:
            self.current_guess = self.dictionary[self.current_dictionary_index]
            self.current_dictionary_index += 1
            if self.current_guess == self.passwordToCrack:
                self.passwordToCrack = None
                return self.current_guess

    def render(self):
        self.screen.fill(self.bg_color)
        self.passwordBox.update()
        self.passwordBox.draw(self.screen)

        ## Taskbar ##
        pygame.draw.rect(self.screen, self.taskbar_color, (0, self.screen.get_height() - self.taskbar_height, self.screen.get_width(), self.taskbar_height))

        # Draw ridge between buttons
        ridge_x = self.buttons[0].right + 5
        pygame.draw.line(self.screen, (100, 100, 100), (ridge_x, self.screen.get_height() - self.taskbar_height + 5), (ridge_x, self.screen.get_height() - 5), 2)

        # Draw buttons with 3D effect
        for i, button in enumerate(self.buttons):
            mouse_pos = pygame.mouse.get_pos()
            if button.collidepoint(mouse_pos) or i == self.selected_button:
                # Caved-in effect
                shadow_rect = button.move(-2, -2)
                pygame.draw.rect(self.screen, self.button_hover_color, shadow_rect)
                highlight_rect = button.move(2, 2)
                pygame.draw.rect(self.screen, self.button_hover_color, highlight_rect)
                pygame.draw.rect(self.screen, self.button_color, button)
            else:
                # Normal button
                shadow_rect = button.move(2, 2)
                pygame.draw.rect(self.screen, self.button_shadow_color, shadow_rect)
                highlight_rect = button.move(-2, -2)
                pygame.draw.rect(self.screen, self.button_highlight_color, highlight_rect)
                pygame.draw.rect(self.screen, self.button_color, button)

            # Draw icon aligned to the left
            icon = self.icons[i]
            icon_rect = icon.get_rect(midleft=(button.left + 5, button.centery))  # Align icon to the left
            self.screen.blit(icon, icon_rect)

            # Draw label centered
            label = self.font98.render(self.button_labels[i], True, (0, 0, 0))
            label_rect = label.get_rect(midleft=(icon_rect.right + 5, button.centery))  # Adjust label position
            self.screen.blit(label, label_rect)

        # Draw clock with caved-in effect
        clock_rect = pygame.Rect(self.screen.get_width() - 110, self.screen.get_height() - self.taskbar_height + 5, 100, 30)
        pygame.draw.rect(self.screen, self.button_shadow_color, clock_rect.move(-2, -2))  # Shadow

        pygame.draw.rect(self.screen, self.button_highlight_color, clock_rect.move(2, 2))  # Highlight
        pygame.draw.rect(self.screen, self.taskbar_color, clock_rect)  # Same background color


        current_time = datetime.datetime.now().strftime("%H:%M")
        clock_surface = self.font98.render(current_time, True, (0, 0, 0))
        clock_text_rect = clock_surface.get_rect(center=clock_rect.center)
        self.screen.blit(clock_surface, clock_text_rect)

        ## Text ##
        if self.passwordToCrack is not None:
            #self.bruteforce()
            #self.dictionaryAttack()
            display_text = self.font.render(self.current_guess, True, (200, 200, 200))
            display_text_rect = display_text.get_rect()
            display_text_rect.center = (300, 300)
            self.app.screen.blit(display_text, display_text_rect)
            self.current_guess = ""

    # Overrides the default events function in app.py
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.app.run = False
                pygame.quit()
            isSubmittedPassword = self.passwordBox.handle_event(event)
            if isSubmittedPassword:
                self.passwordToCrack = self.passwordBox.text
                #print(self.bruteforce())
                print(self.dictionaryAttack())
                print("$")
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    pass
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    for i, button in enumerate(self.buttons):
                        if button.collidepoint(event.pos):
                            print(f"Button {i + 1} clicked")
                            self.selected_button = i