import random

from classes import inputBox
import pygame

class Simulation:
    def __init__(self, app):
        self.app = app
        self.debug = False
        self.bg_color = (33, 33, 33)
        self.screen = self.app.screen
        self.buttons = []
        self.font = pygame.font.SysFont("Arial", 32)
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

    def bruteforce(self): # Assuming the hacker knows the password length
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

        ## Text ##
        if self.passwordToCrack is not None:
            #self.bruteforce()
            self.dictionaryAttack()
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
                #self.bruteforce()
                print(self.dictionaryAttack())
                print("$")
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    pass