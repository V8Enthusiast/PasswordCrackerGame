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
        self.font98_small = pygame.font.Font("fonts/Windows98.ttf", 16)
        self.windows = [
            Window(50, 50, 300, 200, "Internet Explorer", self.font98_small, pygame.transform.scale(pygame.image.load('img/InternetExplorer98.png'), (18, 18))), Minesweeper(50, 50, 300, 200, "Minesweeper", self.font98_small, pygame.transform.scale(pygame.image.load('img/InternetExplorer98.png'), (18, 18)))]
        self.passwordBox = inputBox.InputBox(self.screen.get_width()//2 - 100, self.screen.get_width()//2 - 225 , 200, 50, self.font)
        self.passwordToCrack = None
        self.side_margin = int(20 * self.app.scale)

        self.selected_button = None
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
        self.button_color = (160, 160, 160)  # Slightly darker gray for buttons
        self.button_hover_color = (128, 128, 128)  # Even darker gray for hover effect
        self.button_shadow_color = (10, 10, 10)  # Darker gray for shadow
        self.button_highlight_color = (220, 220, 220)  # Lighter gray for highlight
        self.buttons = [
            pygame.Rect(10, self.screen.get_height() - self.taskbar_height + 5, 90, 30),  # Start button
            pygame.Rect(110, self.screen.get_height() - self.taskbar_height + 5, 190, 30),  # My Computer button
            pygame.Rect(307, self.screen.get_height() - self.taskbar_height + 5, 190, 30),
            pygame.Rect(503, self.screen.get_height() - self.taskbar_height + 5, 190, 30)# Internet Explorer button
        ]
        self.button_labels = ["Start", "My Computer", "Internet Explorer","Calculator"]

        # Load icons
        self.icons = [
            pygame.transform.scale(pygame.image.load('img/win98.png'), (32, 32)),
            pygame.transform.scale(pygame.image.load('img/MyComputer98.png'), (32, 32)),
            pygame.transform.scale(pygame.image.load('img/InternetExplorer98.png'), (24, 24)) , # Ensure icons are the same size
            pygame.transform.scale(pygame.image.load('img/InternetExplorer98.png'), (24, 24))
            # Ensure icons are the same size
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
        for window in self.windows:
            if window.minimized is False:
                window.draw(self.screen)
        self.passwordBox.update()
        self.passwordBox.draw(self.screen)

        ## Taskbar ##
        pygame.draw.rect(self.screen, self.taskbar_color, (0, self.screen.get_height() - self.taskbar_height, self.screen.get_width(), self.taskbar_height))

        # Draw ridge between buttons
        ridge_x = self.buttons[0].right + 5
        pygame.draw.line(self.screen, (100, 100, 100), (ridge_x, self.screen.get_height() - self.taskbar_height + 5), (ridge_x, self.screen.get_height() - 5), 2)

        # Draw buttons with 3D effect
        for i, button in enumerate(self.buttons):
            #mouse_pos = pygame.mouse.get_pos()
            #if button.collidepoint(mouse_pos) or i == self.selected_button: # Hovering over the button selects it
            if i == self.selected_button:
                # Caved-in effect

                shadow_rect = button.move(-2, -2)
                shadow_rect.width += 2
                shadow_rect.height += 2
                pygame.draw.rect(self.screen, self.button_shadow_color, shadow_rect)
                highlight_rect = button.move(0, 0)
                highlight_rect.width += 2
                highlight_rect.height += 2

                pygame.draw.rect(self.screen,  self.button_highlight_color, highlight_rect)
                pygame.draw.rect(self.screen, self.button_color, button)
            else:
                # Normal button
                shadow_rect = button.move(0,0)
                shadow_rect.width += 2
                shadow_rect.height += 2
                pygame.draw.rect(self.screen, self.button_shadow_color, shadow_rect)
                highlight_rect = button.move(-2, -2)
                highlight_rect.width += 2
                highlight_rect.height += 2
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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    pass
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    for i, button in enumerate(self.buttons):
                        if button.collidepoint(event.pos):
                            print(f"Button {i + 1} clicked")
                            self.selected_button = i
                            window_already_open = False
                            for window in self.windows:
                                if window.closed:
                                    self.windows.remove(window)
                                if window.title == self.button_labels[i]:
                                    window_already_open = True
                                    window.minimized = False
                                    window.active = True
                            if window_already_open is False:
                                if self.button_labels[i]=="Calculator":
                                    new_window = Calculator(50, 50, 266, 400, self.button_labels[i], self.font98_small,
                                                        self.icons[i])
                                    new_window.draw(self.screen)
                                    new_window.active = True
                                    self.windows.append(new_window)
                                else:

                                    new_window = Window(50, 50, 300, 200, self.button_labels[i], self.font98_small, self.icons[i])
                                    new_window.draw(self.screen)
                                    new_window.active = True
                                    self.windows.append(new_window)
            for window in self.windows:
                window.handle_event(event)


class Window:
    def __init__(self, x, y, width, height, title, font, icon):
        self.rect = pygame.Rect(x, y, width, height)
        self.title = title
        self.font = font
        self.icon = icon
        self.title_bar_height = 25
        self.bg_color = (192, 192, 192)  # Light gray for Windows 98 look
        self.title_bar_color = (0, 0, 128)  # Dark blue for title bar
        self.title_bar_inactive_color = (128, 128, 128)
        self.title_text_color = (255, 255, 255)  # White for title text
        self.border_color = (160, 160, 160) # Black for window border
        self.light_shadow_color = (220, 220, 220)
        self.dark_shadow_color = (10, 10, 10)
        self.button_color = (168, 160, 160)

        self.active = False
        self.minimized = False
        self.dragging = False
        self.selected_button = None
        self.offset_x = 0
        self.offset_y = 0
        self.closed = False

        # Button size and spacing
        self.button_width = 16
        self.button_height = 16
        self.button_spacing = 4
        self.margin = 3
        self.window_border_width = 3

        # Load icons
        self.minimize_icon = pygame.transform.scale(pygame.image.load('img/minimize.png'), (18, 18))
        self.fullscreen_icon = pygame.transform.scale(pygame.image.load('img/maximize.png'), (18, 18))
        self.exit_icon = pygame.transform.scale(pygame.image.load('img/close.png'), (18, 18))

        self.surface = pygame.Surface((width, height - self.title_bar_height - self.margin))

    def draw(self, screen):
        # Update button positions based on the current window position
        window_bg_rect_big = pygame.Rect(self.rect.x - self.window_border_width -2, self.rect.y - self.window_border_width - 2, self.rect.width + self.window_border_width * 2 + 4,self.rect.height + self.window_border_width +4)
        window_bg_rect = pygame.Rect(self.rect.x - self.window_border_width, self.rect.y - self.window_border_width, self.rect.width + self.window_border_width * 2,self.rect.height + self.window_border_width)
        light_shadow_rect = window_bg_rect.move(-2, -2)
        light_shadow_rect.width += 2
        light_shadow_rect.height += 2
        dark_shadow_rect = window_bg_rect.move(2, 2)

        pygame.draw.rect(screen, self.dark_shadow_color,window_bg_rect_big)
        pygame.draw.rect(screen, self.light_shadow_color, light_shadow_rect)
        pygame.draw.rect(screen, self.dark_shadow_color, dark_shadow_rect)
        pygame.draw.rect(screen, self.border_color, window_bg_rect)

        self.minimize_button = pygame.Rect(self.rect.right - 3 * (self.button_width + self.button_spacing) - self.margin, self.rect.y + (self.title_bar_height - self.button_height)//2 + 1, self.button_width, self.button_height)
        self.fullscreen_button = pygame.Rect(self.rect.right - 2 * (self.button_width + self.button_spacing) - self.margin, self.rect.y + (self.title_bar_height - self.button_height)//2 + 1, self.button_width, self.button_height)
        self.exit_button = pygame.Rect(self.rect.right - (self.button_width + self.button_spacing), self.rect.y + (self.title_bar_height - self.button_height)//2 + 1, self.button_width, self.button_height)


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
        window_bg_rect = pygame.Rect(self.rect.x, self.rect.y + self.title_bar_height, self.rect.width, self.rect.height - self.title_bar_height - self.window_border_width)
        pygame.draw.rect(screen, self.bg_color, window_bg_rect)

        # Draw buttons with 3D effect
        self.draw_button(screen, self.minimize_button, 1, 1, self.minimize_icon)
        self.draw_button(screen, self.fullscreen_button, 2, 1, self.fullscreen_icon)
        self.draw_button(screen, self.exit_button, 3, 1, self.exit_icon)

        screen.blit(self.surface, (self.rect.x, self.rect.y + self.title_bar_height))

    def draw_button(self, screen, button_rect, button_id, shadow_width, icon):

        if button_id == self.selected_button:
            # Caved-in effect
            shadow_rect = button_rect.move(-shadow_width, -shadow_width)
            shadow_rect.width += shadow_width
            shadow_rect.height += shadow_width
            pygame.draw.rect(screen, self.dark_shadow_color, shadow_rect)
            highlight_rect = button_rect.move(0, 0)
            highlight_rect.width += shadow_width
            highlight_rect.height += shadow_width

            pygame.draw.rect(screen, self.light_shadow_color, highlight_rect)
            pygame.draw.rect(screen, self.button_color, button_rect)
        else:
            # Normal button
            shadow_rect = button_rect.move(0, 0)
            shadow_rect.width += shadow_width
            shadow_rect.height += shadow_width
            pygame.draw.rect(screen, self.dark_shadow_color, shadow_rect)
            highlight_rect = button_rect.move(-shadow_width, -shadow_width)
            highlight_rect.width += shadow_width
            highlight_rect.height += shadow_width
            pygame.draw.rect(screen, self.light_shadow_color, highlight_rect)
            pygame.draw.rect(screen, self.button_color, button_rect)

        # # Draw shadow and highlight for 3D effect
        # shadow_rect = button_rect.move(2, 2)
        # pygame.draw.rect(screen, (10, 10, 10), shadow_rect)  # Shadow
        # highlight_rect = button_rect.move(-2, -2)
        # highlight_rect.width += 2
        # highlight_rect.height += 2
        # pygame.draw.rect(screen, (220, 220, 220), highlight_rect)  # Highlight
        # pygame.draw.rect(screen, (160, 160, 160), button_rect)  # Button color

        # Draw icon centered in the button
        icon_rect = icon.get_rect(center=highlight_rect.center)
        screen.blit(icon, icon_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.draggable_area().collidepoint(event.pos):
                self.dragging = True
                self.offset_x = self.rect.x - event.pos[0]
                self.offset_y = self.rect.y - event.pos[1]
            elif self.minimize_button.collidepoint(event.pos):
                print("Minimize button clicked")
                self.selected_button = 1
                self.minimized = True
            elif self.fullscreen_button.collidepoint(event.pos):
                print("Fullscreen button clicked")
                self.selected_button = 2
                self.rect.width = 1200
                self.rect.height = 900
                self.surface = pygame.Surface((self.rect.width, self.rect.height-self.title_bar_height-self.margin))
                self.rect.x = 0
                self.rect.y = 0
                # Implement fullscreen functionality
            elif self.exit_button.collidepoint(event.pos):

                print("Exit button clicked")
                self.selected_button = 3
                self.minimized = True
                self.closed = True



            else:
                self.selected_button = None

            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False

        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
            self.selected_button = None

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.rect.x = event.pos[0] + self.offset_x
                self.rect.y = event.pos[1] + self.offset_y

    def draggable_area(self):
        # Define the draggable area excluding the button area
        return pygame.Rect(self.rect.x, self.rect.y, self.rect.width - 3 * (self.button_width + self.button_spacing), self.title_bar_height)
class Calculator(Window):
    def __init__(self, x, y, width, height, title, font, icon):
        super().__init__(x, y, width, height, title, font, icon)
        self.current_string="8*8"
        self.font2=pygame.font.Font("fonts\\Windows98.ttf",32)
        self.current_text = self.font2.render(self.current_string,True,(255,255,255))
        self.current_text_rect=self.current_text.get_rect()
        self.x=x
        self.y=y

        self.current_text_rect.center=(self.x//2,self.y//2)
    def draw(self,screen):
        super().draw(screen)
        self.surface.blit(self.current_text,self.current_text_rect)
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.draggable_area().collidepoint(event.pos):
                self.dragging = True
                self.offset_x = self.rect.x - event.pos[0]
                self.offset_y = self.rect.y - event.pos[1]
            elif self.minimize_button.collidepoint(event.pos):
                print("Minimize button clicked")
                self.selected_button = 1
                self.minimized = True
            elif self.fullscreen_button.collidepoint(event.pos):
                print("Nope")

            elif self.exit_button.collidepoint(event.pos):
                print("Exit button clicked")
                self.selected_button = 3
            else:
                self.selected_button = None

            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False

        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
            self.selected_button = None

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.rect.x = event.pos[0] + self.offset_x
                self.rect.y = event.pos[1] + self.offset_y

class Minesweeper(Window):
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

        screen.blit(self.surface, (self.rect.x, self.rect.y + self.title_bar_height))

        ##### App Code Starts Here #####
        ROWS = 20
        # pygame.draw.rect(screen, BORDER_COLOR, pygame.Rect(r * TILE_SIZE, c * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        # if gameboard[r][c] == -3:
        #     tile_rect = pygame.Rect(r * TILE_SIZE + BORDER, c * TILE_SIZE + BORDER, TILE_SIZE - BORDER,
        #                             TILE_SIZE - BORDER)
        #     flag_rect = pygame.Rect(r * TILE_SIZE + BORDER + (TILE_SIZE - small_tile_size) / 2,
        #                             c * TILE_SIZE + BORDER + (TILE_SIZE - small_tile_size) / 2,
        #                             TILE_SIZE - BORDER, TILE_SIZE - BORDER)
        #     pygame.draw.rect(screen, flagged_tile_color, tile_rect)
        #     # text = font.render('!', True, (0, 0, 0), None)
        #     # textRect = text.get_rect()
        #     # textRect.center = (
        #     #     r * TILE_SIZE + BORDER + (TILE_SIZE - BORDER) // 2,
        #     #     c * TILE_SIZE + BORDER + (TILE_SIZE - BORDER) // 2)
        #     screen.blit(flag_img, flag_rect)
        # if gameboard[r][c] == -2:
        #     pygame.draw.rect(screen, covered_tile_color,
        #                      pygame.Rect(r * TILE_SIZE + BORDER, c * TILE_SIZE + BORDER, TILE_SIZE - BORDER,
        #                                  TILE_SIZE - BORDER))
        # if gameboard[r][c] == -1:
        #     tile_rect = pygame.Rect(r * TILE_SIZE + BORDER, c * TILE_SIZE + BORDER, TILE_SIZE - BORDER,
        #                             TILE_SIZE - BORDER)
        #     pygame.draw.rect(screen, bomb_tile_color, tile_rect)
        #     screen.blit(bomb_img, tile_rect)
        # if gameboard[r][c] == 0:
        #     pygame.draw.rect(screen, empty_tile_color,
        #                      pygame.Rect(r * TILE_SIZE + BORDER, c * TILE_SIZE + BORDER, TILE_SIZE - BORDER,
        #                                  TILE_SIZE - BORDER))
        # if gameboard[r][c] == 1:
        #     pygame.draw.rect(screen, main_tile_color,
        #                      pygame.Rect(r * TILE_SIZE + BORDER, c * TILE_SIZE + BORDER, TILE_SIZE - BORDER,
        #                                  TILE_SIZE - BORDER))
        #     text = font.render('1', True, (35, 69, 168), None)
        #     textRect = text.get_rect()
        #     textRect.center = (r * TILE_SIZE + BORDER + (TILE_SIZE - BORDER) // 2,
        #                        c * TILE_SIZE + BORDER + (TILE_SIZE - BORDER) // 2)
        #     screen.blit(text, textRect)
        # if gameboard[r][c] == 2:
        #     pygame.draw.rect(screen, main_tile_color,
        #                      pygame.Rect(r * TILE_SIZE + BORDER, c * TILE_SIZE + BORDER, TILE_SIZE - BORDER,
        #                                  TILE_SIZE - BORDER))
        #     text = font.render('2', True, (35, 107, 22), None)
        #     textRect = text.get_rect()
        #     textRect.center = (
        #         r * TILE_SIZE + BORDER + (TILE_SIZE - BORDER) // 2,
        #         c * TILE_SIZE + BORDER + (TILE_SIZE - BORDER) // 2)
        #     screen.blit(text, textRect)
        # if gameboard[r][c] == 3:
        #     pygame.draw.rect(screen, main_tile_color,
        #                      pygame.Rect(r * TILE_SIZE + BORDER, c * TILE_SIZE + BORDER, TILE_SIZE - BORDER,
        #                                  TILE_SIZE - BORDER))
        #     text = font.render('3', True, (107, 22, 22), None)
        #     textRect = text.get_rect()
        #     textRect.center = (
        #         r * TILE_SIZE + BORDER + (TILE_SIZE - BORDER) // 2,
        #         c * TILE_SIZE + BORDER + (TILE_SIZE - BORDER) // 2)
        #     screen.blit(text, textRect)
        # if gameboard[r][c] == 4:
        #     pygame.draw.rect(screen, main_tile_color,
        #                      pygame.Rect(r * TILE_SIZE + BORDER, c * TILE_SIZE + BORDER, TILE_SIZE - BORDER,
        #                                  TILE_SIZE - BORDER))
        #     text = font.render('4', True, (7, 7, 48), None)
        #     textRect = text.get_rect()
        #     textRect.center = (
        #         r * TILE_SIZE + BORDER + (TILE_SIZE - BORDER) // 2,
        #         c * TILE_SIZE + BORDER + (TILE_SIZE - BORDER) // 2)
        #     screen.blit(text, textRect)
        # if gameboard[r][c] == 5:
        #     pygame.draw.rect(screen, main_tile_color,
        #                      pygame.Rect(r * TILE_SIZE + BORDER, c * TILE_SIZE + BORDER, TILE_SIZE - BORDER,
        #                                  TILE_SIZE - BORDER))
        #     text = font.render('5', True, (105, 50, 19), None)
        #     textRect = text.get_rect()
        #     textRect.center = (
        #         r * TILE_SIZE + BORDER + (TILE_SIZE - BORDER) // 2,
        #         c * TILE_SIZE + BORDER + (TILE_SIZE - BORDER) // 2)
        #     screen.blit(text, textRect)
        # if gameboard[r][c] > 5:
        #     pygame.draw.rect(screen, main_tile_color,
        #                      pygame.Rect(r * TILE_SIZE + BORDER, c * TILE_SIZE + BORDER, TILE_SIZE - BORDER,
        #                                  TILE_SIZE - BORDER))
        #     text = font.render(str(gameboard[r][c]), True, (40, 173, 142), None)
        #     textRect = text.get_rect()
        #     textRect.center = (
        #         r * TILE_SIZE + BORDER + (TILE_SIZE - BORDER) // 2,
        #         c * TILE_SIZE + BORDER + (TILE_SIZE - BORDER) // 2)
        #     screen.blit(text, textRect)
        COLUMNS = 20
        for r in range(ROWS):
            for c in range(COLUMNS):
                pass
