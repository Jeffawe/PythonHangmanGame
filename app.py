from flask import Flask
from flask import render_template
from flask import request
import random
from database.shapes import shapes_list
from database.states import states_list
from database.sports import sports_list
from database.games import games_list, games_list_description

app = Flask(__name__)
word = " "
word_completion = " "
guessed = False
guessed_letters = []
guessed_words = []
tries = 6
color = 0
msg = " "
description = " "
score = 0
canContinue = 0
canGuess = 0


def score_control():
    global score
    score += 1
    return score


def get_word(word_list):
    global word

    word = random.choice(word_list)
    print(word)
    return word


def get_description(dword, word_list, word_list_description):
    index = word_list.index(dword)
    thedescription = word_list_description[index]
    print(index)
    print(thedescription)
    return thedescription


def beginning(html_list, form_html, category):
    global word
    global word_completion
    global tries
    global guessed_letters
    global guessed_words
    global guessed
    global color
    global msg, score, canContinue, canGuess

    dword = get_word(html_list)
    word = dword.upper()
    word_completion = "_" * len(word)
    msg = " "
    color = 0
    tries = 6
    canContinue = 0
    canGuess = 0
    guessed_letters = []
    guessed_words = []
    guessed = False
    return render_template("NoDescription.html", word=word_completion, msg=msg, color=0, form_html=form_html,
                           category=category, score=score, canGuess=canGuess)


def beginning_description(html_list, html_list_description, form_html, category):
    global word
    global word_completion
    global tries
    global guessed_letters
    global guessed_words
    global guessed
    global color
    global msg, description, score, canContinue, canGuess

    dword = get_word(html_list)
    word = dword.upper()
    description = get_description(dword, html_list, html_list_description)
    word_completion = "_" * len(word)
    msg = " "
    color = 0
    tries = 6
    canContinue = 0
    canGuess = 0
    guessed_letters = []
    guessed_words = []
    guessed = False
    return render_template("Description.html", word=word_completion, msg=msg, color=0, description=description,
                           form_html=form_html, category=category, score=score, canGuess=canGuess)


def play(html_input, form_html, category):
    global word, color, msg

    global word_completion
    print(word_completion)
    global guessed
    global guessed_letters
    global guessed_words
    global tries, score, canContinue, canGuess

    if not guessed and tries > 0:
        guess_input = request.form[html_input].upper()
        guess = str(guess_input)
        canContinue = 0

        if len(guess) == 1 and guess.isalpha():
            if guess in guessed_letters:
                msg = 'You have already guessed the letter ' + str(guess)
                color = 0
            elif guess not in word:
                msg = str(guess) + ' is not in word'
                color = 1
                tries -= 1
                guessed_letters.append(guess)
            else:
                msg = 'Good job ' + str(guess) + ' is in the word'
                color = 0
                guessed_letters.append(guess)
                print(guessed_letters)

                word_as_list = list(word_completion)

                # enumerate stores each letter of word as [0, b] [1, o] if the word is bo.
                # So if my guess is b. it will return the index 0 into indices
                indices = [i for i, letter in enumerate(word) if letter == guess]

                for index in indices:
                    word_as_list[index] = guess

                # converts it back to string
                word_completion = "".join(word_as_list)

        elif len(guess) == len(word) and guess.isalpha():
            if guess in guessed_words:
                msg = 'you have already guessed the word ' + str(guess)
                color = 0
            elif guess != word:
                msg = str(guess) + ' is not in the word'
                color = 1
                tries -= 1
                guessed_words.append(guess)
            else:
                guessed = True
                word_completion = word
        else:
            msg = 'It is not a valid guess'
            color = 1

        if "_" not in word_completion:
            msg = "You guessed it right. Congrats"
            score = score_control()
            color = 0
            canContinue = 1
            canGuess = 1
            guessed = True

        if tries == 0:
            msg = 'You ran out of tries. The answer was ' + str(word)
            canGuess = 1
            color = 1

    elif guessed:
        msg = "You guessed it right. Congrats"
        score = score_control()
        canGuess = 1
        color = 0
        canContinue = 1

    else:
        msg = 'You ran out of tries. The answer was ' + str(word)
        color = 1
        canContinue = 0
        canGuess = 1

    tries_html = 'You have ' + str(tries) + ' tries left'
    return render_template("NoDescription.html", form_html=form_html, triesnumber=tries_html, tries=tries, msg=msg, color=color,
                           word=word_completion, category=category, score=score, canContinue=canContinue, canGuess=canGuess)


def play_description(html_input, form_html, category):
    global word, color, msg

    global word_completion
    print(word_completion)
    global guessed
    global guessed_letters
    global guessed_words
    global tries, description, score, canContinue, canGuess

    if not guessed and tries > 0:
        guess_input = request.form[html_input].upper()
        guess = str(guess_input)
        canContinue = 0

        if len(guess) == 1 and guess.isalpha():
            if guess in guessed_letters:
                msg = 'You have already guessed the letter ' + str(guess)
                color = 0
            elif guess not in word:
                msg = str(guess) + ' is not in word'
                color = 1
                tries -= 1
                guessed_letters.append(guess)
            else:
                msg = 'Good job ' + str(guess) + ' is in the word'
                color = 0
                guessed_letters.append(guess)
                print(guessed_letters)

                word_as_list = list(word_completion)

                # enumerate stores each letter of word as [0, b] [1, o] if the word is bo.
                # So if my guess is b. it will return the index 0 into indices
                indices = [i for i, letter in enumerate(word) if letter == guess]

                for index in indices:
                    word_as_list[index] = guess

                # converts it back to string
                word_completion = "".join(word_as_list)

        elif len(guess) == len(word) and guess.isalpha():
            if guess in guessed_words:
                msg = 'you have already guessed the word ' + str(guess)
                color = 0
            elif guess != word:
                msg = str(guess) + ' is not in the word'
                color = 1
                tries -= 1
                guessed_words.append(guess)
            else:
                guessed = True
                word_completion = word
        else:
            msg = 'It is not a valid guess'
            color = 1

        if "_" not in word_completion:
            msg = "You guessed it right. Congrats"
            score = score_control()
            canContinue = 1
            color = 0
            guessed = True
            canGuess = 1

        if tries == 0:
            msg = 'You ran out of tries. The answer was ' + str(word)
            color = 1
            canGuess = 1

    elif guessed:
        msg = "You guessed it right. Congrats"
        score = score_control()
        canContinue = 1
        color = 0
        canGuess = 1

    else:
        msg = 'You ran out of tries. The answer was ' + str(word)
        canContinue = 0
        color = 1
        canGuess = 1

    tries_html = 'You have ' + str(tries) + ' tries left'
    return render_template("Description.html", triesnumber=tries_html, tries=tries, msg=msg, color=color, word=word_completion,
                           form_html=form_html, description=description, category=category, score=score, canContinue=canContinue,
                           canGuess=canGuess)


@app.route('/')
def home():
    global score

    score = 0
    return render_template("index.html")


@app.route('/states')
def states():
    return beginning(states_list, "/states", "Countries in Africa")


@app.route('/states', methods=['POST'])
def states_post():
    return play('game_input', "/states", "Countries in Africa")


@app.route('/shapes')
def shapes():
    return beginning(shapes_list, "/shapes", "Shapes")


@app.route('/shapes', methods=['POST'])
def shapes_post():
    return play('game_input', "/shapes", "Shapes")


@app.route('/sports')
def sports():
    return beginning(sports_list, "/sports", "Sports")


@app.route('/sports', methods=['POST'])
def sports_post():
    return play('game_input', "/sports", "Sports")


@app.route('/games')
def games():
    return beginning_description(games_list, games_list_description, "/games", "Video Games")


@app.route('/games', methods=['POST'])
def games_post():
    return play_description('game_input', "/games", "Video Games")


if __name__ == '__main__':
    app.run(debug=True)
