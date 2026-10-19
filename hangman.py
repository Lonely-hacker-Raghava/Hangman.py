import random

WORDS = [
    "PYTHON", "PROGRAM", "COMPUTER", "DATHEON",
    "DEVELOPER", "KEYBOARD", "FUNCTION",
    "VARIABLE", "ALGORITHM", "SOFTWARE"
]

MAX_ATTEMPTS = 6

HANGMAN_STAGES = [
    """
     +---+
     |   |
         |
         |
         |
         |
    =========
    """,
    """
     +---+
     |   |
     O   |
         |
         |
         |
    =========
    """,
    """
     +---+
     |   |
     O   |
     |   |
         |
         |
    =========
    """,
    """
     +---+
     |   |
     O   |
    /|   |
         |
         |
    =========
    """,
    """
     +---+
     |   |
     O   |
    /|\\  |
         |
         |
    =========
    """,
    """
     +---+
     |   |
     O   |
    /|\\  |
    /    |
         |
    =========
    """,
    """
     +---+
     |   |
     O   |
    /|\\  |
    / \\  |
         |
    =========
    """
]


def display_word(secret_word, guessed_letters):
    """Display guessed letters and hide the remaining letters."""
    return " ".join(
        letter if letter in guessed_letters else "_"
        for letter in secret_word
    )


def play_hangman():
    """Run one complete Hangman game."""
    secret_word = random.choice(WORDS)
    guessed_letters = set()
    wrong_guesses = set()

    print("=== WELCOME TO HANGMAN ===")
    print(f"You have {MAX_ATTEMPTS} incorrect guesses.")

    while len(wrong_guesses) < MAX_ATTEMPTS:
        print(HANGMAN_STAGES[len(wrong_guesses)])
        print("Word:", display_word(secret_word, guessed_letters))
        print(
            "Guessed letters:",
            ", ".join(sorted(guessed_letters | wrong_guesses)) or "None"
        )
        print("Attempts remaining:", MAX_ATTEMPTS - len(wrong_guesses))

        guess = input("Enter one letter (A-Z): ").strip().upper()

        if len(guess) != 1 or guess not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            print("Please enter one English letter.\n")
            continue

        if guess in guessed_letters or guess in wrong_guesses:
            print("You already guessed that letter. Try again.\n")
            continue

        if guess in secret_word:
            guessed_letters.add(guess)
            print("Correct guess!\n")

            if all(letter in guessed_letters for letter in secret_word):
                print("Word:", display_word(secret_word, guessed_letters))
                print("Congratulations! YOU WIN!")
                return
        else:
            wrong_guesses.add(guess)
            print("Incorrect guess!\n")

    print(HANGMAN_STAGES[MAX_ATTEMPTS])
    print("GAME OVER!")
    print("The secret word was:", secret_word)


if __name__ == "__main__":
    try:
        play_hangman()
    except (KeyboardInterrupt, EOFError):
        print("\nGame ended. Thanks for playing!")
