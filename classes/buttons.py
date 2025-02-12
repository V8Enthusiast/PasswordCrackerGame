import random
import pygame

class Button:
    def __init__(self, width, height, x, y, font, text, function, app, bgcolor=(25, 25, 25), fgcolor=(90, 90, 90), icon=None, size=None):
        # Save the data passed into the function to variables
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.font = font
        self.bgcolor = bgcolor
        self.fgcolor = fgcolor
        self.app = app
        self.text = text
        self.function = function

        self.selected = False
        self.rect = pygame.Rect(x, y, width, height)

        self.button_color = (160, 160, 160)  # Slightly darker gray for buttons
        self.button_hover_color = (128, 128, 128)  # Even darker gray for hover effect
        self.button_shadow_color = (10, 10, 10)  # Darker gray for shadow
        self.button_highlight_color = (220, 220, 220)  # Lighter gray for highlight

        self.icon = icon
        if self.icon is not None and size is not None:
            self.icon = pygame.image.Calc = pygame.transform.scale(pygame.image.load(self.icon), size)

        pygame.font.init()

    def render(self, screen):
        # # Put together the button based on the parameters
        # self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        # self.font = pygame.font.Font(self.font_type, int(32 * self.app.scale))
        # self.display_text = self.font.render(self.text, True, self.fgcolor)
        # # Get the textbox rect and align its center with the center of the button rect
        # self.display_text_rect = self.display_text.get_rect()
        # self.display_text_rect.center = self.rect.center
        # # Draw the button
        # pygame.draw.rect(self.app.screen, self.bgcolor, self.rect)
        # self.app.screen.blit(self.display_text, self.display_text_rect)

        # mouse_pos = pygame.mouse.get_pos()
        # if button.collidepoint(mouse_pos) or i == self.selected_button: # Hovering over the button selects it
        if self.selected:
            # Caved-in effect

            shadow_rect = self.rect.move(-2, -2)
            shadow_rect.width += 2
            shadow_rect.height += 2
            pygame.draw.rect(screen, self.button_shadow_color, shadow_rect)
            highlight_rect = self.rect.move(0, 0)
            highlight_rect.width += 2
            highlight_rect.height += 2

            pygame.draw.rect(screen, self.button_highlight_color, highlight_rect)
            pygame.draw.rect(screen, self.button_color, self.rect)
        else:
            # Normal button
            shadow_rect = self.rect.move(0, 0)
            shadow_rect.width += 2
            shadow_rect.height += 2
            pygame.draw.rect(screen, self.button_shadow_color, shadow_rect)
            highlight_rect = self.rect.move(-2, -2)
            highlight_rect.width += 2
            highlight_rect.height += 2
            pygame.draw.rect(screen, self.button_highlight_color, highlight_rect)
            pygame.draw.rect(screen, self.button_color, self.rect)

        if self.icon is not None:
            # Draw icon aligned to the left
            icon_rect = self.icon.get_rect(midleft=(self.rect.left + 5, self.rect.centery))  # Align icon to the left
            screen.blit(self.icon, icon_rect)

            # Draw label centered
            label = self.font.render(self.text, True, (0, 0, 0))
            label_rect = label.get_rect(midleft=(icon_rect.right + 5, self.rect.centery))  # Adjust label position
            screen.blit(label, label_rect)
        else:
            if not self.selected:
                # Draw label centered
                label = self.font.render(self.text, True, (0, 0, 0))
                label_rect = label.get_rect(center=(self.rect.centerx, self.rect.centery))  # Adjust label position
                screen.blit(label, label_rect)
            else:
                label = self.font.render(self.text, True, (0, 0, 0))
                label_rect = label.get_rect(center=(self.rect.centerx + 2, self.rect.centery + 2))  # Adjust label position
                screen.blit(label, label_rect)



    def click(self):
        if self.function == 'play':
            self.app.ui = self.app.diffselect # Change the displayed ui to a new simulation
        if self.function == 'back':
            self.app.ui = self.app.active_simulation # Change the displayed ui back to the simulation
            self.app.active_simulation = None
        if self.function == 'plus':
            self.app.ui.add()
        if self.function == 'minus':
            self.app.ui.subtract()
        if self.function == 'start_game':
            self.app.newSimulation()
            self.app.inactive_simulation.start_password = self.app.ui.passwordbox.text
            self.app.inactive_simulation.difficulty = self.app.ui.selected_length
            self.app.ui = self.app.inactive_simulation

        if self.function == 'back_to_menu':
            self.app.ui = self.app.mainmenu
        else:
            self.bgcolor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))