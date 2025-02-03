from classes.window import Window
import pygame
import time
from classes import buttons
import random

class Cmd(Window):
    def __init__(self, x, y, width, height, title, font, icon,app):
        super().__init__(x, y, width, height, title, font, icon)
        self.app=app
        self.first_names=[line.strip() for line in open("AppData\\CMDfiles\\first-names.txt")]
        self.names=[line.strip() for line in open("AppData\\CMDfiles\\names.txt")]



        self.current_string = ""
        self.font2 = pygame.font.Font("fonts\\Windows98.ttf", 32)
        self.small_font = pygame.font.Font("fonts\\Windows98.ttf", 20)

        self.current_text = self.font2.render(self.current_string, True, (255, 255, 255))
        self.current_text_rect = self.current_text.get_rect()
        self.x = x
        self.y = y

        self.current_text_rect.x = self.x - 50
        self.current_text_rect.y = self.y - 50
        self.information = ""
        self.information_text = Multi_Text(self.surface,(""),self.font2,35,(self.x+270,self.y),(255,255,255))
        self.max_length=20

        self.correct_text=Multi_Text(self.surface,(""),self.font2,35,(self.x,self.y),(255,255,255))

        self.generate_password(1)
    def update_string(self):
        self.current_text = self.font2.render(self.current_string, True, (255, 255, 255))
        self.current_text_rect = self.current_text.get_rect()
        self.current_text_rect.x = self.x - 50
        self.current_text_rect.y = self.y - 50
    def draw(self,screen):
        super().draw(screen)
        self.surface.fill((0,0,0))
        self.surface.blit(self.current_text, self.current_text_rect)
        self.information_text.draw()
        self.correct_text.draw()

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
            if len(self.password)>self.max_length:
                self.generate_password(difficulty)
            self.information =f"First name: {self.first_name}Last Name: {self.name}"
            self.information_text.lines=["Information:",f"First name: {self.first_name}",f"Last name: {self.name}"]
            self.information_text.update()
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
                            self.correct_text.color=(0,255,0)
                            self.correct_text.lines=["CORRECT"]
                            self.correct_text.update()

                            a = pygame.mixer.Sound("img/yes.mp3")
                            a.set_volume(1)
                            a.play()
                        # if self.current_string=='Lolek Is Gay':
                        #     print("Correct")
                        #     self.correct_text.color=(0,255,0)
                        #     self.correct_text.lines=["CORRECT"]
                        #     self.correct_text.update()

                            a = pygame.mixer.Sound("img/yes.mp3")
                            a.set_volume(1)
                            a.play()

                        else:
                            print("Incorrect")
                            self.correct_text.color = (255, 0, 0)
                            self.correct_text.lines = ["INCORRECT"]
                            self.correct_text.update()
                            pygame.mixer.music.load("img/no.mp3")
                            pygame.mixer.music.play()
                    except:
                        print("NOPE. Invalid")
                    # eval(f" = {}")
                    print(self.current_string)
                elif event.key == pygame.K_BACKSPACE:
                    self.current_string = self.current_string[:-1]
                else:
                    print('aaaaaaa')
                    if len(self.current_string)<self.max_length:
                        self.current_string += event.unicode
                self.update_string()
class Multi_Text():
    def __init__(self,surface,lines,font ,size,pos,color):
        self.lines=lines
        self.surface=surface

        self.pos=pos
        self.texts=[]
        self.size=size
        self.font=font
        self.color=color
        for x in range(len(self.lines)):
            a=self.font.render(self.lines[x], True, self.color)
            a_rect = self.a.get_rect()
            a_rect.x = self.pos[0]
            a_rect.y = self.pos[1]+(self.size+2)*x
            self.texts.append((a,a_rect))


    def update(self):
        self.texts = []
        for x in range(len(self.lines)):
            a = self.font.render(self.lines[x], True, self.color)
            a_rect = a.get_rect()
            a_rect.x = self.pos[0]
            a_rect.y = self.pos[1] + (self.size + 2) * x
            self.texts.append((a, a_rect))
    def draw(self):
        for x in range(len(self.texts)):
            self.surface.blit(self.texts[x][0],self.texts[x][1])