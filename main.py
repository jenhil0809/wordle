from wordfreq import zipf_frequency, top_n_list
from random import choice
from colorama import Fore


class Wordle:
    def __init__(self, length: int = 5):
        self.length = length
        self.common_words = [word for word in top_n_list('en', 10000)
                             if len(word) == self.length and "'" not in word]
        self.secret_word = ""
        self.set_secret_word()
        self.guessed_word = ""
        self.game = Game(self)

    def set_secret_word(self):
        self.secret_word = choice(self.common_words)

    def set_guessed_word(self, word):
        self.guessed_word = word

    def matches(self):
        lst = []
        for i in range(self.length):
            if self.guessed_word[i] == self.secret_word[i]:
                lst.append((self.guessed_word[i], 2))
            elif self.guessed_word[i] in self.secret_word:
                lst.append((self.guessed_word[i], 1))
            else:
                lst.append((self.guessed_word[i], 0))
        return self.guessed_word == self.secret_word, lst


class Game:
    def __init__(self, master, guess_num: int = 6):
        self.master = master
        self.guess_num = guess_num
        self.guesses = []
        self.interface = Interface()
        self.play_game()

    def play_game(self):
        self.get_guess()
        while len(self.guesses) < self.guess_num and not self.master.matches()[0]:
            self.get_guess()
        print(f"Answer={self.master.secret_word}\n\n")
        self.reset_game()

    def get_guess(self):
        guess = self.interface.get_guess(self.master.length, self.guesses)
        self.guesses.append(guess.upper())
        self.master.set_guessed_word(guess)
        self.interface.print_guess(guess, self.master.matches()[1])

    def reset_game(self):
        self.guesses = []
        self.master.set_secret_word()
        self.play_game()


class Interface:
    def __init__(self):
        self.matches = []

    def print_guess(self, guess, matches):
        self.matches = matches
        for i in range(len(guess)):
            if self.matches[i][1] == 0:
                print(f"{Fore.RED}{guess[i].upper()}{Fore.WHITE}", end="")
            elif self.matches[i][1] == 1:
                print(f"{Fore.YELLOW}{guess[i].upper()}{Fore.WHITE}", end="")
            else:
                print(f"{Fore.GREEN}{guess[i].upper()}{Fore.WHITE}", end="")
        print("\n")

    def get_guess(self, length, guesses):
        guess = ""
        while (len(guess) != length or zipf_frequency(guess, "en") == 0.0 or
               guess.upper() in guesses or not guess.isalpha()):
            guess = input("Guess: ")
        return guess


if __name__ == "__main__":
    game = (Wordle(5))
