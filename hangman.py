import random, string


def hide(word):
    hidden = ''
    for letter in word:
        hidden += '_'
    return hidden

def check_answer(guess, word, hidden_word, guesses, errors, max_err):
    if guess in hidden_word or guess in guesses:
        print('\nYou have already guessed this letter!')
        return hidden_word, errors
    if guess not in word:
        errors = mistake(errors, max_err)
        
        return hidden_word, errors
    else:
        for i in range(len(word)):
            if word[i] == guess:
                hidden_word = hidden_word[:i] + guess + hidden_word[i+1:]
    return hidden_word, errors


def mistake(err, max_err):
    print('\n######    NOPE!    ######\n')
    err += 1
    if err >= max_err:
        return None
    print(f'You guessed wrong {err} time(s) so far, {max_err - err} mistakes left')
    return err


def start_game():
    word = random.choice(['dog', 'cat', 'pony', 'horse', 'dragon', 'automobile', 'whatever'])
    max_err = 6 # TODO make a choice of difficulty
    hidden = hide(word)
    print("###############################\n\n\n         HANGMAN GAME            \n\n\n###############################")
    print(f'\n\nYour word is {hidden} : it is {len(hidden)} characters long.\n\n')
    return word, hidden, max_err


def play_again(err):
    if err == None:
        print('###############################\n\non\n            YOU LOST!            \n\n\n###############################')
    else:
        print("###############################\n\n\n         CONGRATULATIONS!         \n\n\n###############################")
    choice = input("Do you wish to play again? (y/n): ")
    while choice not in ['y', 'n', 'Y', 'N']:
        choice = input('please input a valid choice (y/n)')
        continue
    return choice


def check_validity(guess):
    if guess in string.ascii_letters:
        return True
    return False


while True:
    w, h, max_err = start_game()
    guesses = []
    errors = 0

    while h != w:
        guess = input("Please give me a guess (only letters a-z):\t").lower()
        while not check_validity(guess):
            guess = input("Please give me valid letter (a-z):\n")
        h, errors = check_answer(guess, w, h, guesses, errors, max_err)
        if guess not in guesses:
            guesses.append(guess)
        if errors != None:
            print('\n',h,'\n')
            continue
        else:
            break
    if play := play_again(errors) in ['y', 'Y']:
        continue
    else:
        print('Bye Bye')
        break
