import datetime
import random
import configparser
import time

from pygame import mixer

from classes import inputBox
from classes.minesweeper import Minesweeper
from classes.calculator import Calculator
from classes.window import Window
from classes import images
from classes import particles
from classes.buttons import Button
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
        self.font98_small = pygame.font.Font("fonts/Windows98.ttf", 16)
        self.windows = [
            Window(50, 50, 300, 200, "Internet Explorer", self.font98_small, pygame.transform.scale(pygame.image.load('img/InternetExplorer98.png'), (18, 18))),
            Minesweeper(50, 50, 300, 200, "Minesweeper", self.font98_small, pygame.transform.scale(pygame.image.load('img/InternetExplorer98.png'), (18, 18)))]
        self.passwordBox = inputBox.InputBox(self.screen.get_width()//2 - 100, self.screen.get_width()//2 - 225 , 200, 50, self.font)
        self.passwordToCrack = None
        self.side_margin = int(20 * self.app.scale)
        self.widthA = 200
        self.heightA = 300


        self.current_guess = ""
        self.dictionary = []
        self.current_dictionary_index = 0
        f = open("Words.list", "r")
        for line in f:
            self.dictionary.append(line.strip())

        self.dictionary_len = len(self.dictionary)

        # Define taskbar and buttons
        self.taskbar_height = 40
        self.taskbar_color = (192, 192, 192)  # Light gray color for Windows 98 look

        self.start_height = 40
        self.start_color = (192, 192, 192)  # Light gray color for Windows 98 look
        self.button_shadow_color = (10, 10, 10)  # Darker gray for shadow
        self.button_highlight_color = (220, 220, 220)  # Lighter gray for highlight
        self.buttons = [
            Button(90, 30,10, self.screen.get_height() - self.taskbar_height + 5, self.font98,"Start", 'start', self.app, icon='img/win98.png', size=(32,32)),
            Button(190, 30,110, self.screen.get_height() - self.taskbar_height + 5, self.font98,"My Computer", 'mycomputer', self.app, icon='img/MyComputer98.png',size=(32, 32)),
            Button(190, 30,307, self.screen.get_height() - self.taskbar_height + 5, self.font98,"Internet Explorer", 'internetexplorer', self.app, icon='img/InternetExplorer98.png',size=(24, 24)),
            Button(190, 30,503, self.screen.get_height() - self.taskbar_height + 5, self.font98,"Calculator", 'calculator', self.app, icon='img/Calc.png',size=(24, 24))
        ]
        self.active_button = None

        # Load icons
        self.icons = [
            pygame.transform.scale(pygame.image.load('img/win98.png'), (32, 32)),
            pygame.transform.scale(pygame.image.load('img/MyComputer98.png'), (32, 32)),
            pygame.transform.scale(pygame.image.load('img/InternetExplorer98.png'),(24, 24)),  # Ensure icons are the same size
            pygame.transform.scale(pygame.image.load('img/Calc.png'), (24, 24))
        ]

        self.cache_passwords = True
        self.use_cached_passwords = True
        self.passwords_to_cache = []

    def bruteforce2(self): # Assuming the hacker knows the password length
        for n in range(1,10):
            list=[0 for x in range(n)]
            print(list)
            string=""
            run=True
            while run:
                string=""
                for x in range(n):
                    string += chr(list[x] + 32)

                if string==self.passwordToCrack:
                    self.passwordToCrack = None
                    return self.current_guess
                else:
                    print(string)
                    list[0]+=1
                    i=0
                    while True:
                        print(i,n-1)
                        print(list[i])
                        if list[i]>94:
                            list[i]=0
                            if i+1>n-1:
                                run=False
                                print('aaaaaaaaaaaaaaaaaa')
                            else:
                                list[i+1]+=1
                            i += 1
                        else:
                            break

    # O(k^n) k - charset length; n - password length
    def crackPwd(self, prev_char, length_remaining, current_guess):
        if length_remaining == 0:
            self.passwords_to_cache.append(current_guess)
            return current_guess

        for i in range(32, 126):
            t = self.crackPwd(prev_char + 1, length_remaining - 1, current_guess + chr(i))
            if t == self.passwordToCrack:
                return t

    def bruteforce(self): # Assuming the hacker knows the password length
        self.cache_passwords = False
        self.use_cached_passwords = False
        #### Settings changed to false for debugging ####

        # Search cached passwords
        if self.use_cached_passwords:
            f = open("cache/cached_passwords.txt", "r")
            for line in f:
                if line.strip() == self.passwordToCrack:
                    return line

        self.passwords_to_cache = []
        pwd = self.crackPwd(32, len(self.passwordToCrack), "")

        # Save generated passwords
        if self.cache_passwords:
            f = open("cache/cached_passwords.txt", "w")
            for n in self.passwords_to_cache:
                f.write(n+"\n")
            f.close()
        return pwd

    def dictionaryAttack(self):
        print(self.dictionary_len)
        current_dictionary_index = 0
        while True:
            try:
                self.current_guess = self.dictionary[current_dictionary_index]
                print(self.current_guess)
                current_dictionary_index += 1
            except:
                return
            if self.current_guess == self.passwordToCrack:
                self.passwordToCrack = None
                return self.current_guess

    def render(self):
        self.screen.fill(self.bg_color)
        self.passwordBox.update()
        self.passwordBox.draw(self.screen)
        for window in self.windows:
            if window.minimized is False:
                window.draw(self.screen)


        ## Taskbar ##
        pygame.draw.rect(self.screen, self.taskbar_color, (0, self.screen.get_height() - self.taskbar_height, self.screen.get_width(), self.taskbar_height))

        # Draw ridge between buttons
        ridge_x = self.buttons[0].rect.right + 5
        pygame.draw.line(self.screen, (100, 100, 100), (ridge_x, self.screen.get_height() - self.taskbar_height + 5), (ridge_x, self.screen.get_height() - 5), 2)

        # Draw buttons with 3D effect
        for i, button in enumerate(self.buttons):
                button.render(self.screen)

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
            display_text_rect.center = (self.screen.get_width()//2 - 100, self.screen.get_height()//2)
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
                print(self.bruteforce())
                # print(self.dictionaryAttack())
                print("$")
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    for i, button in enumerate(self.buttons):
                        if button.rect.collidepoint(event.pos):
                            print(f"Button {i + 1} clicked")
                            if self.active_button is not None:
                                self.active_button.selected = False
                            button.selected = True
                            self.active_button = button
                            window_already_open = False
                            for window in self.windows:
                                if window.closed:
                                    self.windows.remove(window)
                                if window.title == button.text:
                                    window_already_open = True
                                    window.minimized = False
                                    window.active = True

                            if window_already_open is False:
                                if button.text=="Start":
                                    self.widthA = 200
                                    self.heightA = 300
                                    new_window = Calculator(0, self.app.height - self.heightA - self.taskbar_height, self.widthA, self.heightA, button.text, self.font98_small,
                                                        self.icons[i], self.app)
                                    new_window.draw(self.screen)
                                    new_window.active = True
                                    self.windows.append(new_window)
                                # elif button.text=="Calculator":
                                #     new_window = Calculator(50, 50, 266, 400, self.button_labels[i], self.font98_small,
                                #                         self.icons[i], self.app)
                                elif button.text=="Calculator":
                                    new_window = Calculator(50, 50, 240, 400, button.text, self.font98_small,
                                                        self.icons[i],self.app)
                                    new_window.draw(self.screen)
                                    new_window.active = True
                                    self.windows.append(new_window)
                                else:
                                    new_window = Window(50, 50, 300, 200, button.text, self.font98_small, self.icons[i])
                                    new_window.draw(self.screen)
                                    new_window.active = True
                                    self.windows.append(new_window)
            for window in self.windows:
                window.handle_event(event)