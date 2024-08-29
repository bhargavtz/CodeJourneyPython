import random

def guess_the_number():
    # Step 1: Generate a random number between 1 and 100
    number_to_guess = random.randint(1, 100)
    attempts = 0
    guessed = False

    print("Welcome to 'Guess the Number'!")
    print("I'm thinking of a number between 1 and 100.")

    # Step 2: Loop until the user guesses the number
    while not guessed:
        try:
            # Step 3: Get user's guess
            user_guess = int(input("Enter your guess: "))
            attempts += 1
            
            # Step 4: Check the guess
            if user_guess < number_to_guess:
                print("Too low! Try again.")
            elif user_guess > number_to_guess:
                print("Too high! Try again.")
            else:
                print(f"Congratulations! You've guessed the number {number_to_guess} in {attempts} attempts.")
                guessed = True
        except ValueError:
            print("Please enter a valid integer.")

# Run the game
if __name__ == "__main__":
    guess_the_number()
