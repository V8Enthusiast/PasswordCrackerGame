import random
import time


class Cracker:
    def __init__(self, simulation):
        self.simulation = simulation
        self.cache_passwords = self.simulation.cache_passwords
        self.use_cached_passwords = self.simulation.use_cached_passwords
        self.passwords_to_cache = []
        self.tried_passwords = []

        self.numbers = []

        self.dictionary = self.simulation.dictionary
        self.timeout_prob = 40

        f = open("cache/used_passwords.txt", "r")
        for line in f:
            if line.strip() == self.simulation.passwordToCrack:
                self.tried_passwords.append(line.strip())

        self.generate_numbers()

        self.lowercase_ascii_min = 97
        self.uppercase_ascii_min = 65
        self.special_ascii_min = 32

    def save_used_passwords(self):
        f = open("cache/used_passwords.txt", "w")
        for n in self.tried_passwords:
            f.write(n + "\n")
        f.close()

    def generate_numbers(self):
        for i in range(10**self.simulation.difficulty):
            if len(str(i)) >= 5:
                self.numbers.append(str(i))

    # O(k^n) k - charset length; n - password length
    def crackPwd(self, prev_char, length_remaining, current_guess, min_ascii):
        if length_remaining == 0:
            if self.cache_passwords:
                self.passwords_to_cache.append(current_guess)
            return current_guess

        for i in range(min_ascii, 126):
            t = self.crackPwd(prev_char + 1, length_remaining - 1, current_guess + chr(i), min_ascii)
            if t == self.simulation.passwordToCrack:
                self.simulation.current_guess = t
                if self.simulation.current_guess not in self.tried_passwords:
                    self.tried_passwords.append(self.simulation.current_guess)
                    self.save_used_passwords()
                if random.randint(0, 200) < self.timeout_prob:
                    self.simulation.internet_explorer.isTimedOut = True
                return t

    def crack(self):
        self.cache_passwords = False
        self.use_cached_passwords = False
        #### Settings changed to false for debugging ####

        # search cached passwords
        if self.use_cached_passwords:
            f = open("cache/cached_passwords.txt", "r")
            for line in f:
                if line.strip() == self.simulation.passwordToCrack:
                    return line

        self.passwords_to_cache = []

        for usedpwd in self.tried_passwords:
            if self.simulation.passwordToCrack == usedpwd:
                self.simulation.internet_explorer.selected_tab = 1
                self.simulation.current_guess = usedpwd
                if random.randint(0, 200) < self.timeout_prob:
                    self.simulation.internet_explorer.isTimedOut = True
                self.simulation.hack_method = "Known password"
                print("known password")
                return usedpwd

        # dictionary attack
        if self.dictionaryAttack() == self.simulation.passwordToCrack:
            self.simulation.internet_explorer.selected_tab = 1
            return self.simulation.passwordToCrack
        else:
            # number attack
            for num in self.numbers:
                if num == self.simulation.passwordToCrack:
                    self.simulation.internet_explorer.selected_tab = 1
                    self.simulation.current_guess = num
                    if random.randint(0, 200) < self.timeout_prob:
                        self.simulation.internet_explorer.isTimedOut = True
                    if self.simulation.current_guess not in self.tried_passwords:
                        self.tried_passwords.append(self.simulation.current_guess)
                        self.save_used_passwords()
                    self.simulation.hack_method = "Number attack"
                    print("number attack")
                    return num

            # bruteforce attack
            start_time = time.time()
            pwd = self.crackPwd(32, len(self.simulation.passwordToCrack), "", self.lowercase_ascii_min)
            if pwd != self.simulation.passwordToCrack:
                pwd = self.crackPwd(32, len(self.simulation.passwordToCrack), "", self.uppercase_ascii_min)
                if pwd != self.simulation.passwordToCrack:
                    pwd = self.crackPwd(32, len(self.simulation.passwordToCrack), "", self.special_ascii_min)
            print("Password: ", pwd)
            print("Time to find:", time.time() - start_time)
            self.simulation.internet_explorer.selected_tab = 1

            # save generated passwords
            if self.cache_passwords:
                f = open("cache/cached_passwords.txt", "w")
                for n in self.passwords_to_cache:
                    f.write(n+"\n")
                f.close()

            self.simulation.hack_method = "Bruteforce attack"
            print("bruteforce attack")
            self.save_used_passwords()
            return pwd

    def dictionaryAttack(self):
        current_dictionary_index = 0
        while True:
            try:
                self.simulation.current_guess = self.dictionary[current_dictionary_index][:self.simulation.difficulty]
                current_dictionary_index += 1
            except:
                return
            if self.simulation.current_guess == self.simulation.passwordToCrack:
                #self.simulation.passwordToCrack = None
                if random.randint(0, 200) < self.timeout_prob:
                    self.simulation.internet_explorer.isTimedOut = True

                if self.simulation.current_guess not in self.tried_passwords:
                    self.tried_passwords.append(self.simulation.current_guess)
                    self.save_used_passwords()
                self.simulation.hack_method = "Dictionary attack"
                print("dictionary attack")

                return self.simulation.current_guess


    def bruteforce2(self): # unused
        for n in range(1,10):
            list=[0 for x in range(n)]
            print(list)
            string=""
            run=True
            while run:
                string=""
                for x in range(n):
                    string += chr(list[x] + 32)

                if string==self.simulation.passwordToCrack:
                    self.simulation.passwordToCrack = None
                    return self.simulation.current_guess
                else:
                    print(string)
                    list[0]+=1
                    i=0
                    while True:
                        print(i,n-1)
                        print(list[i])
                        if list[i]>94:
                            list[i]=0
                            if i+1>n-1:
                                run=False
                                print('aaaaaaaaaaaaaaaaaa')
                            else:
                                list[i+1]+=1
                            i += 1
                        else:
                            break