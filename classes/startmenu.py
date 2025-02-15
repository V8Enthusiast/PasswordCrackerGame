from classes.buttons import Button
from classes.window import Window
import pygame

class StartMenu(Window):
    def __init__(self, x, y, width, height, title, font, icon, app, simulation):
        super().__init__(x, y, width, height, title, font, icon)
        self.app = app
        self.width = width
        self.height = height
        self.length_x = 197
        self.length_y = 50
        self.widthA = 200
        self.heightA = 300
        self.taskbar_height = 40
        self.x = x
        self.y = y
        self.buttons = []
        self.simulation = simulation

        self.create_buttons()


    def draw(self, screen):
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

        self.exit_button = pygame.Rect(self.rect.right - (self.button_width + self.button_spacing), self.rect.y + (self.title_bar_height - self.button_height)//2 + 1, self.button_width, self.button_height)

        if self.active:
            title_bar_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.title_bar_height)
            pygame.draw.rect(screen, self.title_bar_color, title_bar_rect)
        else:
            title_bar_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.title_bar_height)
            pygame.draw.rect(screen, self.title_bar_inactive_color, title_bar_rect)

        icon = self.icon
        icon_rect = icon.get_rect(midleft=(title_bar_rect.left + 5, title_bar_rect.centery))  # Align icon to the left
        screen.blit(icon, icon_rect)

        title_surface = self.font.render(self.title, True, self.title_text_color)
        title_rect = title_surface.get_rect(midleft=(icon_rect.right + 5, title_bar_rect.centery))
        screen.blit(title_surface, title_rect)

        window_bg_rect = pygame.Rect(self.rect.x, self.rect.y + self.title_bar_height, self.rect.width, self.rect.height - self.title_bar_height - self.window_border_width)
        pygame.draw.rect(screen, self.bg_color, window_bg_rect)

        self.draw_button(screen, self.exit_button, 3, 1, self.exit_icon)

        screen.blit(self.surface, (self.rect.x, self.rect.y + self.title_bar_height))




        for button in self.new_buttons:
            button.render(screen)
            self.buttons.append(button)




    def create_buttons(self):
        offset = 4
        self.new_buttons = []
        self.new_buttons.append(
            Button(self.length_x, self.length_y + offset, self.x + offset / 2,
                   0 * (self.length_y + offset) + self.y + self.title_bar_height + offset, self.font, "Calculator",
                   "", self.app, bgcolor=(25, 25, 25), fgcolor=(90, 90, 90), icon='img/Calc.png',
                   size=(32, 32)))
        self.new_buttons.append(
            Button(self.length_x, self.length_y + offset, self.x + offset / 2,
                   1 * (self.length_y + offset) + self.y + self.title_bar_height + offset, self.font, "Terminal",
                   "", self.app, bgcolor=(25, 25, 25), fgcolor=(90, 90, 90), icon='img/MyComputer98.png',
                   size=(32, 32)))
        self.new_buttons.append(
            Button(self.length_x, self.length_y + offset, self.x + offset / 2,
                   2 * (self.length_y + offset) + self.y + self.title_bar_height + offset, self.font, "Need For Speed",
                   "", self.app, bgcolor=(25, 25, 25), fgcolor=(90, 90, 90), icon='img/car.png',
                   size=(32, 32)))
        self.new_buttons.append(
            Button(self.length_x, self.length_y + offset, self.x + offset / 2,
                   3 * (self.length_y + offset) + self.y + self.title_bar_height + offset, self.font, "Minesweeper",
                   "", self.app, bgcolor=(25, 25, 25), fgcolor=(90, 90, 90), icon='img/mine.png',
                   size=(32, 32)))
        self.new_buttons.append(
            Button(self.length_x, self.length_y + offset, self.x + offset / 2,
                   4 * (self.length_y + offset) + self.y + self.title_bar_height + offset, self.font, "Internet Explorer",
                   "", self.app, bgcolor=(25, 25, 25), fgcolor=(90, 90, 90), icon='img/explorer.png',
                   size=(32, 32)))

                    # Overrides the default events function in app.py
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.new_buttons:
                if button.rect.collidepoint(event.pos):
                    button.selected = True
            # if self.minimize_button.collidepoint(event.pos):
            #     print("Minimize button clicked")
            #     self.selected_button = 1
            #     self.minimized = True
            #
            # elif self.fullscreen_button.collidepoint(event.pos):
            #     print("Fullscreen button clicked")
            #     self.selected_button = 2
            #     print("No")
                # self.rect.width = 1200
                # self.rect.height = 900
                # self.surface = pygame.Surface((self.rect.width, self.rect.height - self.title_bar_height - self.margin))
                # self.rect.x = 0
                # self.rect.y = 0
                # Implement fullscreen functionality

            if self.exit_button.collidepoint(event.pos):

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
            for button in self.new_buttons:
                if button.selected:
                    self.simulation.open_app(button.text)
                    button.selected = False