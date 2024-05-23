import main
import tkinter as tk
from time import sleep

class GameApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title = "Wordle"
        self.game = main.Wordle(5, 6, "en")
        self.guess = tk.StringVar()
        self.screen = Game(self)
        self.screen.pack()


class Game(tk.Frame):
    def __init__(self, master: GameApp):
        super().__init__()
        self.master: GameApp = master
        self.squares = [tk.Button(self, text=" ", height=2, width=5, bg="light gray") for i in range(self.master.game.length*self.master.game.game.guess_num)]
        self.submit_button = tk.Button(self, text="Submit", command = self.set_guess)
        self.word_input = tk.Entry(self, textvariable=self.master.guess)
        self.error_message = tk.Label(self, text="", wraplength=100)
        self.answer = tk.Label(self, text="", wraplength=100)
        self.place_widgets()

    def set_guess(self):
        guess = self.master.guess.get()
        if (len(guess) == self.master.game.length and main.zipf_frequency(guess, self.master.game.lang) != 0.0 and
               guess.upper() not in self.master.game.game.guesses and guess.isalpha()):
            self.master.game.game.guesses.append(guess.upper())
            self.master.game.set_guessed_word(guess)
            for i in range(self.master.game.length):
                self.squares[i+(len(self.master.game.game.guesses)-1)*self.master.game.length].config(text=guess[i])
                if self.master.game.matches[i][1] == 2:
                    self.squares[i+(len(self.master.game.game.guesses)-1)*self.master.game.length].config(bg="green")
                elif self.master.game.matches[i][1] == 1:
                    self.squares[i+(len(self.master.game.game.guesses)-1)*self.master.game.length].config(bg="orange")
            self.place_widgets()
            if self.master.game.finished or self.master.game.game.guess_num == len(self.master.game.game.guesses):
                self.answer.config(text=self.master.game.get_secret_word())
                self.place_widgets()
                self.reset()

    def reset(self):
        self.master.screen.update_idletasks()
        sleep(2)
        self.place_widgets()
        self.answer.config(text="")
        self.master.game.game.reset_game()
        for square in self.squares:
            square.config(bg="light gray")
            square.config(text=" ")
        self.place_widgets()

    def place_widgets(self):
        for i in range(self.master.game.length*self.master.game.game.guess_num):
            self.squares[i].grid(row=i //self.master.game.length, column=i%self.master.game.length, padx=5, pady=5)
        self.word_input.grid(row=2, column=13)
        self.submit_button.grid(row=3, column=13)
        self.answer.grid(row=4, column=13)
        self.error_message.grid(row=4, column=12, columnspan=2, rowspan=3)


if __name__ == "__main__":
    app = GameApp()
    app.mainloop()