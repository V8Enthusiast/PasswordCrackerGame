import random


class Cracker:
    def __init__(self, simulation):
        self.simulation = simulation
        self.cache_passwords = self.simulation.cache_passwords
        self.use_cached_passwords = self.simulation.use_cached_passwords
        self.passwords_to_cache = []
        self.tried_passwords = []
        self.dictionary = self.simulation.dictionary
        self.timeout_prob = 40

    # O(k^n) k - charset length; n - password length
    def crackPwd(self, prev_char, length_remaining, current_guess):
        if length_remaining == 0:
            if self.cache_passwords:
                self.passwords_to_cache.append(current_guess)
            return current_guess

        for i in range(32, 126):
            t = self.crackPwd(prev_char + 1, length_remaining - 1, current_guess + chr(i))
            if t == self.simulation.passwordToCrack:
                self.simulation.current_guess = t
                self.tried_passwords.append(t)
                if random.randint(0, 200) < self.timeout_prob:
                    self.simulation.internet_explorer.isTimedOut = True
                return t

    def bruteforce(self):
        self.cache_passwords = False
        self.use_cached_passwords = False
        #### Settings changed to false for debugging ####

        # Search cached passwords
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
                return usedpwd

        pwd = self.crackPwd(32, len(self.simulation.passwordToCrack), "")
        self.simulation.internet_explorer.selected_tab = 1

        # Save generated passwords
        if self.cache_passwords:
            f = open("cache/cached_passwords.txt", "w")
            for n in self.passwords_to_cache:
                f.write(n+"\n")
            f.close()
        return pwd

    def dictionaryAttack(self):
        current_dictionary_index = 0
        while True:
            try:
                self.simulation.current_guess = self.dictionary[current_dictionary_index]
                current_dictionary_index += 1
            except:
                return
            if self.simulation.current_guess == self.simulation.passwordToCrack:
                self.simulation.passwordToCrack = None
                return self.simulation.current_guess


    def bruteforce2(self): # Assuming the hacker knows the password length
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