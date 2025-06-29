import tkinter as tk
from tkinter import messagebox
import random
import time
import json
import os

# File path for leaderboard
LEADERBOARD_FILE = "leaderboard.json"

def load_leaderboard():
    if os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, "r") as file:
            return json.load(file)
    return {}

def save_leaderboard(leaderboard):
    with open(LEADERBOARD_FILE, "w") as file:
        json.dump(leaderboard, file, indent=4)

class NumberGuessingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Number Guessing Game")
        self.root.geometry("500x400")
        self.root.resizable(False, False)

        self.number_to_guess = 0
        self.attempts = 0
        self.max_attempts = 0
        self.start_time = None
        self.difficulty = "Medium"

        self.create_widgets()

    def create_widgets(self):
        # Title
        tk.Label(self.root, text="Number Guessing Game", font=("Helvetica", 16, "bold")).pack(pady=10)

        # Difficulty selection
        tk.Label(self.root, text="Select Difficulty:").pack()
        self.difficulty_var = tk.StringVar(value="Medium")
        tk.OptionMenu(self.root, self.difficulty_var, "Easy", "Medium", "Hard").pack(pady=5)

        # Start button
        tk.Button(self.root, text="Start Game", command=self.start_game).pack(pady=10)

        # Game instructions
        self.instruction_label = tk.Label(self.root, text="", font=("Helvetica", 12))
        self.instruction_label.pack(pady=5)

        # Guess input
        self.guess_entry = tk.Entry(self.root, state="disabled", justify="center", font=("Helvetica", 14))
        self.guess_entry.pack(pady=5)

        # Submit button
        self.submit_button = tk.Button(self.root, text="Submit Guess", state="disabled", command=self.check_guess)
        self.submit_button.pack(pady=5)

        # Result message
        self.result_label = tk.Label(self.root, text="", font=("Helvetica", 12))
        self.result_label.pack(pady=10)

        # Leaderboard button
        tk.Button(self.root, text="View Leaderboard", command=self.view_leaderboard).pack(pady=10)

    def start_game(self):
        self.difficulty = self.difficulty_var.get()
        self.attempts = 0
        self.start_time = time.time()

        if self.difficulty == "Easy":
            self.number_to_guess = random.randint(1, 50)
            self.max_attempts = 10
        elif self.difficulty == "Medium":
            self.number_to_guess = random.randint(1, 100)
            self.max_attempts = 10
        else:
            self.number_to_guess = random.randint(1, 200)
            self.max_attempts = 12

        self.instruction_label.config(text=f"Guess a number between 1 and {self.number_to_guess}. You have {self.max_attempts} attempts.")
        self.result_label.config(text="")
        self.guess_entry.config(state="normal")
        self.submit_button.config(state="normal")

    def check_guess(self):
        try:
            guess = int(self.guess_entry.get())
            self.attempts += 1

            if guess < self.number_to_guess:
                self.result_label.config(text="Too low! Try again.")
            elif guess > self.number_to_guess:
                self.result_label.config(text="Too high! Try again.")
            else:
                elapsed_time = round(time.time() - self.start_time, 2)
                self.result_label.config(text=f"Congratulations! You guessed the number in {self.attempts} attempts and {elapsed_time} seconds.")
                self.save_score(elapsed_time)
                self.guess_entry.config(state="disabled")
                self.submit_button.config(state="disabled")
                return

            if self.attempts == self.max_attempts:
                self.result_label.config(text=f"Game Over! The number was {self.number_to_guess}.")
                self.guess_entry.config(state="disabled")
                self.submit_button.config(state="disabled")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number.")

    def save_score(self, elapsed_time):
        leaderboard = load_leaderboard()
        name = tk.simpledialog.askstring("Enter Name", "Enter your name:")
        if name:
            leaderboard[name] = {"attempts": self.attempts, "time": elapsed_time}
            save_leaderboard(leaderboard)

    def view_leaderboard(self):
        leaderboard = load_leaderboard()
        if not leaderboard:
            messagebox.showinfo("Leaderboard", "No scores yet!")
            return

        leaderboard_text = "\n".join([f"{name}: {data['attempts']} attempts, {data['time']} seconds" for name, data in sorted(leaderboard.items(), key=lambda x: x[1]["attempts"])])
        messagebox.showinfo("Leaderboard", leaderboard_text)


# Run the game
if __name__ == "__main__":
    root = tk.Tk()
    game = NumberGuessingGame(root)
    root.mainloop()
