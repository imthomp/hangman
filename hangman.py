import random
import os

# ASCII Art title
title = """
 _                                             
| |                                            
| |__   __ _ _ __   __ _ _ __ ___   __ _ _ __  
| '_ \ / _` | '_ \ / _` | '_ ` _ \ / _` | '_ \ 
| | | | (_| | | | | (_| | | | | | | (_| | | | |
|_| |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|
                    __/ |                      
                   |___/                       
"""

# Word categories
word_categories = {
    "programming": ["python", "java", "javascript", "ruby", "php", "csharp", "cplusplus", "go", "swift", "fortran"],
    "animals": ["dog", "cat", "elephant", "giraffe", "kangaroo", "lion", "tiger", "bear", "zebra", "penguin"],
    "countries": ["mexico", "canada", "brazil", "argentina", "india", "china", "japan", "australia", "germany", "france"],
    "colors": ["red", "orange", "yellow", "green", "blue", "indigo", "violet", "pink", "brown", "black"],
    "cities": ["newyork", "london", "paris", "tokyo", "berlin", "rome", "moscow", "madrid", "beijing", "mumbai"],
}

# Hangman stages to be displayed during the game
hangman_stages = [
    """
    -----
    |   |
        |
        |
        |
        |
    """,
    """
    -----
    |   |
    O   |
        |
        |
        |
    """,
    """
    -----
    |   |
    O   |
    |   |
        |
        |
    """,
    """
    -----
    |   |
    O   |
   /|   |
        |
        |
    """,
    """
    -----
    |   |
    O   |
   /|\\  |
        |
        |
    """,
    """
    -----
    |   |
    O   |
   /|\\  |
   /    |
        |
    """,
    """
    -----
    |   |
    O   |
   /|\\  |
   / \\  |
        |
    """
]

# Class to hold the state of the game
class GameState:
    def __init__(self, word, chances):
        self.word = word  # Word to be guessed
        self.guesses = set()  # All guesses made by the player
        self.correct_guesses = set()  # Correct guesses
        self.incorrect_guesses = set()  # Incorrect guesses
        self.chances = chances  # Number of chances left

    # Method to handle player's guess
    def guess_letter(self, letter):
        # Validate input
        if not letter.isalpha() or len(letter) != 1:
            print("Invalid input. Please enter a single letter.")
            return
        letter = letter.lower()
        # Check if letter has already been guessed
        if letter in self.guesses:
            print("You've already guessed that letter.")
            return
        # Add letter to guesses
        self.guesses.add(letter)
        # Check if letter is in word
        if letter in self.word:
            self.correct_guesses.add(letter)
        else:
            self.chances -= 1
            self.incorrect_guesses.add(letter)

    # Check if the word has been guessed
    def is_word_guessed(self):
        return set(self.word) <= self.correct_guesses

# Function to clear the console
def clear_screen():
    os.system('cls')

# Function to print the hangman stage based on the number of chances left
def print_stage(chances):
    clear_screen()
    print(hangman_stages[5-chances])

# Function to print the word with guessed and unguessed letters
def print_word(game_state):
    for char in game_state.word:
        if char in game_state.guesses:
            print(char, end=" ")
        else:
            print("_", end=" ")
    print()

# Function to get user input
def get_user_input(prompt):
    return input(prompt)

# Function to get a valid guess from the user
def get_valid_guess(game_state):
    while True:
        guess = get_user_input("Guess a letter or type 'hint' for a hint: ")
        if len(guess) == 1 and guess.isalpha():
            if guess.lower() in game_state.guesses:
                print("You have already guessed that letter. Try again.")
            else:
                return guess.lower()
        elif guess.lower() == 'hint':
            return guess.lower()
        else:
            print("Invalid guess. Please enter a single letter or 'hint'.")

# Function to get a valid category from the user
def get_valid_category():
    categories = sorted(list(word_categories.keys()))
    display_categories = ', '.join(categories[:-1]) + ' and ' + categories[-1]
    while True:
        category = get_user_input(f"Choose a category from {display_categories}: ")
        if category in word_categories:
            return category
        else:
            print(f"Invalid category. Please choose from {display_categories}.")

# Function to get a hint for the word
def get_hint(game_state):
    for letter in game_state.word:
        if letter not in game_state.guesses:
            return letter
    return None

# Function to play a game
def play_game():
    clear_screen()
    print(title)
    print("Welcome to Hangman!")
    print("Guess the word before you run out of chances!")
    category = get_valid_category()
    game_state = GameState(random.choice(word_categories[category]), 5)
    print(f"You have {game_state.chances} chances to guess the word.")
    print("Good luck!")
    input("Press enter to start.")
    print_stage(game_state.chances)
    print(f"The word has {len(game_state.word)} letters.")
    while game_state.chances > 0:
        print_word(game_state)
        guess = get_valid_guess(game_state)
        if guess == 'hint':
            hint = get_hint(game_state)
            if hint:
                print(f"Hint: The word contains the letter '{hint}'.")
            else:
                print("No more hints available.")
            continue
        game_state.guess_letter(guess)
        print_stage(game_state.chances)
        print(f"You have made {len(game_state.guesses)} guesses. {len(game_state.correct_guesses)} correct and {len(game_state.incorrect_guesses)} incorrect.")
        if game_state.is_word_guessed():
            print(f'Congratulations! You guessed the word! It was "{game_state.word}."')
            print(f"It took you {len(game_state.guesses)} guesses.")
            break
        if game_state.chances == 0:
            print_stage(-1)
            print("You lose!")
            print(f"The word was {game_state.word}.")
            break
    print()
    print("Thanks for playing!")

# Main function to run the game
def main():
    while True:
        play_game()
        play_again = get_user_input("Would you like to play again? (yes/no): ")
        if play_again.lower() != "yes" and play_again.lower() != "y":
            break
    clear_screen()

if __name__ == "__main__":
    main()
