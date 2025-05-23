import time

import pygame
import random
import string
from classes import buttons


class MainMenu:
    def __init__(self, app):
        self.app = app
        self.debug = False

        self.MATRIX_GREEN = (0, 255, 0)
        self.DARK_GREEN = (0, 100, 0)
        self.BLACK = (0, 0, 0)

        self.dictionary = []
        self.current_dictionary_index = 0
        f = open("Dictionaries/Words.list", "r")
        for line in f:
            self.dictionary.append(line.strip())

        self.font = pygame.font.Font("fonts/Windows98.ttf", int(48 * self.app.scale))
        self.font_small = pygame.font.Font("fonts/Windows98.ttf", int(16 * self.app.scale))

        button_width = 200 * self.app.scale
        button_height = 75 * self.app.scale
        self.buttons = [
            buttons.Button(
                button_width,
                button_height,
                self.app.width / 2 - button_width / 2,
                self.app.height / 2 - button_height / 2,
                self.font,
                "Start",
                'play',
                self.app
            )
        ]

        self.CHAR_WIDTH = 20
        self.CHAR_HEIGHT = 20
        self.columns = self.app.width // self.CHAR_WIDTH
        self.matrix_streams = []

        for i in range(self.columns):
            length = random.randint(5, 8)
            self.matrix_streams.append({
                'x': i * self.CHAR_WIDTH,
                'y': random.randint(-200, -100),
                'speed': random.uniform(1, 3),
                'length': length, # Variable length
                'chars': [random.choice(string.ascii_letters + string.digits)
                          for _ in range(length)]
            })

        self.password_chars = list(random.choice(self.dictionary))
        self.current_guess = ['*'] * len(self.password_chars)
        self.crack_position = 0
        self.crack_delay = 15
        self.crack_counter = 0

        self.binary_particles = []
        for _ in range(50):
            self.binary_particles.append({
                'x': random.randint(0, self.app.width),
                'y': random.randint(0, self.app.height),
                'speed': random.uniform(1, 2),
                'char': random.choice(['0', '1']),
                'alpha': random.randint(50, 255)
            })

        self.password_cracked_time = None

    def update_matrix_effect(self):
        for stream in self.matrix_streams:
            stream['y'] += stream['speed']

            if stream['y'] > self.app.height:
                stream['y'] = random.randint(-150, -100)
                stream['speed'] = random.uniform(1, 3)
                stream['length'] = random.randint(5, 7)
                stream['chars'] = [random.choice(string.ascii_letters + string.digits)
                                   for _ in range(stream['length'])]

            if random.random() < 0.1:
                char_index = random.randint(0, len(stream['chars']) - 1)
                stream['chars'][char_index] = random.choice(string.ascii_letters + string.digits)

    def update_password_crack(self):
        self.crack_counter += 1
        if self.crack_counter >= self.crack_delay:
            self.crack_counter = 0
            if self.crack_position < len(self.password_chars):
                if random.random() > 0.7:
                    self.current_guess[self.crack_position] = self.password_chars[self.crack_position]
                    self.crack_position += 1
                else:
                    self.current_guess[self.crack_position] = random.choice(
                        string.ascii_letters + string.digits + string.punctuation)
        self.password_cracked_time = time.time()

    def update_binary_particles(self):
        for particle in self.binary_particles:
            particle['y'] -= particle['speed']
            if particle['y'] < 0:
                particle['y'] = self.app.height
                particle['x'] = random.randint(0, self.app.width)

    def render(self):
        self.app.screen.fill(self.BLACK)

        for stream in self.matrix_streams:
            for i, char in enumerate(stream['chars']):
                char_y = stream['y'] + (i * self.CHAR_HEIGHT)

                if -self.CHAR_HEIGHT <= char_y <= self.app.height:
                    alpha = max(0, min(255, 255 - (i * 25)))
                    color = (self.MATRIX_GREEN[0],
                             self.MATRIX_GREEN[1],
                             self.MATRIX_GREEN[2],
                             alpha)

                    text_surface = self.font_small.render(char, True, color)
                    self.app.screen.blit(text_surface, (stream['x'], char_y))

        for particle in self.binary_particles:
            text_surface = self.font_small.render(particle['char'], True, self.MATRIX_GREEN)
            text_surface.set_alpha(particle['alpha'])
            self.app.screen.blit(text_surface, (particle['x'], particle['y']))

        guess_text = ''.join(self.current_guess)

        if self.current_guess == self.password_chars and self.password_cracked_time + 3 < time.time():
            self.password_chars = list(random.choice(self.dictionary))
            self.current_guess = ['*'] * len(self.password_chars)
            self.crack_position = 0
            self.crack_counter = 0

        text_surface = self.font.render(f"{guess_text}", True, self.MATRIX_GREEN)
        self.app.screen.blit(text_surface, (self.app.width // 2 - text_surface.get_width() // 2, 200))

        title = self.font.render("PASSWORD CRACKER GAME", True, (255, 255, 255))
        self.app.screen.blit(title, (self.app.width // 2 - title.get_width() // 2, 100))

        for button in self.buttons:
            button.render(self.app.screen)

    def events(self):
        self.update_matrix_effect()
        if self.current_guess != self.password_chars:
            self.update_password_crack()
        self.update_binary_particles()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.buttons:
                if button.rect.collidepoint(event.pos):
                    button.click()