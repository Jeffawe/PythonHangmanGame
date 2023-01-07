from flask import Flask
from flask import session
from flask import render_template
from flask import request
import random
from database.shapes import shapes_list
from database.states import states_list
from database.sports import sports_list
from database.games import games_list, games_list_description
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = b'\x8c\xa1\xb2\xb1\x16\x0c1b\x0e\xfd|1\xef\x10\x92,~\x11>\xa8\xa5\x9c$\x05'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_COOKIE_NAME'] = "my_session"


def score_control():
    score = session['score']

    score += 1
    session['score'] = score
    return score


def store_session(word_input, word_completion_input, msg_input, color_input, tries_input, CanContinue_input,
                  CanGuess_input, guessed_letters_input, guessed_words_input, guessed_input, score_input):
    session['word'] = word_input
    session['word_completion'] = word_completion_input
    session['msg'] = msg_input
    session['color'] = color_input
    session['tries'] = tries_input
    session['canContinue'] = CanContinue_input
    session['canGuess'] = CanGuess_input
    session['guessed_letters'] = guessed_letters_input
    session['guessed_words'] = guessed_words_input
    session['guessed'] = guessed_input
    session['score'] = score_input


def get_word(word_list):
    aword = random.choice(word_list)
    print(aword)
    return aword


def get_description(dword, word_list, word_list_description):
    index = word_list.index(dword)
    thedescription = word_list_description[index]
    print(index)
    print(thedescription)
    return thedescription


def beginning(html_list, form_html, category):
    dword = get_word(html_list)
    session['word'] = dword.upper()
    word = session['word']
    session['word_completion'] = "_" * len(word)
    word_completion = session['word_completion']
    session['msg'] = " "
    msg = session['msg']
    session['color'] = 0
    session['tries'] = 6
    session['canContinue'] = 0
    session['canGuess'] = 0
    canGuess = session['canGuess']
    session['guessed_letters'] = []
    session['guessed_words'] = []
    session['guessed'] = False
    score = session['score']
    return render_template("NoDescription.html", word=word_completion, msg=msg, color=0, form_html=form_html,
                           category=category, score=score, canGuess=canGuess)


def beginning_description(html_list, html_list_description, form_html, category):
    dword = get_word(html_list)
    session['word'] = dword.upper()
    word = session['word']
    session['word_completion'] = "_" * len(word)
    word_completion = session['word_completion']
    session['msg'] = " "
    msg = session['msg']
    session['color'] = 0
    session['tries'] = 6
    session['canContinue'] = 0
    session['canGuess'] = 0
    canGuess = session['canGuess']
    session['guessed_letters'] = []
    session['guessed_words'] = []
    session['guessed'] = False
    score = session['score']
    session['description'] = get_description(dword, html_list, html_list_description)
    description = session['description']
    return render_template("Description.html", word=word_completion, msg=msg, color=0, description=description,
                           form_html=form_html, category=category, score=score, canGuess=canGuess)


def play(html_input, form_html, category):
    word1 = session.get('word')
    word_completion1 = session.get('word_completion')
    msg1 = session.get('msg')
    color1 = session.get('color')
    tries1 = session.get('tries')
    CanContinue1 = session.get('canContinue')
    CanGuess1 = session.get('canGuess')
    guessed_letters1 = session.get('guessed_letters')
    guessed_words1 = session.get('guessed_words')
    guessed1 = session.get('guessed')
    score1 = session.get('score')

    print(word_completion1)

    if not guessed1 and tries1 > 0:
        guess_input = request.form[html_input].upper()
        guess = str(guess_input)
        CanContinue1 = 0

        if len(guess) == 1 and guess.isalpha():
            if guess in guessed_letters1:
                msg1 = 'You have already guessed the letter ' + str(guess)
                color1 = 0
            elif guess not in word1:
                msg1 = str(guess) + ' is not in word'
                color1 = 1
                tries1 -= 1
                guessed_letters1.append(guess)
            else:
                msg1 = 'Good job ' + str(guess) + ' is in the word'
                color1 = 0
                guessed_letters1.append(guess)
                print(guessed_letters1)

                word_as_list = list(word_completion1)

                # enumerate stores each letter of word as [0, b] [1, o] if the word is bo.
                # So if my guess is b. it will return the index 0 into indices
                indices = [i for i, letter in enumerate(word1) if letter == guess]

                for index in indices:
                    word_as_list[index] = guess

                # converts it back to string
                word_completion1 = "".join(word_as_list)

        elif len(guess) == len(word1) and guess.isalpha():
            if guess in guessed_words1:
                msg1 = 'you have already guessed the word ' + str(guess)
                color1 = 0
            elif guess != word1:
                msg1 = str(guess) + ' is not in the word'
                color1 = 1
                tries1 -= 1
                guessed_words1.append(guess)
            else:
                guessed1 = True
                word_completion1 = word1
        else:
            msg1 = 'It is not a valid guess'
            color1 = 1

        if "_" not in word_completion1:
            msg1 = "You guessed it right. Congrats"
            score1 = score_control()
            color1 = 0
            CanContinue1 = 1
            CanGuess1 = 1
            guessed1 = True

        if tries1 == 0:
            msg1 = 'You ran out of tries. The answer was ' + str(word1)
            CanGuess1 = 1
            color1 = 1

    elif guessed1:
        msg1 = "You guessed it right. Congrats"
        score1 = score_control()
        CanGuess1 = 1
        color1 = 0
        CanContinue1 = 1

    else:
        msg1 = 'You ran out of tries. The answer was ' + str(word1)
        color1 = 1
        CanContinue1 = 0
        CanGuess1 = 1

    tries_html = 'You have ' + str(tries1) + ' tries left'
    store_session(word1, word_completion1, msg1, color1, tries1, CanContinue1, CanGuess1, guessed_letters1,
                  guessed_words1, guessed1, score1)
    return render_template("NoDescription.html", form_html=form_html, triesnumber=tries_html, tries=tries1, msg=msg1, color=color1,
                           word=word_completion1, category=category, score=score1, canContinue=CanContinue1, canGuess=CanGuess1)


def play_description(html_input, form_html, category):
    word = session.get('word')
    word_completion = session.get('word_completion')
    msg = session.get('msg')
    color = session.get('color')
    tries = session.get('tries')
    can_continue = session.get('can_continue')
    can_guess = session.get('can_guess')
    guessed_letters = session.get('guessed_letters')
    guessed_words = session.get('guessed_words')
    guessed = session.get('guessed')
    score = session.get('score')
    description = session.get('description')

    if not guessed and tries > 0:
        guess_input = request.form[html_input].upper()
        guess = str(guess_input)
        can_continue = 0

        if len(guess) == 1 and guess.isalpha():
            if guess in guessed_letters:
                msg = 'You have already guessed the letter ' + str(guess)
                can_guess = 0
                color = 0
            elif guess not in word:
                msg = str(guess) + ' is not in word'
                can_guess = 0
                color = 1
                tries -= 1
                guessed_letters.append(guess)
            else:
                msg = 'Good job ' + str(guess) + ' is in the word'
                can_guess = 0
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
                can_guess = 0
                color = 0
            elif guess != word:
                msg = str(guess) + ' is not in the word'
                can_guess = 0
                color = 1
                tries -= 1
                guessed_words.append(guess)
            else:
                guessed = True
                word_completion = word
                can_guess = 0
        else:
            msg = 'It is not a valid guess'
            color = 1
            can_guess = 0

        if "_" not in word_completion:
            msg = "You guessed it right. Congrats"
            score = score_control()
            can_continue = 1
            color = 0
            guessed = True
            can_guess = 1

        if tries == 0:
            msg = 'You ran out of tries. The answer was ' + str(word)
            color = 1
            can_guess = 1

    elif guessed:
        msg = "You guessed it right. Congrats"
        score = score_control()
        can_continue = 1
        color = 0
        can_guess = 1

    else:
        msg = 'You ran out of tries. The answer was ' + str(word)
        can_continue = 0
        color = 1
        can_guess = 1

    tries_html = 'You have ' + str(tries) + ' tries left'
    store_session(word, word_completion, msg, color, tries, can_continue, can_guess, guessed_letters,
                  guessed_words, guessed, score)
    return render_template("Description.html", triesnumber=tries_html, tries=tries, msg=msg, color=color, word=word_completion,
                           form_html=form_html + "?t=" + str(time.time()), description=description, category=category, score=score, canContinue=can_continue,
                           canGuess=can_guess)


@app.route('/')
def home():
    session['score'] = 0
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
