import pygame
import sys
from classes.inputBox import InputBox
from classes.window import Window


class InternetExplorer(Window):
    def __init__(self, x, y, width, height, title, font, icon, simulation):
        super().__init__(x, y, width, height, title, font, icon)

        # Window dimensions
        self.width = width
        self.height = height
        self.page_height = int(.8*height)
        self.page_width = int(1*width)
        self.address_bar_height = 30
        self.address_bar_offset = 60
        self.simulation = simulation

        # Tab bar dimensions
        self.tab_height = 30
        self.tab_width = 200
        self.center_x = self.rect.x + self.width // 2
        self.center_y = self.rect.y + self.height // 2
        self.top_y = self.rect.y + self.title_bar_height + self.tab_height + self.address_bar_height
        self.tabs = ['Reset Password', 'Cayman Savings Bank', 'New tab']
        self.selected_tab = 0  # Current active tab

        self.bigfont = pygame.font.Font("fonts/Windows98.ttf", 24)

        # Create an address bar (input box)
        self.address_bar = InputBox(self.rect.x + self.address_bar_offset, self.rect.y + self.title_bar_height + self.tab_height, self.width - 20, 30, self.font)
        # Create an input box for the content area (optional: here we simulate content area)
        self.content_box = pygame.Rect(self.rect.x, self.rect.y + 50 + self.address_bar_height, self.page_width, self.page_height)

        # Create a simple close button for the window (if we ever want to add it back)
        self.close_button_rect = pygame.Rect(self.rect.x + self.width - 20, self.rect.y + 5, 15, 15)

        self.passwordBox = InputBox(self.center_x - 75, self.center_y,
                                    150, 30, self.font)
        # self.passwordBox.rect.x = self.rect.x + self.passwordBox.x
        # self.passwordBox.rect.y = self.rect.y + self.passwordBox.y


    def draw(self, screen):
        super().draw(screen)
        self.surface.fill((192, 192, 192))

        # Draw the tabs area (mimic tab bar from Internet Explorer)
        tab_bar_y = self.rect.y + self.title_bar_height
        tab_bar_height = self.tab_height

        # Draw tab bar background (light gray)
        pygame.draw.rect(screen, (192, 192, 192), (self.rect.x, tab_bar_y, self.width, tab_bar_height))

        # Draw tabs
        for i, tab in enumerate(self.tabs):
            tab_color = (255, 255, 255) if i == self.selected_tab else (220, 220, 220)  # Active tab color
            tab_rect = pygame.Rect(self.rect.x + i * self.tab_width, tab_bar_y, self.tab_width, tab_bar_height)
            pygame.draw.rect(screen, tab_color, tab_rect)
            pygame.draw.rect(screen, (0, 0, 0), tab_rect, 1)  # Tab border
            screen.blit(self.font.render(tab, True, (0, 0, 0)), (tab_rect.x + 10, tab_rect.y + 5))

        # Draw address bar
        pygame.draw.rect(screen, (255, 255, 255), self.address_bar.rect)  # Address bar background
        pygame.draw.rect(screen, (0, 0, 0), self.address_bar.rect, 2)  # Address bar border
        self.address_bar.update()
        self.address_bar.draw(screen)

        # Draw the content area (here it's just a placeholder)
        pygame.draw.rect(screen, (255, 255, 255), self.content_box)  # Content background
        pygame.draw.rect(screen, (0, 0, 0), self.content_box, 2)  # Content border

        self.center_x = self.rect.x + self.width // 2
        self.center_y = self.rect.y + self.height // 2
        self.top_y = self.rect.y + self.title_bar_height + self.tab_height + self.address_bar_height

        self.passwordBox.rect.x = self.center_x - 75
        self.passwordBox.rect.y =  self.center_y

        # Optionally add some text to simulate content (can be replaced by actual content later)
        if self.selected_tab == 0:
            screen.blit(self.bigfont.render("Reset Password", True, (0, 0, 0)),
                        (self.center_x  - 75, self.top_y))
            self.passwordBox.update()
            self.passwordBox.draw(screen)
        elif self.selected_tab == 1:
            screen.blit(self.font.render("Money: $69000", True, (0, 0, 0)),
                        (self.content_box.x + 10, self.content_box.y + 10))
        elif self.selected_tab == 2:
            screen.blit(self.font.render("New Tab", True, (0, 0, 0)),
                        (self.content_box.x + 10, self.content_box.y + 10))

        screen.blit(self.font.render("Address", True, (0, 0, 0)),
                    (self.rect.x + 5, self.rect.y + self.tab_height + self.title_bar_height + 3))

        # Draw the window frame
        pygame.draw.rect(screen, (0, 0, 0), (self.rect.x, self.rect.y, self.width, self.height), 2)  # Border

    def handle_event(self, event):
        super().handle_event(event)
        self.address_bar.handle_event(event)
        pwd = self.passwordBox.handle_event(event)
        if pwd != 0:
            print("aaaaaa")
            self.simulation.new_password = True
            self.simulation.passwordToCrack = pwd

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Handle tab click (simply switch to that tab)
            if event.button == 1:  # Left click
                for i in range(len(self.tabs)):
                    tab_rect = pygame.Rect(self.rect.x + i * self.tab_width, self.rect.y + self.title_bar_height, self.tab_width,
                                           self.tab_height)
                    if tab_rect.collidepoint(event.pos):
                        self.selected_tab = i

        # Handle address bar events (e.g., typing in the address bar)


        if event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.rect.x = event.pos[0] + self.offset_x
                self.rect.y = event.pos[1] + self.offset_y
                self.address_bar.rect.x = self.rect.x + self.address_bar_offset
                self.address_bar.rect.y = self.rect.y + self.title_bar_height + self.tab_height
                self.content_box.x = self.rect.x
                self.content_box.y = self.rect.y + 50 + self.address_bar_height
