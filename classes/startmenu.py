from classes.buttons import Button
from classes.window import Window
import pygame

class StartMenu(Window):
    def __init__(self, x, y, width, height, title, font, icon, app):
        super().__init__(x, y, width, height, title, font, icon)
        self.app = app
        self.width = width
        self.height = height
        self.length_x = 197
        self.length_y = 54
        self.widthA = 200
        self.heightA = 300
        self.taskbar_height = 40
        self.x = x
        self.y = y
        self.buttons = []

        self.create_buttons()


    def draw(self, screen):
        super().draw(screen)
        for button in self.new_buttons:
            button.render(screen)
            self.buttons.append(button)




    def create_buttons(self):
        offset = 4
        length_x = self.length_x
        length_y = self.length_y
        self.new_buttons = []
        for x in range(1):
            for y in range(0, 5):

                self.new_buttons.append(
                    Button(self.length_x, self.length_y + offset , self.x + offset/2,y*(self.length_y + offset) + self.y + self.title_bar_height + offset, self.font, "Calc", "", self.app, bgcolor=(25, 25, 25), fgcolor=(90, 90, 90), icon='img/Calc.png', size=(32, 32)))

    # Overrides the default events function in app.py
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.buttons[0].rect.collidepoint(event.pos):
                print('yoooooo')
            if self.buttons[1].rect.collidepoint(event.pos):
                self.selected_button = 11
                print("yooooo")
            if self.buttons[2].rect.collidepoint(event.pos):
                self.selected_button = 12
                print("yooooo")
            if self.buttons[3].rect.collidepoint(event.pos):
                self.selected_button = 13
                print("yooooo")
            if self.buttons[4].rect.collidepoint(event.pos):
                self.selected_button = 14
                print("yooooo")
            if self.minimize_button.collidepoint(event.pos):
                print("Minimize button clicked")
                self.selected_button = 1
                self.minimized = True

            elif self.fullscreen_button.collidepoint(event.pos):
                print("Fullscreen button clicked")
                self.selected_button = 2
                print("No")
                # self.rect.width = 1200
                # self.rect.height = 900
                # self.surface = pygame.Surface((self.rect.width, self.rect.height - self.title_bar_height - self.margin))
                # self.rect.x = 0
                # self.rect.y = 0
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