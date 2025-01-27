from classes.window import Window
import pygame
from classes import buttons

class Calculator(Window):
    def __init__(self, x, y, width, height, title, font, icon,app):
        super().__init__(x, y, width, height, title, font, icon)
        self.app=app
        self.current_string="8*8"
        self.font2=pygame.font.Font("fonts\\Windows98.ttf",32)
        self.small_font=pygame.font.Font("fonts\\Windows98.ttf",20)

        self.current_text = self.font2.render(self.current_string,True,(255,255,255))
        self.current_text_rect=self.current_text.get_rect()
        self.x=x
        self.y=y

        self.current_text_rect.x = self.x-50
        self.current_text_rect.y = self.y-50
        self.length = 59
        self.button0_icon = pygame.transform.scale(pygame.image.load('img/button0.png'), (self.length, self.length))

        self.create_buttons()
        self.button_images=[]
    def create_buttons(self):
        self.new_buttons=[]
        offset=3
        length=self.length
        self.buttons_characters=["1","2","3","/","4","5","6","*","7","8","9","-",".","0","=","+","Back"]
        i=0
        for y in range(0,4):
            for x in range(0,4):
                new_button=buttons.Button(length - 2 * offset, length - 2 * offset, 2 + length * x + offset,
                               135 + y * length + offset, self.font2, self.buttons_characters[i], None, self.app)
                self.new_buttons.append(new_button)
                new_button.new_index=i
                i+=1
        new_button = buttons.Button(length - 2 * offset, length - 2 * offset, 2 + length * 3 + offset,
                                    135 + -1 * length + offset, self.small_font, self.buttons_characters[i], None, self.app)
        self.new_buttons.append(new_button)
        new_button.new_index = i
        self.new_buttons.append(new_button)
    def update_string(self):
        self.current_text = self.font2.render(self.current_string, True, (255, 255, 255))
        self.current_text_rect = self.current_text.get_rect()
        self.current_text_rect.x = self.x - 50
        self.current_text_rect.y = self.y - 50
    def draw(self,screen):
        super().draw(screen)
        self.surface.fill((0,0,0))
        self.surface.blit(self.current_text, self.current_text_rect)

        for button in self.new_buttons:
            button.render(self.surface)

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

            for button in self.new_buttons:
                if button.rect.collidepoint((event.pos[0]-self.rect.x,event.pos[1]-self.rect.y-25)):
                    if not (button.text=="=" or button.text=="Back"):
                        self.current_string+=button.text
                        self.update_string()
                    elif button.text=="=":

                        try:
                            self.current_string = str(eval(self.current_string))

                            self.update_string()

                        except:
                            print("NOPE. Invalid")
                        # eval(f" = {}")
                        print(self.current_string)
                    elif button.text=="Back":
                        print(self.current_string)
                        self.current_string=self.current_string[0:len(self.current_string)-1]
                        print(self.current_string)
                        self.update_string()
                        break



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

                        self.current_string=str(eval(self.current_string))
                    except:
                        print("NOPE. Invalid")
                    # eval(f" = {}")
                    print(self.current_string)
                elif event.key == pygame.K_BACKSPACE:
                    self.current_string = self.current_string[:-1]
                else:
                    self.current_string += event.unicode
                self.update_string()