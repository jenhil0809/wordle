from wordfreq import zipf_frequency, top_n_list
from random import choice
from colorama import Fore


class Wordle:
    def __init__(self, length: int = 5, guess_num: int = 6, lang="en"):
        self.length = length
        self.lang = lang
        self.common_words = [word for word in top_n_list(self.lang, 10000)
                             if len(word) == self.length and "'" not in word]
        self._secret_word = ""
        self.set_secret_word()
        self._guessed_word = " " * self.length
        self.game = Game(self, guess_num)

    def set_secret_word(self):
        self._secret_word = choice(self.common_words)

    def get_secret_word(self):
        return self._secret_word

    def set_guessed_word(self, word):
        self._guessed_word = word

    @property
    def matches(self):
        lst = []
        for i in range(self.length):
            if self._guessed_word[i] == self._secret_word[i]:
                lst.append((self._guessed_word[i], 2))
            elif self._guessed_word[i] in self._secret_word:
                lst.append((self._guessed_word[i], 1))
            else:
                lst.append((self._guessed_word[i], 0))
        return lst

    @property
    def finished(self):
        return self._guessed_word == self._secret_word


class Game:
    def __init__(self, master: Wordle, guess_num: int = 6):
        self.master = master
        self.guess_num = guess_num
        self.guesses = []

    def reset_game(self):
        self.guesses = []
        self.master.set_secret_word()


class Interface:
    def __init__(self, master: Game):
        self.matches = []
        self.master = master

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

    def play_game(self):
        self.get_guess(self.master.master.length, self.master.guesses, self.master.master.lang)
        while len(self.master.guesses) < self.master.guess_num and not self.master.master.finished:
            self.get_guess(self.master.master.length, self.master.guesses, self.master.master.lang)
        self.end_game()

    def get_guess(self, length, guesses, lang):
        guess = ""
        while (len(guess) != length or zipf_frequency(guess, lang) == 0.0 or
               guess.upper() in guesses or not guess.isalpha()):
            guess = input("Guess: ")
        self.master.guesses.append(guess.upper())
        self.master.master.set_guessed_word(guess)
        self.print_guess(guess, self.master.master.matches)

    def end_game(self):
        print(f"Answer={Fore.GREEN}{self.master.master.get_secret_word()}{Fore.WHITE}")
        self.master.reset_game()
        self.play_game()


if __name__ == "__main__":
    game = Wordle(5, 3, "en")
    interface = Interface(game.game)
    interface.play_game()
