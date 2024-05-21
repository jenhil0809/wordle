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
    def __init__(self, master):
        self.master = master
        self.guesses = []
        self.play_game()

    def play_game(self):
        self.get_guess()
        while len(self.guesses) < 6 and not self.master.matches()[0]:
            self.get_guess()
        print(f"Answer={self.master.secret_word}\n\n")
        self.reset_game()

    def get_guess(self):
        guess = ""
        while (len(guess) != self.master.length or zipf_frequency(guess, "en") == 0.0 or
               guess.upper() in self.guesses or not guess.isalpha()):
            guess = input("Guess: ")
        self.guesses.append(guess.upper())
        self.master.set_guessed_word(guess)
        self.print_guess(guess)

    def print_guess(self, guess):
        matches = self.master.matches()[1]
        for i in range(len(guess)):
            if matches[i][1] == 0:
                print(f"{Fore.RED}{guess[i].upper()}{Fore.WHITE}", end="")
            elif matches[i][1] == 1:
                print(f"{Fore.YELLOW}{guess[i].upper()}{Fore.WHITE}", end="")
            else:
                print(f"{Fore.GREEN}{guess[i].upper()}{Fore.WHITE}", end="")
        print("\n")

    def reset_game(self):
        self.guesses = []
        self.master.set_secret_word()
        self.play_game()


game = (Wordle(5))
