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
        self.tabs = ['Reset Password', 'Pacific Standard Bank', 'FREE RAM!']
        self.selected_tab = 0  # Current active tab

        self.bigfont = pygame.font.Font("fonts/Windows98.ttf", 24)

        # Create an address bar (input box)
        self.address_bar = InputBox(self.rect.x + self.address_bar_offset, self.rect.y + self.title_bar_height + self.tab_height, self.width - 20, 30, self.font, text="https://pacificbank.com")
        # Create an input box for the content area (optional: here we simulate content area)
        self.content_box = pygame.Rect(self.rect.x, self.rect.y + 50 + self.address_bar_height, self.page_width, self.page_height)

        # Create a simple close button for the window (if we ever want to add it back)
        self.close_button_rect = pygame.Rect(self.rect.x + self.width - 20, self.rect.y + 5, 15, 15)

        self.passwordBox = InputBox(self.center_x - 75, self.center_y,
                                    150, 30, self.font, max_length=self.simulation.difficulty)
        # self.passwordBox.rect.x = self.rect.x + self.passwordBox.x
        # self.passwordBox.rect.y = self.rect.y + self.passwordBox.y

        self.submit_pwd_rect = pygame.Rect(self.center_x - 50, self.content_box.y + 210, 100, 25)

        self.isTimedOut = False
        self.loginbox = InputBox(self.center_x - 75, self.center_y,
                                    150, 30, self.font, max_length=self.simulation.difficulty)

        self.transactions = [
            ("05/15/95", "GROCERY STORE", "-$45.82", "$100,000.00"),
            ("05/14/95", "SALARY DEPOSIT", "+$33,500.00", "$69,045.82"),
            ("05/13/95", "GAS STATION", "-$22.15", "$66,545.82"),
            ("05/12/95", "MOVIE RENTAL", "-$3.99", "$66,567.97"),
            # ("05/11/95", "PHONE BILL", "-$65.00", "$66,571.96")
        ]


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
        if self.selected_tab in (0, 1):
            self.address_bar.text = "https://pacificbank.com"
        elif self.selected_tab == 2:
            self.address_bar.text = "http://downloadram.xyz"


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
            if not self.isTimedOut:
                pygame.draw.rect(screen, (192, 192, 192), self.content_box)

                # Draw blue header bar
                header_rect = pygame.Rect(self.content_box.x, self.content_box.y, self.content_box.width, 30)
                pygame.draw.rect(screen, (0, 0, 128), header_rect)

                # Header text
                header_text = self.font.render("Pacific Standard Bank - Password Reset", True, (255, 255, 255))
                screen.blit(header_text, (self.content_box.x + 10, self.content_box.y + 5))

                # Security notice box
                notice_y = self.content_box.y + 50
                notice_box = pygame.Rect(self.content_box.x + 20, notice_y, self.content_box.width - 40, 60)
                pygame.draw.rect(screen, (255, 255, 192), notice_box)  # Light yellow background
                pygame.draw.rect(screen, (128, 128, 128), notice_box, 1)

                # Security notice text
                notice_text = [
                    "SECURITY NOTICE: We currently don't have much storage space for passwords.",
                    f"Password must be up to {self.simulation.difficulty} characters long"
                ]

                for i, line in enumerate(notice_text):
                    text = self.font.render(line, True, (128, 0, 0))  # Dark red text
                    screen.blit(text, (self.content_box.x + 30, notice_y + 10 + (i * 20)))

                # Password input section
                input_y = notice_y + 80
                input_box = pygame.Rect(self.content_box.x + 20, input_y, self.content_box.width - 40, 120)
                pygame.draw.rect(screen, (255, 255, 255), input_box)
                pygame.draw.rect(screen, (128, 128, 128), input_box, 1)

                # Labels and input boxes
                label_x = self.content_box.x + 30
                self.passwordBox.rect.x = label_x + 140
                self.passwordBox.rect.y = input_y + 20

                # Current password label
                current_text = self.font.render("New Password:", True, (0, 0, 0))
                screen.blit(current_text, (label_x, input_y + 25))

                # Draw the password input box
                self.passwordBox.update()
                self.passwordBox.draw(screen)

                # Submit button
                button_rect = pygame.Rect(self.center_x - 50, input_y + 80, 100, 25)
                pygame.draw.rect(screen, (0, 0, 128), button_rect)
                pygame.draw.rect(screen, (128, 128, 128), button_rect, 1)

                # Button text
                button_text = self.font.render("Submit", True, (255, 255, 255))
                text_rect = button_text.get_rect(center=button_rect.center)
                screen.blit(button_text, text_rect)

                self.submit_pwd_rect = button_rect
            else:
                pygame.draw.rect(screen, (192, 192, 192), self.content_box)

                # Draw blue header bar
                header_rect = pygame.Rect(self.content_box.x, self.content_box.y, self.content_box.width, 30)
                pygame.draw.rect(screen, (0, 0, 128), header_rect)

                # Header text
                header_text = self.font.render("Pacific Standard Bank - Log in", True, (255, 255, 255))
                screen.blit(header_text, (self.content_box.x + 10, self.content_box.y + 5))

                # Security notice box
                notice_y = self.content_box.y + 50
                notice_box = pygame.Rect(self.content_box.x + 20, notice_y, self.content_box.width - 40, 60)
                pygame.draw.rect(screen, (255, 255, 192), notice_box)  # Light yellow background
                pygame.draw.rect(screen, (128, 128, 128), notice_box, 1)

                # Security notice text
                notice_text = [
                    "ERROR: Session expired. Please re-enter your password.",
                ]

                for i, line in enumerate(notice_text):
                    text = self.font.render(line, True, (128, 0, 0))  # Dark red text
                    screen.blit(text, (self.content_box.x + 30, notice_y + 10 + (i * 20)))

                # Password input section
                input_y = notice_y + 80
                input_box = pygame.Rect(self.content_box.x + 20, input_y, self.content_box.width - 40, 120)
                pygame.draw.rect(screen, (255, 255, 255), input_box)
                pygame.draw.rect(screen, (128, 128, 128), input_box, 1)

                # Labels and input boxes
                label_x = self.content_box.x + 30
                self.loginbox.rect.x = label_x + 140
                self.loginbox.rect.y = input_y + 20

                # Current password label
                current_text = self.font.render("Password:", True, (0, 0, 0))
                screen.blit(current_text, (label_x, input_y + 25))

                # Draw the password input box
                self.loginbox.update()
                self.loginbox.draw(screen)

                # Submit button
                button_rect = pygame.Rect(self.center_x - 50, input_y + 80, 100, 25)
                pygame.draw.rect(screen, (0, 0, 128), button_rect)
                pygame.draw.rect(screen, (128, 128, 128), button_rect, 1)

                # Button text
                button_text = self.font.render("Log in", True, (255, 255, 255))
                text_rect = button_text.get_rect(center=button_rect.center)
                screen.blit(button_text, text_rect)

                self.submit_pwd_rect = button_rect

        elif self.selected_tab == 1:
            if self.selected_tab == 1:
                # Background color - classic gray
                pygame.draw.rect(screen, (192, 192, 192), self.content_box)

                # Draw blue header bar
                header_rect = pygame.Rect(self.content_box.x, self.content_box.y, self.content_box.width, 30)
                pygame.draw.rect(screen, (0, 0, 128), header_rect)

                # Header text
                header_text = self.font.render("Pacific Standard Bank - Account Summary", True, (255, 255, 255))
                screen.blit(header_text, (self.content_box.x + 10, self.content_box.y + 5))

                # Account information
                y_pos = self.content_box.y + 50
                info_color = (0, 0, 0)

                # Draw account details box
                details_box = pygame.Rect(self.content_box.x + 10, y_pos, self.content_box.width - 20, 110)
                pygame.draw.rect(screen, (255, 255, 255), details_box)
                pygame.draw.rect(screen, (128, 128, 128), details_box, 1)

                # Account information
                account_info = [
                    "Account Holder: Jeff Jefferson",
                    "Account Number: ****-****-****-1234",
                    f"Balance: ${self.simulation.money//1000},{self.simulation.money%1000}.00",
                    "Available Credit: $25,000.00"
                ]

                for info in account_info:
                    text = self.font.render(info, True, info_color)
                    screen.blit(text, (self.content_box.x + 20, y_pos + 10))
                    y_pos += 25

                # Transaction history
                y_pos += 20
                history_header = self.font.render("Recent Transactions:", True, info_color)
                screen.blit(history_header, (self.content_box.x + 10, y_pos))

                # Transaction table headers
                y_pos += 30
                headers = ["Date", "Description", "Amount", "Balance"]
                x_pos = self.content_box.x + 10

                for header in headers:
                    pygame.draw.rect(screen, (0, 0, 128), (x_pos, y_pos, 120, 20))
                    header_text = self.font.render(header, True, (255, 255, 255))
                    screen.blit(header_text, (x_pos + 5, y_pos + 2))
                    x_pos += 120

                y_pos += 25
                for transaction in self.transactions:
                    x_pos = self.content_box.x + 10
                    for item in transaction:
                        cell_rect = pygame.Rect(x_pos, y_pos, 120, 20)
                        pygame.draw.rect(screen, (255, 255, 255), cell_rect)
                        pygame.draw.rect(screen, (128, 128, 128), cell_rect, 1)

                        text = self.font.render(item, True, info_color)
                        screen.blit(text, (x_pos + 5, y_pos + 2))
                        x_pos += 120
                    y_pos += 20

                # Footer
                #footer_text = self.font.render("Last updated: 05/15/1995 14:32:15", True, (128, 128, 128))
                #screen.blit(footer_text, (self.content_box.x + 10, self.content_box.height - 30))
        elif self.selected_tab == 2:
                # Background - classic eye-straining pattern
                for y in range(self.content_box.y, self.content_box.y + self.content_box.height, 4):
                    for x in range(self.content_box.x, self.content_box.x + self.content_box.width, 4):
                            pygame.draw.rect(screen, (0, 0, 255), (x, y, 2, 2))

                # Main content area
                content_area = pygame.Rect(
                    self.content_box.x + 20,
                    self.content_box.y + 20,
                    self.content_box.width - 40,
                    self.content_box.height - 40
                )
                pygame.draw.rect(screen, (255, 255, 255), content_area)
                pygame.draw.rect(screen, (255, 0, 0), content_area, 3)

                # Flashing text effect (using game tick)
                if pygame.time.get_ticks() % 1000 < 500:
                    text_color = (255, 0, 0)
                else:
                    text_color = (0, 0, 255)

                # Header
                header_text = self.font.render("!!! FREE RAM DOWNLOAD !!!", True, text_color)
                screen.blit(header_text, (self.content_box.x + 50, self.content_box.y + 40))

                # Calculate layout dimensions
                left_section_width = (self.content_box.width - 60) // 2
                right_section_x = self.content_box.x + left_section_width + 40

                # Main text content (Left side)
                texts = [
                    "⚡ AMAZING OFFER - DON'T MISS OUT ⚡",
                    "Download More RAM instantly!!!",
                    "✓ 16 MEGABYTES of RAM - FREE!",
                    "✓ Make your computer 500% faster",
                    "✓ NO VIRUS GUARANTEED",
                    "✓ Used by over 1,000,000 people!",
                    "",
                    "[ DOWNLOAD NOW - CLICK HERE ]",
                ]

                y_offset = 70
                for text in texts:
                    color = (0, 0, 255) if "DOWNLOAD NOW" in text else (0, 0, 0)
                    text_surface = self.font.render(text, True, color)
                    screen.blit(text_surface, (self.content_box.x + 40, self.content_box.y + y_offset))
                    y_offset += 30

                # Right side content
                # Visitor counter (Right side)
                counter_box = pygame.Rect(
                    right_section_x,
                    self.content_box.y + 100,
                    200,
                    30
                )
                pygame.draw.rect(screen, (0, 0, 0), counter_box, 1)
                counter_text = self.font.render("Visitors: 000,012,345", True, (0, 0, 0))
                screen.blit(counter_text, (counter_box.x + 10, counter_box.y + 5))

                # Awards (Right side)
                awards = [
                    "Best Download 1995",
                    "100% Safe Award",
                    "Top RAM Site",
                    "Netscape Choice",
                    "Windows 95 Ready"
                ]

                award_y = self.content_box.y + 150
                for award in awards:
                    award_box = pygame.Rect(
                        right_section_x,
                        award_y,
                        180,
                        20
                    )
                    pygame.draw.rect(screen, (255, 215, 0), award_box)
                    pygame.draw.rect(screen, (0, 0, 0), award_box, 1)
                    award_text = self.font.render(award, True, (0, 0, 0))
                    screen.blit(award_text, (award_box.x + 5, award_box.y + 2))
                    award_y += 30

                # # Add "As seen on" section (Right side)
                # seen_on_y = award_y + 20
                # seen_on_text = self.font.render("AS SEEN ON:", True, (0, 0, 0))
                # screen.blit(seen_on_text, (right_section_x, seen_on_y))
                #
                # websites = ["YAHOO!", "GEOCITIES", "ALTAVISTA", "LYCOS"]
                # seen_on_y += 25
                # for site in websites:
                #     site_text = self.font.render("* " + site, True, (0, 0, 255))
                #     screen.blit(site_text, (right_section_x, seen_on_y))
                #     seen_on_y += 20
                #
                # # Footer
                # footer_text = self.font.render("Copyright (C) 1995 RAM-DOWNLOAD-NOW.COM", True, (128, 128, 128))
                # screen.blit(footer_text, (self.content_box.x + 20, self.content_box.height - 30))

        screen.blit(self.font.render("Address", True, (0, 0, 0)),
                    (self.rect.x + 5, self.rect.y + self.tab_height + self.title_bar_height + 3))

        # Draw the window frame
        pygame.draw.rect(screen, (0, 0, 0), (self.rect.x, self.rect.y, self.width, self.height), 2)  # Border

    def handle_event(self, event):
        super().handle_event(event)
        self.address_bar.handle_event(event)

        if self.isTimedOut and self.selected_tab == 0:
            credentials = self.loginbox.handle_event(event)
            if credentials == self.simulation.passwordToCrack:
                self.isTimedOut = False
                self.loginbox.text = ""


        if not self.simulation.is_cracking:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                if self.submit_pwd_rect.collidepoint(pos[0], pos[1]) and self.selected_tab == 0 and not self.isTimedOut:
                    self.passwordBox.active = False
                    print("Submit btn clicked")
                    self.simulation.new_password = True
                    self.simulation.passwordToCrack = self.passwordBox.text
                    self.passwordBox.text = ""
                elif self.submit_pwd_rect.collidepoint(pos[0], pos[1]) and self.selected_tab == 0 and self.isTimedOut:
                    if self.loginbox.text == self.simulation.passwordToCrack:
                        self.loginbox.active = False
                        print("Login btn clicked")
                        self.isTimedOut = False
                        self.loginbox.text = ""

            pwd = self.passwordBox.handle_event(event)
            if pwd != 0:
                print("Enter")
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
