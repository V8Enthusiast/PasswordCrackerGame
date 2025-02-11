from classes.window import Window
import pygame
import time
from classes import buttons
import random

class Cmd(Window):
    def __init__(self, x, y, width, height, title, font, icon,app, simulation):
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
        self.information_text = Multi_Text(self.surface,(""),self.font2,35,(self.x+220,self.y),(255,255,255))
        self.max_length=20
        self.max_diff=8
        self.correct_text=Multi_Text(self.surface,(""),self.font2,35,(self.x,self.y),(255,255,255))
        self.diff_text=Multi_Text(self.surface,(""),self.small_font,35,(self.x+465,self.y-50),(255,255,255))
        self.generate_password(8)
        self.simulation = simulation

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
        self.diff_text.draw()

    def generate_password(self,difficulty):
        self.diff_text.lines=[f"Difficulty: {difficulty}"]
        self.diff_text.update()
        if difficulty==1:
            self.name = random.choice(self.names)
            self.ye = str(random.randint(1960, 2020))
            self.m = str(random.randint(1, 12))
            if len(self.m) == 1:
                self.m = f"0{self.m}"

            self.d = str(random.randint(1, 28))
            if len(self.d) == 1:
                self.d = f"0{self.d}"
            self.password=self.ye
            if len(self.password) > self.max_length:
                self.generate_password(difficulty)

            self.information_text.lines = ["Information:",
                                           f"Birthday: {self.d}.{self.m}.{self.ye}","Note: 'Password ","contains only numbers'"]
            self.information_text.update()
            print(self.password)


        elif difficulty==2:
            self.first_name=random.choice(self.first_names)
            self.name=random.choice(self.names)
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
        elif difficulty==3:
            self.name = random.choice(self.names)
            self.ye=str(random.randint(1960,2020))
            self.m=str(random.randint(1,12))
            if len(self.m)==1:
                self.m=f"0{self.m}"

            self.d=str(random.randint(1,28))
            if len(self.d)==1:
                self.d=f"0{self.d}"
            a = random.randint(0, 2)
            if a==0:
                self.password=self.name+str(self.ye)
            elif a==1:
                self.password=self.name+str(self.m)
            elif a==2:
                self.password=self.name+str(self.d)
            if len(self.password) > self.max_length:
                self.generate_password(difficulty)

            self.information_text.lines = ["Information:", f"Last name: {self.name}",f"Birthday: {self.d}.{self.m}.{self.ye}"]
            self.information_text.update()
            print(self.password)
        elif difficulty==4:
            self.name = random.choice(self.names)
            self.age=random.randint(10,90)
            self.password_age=random.randint(2,9)
            self.password=self.name+str(self.age-self.password_age)
            self.information_text.lines = ["Information:",
                                           f"Last name: {self.name}", f"Age: {self.age}","Note: 'Password was ",
                                           f"created {self.password_age} years ago'" ]
            self.information_text.update()
        elif difficulty==5:
            self.first_name = random.choice(self.first_names)
            self.name = random.choice(self.names)
            self.favourite_number=random.randint(11,99)
            a = random.randint(0, 3)

            if a == 0:
                self.password = self.first_name + self.name
            elif a == 1:
                self.password = self.name + self.first_name
            elif a == 2:
                self.password = self.name
            else:
                self.password = self.first_name
            if random.randint(0,1)==0:
                self.password+=str(self.favourite_number)
            if len(self.password) > self.max_length:
                self.generate_password(difficulty)
            self.information = f"First name: {self.first_name}Last Name: {self.name}"
            self.information_text.lines = ["Information:", f"First name: {self.first_name}", f"Last name: {self.name}",f"Favourite number: {self.favourite_number}",f"Note: 'Number may be" ,"placed on the end'"]
            self.information_text.update()
            print(self.password)
        elif difficulty==6:
            self.first_name = random.choice(self.first_names)
            self.name = random.choice(self.names)
            self.favourite_number = random.randint(11, 99)
            a = random.randint(0, 1)

            if a == 0:
                self.password = self.first_name +"_"+ self.name
            elif a == 1:
                self.password = self.name +"_"+ self.first_name
            self.password += str(self.favourite_number)
            if len(self.password) > self.max_length:
                self.generate_password(difficulty)
            self.information = f"First name: {self.first_name}Last Name: {self.name}"
            self.information_text.lines = ["Information:", f"First name: {self.first_name}", f"Last name: {self.name}",
                                           f"Favourite number: {self.favourite_number}", f"Note: 'Password contains _'"]
            self.information_text.update()
            print(self.password)
        elif difficulty==7:
            self.random_number=str(random.randint(0,9))
            self.name = random.choice(self.names)
            self.password=self.name+self.random_number
            self.information_text.lines = ["Information:",  f"Last name: {self.name}",
                                            f"Note: 'Password contains","single digit number'"]
            self.information_text.update()
            print(self.password)
        elif difficulty==8:
            self.first_name = random.choice(self.first_names)
            self.name = random.choice(self.names)
            if random.randint(0,1)==1:
                self.password=self.first_name+self.name[0]
            else:
                self.password = self.first_name + self.name[0:2]
            self.information_text.lines=["Information:",f"First name {self.first_name}", f"Last name: {self.name}",
             f"Note: 'User usually", "doesn't use full last name'",""]
            self.information_text.update()
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
                            print(self.first_name)
                            print(self.name)
                            self.simulation.hacked_person_name = self.first_name + " " + self.name
                            self.correct_text.color=(0,255,0)
                            self.correct_text.lines=["CORRECT"]
                            self.correct_text.update()

                            self.simulation.didJustGuessPassword = True

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

                            self.generate_password(random.randint(1,self.max_diff))
                            self.current_string=""
                            self.update_string()
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