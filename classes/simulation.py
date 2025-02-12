import os
import time

import pygame
import threading
import datetime
from typing import Optional, List, Union

import random

from classes import gameover, winscreen
from classes.minesweeper import Minesweeper
from classes.calculator import Calculator
from classes.Cmd import Cmd
from classes.startmenu import StartMenu
from classes.internet_explorer import InternetExplorer
from classes.nfs import VroomVroom
from classes.window import Window
from classes.buttons import Button
from classes.cracking import Cracker

class Simulation:
    def __init__(self, app, start_pwd, diff):
        self.app = app
        self.debug = False
        self.bg_color = (0, 142, 144)
        self.screen = self.app.screen
        self.buttons = []
        self.font = pygame.font.SysFont("Arial", 32)
        self.font98 = pygame.font.Font("fonts/Windows98.ttf", 24)
        self.font98_small = pygame.font.Font("fonts/Windows98.ttf", 16)

        self.side_margin = int(20 * self.app.scale)
        self.widthA = 200
        self.heightA = 300

        # Define taskbar and buttons
        self.taskbar_height = 40
        self.taskbar_color = (192, 192, 192)

        self.start_height = 40
        self.start_color = (192, 192, 192)
        self.button_shadow_color = (10, 10, 10)
        self.button_highlight_color = (220, 220, 220)
        self.buttons = [
            Button(90, 30,10, self.screen.get_height() - self.taskbar_height + 5, self.font98,"Start", 'start', self.app, icon='img/win98.png', size=(32,32)),
            Button(190, 30,110, self.screen.get_height() - self.taskbar_height + 5, self.font98,"Terminal", 'mycomputer', self.app, icon='img/MyComputer98.png',size=(32, 32)),
            Button(190, 30,307, self.screen.get_height() - self.taskbar_height + 5, self.font98,"Internet Explorer", 'internetexplorer', self.app, icon='img/InternetExplorer98.png',size=(24, 24)),
            Button(190, 30,503, self.screen.get_height() - self.taskbar_height + 5, self.font98,"Calculator", 'calculator', self.app, icon='img/Calc.png',size=(24, 24))
        ]
        self.active_button = None
        self.transactions = [
            ("05/15/95", "GROCERY STORE", "-$45.82", "$100,000.00"),
            ("05/14/95", "SALARY DEPOSIT", "+$33,500.00", "$69,045.82"),
            ("05/13/95", "GAS STATION", "-$22.15", "$66,545.82"),
            ("05/12/95", "MOVIE RENTAL", "-$3.99", "$66,567.97"),
            # ("05/11/95", "PHONE BILL", "-$65.00", "$66,571.96")
        ]

        self.icons = [
            pygame.transform.scale(pygame.image.load('img/win98.png'), (32, 32)),
            pygame.transform.scale(pygame.image.load('img/MyComputer98.png'), (32, 32)),
            pygame.transform.scale(pygame.image.load('img/InternetExplorer98.png'),(24, 24)),
            pygame.transform.scale(pygame.image.load('img/Calc.png'), (24, 24))
        ]

        self.cache_passwords = True
        self.use_cached_passwords = True
        self.passwords_to_cache = []

        self.cracking_thread = None
        self.is_cracking = False
        self.thread_lock = threading.Lock()

        self.priority_manager = ThreadPriorityManager()
        self.cpu_affinity = None

        self.start_time = time.time()
        self.end_time = None
        self.start_password = start_pwd
        self.difficulty = diff # max length of the password
        self.money = 100_000
        self.money_lost_per_frame = 100

        self.passwordToCrack = self.start_password
        self.new_password = True
        self.GameOver = False
        self.hack_method = ""


        self.current_guess = ""
        self.dictionary = []
        self.current_dictionary_index = 0
        f = open("Dictionaries/Words.list", "r")
        for line in f:
            self.dictionary.append(line.strip())
        f.close()

        f = open("Dictionaries/polskie_hasla.txt", "r")
        for line in f:
            self.dictionary.append(line.strip())
        f.close()


        self.dictionary_len = len(self.dictionary)
        self.cracker = Cracker(self)

        self.internet_explorer = InternetExplorer(150, 150, 600, 400, "Internet Explorer", self.font98_small,
                                                  pygame.transform.scale(
                                                      pygame.image.load('img/InternetExplorer98.png'), (18, 18)), self)

        self.windows = [
            Minesweeper(50, 50, 300, 200, "Minesweeper", self.font98_small, pygame.transform.scale(pygame.image.load('img/InternetExplorer98.png'), (18, 18))),
            VroomVroom(50, 50, 600, 400, "NFS pre-alpha", self.font98_small, pygame.transform.scale(pygame.image.load('img/InternetExplorer98.png'), (18, 18))),
            self.internet_explorer
            ]

        self.didJustGuessPassword = False
        self.hacked_person_name = ""
        self.isFreeRAMDownloaded = False
        self.free_ram_download_time = None
        self.epilepsy_mode = False
        self.change_colors = True

        self.timeout = 600 # seconds
        # Around 25 - 30 mins to bruteforce 5 char long password with special chars
        self.current_password_time = time.time()
        self.didWinGame = False






    def set_thread_priority(self):
        self.priority_manager.set_high_priority("ALL")

    def start_cracking_thread(self):
        """Starts the password cracking in a separate thread with enhanced priority"""
        if self.cracking_thread is None or not self.cracking_thread.is_alive():
            self.is_cracking = True
            self.cracking_thread = threading.Thread(
                target=self.run_cracking,
                name="CrackingThread",
                daemon=True
            )

            self.cracking_thread.start()

            threading.Thread(target=self.set_thread_priority, daemon=True).start()

    def run_cracking(self):
        """Enhanced cracking thread with resource management"""
        try:
            if self.cpu_affinity:
                if os.name == 'nt':
                    import win32api
                    win32api.SetThreadAffinityMask(win32api.GetCurrentThread(), self.cpu_affinity)

            result = self.cracker.crack()

            with self.thread_lock:
                print(f"Password found: {result}")
                self.is_cracking = False

        except Exception as e:
            print(f"Error in cracking thread: {e}")
            self.is_cracking = False
        finally:
            if self.cpu_affinity:
                try:
                    if os.name == 'nt':
                        import win32api
                        import win32process
                        process = win32api.GetCurrentProcess()
                        win32process.SetProcessAffinityMask(process, 0xFFFF)  # Reset to all cores
                except:
                    pass
    def cleanup_threads(self):
        """Clean up thread resources before exit"""
        if self.cracking_thread and self.cracking_thread.is_alive():
            self.is_cracking = False
            self.cracking_thread.join(timeout=2.0)

    def render(self):
        if self.isFreeRAMDownloaded and self.free_ram_download_time + 7 > time.time() and self.epilepsy_mode:

            self.bg_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            self.taskbar_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            self.start_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            self.button_shadow_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            self.button_highlight_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        elif self.isFreeRAMDownloaded and self.change_colors:
            self.bg_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            self.taskbar_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            self.start_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            self.button_shadow_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            self.button_highlight_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            self.change_colors = False
            self.buttons = [
                Button(190, 30, random.randint(0, 1200), random.randint(0, 800), self.font98, "FREE RAM!!", 'start',
                       self.app, icon='img/win98.png', size=(32, 32)),
                Button(190, 30, random.randint(0, 1200),  random.randint(0, 800), self.font98, "FREE RAM!!",
                       'mycomputer', self.app, icon='img/MyComputer98.png', size=(32, 32)),
                Button(190, 30, random.randint(0, 1200),  random.randint(0, 800), self.font98,
                       "Internet Explorer", 'internetexplorer', self.app, icon='img/InternetExplorer98.png',
                       size=(24, 24)),
                Button(190, 30, random.randint(0, 1200), random.randint(0, 800), self.font98, "FREE RAM!!",
                       'calculator', self.app, icon='img/Calc.png', size=(24, 24))
            ]

        elif self.isFreeRAMDownloaded and self.free_ram_download_time + 7 < time.time():
            self.hack_method = "FREE RAM"
            self.GameOver = True
            self.end_time = time.time()

        self.screen.fill(self.bg_color)

        if self.GameOver:
            print("You Lose!")
            print("Score: ", self.end_time - self.start_time)
            self.app.ui = gameover.GameOver(self.app, self.end_time - self.start_time)

        if time.time() > self.current_password_time + self.timeout and not self.didWinGame:
            print("Password seems good!")
            self.app.ui = winscreen.WinScreen(self.app, self.money)
            self.didWinGame = True

        active_window = None
        breach = False
        if self.passwordToCrack == self.current_guess:
            if self.money - self.money_lost_per_frame <= 0 and self.GameOver is False:
                self.money = 0
                self.GameOver = True
                self.end_time = time.time()
            elif self.GameOver is False:
                self.money -= self.money_lost_per_frame
                self.transactions.pop(-1)
                self.transactions.insert(0, ("05/15/95", "SHADYDEALS CO", f"-${self.money_lost_per_frame}", f"${self.money//1000},{self.money%1000:03d}.00"))
            #print(self.money)
            active_window = self.internet_explorer
            breach = True

        for window in self.windows:
            if window.minimized is False:
                if not window.active or active_window is not None or breach:
                    window.draw(self.screen)
                else:
                    active_window = window
        if active_window is not None:
            active_window.draw(self.screen)

        if self.didJustGuessPassword:
            randomReward = random.randint(2500, 5000)
            self.money += randomReward
            self.transactions.pop(-1)
            self.transactions.insert(0, (
            "05/15/95", self.hacked_person_name, f"+${randomReward}",
            f"${self.money // 1000},{self.money%1000:03d}.00"))
            self.didJustGuessPassword = False

        ## Taskbar ##
        pygame.draw.rect(self.screen, self.taskbar_color, (0, self.screen.get_height() - self.taskbar_height, self.screen.get_width(), self.taskbar_height))

        ## Buttons ##

        # draw ridge between buttons
        ridge_x = self.buttons[0].rect.right + 5
        pygame.draw.line(self.screen, (100, 100, 100), (ridge_x, self.screen.get_height() - self.taskbar_height + 5), (ridge_x, self.screen.get_height() - 5), 2)

        # draw buttons
        for i, button in enumerate(self.buttons):
                button.render(self.screen)

        ## Clock ##
        clock_rect = pygame.Rect(self.screen.get_width() - 110, self.screen.get_height() - self.taskbar_height + 5, 100, 30)
        pygame.draw.rect(self.screen, self.button_shadow_color, clock_rect.move(-2, -2))  # Shadow

        pygame.draw.rect(self.screen, self.button_highlight_color, clock_rect.move(2, 2))  # Highlight
        pygame.draw.rect(self.screen, self.taskbar_color, clock_rect)  # Same background color


        current_time = datetime.datetime.now().strftime("%H:%M")
        clock_surface = self.font98.render(current_time, True, (0, 0, 0))
        clock_text_rect = clock_surface.get_rect(center=clock_rect.center)
        self.screen.blit(clock_surface, clock_text_rect)

        ## Text ##
        # with self.thread_lock:
        #     if self.passwordToCrack is not None and self.is_cracking:
        #         display_text = self.font.render(self.current_guess, True, (200, 200, 200))
        #         display_text_rect = display_text.get_rect()
        #         display_text_rect.center = (self.screen.get_width()//2 - 100, self.screen.get_height()//2)
        #         self.app.screen.blit(display_text, display_text_rect)

    def events(self):
        if not self.isFreeRAMDownloaded:
            for event in pygame.event.get():
                for window in self.windows:
                    window.handle_event(event)
                    if window.active:
                        for button in self.buttons:
                            if button.text == window.title:
                                button.selected = True
                            else:
                                button.selected = False
                    if window.minimized:
                        for button in self.buttons:
                            if window.minimized and button.text == window.title and button.selected:
                                button.selected = False

                if event.type == pygame.QUIT:
                    self.cleanup_threads()
                    self.app.run = False

                if self.passwordToCrack and self.new_password:

                    self.start_cracking_thread()
                    self.new_password = False
                    self.current_password_time = time.time()
                    #self.current_guess = ""
                    #print(self.cracker.bruteforce())
                    # print(self.dictionaryAttack())
                    print("$")
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        for i, button in enumerate(self.buttons):
                            if button.rect.collidepoint(event.pos):
                                print(f"Button {i + 1} clicked")
                                if self.active_button is not None:
                                    self.active_button.selected = False
                                button.selected = True
                                self.active_button = button
                                window_already_open = False
                                for window in self.windows:
                                    if window.closed:
                                        self.windows.remove(window)
                                    if window.title == button.text:
                                        window_already_open = True
                                        window.minimized = False
                                        window.active = True

                                if window_already_open is False:
                                    if button.text=="Start":
                                        self.widthA = 200
                                        self.heightA = 300
                                        new_window = StartMenu(0, self.app.height - self.heightA - self.taskbar_height, self.widthA, self.heightA, button.text, self.font98_small,
                                                            self.icons[i], self.app)
                                        new_window.draw(self.screen)
                                        new_window.active = True
                                        self.windows.append(new_window)
                                    # elif button.text=="Calculator":
                                    #     new_window = Calculator(50, 50, 266, 400, self.button_labels[i], self.font98_small,
                                    #                         self.icons[i], self.app)
                                    elif button.text=="Calculator":
                                        new_window = Calculator(50, 50, 240, 400, button.text, self.font98_small,
                                                            self.icons[i],self.app)
                                        new_window.draw(self.screen)
                                        new_window.active = True
                                        self.windows.append(new_window)
                                    elif button.text=="Terminal":
                                        new_window = Cmd(50, 50, 600, 400, button.text, self.font98_small,
                                                                self.icons[i], self.app, self)
                                        new_window.draw(self.screen)
                                        new_window.active = True
                                        self.windows.append(new_window)
                                    elif button.text=="Internet Explorer":
                                        # new_window = InternetExplorer(50, 50, 600, 400, "Internet Explorer", self.font98_small, pygame.transform.scale(pygame.image.load('img/InternetExplorer98.png'), (18, 18)))
                                        # new_window.draw(self.screen)
                                        # new_window.active = True
                                        # self.windows.append(new_window)
                                        self.internet_explorer = InternetExplorer(150, 150, 600, 400, "Internet Explorer",
                                                                                  self.font98_small, pygame.transform.scale(
                                                pygame.image.load('img/InternetExplorer98.png'), (18, 18)), self)
                                        self.internet_explorer.draw(self.screen)
                                        self.internet_explorer.active = True
                                        self.windows.append(self.internet_explorer)
                                    else:
                                        new_window = Window(50, 50, 600, 400, button.text, self.font98_small, self.icons[i])
                                        new_window.draw(self.screen)
                                        new_window.active = True
                                        self.windows.append(new_window)

class ThreadPriorityManager:
    def __init__(self):
        self.is_windows = os.name == 'nt'
        self._win32process = None
        self._win32api = None
        self._psutil = None

        if self.is_windows:
            try:
                import win32process
                import win32api
                self._win32process = win32process
                self._win32api = win32api
            except ImportError:
                print("Warning: win32api not found. Install pywin32 for Windows priority management")
        else:
            try:
                import psutil
                self._psutil = psutil
            except ImportError:
                print("Warning: psutil not found. Install psutil for Unix priority management")

    def get_available_cores(self) -> int:
        """Returns the number of CPU cores available on the system"""
        try:
            if self.is_windows:
                return len(os.sched_getaffinity(0)) if hasattr(os, 'sched_getaffinity') else os.cpu_count()
            else:
                import psutil
                return len(psutil.Process().cpu_affinity())
        except:
            return os.cpu_count() or 1

    def set_high_priority(self, cpu_cores: Optional[Union[List[int], str]] = None) -> bool:
        """
        Sets the current thread to high priority and assigns CPU cores.

        Args:
            cpu_cores: List of CPU core numbers or "ALL" to use all cores
                      Example: [0,1,2,3] for first four cores, or "ALL" for all cores

        Returns:
            bool: True if priority was set successfully
        """
        try:
            if cpu_cores == "ALL":
                available_cores = self.get_available_cores()
                cpu_cores = list(range(available_cores))

            if self.is_windows:
                return self._set_windows_priority(cpu_cores)
            return self._set_unix_priority(cpu_cores)
        except Exception as e:
            print(f"Failed to set thread priority: {e}")
            return False

    def _set_windows_priority(self, cpu_cores: Optional[List[int]]) -> bool:
        """Sets high priority for Windows systems"""
        if not self._win32process or not self._win32api:
            return False

        try:
            current_thread = self._win32api.GetCurrentThread()
            self._win32process.SetThreadPriority(
                current_thread,
                self._win32process.THREAD_PRIORITY_HIGHEST
            )

            if cpu_cores is not None:
                process = self._win32api.GetCurrentProcess()
                mask = sum(1 << core for core in cpu_cores)
                self._win32process.SetProcessAffinityMask(process, mask)

            return True
        except Exception as e:
            print(f"Windows priority setting failed: {e}")
            return False

    def _set_unix_priority(self, cpu_cores: Optional[List[int]]) -> bool:
        """Sets high priority for Unix-like systems"""
        if not self._psutil:
            return False

        try:
            process = self._psutil.Process()

            process.nice(-20)

            if cpu_cores is not None:
                process.cpu_affinity(cpu_cores)

            return True
        except Exception as e:
            print(f"Unix priority setting failed: {e}")
            return False

    def reset_priority(self) -> bool:
        """Resets thread priority and CPU affinity to default values"""
        try:
            if self.is_windows:
                if self._win32process and self._win32api:
                    current_thread = self._win32api.GetCurrentThread()
                    self._win32process.SetThreadPriority(
                        current_thread,
                        self._win32process.THREAD_PRIORITY_NORMAL
                    )
                    process = self._win32api.GetCurrentProcess()
                    all_cores_mask = (1 << self.get_available_cores()) - 1
                    self._win32process.SetProcessAffinityMask(process, all_cores_mask)
            else:
                if self._psutil:
                    process = self._psutil.Process()
                    process.nice(0)
                    all_cores = list(range(self.get_available_cores()))
                    process.cpu_affinity(all_cores)

            return True
        except Exception as e:
            print(f"Failed to reset priority: {e}")
            return False