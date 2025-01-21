from classes.window import Window
from classes import particles
from pygame import mixer
import pygame
import configparser
import random
import time

class Minesweeper(Window):
    def read_theme_from_ini(self, file_path):
        config = configparser.ConfigParser()
        config.read(file_path)

        theme = {}
        for key, value in config.items('Colors'):
            theme[key] = tuple(map(int, value.split(',')))

        return theme

    def read_settings_from_ini(self, file_path):
        config = configparser.ConfigParser()
        config.read(file_path)
        settings = {}
        for key, value in config.items('Settings'):
            settings[key] = int(value)
        return settings

    def __init__(self, x, y, width, height, title, font, icon):
        theme_file = "AppData/Minesweeper/theme.ini"
        settings_file = "AppData/Minesweeper/settings.ini"
        theme_colors = self.read_theme_from_ini(theme_file)
        settings = self.read_settings_from_ini(settings_file)

        self.ROWS = settings['rows']
        self.COLUMNS = settings['columns']
        self.BOMBS = settings['bombs']
        self.TILE_SIZE = settings['tile_size']
        self.BORDER = settings['border']

        self.main_tile_color = theme_colors['main_tile_color']
        self.covered_tile_color = theme_colors['covered_tile_color']
        self.empty_tile_color = theme_colors['empty_tile_color']
        self.bomb_tile_color = theme_colors['bomb_tile_color']
        self.flagged_tile_color = theme_colors['flagged_tile_color']
        self.BORDER_COLOR = theme_colors['border_color']
        self.font_color = theme_colors['font_color']
        self.ui_color = theme_colors['ui_color']

        self.board = [[0 for _ in range(self.COLUMNS)] for _ in range(self.ROWS)]
        bombs_left = self.BOMBS

        for r in range(self.ROWS):
            for c in range(self.COLUMNS):
                random1 = random.randint(0, 1)
                randomxcoord = random.randint(0, self.COLUMNS - 1)
                randomycoord = random.randint(0, self.ROWS - 1)

                if random1 == 1 and self.board[randomycoord][randomxcoord] == 0 and bombs_left > 0:
                    self.board[randomycoord][randomxcoord] = -1
                    bombs_left -= 1

        self.gameboard = self.board

        x = 0
        y = 0
        for r in self.board:

            for c in r:
                if c != -1:
                    tile = Tile(x, y, 0)
                    self.gameboard[x][y] = tile.calculate_value(self.board, self.ROWS, self.COLUMNS)
                y += 1
            x += 1
            y = 0

        self.WIDTH = (self.COLUMNS) * self.TILE_SIZE
        self.HEIGHT = (self.ROWS) * self.TILE_SIZE
        self.MAIN_HEIGHT = self.HEIGHT + 100

        pygame.font.init()
        mixer.init()

        self.explosion = pygame.mixer.Sound('AppData/Minesweeper/sounds/explosion.mp3')  # argument must be int
        pygame.mixer.music.load('AppData/Minesweeper/sounds/sound.mp3')

        font = pygame.font.Font('fonts/Windows98.ttf', self.TILE_SIZE // 2)

        self.clock = pygame.time.Clock()

        self.particle_group = pygame.sprite.Group()

        self.small_tile_size = int(.75 * self.TILE_SIZE)

        bomb_img = pygame.image.load("AppData/Minesweeper/img/bomb.png").convert_alpha()
        self.bomb_img = pygame.transform.scale(bomb_img, (self.TILE_SIZE, self.TILE_SIZE))

        flag_img = pygame.image.load("AppData/Minesweeper/img/flag.png").convert_alpha()
        self.flag_img = pygame.transform.scale(flag_img, (self.small_tile_size, self.small_tile_size))

        self.img = pygame.image.load("AppData/Minesweeper/img/gameover.jpg").convert()

        self.hidden_board = [[-2 for _ in range(self.COLUMNS)] for i in range(self.ROWS)]
        temp = self.gameboard
        self.gameboard = self.hidden_board
        self.hidden_board = temp
        self.checked_tiles = []

        self.failed = False
        self.render_fail_text = False
        self.solved = False
        self.bombs_left_to_find = self.BOMBS
        self.placed_flags = 0
        self.main_text_message = "Minesweeper"
        self.start_time = time.time()
        self.update_timer = True
        self.display_time = "00 : 00"
        self.animation = False
        self.animation_start_time = None

        super().__init__(x, y, self.WIDTH, self.MAIN_HEIGHT, title, font, icon)

    def draw(self, screen):
        # Update button positions based on the current window position
        window_bg_rect_big = pygame.Rect(self.rect.x - self.window_border_width - 2,
                                         self.rect.y - self.window_border_width - 2,
                                         self.rect.width + self.window_border_width * 2 + 4,
                                         self.rect.height + self.window_border_width + 4)
        window_bg_rect = pygame.Rect(self.rect.x - self.window_border_width, self.rect.y - self.window_border_width,
                                     self.rect.width + self.window_border_width * 2,
                                     self.rect.height + self.window_border_width)
        light_shadow_rect = window_bg_rect.move(-2, -2)
        light_shadow_rect.width += 2
        light_shadow_rect.height += 2
        dark_shadow_rect = window_bg_rect.move(2, 2)

        pygame.draw.rect(screen, self.dark_shadow_color, window_bg_rect_big)
        pygame.draw.rect(screen, self.light_shadow_color, light_shadow_rect)
        pygame.draw.rect(screen, self.dark_shadow_color, dark_shadow_rect)
        pygame.draw.rect(screen, self.border_color, window_bg_rect)

        self.minimize_button = pygame.Rect(
            self.rect.right - 3 * (self.button_width + self.button_spacing) - self.margin,
            self.rect.y + (self.title_bar_height - self.button_height) // 2 + 1, self.button_width, self.button_height)
        self.fullscreen_button = pygame.Rect(
            self.rect.right - 2 * (self.button_width + self.button_spacing) - self.margin,
            self.rect.y + (self.title_bar_height - self.button_height) // 2 + 1, self.button_width, self.button_height)
        self.exit_button = pygame.Rect(self.rect.right - (self.button_width + self.button_spacing),
                                       self.rect.y + (self.title_bar_height - self.button_height) // 2 + 1,
                                       self.button_width, self.button_height)

        # Draw title bar
        if self.active:
            title_bar_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.title_bar_height)
            pygame.draw.rect(screen, self.title_bar_color, title_bar_rect)
        else:
            title_bar_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.title_bar_height)
            pygame.draw.rect(screen, self.title_bar_inactive_color, title_bar_rect)

        icon = self.icon
        icon_rect = icon.get_rect(midleft=(title_bar_rect.left + 5, title_bar_rect.centery))  # Align icon to the left
        screen.blit(icon, icon_rect)

        # Draw title text
        title_surface = self.font.render(self.title, True, self.title_text_color)
        title_rect = title_surface.get_rect(midleft=(icon_rect.right + 5, title_bar_rect.centery))
        screen.blit(title_surface, title_rect)

        # Draw window background
        window_bg_rect = pygame.Rect(self.rect.x, self.rect.y + self.title_bar_height, self.rect.width,
                                     self.rect.height - self.title_bar_height - self.window_border_width)
        pygame.draw.rect(screen, self.bg_color, window_bg_rect)

        # Draw buttons with 3D effect
        self.draw_button(screen, self.minimize_button, 1, 1, self.minimize_icon)
        self.draw_button(screen, self.fullscreen_button, 2, 1, self.fullscreen_icon)
        self.draw_button(screen, self.exit_button, 3, 1, self.exit_icon)

        self.surface.fill((0, 0, 0))



        ##### App Code Starts Here #####

        for r in range(self.ROWS):
            for c in range(self.COLUMNS):
                pygame.draw.rect(self.surface, self.BORDER_COLOR, pygame.Rect(r * self.TILE_SIZE, c * self.TILE_SIZE, self.TILE_SIZE, self.TILE_SIZE))
                if self.gameboard[r][c] == -3:
                    tile_rect = pygame.Rect(r * self.TILE_SIZE + self.BORDER, c * self.TILE_SIZE + self.BORDER, self.TILE_SIZE - self.BORDER,
                                            self.TILE_SIZE - self.BORDER)
                    flag_rect = pygame.Rect(r * self.TILE_SIZE + self.BORDER + (self.TILE_SIZE - self.small_tile_size) / 2,
                                            c * self.TILE_SIZE + self.BORDER + (self.TILE_SIZE - self.small_tile_size) / 2,
                                            self.TILE_SIZE - self.BORDER, self.TILE_SIZE - self.BORDER)
                    pygame.draw.rect(self.surface, self.flagged_tile_color, tile_rect)
                    # text = font.render('!', True, (0, 0, 0), None)
                    # textRect = text.get_rect()
                    # textRect.center = (
                    #     r * TILE_SIZE + BORDER + (TILE_SIZE - BORDER) // 2,
                    #     c * TILE_SIZE + BORDER + (TILE_SIZE - BORDER) // 2)

                    self.surface.blit(self.flag_img, flag_rect)
                if self.gameboard[r][c] == -2:
                    pygame.draw.rect(self.surface, self.covered_tile_color,
                                     pygame.Rect(r * self.TILE_SIZE + self.BORDER, c * self.TILE_SIZE + self.BORDER, self.TILE_SIZE - self.BORDER,
                                                 self.TILE_SIZE - self.BORDER))
                if self.gameboard[r][c] == -1:
                    tile_rect = pygame.Rect(r * self.TILE_SIZE + self.BORDER, c * self.TILE_SIZE + self.BORDER, self.TILE_SIZE - self.BORDER,
                                            self.TILE_SIZE - self.BORDER)
                    pygame.draw.rect(self.surface, self.bomb_tile_color, tile_rect)
                    self.surface.blit(self.bomb_img, tile_rect)
                if self.gameboard[r][c] == 0:
                    pygame.draw.rect(self.surface, self.empty_tile_color,
                                     pygame.Rect(r * self.TILE_SIZE + self.BORDER, c * self.TILE_SIZE + self.BORDER, self.TILE_SIZE - self.BORDER,
                                                 self.TILE_SIZE - self.BORDER))
                if self.gameboard[r][c] == 1:
                    pygame.draw.rect(self.surface, self.main_tile_color,
                                     pygame.Rect(r * self.TILE_SIZE + self.BORDER, c * self.TILE_SIZE + self.BORDER, self.TILE_SIZE - self.BORDER,
                                                 self.TILE_SIZE - self.BORDER))
                    text = self.font.render('1', True, (35, 69, 168), None)
                    textRect = text.get_rect()
                    textRect.center = (r * self.TILE_SIZE + self.BORDER + (self.TILE_SIZE - self.BORDER) // 2,
                                       c * self.TILE_SIZE + self.BORDER + (self.TILE_SIZE - self.BORDER) // 2)
                    self.surface.blit(text, textRect)
                if self.gameboard[r][c] == 2:
                    pygame.draw.rect(self.surface, self.main_tile_color,
                                     pygame.Rect(r * self.TILE_SIZE + self.BORDER, c * self.TILE_SIZE + self.BORDER, self.TILE_SIZE - self.BORDER,
                                                 self.TILE_SIZE - self.BORDER))
                    text = self.font.render('2', True, (35, 107, 22), None)
                    textRect = text.get_rect()
                    textRect.center = (
                        r * self.TILE_SIZE + self.BORDER + (self.TILE_SIZE - self.BORDER) // 2,
                        c * self.TILE_SIZE + self.BORDER + (self.TILE_SIZE - self.BORDER) // 2)
                    self.surface.blit(text, textRect)
                if self.gameboard[r][c] == 3:
                    pygame.draw.rect(self.surface, self.main_tile_color,
                                     pygame.Rect(r * self.TILE_SIZE + self.BORDER, c * self.TILE_SIZE + self.BORDER, self.TILE_SIZE - self.BORDER,
                                                 self.TILE_SIZE - self.BORDER))
                    text = self.font.render('3', True, (107, 22, 22), None)
                    textRect = text.get_rect()
                    textRect.center = (
                        r * self.TILE_SIZE + self.BORDER + (self.TILE_SIZE - self.BORDER) // 2,
                        c * self.TILE_SIZE + self.BORDER + (self.TILE_SIZE - self.BORDER) // 2)
                    self.surface.blit(text, textRect)
                if self.gameboard[r][c] == 4:
                    pygame.draw.rect(self.surface, self.main_tile_color,
                                     pygame.Rect(r * self.TILE_SIZE + self.BORDER, c * self.TILE_SIZE + self.BORDER, self.TILE_SIZE - self.BORDER,
                                                 self.TILE_SIZE - self.BORDER))
                    text = self.font.render('4', True, (7, 7, 48), None)
                    textRect = text.get_rect()
                    textRect.center = (
                        r * self.TILE_SIZE + self.BORDER + (self.TILE_SIZE - self.BORDER) // 2,
                        c * self.TILE_SIZE + self.BORDER + (self.TILE_SIZE - self.BORDER) // 2)
                    self.surface.blit(text, textRect)
                if self.gameboard[r][c] == 5:
                    pygame.draw.rect(self.surface, self.main_tile_color,
                                     pygame.Rect(r * self.TILE_SIZE + self.BORDER, c * self.TILE_SIZE + self.BORDER, self.TILE_SIZE - self.BORDER,
                                                 self.TILE_SIZE - self.BORDER))
                    text = self.font.render('5', True, (105, 50, 19), None)
                    textRect = text.get_rect()
                    textRect.center = (
                        r * self.TILE_SIZE + self.BORDER + (self.TILE_SIZE - self.BORDER) // 2,
                        c * self.TILE_SIZE + self.BORDER + (self.TILE_SIZE - self.BORDER) // 2)
                    self.surface.blit(text, textRect)
                if self.gameboard[r][c] > 5:
                    pygame.draw.rect(self.surface, self.main_tile_color,
                                     pygame.Rect(r * self.TILE_SIZE + self.BORDER, c * self.TILE_SIZE + self.BORDER, self.TILE_SIZE - self.BORDER,
                                                 self.TILE_SIZE - self.BORDER))
                    text = self.font.render(str(self.gameboard[r][c]), True, (40, 173, 142), None)
                    textRect = text.get_rect()
                    textRect.center = (
                        r * self.TILE_SIZE + self.BORDER + (self.TILE_SIZE - self.BORDER) // 2,
                        c * self.TILE_SIZE + self.BORDER + (self.TILE_SIZE - self.BORDER) // 2)
                    self.surface.blit(text, textRect)

        if self.update_timer:
            current_time = time.time()
            timer_time = current_time - self.start_time
            minutes = int(timer_time // 60)
            seconds = int(timer_time % 60)
            self.display_time = f'{minutes:02d} : {seconds:02d}'

        main_text = self.font.render(self.main_text_message, True, self.font_color, None)
        main_textRect = main_text.get_rect()
        main_textRect.center = (
            self.WIDTH // 2,
            self.MAIN_HEIGHT - 50)
        self.surface.blit(main_text, main_textRect)

        timer_text = self.font.render(self.display_time, True, self.font_color, None)
        timer_textRect = timer_text.get_rect()
        timer_textRect.center = (
            self.WIDTH // 2 - 200,
            self.MAIN_HEIGHT - 50)
        self.surface.blit(timer_text, timer_textRect)

        flag_text = self.font.render(f'Flags: {self.placed_flags}/{self.BOMBS}', True, self.font_color, None)
        flag_textRect = flag_text.get_rect()
        flag_textRect.center = (
            self.WIDTH // 2 + 200,
            self.MAIN_HEIGHT - 50)
        self.surface.blit(flag_text, flag_textRect)

        delta_time = self.clock.tick() / 1000

        self.particle_group.draw(self.surface)

        self.particle_group.update(delta_time)

        screen.blit(self.surface, (self.rect.x, self.rect.y + self.title_bar_height))

    def draw_empty_tiles(self, point):
        x = point[0]
        y = point[1]
        tiles_to_check = []
        if x - 1 >= 0:
            if self.board[x - 1][y] == 0:
                self.gameboard[x - 1][y] = 0
                tiles_to_check.append((x - 1, y))
            if self.board[x - 1][y] > 0:
                self.gameboard[x - 1][y] = self.board[x - 1][y]
        if x + 1 < self.ROWS:
            if self.board[x + 1][y] == 0:
                self.gameboard[x + 1][y] = 0
                tiles_to_check.append((x + 1, y))
            if self.board[x + 1][y] > 0:
                self.gameboard[x + 1][y] = self.board[x + 1][y]
        if x + 1 < self.ROWS and y + 1 < self.COLUMNS:
            if self.board[x + 1][y + 1] == 0:
                self.gameboard[x + 1][y + 1] = 0
                tiles_to_check.append((x + 1, y + 1))
            if self.board[x + 1][y + 1] > 0:
                self.gameboard[x + 1][y + 1] = self.board[x + 1][y + 1]
        if x - 1 >= 0 and y - 1 >= 0:
            if self.board[x - 1][y - 1] == 0:
                self.gameboard[x - 1][y - 1] = 0
                tiles_to_check.append((x - 1, y - 1))
            if self.board[x - 1][y - 1] > 0:
                self.gameboard[x - 1][y - 1] = self.board[x - 1][y - 1]
        if x + 1 < self.ROWS and y - 1 >= 0:
            if self.board[x + 1][y - 1] == 0:
                self.gameboard[x + 1][y - 1] = 0
                tiles_to_check.append((x + 1, y - 1))
            if self.board[x + 1][y - 1] > 0:
                self.gameboard[x + 1][y - 1] = self.board[x + 1][y - 1]
        if x - 1 >= 0 and y + 1 < self.COLUMNS:
            if self.board[x - 1][y + 1] == 0:
                self.gameboard[x - 1][y + 1] = 0
                tiles_to_check.append((x - 1, y + 1))
            if self.board[x - 1][y + 1] > 0:
                self.gameboard[x - 1][y + 1] = self.board[x - 1][y + 1]
        if y + 1 < self.COLUMNS:
            if self.board[x][y + 1] == 0:
                self.gameboard[x][y + 1] = 0
                tiles_to_check.append((x, y + 1))
            if self.board[x][y + 1] > 0:
                self.gameboard[x][y + 1] = self.board[x][y + 1]
        if y - 1 >= 0:
            if self.board[x][y - 1] == 0:
                self.gameboard[x][y - 1] = 0
                tiles_to_check.append((x, y - 1))
            if self.board[x][y - 1] > 0:
                self.gameboard[x][y - 1] = self.board[x][y - 1]
        self.checked_tiles.append(point)
        return tiles_to_check

    def handle_event(self, event):
        super().handle_event(event)

        if event.type == pygame.KEYDOWN:
            if self.failed or self.solved:
                self.board = [[0 for _ in range(self.COLUMNS)] for _ in range(self.ROWS)]
                bombs_left = self.BOMBS

                for r in range(self.ROWS):
                    for c in range(self.COLUMNS):
                        random1 = random.randint(0, 1)
                        randomxcoord = random.randint(0, self.COLUMNS - 1)
                        randomycoord = random.randint(0, self.ROWS - 1)

                        if random1 == 1 and self.board[randomycoord][randomxcoord] == 0 and bombs_left > 0:
                            self.board[randomycoord][randomxcoord] = -1
                            bombs_left -= 1
                self.gameboard = self.board
                x = 0
                y = 0
                for r in self.board:

                    for c in r:
                        if c != -1:
                            tile = Tile(x, y, 0)
                            self.gameboard[x][y] = tile.calculate_value(self.board, self.ROWS, self.COLUMNS)
                        y += 1
                    x += 1
                    y = 0

                self.WIDTH = (self.COLUMNS) * self.TILE_SIZE
                self.HEIGHT = (self.ROWS) * self.TILE_SIZE

                self.hidden_board = [[-2 for _ in range(self.COLUMNS)] for i in range(self.ROWS)]
                temp = self.gameboard
                self.gameboard = self.hidden_board
                self.hidden_board = temp

                self.checked_tiles = []
                self.main_text_message = "Minesweeper"
                self.failed = False
                self.solved = False
                self.bombs_left_to_find = self.BOMBS
                self.placed_flags = 0
                self.update_timer = True
                self.render_fail_text = False
                self.display_time = "00 : 00"
                self.start_time = time.time()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.failed:
                    if self.render_fail_text:
                        self.render_fail_text = False
                        self.main_text_message = "Press any key to restart"
                    else:
                        Mouse_x, Mouse_y = pygame.mouse.get_pos()
                        clicked_row = round((Mouse_y - self.rect.topleft[1]) / self.TILE_SIZE) - 1
                        clicked_column = int((Mouse_x - self.rect.topleft[0]) / self.TILE_SIZE)
                        if clicked_column >= self.COLUMNS or clicked_row >= self.ROWS or clicked_row < 0 or clicked_column < 0:
                            return
                        if self.gameboard[clicked_column][clicked_row] == -3:
                            return
                        if self.hidden_board[clicked_column][clicked_row] == -1:

                            self.gameboard[clicked_column][clicked_row] = self.hidden_board[clicked_column][clicked_row]
                            self.hidden_board[clicked_column][clicked_row] = -5
                            self.explode(Mouse_x - self.rect.x, Mouse_y - self.rect.y - self.title_bar_height)
                else:
                    Mouse_x, Mouse_y = pygame.mouse.get_pos()
                    clicked_row = round((Mouse_y - self.rect.topleft[1]) / self.TILE_SIZE) - 1
                    clicked_column = int((Mouse_x - self.rect.topleft[0]) / self.TILE_SIZE)
                    if clicked_column >= self.COLUMNS or clicked_row >= self.ROWS or clicked_row < 0 or clicked_column < 0:
                        return
                    if self.gameboard[clicked_column][clicked_row] == -3:
                        return
                    self.gameboard[clicked_column][clicked_row] = self.hidden_board[clicked_column][clicked_row]
                    if self.gameboard[clicked_column][clicked_row] == -1:

                        self.hidden_board[clicked_column][clicked_row] = -5
                        # running = False
                        self.failed = True
                        self.main_text_message = "Your computer has exploded!"
                        self.update_timer = False
                        self.explode(Mouse_x - self.rect.x, Mouse_y - self.rect.y - self.title_bar_height)
                        self.animation = True
                        self.animation_start_time = time.time()

                    if self.gameboard[clicked_column][clicked_row] == 0:
                        print(clicked_row)
                        empty_list = self.draw_empty_tiles((clicked_column, clicked_row))
                        while empty_list != []:
                            new_empty_list = []
                            for coord in empty_list:
                                if coord not in self.checked_tiles:
                                    temp_list = self.draw_empty_tiles(coord)
                                    for coordinate in temp_list:
                                        new_empty_list.append(coordinate)
                            empty_list = new_empty_list

            if event.button == 3:
                Mouse_x, Mouse_y = pygame.mouse.get_pos()
                clicked_row = round((Mouse_y - self.rect.topleft[1]) / self.TILE_SIZE) - 1
                clicked_column = int((Mouse_x - self.rect.topleft[0]) / self.TILE_SIZE)
                if clicked_column >= self.COLUMNS or clicked_row >= self.ROWS or clicked_row < 0 or clicked_column < 0:
                    return
                if not self.failed:
                    if self.gameboard[clicked_column][clicked_row] == -3:
                        self.gameboard[clicked_column][clicked_row] = -2
                        self.placed_flags -= 1
                    elif self.gameboard[clicked_column][
                        clicked_row] == -2:  # and placed_flags < BOMBS # bug when revealing map segment on which a flag is already standing
                        self.gameboard[clicked_column][clicked_row] = -3
                        self.placed_flags += 1
        if self.placed_flags == self.BOMBS:
            correct = 0
            for r in range(self.ROWS):
                for c in range(self.COLUMNS):
                    if self.gameboard[r][c] == -2:
                        break
                    if self.board[r][c] == -1 and self.gameboard[r][c] == -3:
                        correct += 1
            if correct == self.BOMBS and self.solved is False:
                Mouse_x, Mouse_y = pygame.mouse.get_pos()
                self.solved = True
                self.confetti(Mouse_x - self.rect.x, Mouse_y - self.rect.y - self.title_bar_height)
                self.main_text_message = "Congrats! You beat the game!"
                self.update_timer = False

    def explode(self, Mouse_x, Mouse_y):
        self.explosion.play()
        for _ in range(2024):
            color = random.choice(((227, 23, 10), (225, 96, 54), (234, 196, 53), (42, 45, 52)))
            direction = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
            direction = direction.normalize()
            speed = random.randint(60, 400)
            particles.Particle(self.particle_group, (Mouse_x, Mouse_y), color, direction, speed)
        for _ in range(2024):
            color = random.choice(((227, 23, 10), (225, 96, 54), (234, 196, 53), (42, 45, 52)))
            direction = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
            direction = direction.normalize()
            speed = random.randint(400, 700)
            particles.Particle(self.particle_group, (Mouse_x, Mouse_y), color, direction, speed)

    def confetti(self, Mouse_x, Mouse_y):
        mixer.music.play()
        for _ in range(2024):
            color = random.choice(((48, 188, 237), (123, 201, 80), (255, 184, 0), (244, 91, 105)))
            direction = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
            direction = direction.normalize()
            speed = random.randint(60, 300)
            particles.Particle(self.particle_group, (Mouse_x, Mouse_y), color, direction, speed)
        for _ in range(2024):
            color = random.choice(((48, 188, 237), (123, 201, 80), (255, 184, 0), (244, 91, 105)))
            direction = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
            direction = direction.normalize()
            speed = random.randint(400, 600)
            particles.Particle(self.particle_group, (Mouse_x, Mouse_y), color, direction, speed)


class Tile:
    def __init__(self,x ,y, value):
        self.x = x
        self.y = y
        self.value = value
        self.revealed = False
        self.flagged = False

    def calculate_value(self, board, ROWS, COLUMNS):
        neighbouring_mines = 0
        x = self.x
        y = self.y

        if x - 1 >= 0 and board[x - 1][y] == -1:
            neighbouring_mines += 1
        if x + 1 < ROWS and board[x + 1][y] == -1:
            neighbouring_mines += 1
        if x + 1 < ROWS and y + 1 < COLUMNS and board[x + 1][y + 1] == -1:
            neighbouring_mines += 1
        if x - 1 >= 0 and y - 1 >= 0 and board[x - 1][y - 1] == -1:
            neighbouring_mines += 1
        if x + 1 < ROWS and y - 1 >= 0 and board[x + 1][y - 1] == -1:
            neighbouring_mines += 1
        if x - 1 >= 0 and y + 1 < COLUMNS and board[x - 1][y + 1] == -1:
            neighbouring_mines += 1
        if y + 1 < COLUMNS and board[x][y + 1] == -1:
            neighbouring_mines += 1
        if y - 1 >= 0 and board[x][y - 1] == -1:
            neighbouring_mines += 1

        self.value = neighbouring_mines
        return neighbouring_mines