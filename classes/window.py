import pygame

class Window:
    def __init__(self, x, y, width, height, title, font, icon):
        self.rect = pygame.Rect(x, y, width, height)
        self.title = title
        self.font = font
        self.icon = icon
        self.title_bar_height = 25
        self.bg_color = (192, 192, 192)
        self.title_bar_color = (0, 0, 128)
        self.title_bar_inactive_color = (128, 128, 128)
        self.title_text_color = (255, 255, 255)
        self.border_color = (160, 160, 160)
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

        self.button_width = 16
        self.button_height = 16
        self.button_spacing = 4
        self.margin = 3
        self.window_border_width = 3

        self.minimize_icon = pygame.transform.scale(pygame.image.load('img/minimize.png'), (18, 18))
        self.fullscreen_icon = pygame.transform.scale(pygame.image.load('img/maximize.png'), (18, 18))
        self.exit_icon = pygame.transform.scale(pygame.image.load('img/close.png'), (18, 18))

        self.surface = pygame.Surface((width, height - self.title_bar_height - self.margin))

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

        self.minimize_button = pygame.Rect(self.rect.right - 3 * (self.button_width + self.button_spacing) - self.margin, self.rect.y + (self.title_bar_height - self.button_height)//2 + 1, self.button_width, self.button_height)
        self.fullscreen_button = pygame.Rect(self.rect.right - 2 * (self.button_width + self.button_spacing) - self.margin, self.rect.y + (self.title_bar_height - self.button_height)//2 + 1, self.button_width, self.button_height)
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

        self.draw_button(screen, self.minimize_button, 1, 1, self.minimize_icon)
        self.draw_button(screen, self.fullscreen_button, 2, 1, self.fullscreen_icon)
        self.draw_button(screen, self.exit_button, 3, 1, self.exit_icon)

        screen.blit(self.surface, (self.rect.x, self.rect.y + self.title_bar_height))

    def draw_button(self, screen, button_rect, button_id, shadow_width, icon):

        if button_id == self.selected_button:
            # caved-in effect
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
            # normal button
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

        icon_rect = icon.get_rect(center=highlight_rect.center)
        screen.blit(icon, icon_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:

            if self.draggable_area().collidepoint(event.pos) and self.minimized is False:
                self.dragging = True
                self.offset_x = self.rect.x - event.pos[0]
                self.offset_y = self.rect.y - event.pos[1]
            elif self.minimize_button.collidepoint(event.pos):
                #print("Minimize button clicked")
                self.selected_button = 1
                self.minimized = True
            elif self.fullscreen_button.collidepoint(event.pos):
                #print("Don't...")
                self.selected_button = 2
                # self.rect.width = 1200
                # self.rect.height = 900
                # self.surface = pygame.Surface((self.rect.width, self.rect.height-self.title_bar_height-self.margin))
                # self.rect.x = 0
                # self.rect.y = 0
                # Implement fullscreen functionality
            elif self.exit_button.collidepoint(event.pos):

                #print("Exit button clicked")
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
        return pygame.Rect(self.rect.x, self.rect.y, self.rect.width - 3 * (self.button_width + self.button_spacing), self.title_bar_height)