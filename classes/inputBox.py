import pygame
class InputBox:
    def __init__(self, x, y, w, h, font, text='', max_length=-1, font_color=(0, 0, 0)):
        self.rect = pygame.Rect(x, y, w, h)
        self.color_inactive = (192, 192, 192)
        self.color_active = (160, 160, 160)
        self.text_color_active = font_color
        self.text_color_inactive = font_color
        if text != '':
            self.text_color_inactive = font_color
        self.max_length = 2000
        if max_length != -1:
            self.max_length = max_length
        self.color = self.color_inactive
        self.text = text
        self.font = font
        self.txt_surface = self.font.render(self.text, True, self.text_color_inactive)
        self.active = False
        self.x = x
        self.y = y

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = self.color_active if self.active else self.color_inactive
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)  # For debugging purposes
                    return self.text
                    #self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if len(self.text) < self.max_length:
                        self.text += event.unicode
                # Re-render the text.
                self.txt_surface = self.font.render(self.text, True, self.text_color_active)
            else:
                self.txt_surface = self.font.render(self.text, True, self.text_color_inactive)
        return 0

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        self.txt_surface = self.font.render(self.text, True, self.text_color_inactive)
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)
