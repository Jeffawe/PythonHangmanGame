import random
from words import word_list


def get_word():
    word = random.choice(word_list)
    return word.upper()


def play(word):
    word_completion = "_" * len(word)
    guessed = False
    guessed_letters = []
    guessed_words = []
    tries = 6

    print("Let's play hangman")
    print(word_completion)
    print("\n")

    while not guessed and tries > 0:
        guess = input("Please guess a letter or word: ").upper()
        if len(guess) == 1 and guess.isalpha():
            if guess in guessed_letters:
                print("You already guessed the letter ", guess)
                print(guessed_letters)
            elif guess not in word:
                print(guess, "is not in the word")
                tries -= 1
                guessed_letters.append(guess)
            else:
                print("Good job", guess, "is in the word!")
                guessed_letters.append(guess)

                word_as_list = list(word_completion)

                # enumerate stores each letter of word as [0, b] [1, o] if the word is bo.
                # So if my guess is b. it will return the index 0 into indices
                indices = [i for i, letter in enumerate(word) if letter == guess]

                # for every index [0] if guess is b. it will convert "_" to that guess that the index points to
                for index in indices:
                    word_as_list[index] = guess

                # converts it back to string
                word_completion = "".join(word_as_list)

                if "_" not in word_completion:
                    guessed = True

        elif len(guess) == len(word) and guess.isalpha():
            if guess in guessed_words:
                print("You have already guessed the word", guess)
            elif guess != word:
                print(guess, "is not in word")
                tries -= 1
                guessed_words.append(guess)
            else:
                guessed = True
                word_completion = word

        else:
            print("Not a valid guess")

        print(word_completion)
        print("you have", tries, "tries left")

    if guessed:
        print ("Congrats you guessed it right")
    else:
        print("you ran out of tries. Try again next time")


def main():
    word = get_word()
    play(word)

    while input("Play Again (Y/N) ").upper() == "Y":
        word = get_word()
        play(word)


if __name__ == "__main__":
    main()