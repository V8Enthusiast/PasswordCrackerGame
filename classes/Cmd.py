from classes.window import Window
import pygame
from classes import buttons
import random

class Cmd(Window):
    def __init__(self, x, y, width, height, title, font, icon,app):
        super().__init__(x, y, width, height, title, font, icon)
        self.app=app
        self.first_names=[line.strip() for line in open("AppData\\CMDfiles\\first-names.txt")]
        self.names=[line.strip() for line in open("AppData\\CMDfiles\\names.txt")]
        self.generate_password(1)


        self.current_string = ""
        self.font2 = pygame.font.Font("fonts\\Windows98.ttf", 32)
        self.small_font = pygame.font.Font("fonts\\Windows98.ttf", 20)

        self.current_text = self.font2.render(self.current_string, True, (255, 255, 255))
        self.current_text_rect = self.current_text.get_rect()
        self.x = x
        self.y = y

        self.current_text_rect.x = self.x - 50
        self.current_text_rect.y = self.y - 50
    def update_string(self):
        self.current_text = self.font2.render(self.current_string, True, (255, 255, 255))
        self.current_text_rect = self.current_text.get_rect()
        self.current_text_rect.x = self.x - 50
        self.current_text_rect.y = self.y - 50
    def draw(self,screen):
        super().draw(screen)
        self.surface.fill((0,0,0))
        self.surface.blit(self.current_text, self.current_text_rect)
    def generate_password(self,difficulty):
        if difficulty==1:
            self.first_name=random.choice(self.first_names)
            self.name=random.choice(self.first_names)
            print(self.first_name,self.name)
            a=random.randint(0,3)
            if a==0:
                self.password=self.first_name+self.name
            elif a==1:
                self.password = self.name + self.first_name
            elif a==2:
                self.password = self.name
            else:
                self.password = self.first_name
            print(self.password)
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
                print("Nuhuh")

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


        #     dict={pygame.K_0:("0",")"),pygame.K_1:("1",""),pygame.K_2:("2",""),pygame.K_3:("3",""),pygame.K_4:("4",""),pygame.K_5:("5",""),pygame.K_6:("6",""),pygame.K_7:("7",""),pygame.K_8:("8","*"),pygame.K_9:("9","("),pygame.K_SPACE:(" ",""),pygame.K_EQUALS:("","+"),pygame.K_MINUS:("-",""),pygame.K_SLASH:(":",""),pygame.K_SEMICOLON:("",":")}
        #
        #     e=event.key
        #     print(e)
        #     if e == pygame.K_LSHIFT or e == pygame.K_RSHIFT:
        #         self.shift = True
        #     for x in dict.keys():
        #         if e==x:
        #             if self.shift:
        #                 self.current_string+=dict[e][1]
        #             else:
        #
        #                 self.current_string += dict[e][0]
        #             self.update_string()
        # elif event.type==pygame.KEYUP:
        #     if event.key==pygame.K_LSHIFT or event.key==pygame.K_RSHIFT:
        #         self.shift=False\

        elif event.type == pygame.KEYDOWN:

            if self.active:
                if event.key == pygame.K_RETURN:
                    try:

                        if self.current_string==self.password:
                            print("Correct")
                    except:
                        print("NOPE. Invalid")
                    # eval(f" = {}")
                    print(self.current_string)
                elif event.key == pygame.K_BACKSPACE:
                    self.current_string = self.current_string[:-1]
                else:
                    print('aaaaaaa')
                    self.current_string += event.unicode
                self.update_string()
