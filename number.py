import random
import time
import json
import os

# File path to save the leaderboard
LEADERBOARD_FILE = "leaderboard.json"

def load_leaderboard():
    """Load the leaderboard from a file."""
    if os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, "r") as file:
            return json.load(file)
    return {}

def save_leaderboard(leaderboard):
    """Save the leaderboard to a file."""
    with open(LEADERBOARD_FILE, "w") as file:
        json.dump(leaderboard, file, indent=4)

def display_leaderboard(leaderboard):
    """Display the leaderboard."""
    print("\nLeaderboard:")
    if leaderboard:
        sorted_leaderboard = sorted(leaderboard.items(), key=lambda x: x[1]['attempts'])
        for name, data in sorted_leaderboard:
            print(f"{name}: {data['attempts']} attempts, Time: {data['time']} seconds")
    else:
        print("No scores yet.")

def number_guessing_game():
    """Main game function."""
    print("Welcome to the Number Guessing Game!")
    
    # Get user name
    user_name = input("Enter your name: ")

    # Select difficulty level
    print("\nChoose a difficulty level:")
    print("1. Easy (1-50)")
    print("2. Medium (1-100)")
    print("3. Hard (1-200)")
    level = input("Enter level (1/2/3): ")

    if level == '1':
        number_range = 50
        max_attempts = 10
    elif level == '2':
        number_range = 100
        max_attempts = 10
    else:
        number_range = 200
        max_attempts = 12

    number_to_guess = random.randint(1, number_range)
    attempts = 0
    start_time = time.time()

    print(f"\nGuess the number between 1 and {number_range}!")

    while attempts < max_attempts:
        try:
            guess = int(input(f"Attempt {attempts + 1}/{max_attempts}: Guess a number: "))
            attempts += 1

            if guess < number_to_guess:
                print("Too low! Try again.")
            elif guess > number_to_guess:
                print("Too high! Try again.")
            else:
                print(f"Congratulations! You guessed the number in {attempts} attempts!")
                end_time = time.time()
                elapsed_time = round(end_time - start_time, 2)
                print(f"Time taken: {elapsed_time} seconds.")
                
                # Update leaderboard
                leaderboard = load_leaderboard()
                leaderboard[user_name] = {"attempts": attempts, "time": elapsed_time}
                save_leaderboard(leaderboard)
                break
        except ValueError:
            print("Please enter a valid number.")
        
        if attempts == max_attempts:
            print(f"\nSorry! You've reached the maximum attempts. The number was {number_to_guess}.")
            break

    # Display leaderboard after game
    display_leaderboard(load_leaderboard())

# Run the game
number_guessing_game()
